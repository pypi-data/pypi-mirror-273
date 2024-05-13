# This code is part of qmatchatea.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Core functions to run the Fortran MPS simulation. In particular, the :py:func:`run_simulation`
function is the most important one, and one should make particular attention to it.

Running the program
-------------------

 It is possible to choose between different approaches for running the simulation:
 - The backend can be either python "PY" or fortran "FR".
 - The machine precision can be either double complex "Z" or single complex "C".
 - The device of the simulation can be either "cpu" or "gpu".
 - The number of processes for the MPI simulation. If 1 is passed, then a serial
   program is run.
 - The approach for the MPI simulation. Either master/worker "MW", cartesian "CT" or
   serial "SR".


Serial program
~~~~~~~~~~~~~~

The default way of running this program is to run it serially. While it may be slower than a
parallel implementation it is safer, since the approximation we do on the state is minor.
There are different possibilities to run the program serially:

- Using the Fortran backend (``mpi_approach='SR'``). It is the faster implementation, but requires
  the presence of the executable ``main_qmatchatea.exe``.
- Using the Python backend (``backend='PY'``). The backend is entirely built with numpy, it
  is optimized but slightly slower than the fortran backend.
- Using the Python GPU backend (``backend='PY'``, ``device='gpu'``).
  The backend is entirely built with cupy,
  and runs the simulation on a GPU, giving back the results on the CPU.

Parallel program
~~~~~~~~~~~~~~~~

There are three possible algorithm provided to run the program on multiple cores:

- a Master/Worker approach (``mpi_approach='MW'``), where you store the state in the master
  process and perform the application of the evolution operators on the workers.
  It has the advantages that fewer workers are idle during the computation.
- a Cartesian approach (``mpi_approach='CT'``), where the MPS is evenly divided among different
  processes, and each process perform the evolution only on his subsystem
- running multiple independent serial simulations on multiple cores. To know more see
  :doc:`par_simulations`

At the end of the evolution the MPS is brought back together into the master process and the
measurements are performed. The command to call the parallel program should be
:code:`mpirun -np np ./par_main_qmatchatea.exe` where :code:`np` is the
number of processes you will use. It should be given as input to the :class:`IO_INFO`.
For further details on the input class see :doc:`utils`.

Remember that there are communications involved in the MPI parallel program.
You should use it only if your system is large enough or if the bond
dimension used is big enough.

Checking the convergence: Singular values cut
---------------------------------------------

The singular values cut are an indication of the approximation taking place during the
simulation. Indeed, at each application of two-qubit there is an approximation going on,
subject to the *bond_dim* :math:`\\chi` and the *cut_ratio* :math:`\\epsilon` parameters.
Based on the *trunc_tracking_mode* the singular values are reported:

- *trunc_tracking_mode=M*, at each two-site operator we save the maximum of the singular values cut
- *trunc_tracking_mode=C*, at each two-site operator we save the **sum** of the singular values cut

We recall that, given a decreasing-ordered vector of singular values
:math:`S=(s_1, s_2, \\dots, s_n)` we truncate all the singular values:

.. math::

        s_i \\; \\mbox{ is truncated }\\quad \\mbox{if} \\; i>\\chi \\; \\mbox{ or } \\;
        \\frac{s_i}{s_1}<\\epsilon

Observables
-----------

For a detailed description of the observables, i.e. the measurable quantities, please refer
to :doc:`observables`

"""

# Numpy
import os
import os.path
from typing import OrderedDict
import subprocess
import sys
import pickle

import numpy as np
from qtealeaves import write_nml
from qtealeaves.observables import TNObservables

from qmatchatea.py_emulator import run_py_simulation
from qmatchatea.circuit import Qcircuit
from .preprocessing import pre_parser, preprocess
from .utils.tn_utils import QCOperators, read_nml
from .utils.mpi_utils import to_layered_circ
from .utils.qk_utils import qk_transpilation_params
from .utils.utils import (
    QCCheckpoints,
    QCIO,
    QCConvergenceParameters,
    merge_ordered_dicts,
    QCBackend,
)
from .utils.simulation_results import SimulationResults

__all__ = ["run_simulation", "SimulationResults", "restart_from_checkpoint"]


def run_simulation(
    circ,
    local_dim=2,
    convergence_parameters=QCConvergenceParameters(),
    operators=QCOperators(),
    io_info=QCIO(),
    observables=TNObservables(),
    transpilation_parameters=qk_transpilation_params(),
    checkpoints=QCCheckpoints(),
    where_barriers=-1,
    backend=QCBackend(),
):
    """
    Transpile the circuit to adapt it to the linear structure of the MPS and run the circuit,
    obtaining in output the measurements.

    Parameters
    ----------
    circ: QuantumCircuit | strawberryfields.Program | Qcircuit
        Quantum circuit object to simulate.
        Be careful, if one passes a Qcircuit **no check** is done on the quantum circuit, i.e.
        it is not linearized and no barriers are added automatically.
    local_dim: int, optional
        Local dimension of the single degree of freedom. Default is 2, for qubits
    convergence_parameters: :py:class:`QCConvergenceParameters`, optional
        Maximum bond dimension and cut ratio. Default to max_bond_dim=10, cut_ratio=1e-9.
    operators: :py:class:`QCOperators`, optional
        Operator class with the observables operators ALREADY THERE. If None, then it is
        initialized empty. Default to None.
    io_info: :py:class:`QCIO`, optional
        Informations about input/output files to interface with the FORTRAN simulator
    observables: :py:class:`TNObservables`, optional
        The observables to be measured at the end of the simulation. Default to TNObservables(),
        which contains no observables to measure.
    transpilation_parameters: :py:class:`qk_transpilation_params`, optional
        Parameters used in the qiskit transpilation phase. Default to qk_transpilation_params().
    checkpoints: :py:class:`QCCheckpoints`, optional
        Class to handle checkpoints in the simulation
    where_barriers: int, optional
        This parameter is important only if you want to use MPI parallelization.
        If where_barriers > 0 then the circuit gets ordered in layers and a barrier is applyed
        each where_barriers layers. We recall that a barrier is equivalent to a canonization in
        the MPS simulation. Default to -1.
    backend: :py:class:`QCBackend`, optional
        Backend containing all the information for where to run the simulation

    Returns
    -------
    result: qmatchatea.SimulationResults
        Results of the simulation, containing the following data:
        - Measures
        - Statevector
        - Computational time
        - Singular values cut
        - Entanglement
        - Measure probabilities
        - MPS state
        - Observables measurements
    """
    # Checks on input parameters
    if not isinstance(convergence_parameters, QCConvergenceParameters):
        raise TypeError(
            "convergence_parameters must be of type QCConvergenceParameters"
        )
    if not isinstance(operators, QCOperators):
        raise TypeError("operators must be of type QCOperators")
    if not isinstance(io_info, QCIO):
        raise TypeError("io_info must be of type QCIO")
    if not isinstance(observables, TNObservables):
        raise TypeError("observables must be of type TNObservables")
    if not isinstance(transpilation_parameters, qk_transpilation_params):
        raise TypeError(
            "transpilation_parameters must be of type qk_transpilation_params"
        )
    if not isinstance(checkpoints, QCCheckpoints):
        raise TypeError("checkpoints must be of type QCCheckpoints")
    if not isinstance(backend, QCBackend):
        raise TypeError("backend must be of type QCBackend")

    # Ensure observables output folders is present and set IO
    io_info.setup(backend.backend == "FR")

    if backend.num_procs > 1:
        new_exe = backend.mpi_command + [
            "-n",
            str(backend.num_procs),
            *io_info.exe_file,
        ]
        io_info.set_exe_file(new_exe)

    # Set the PATH to the saved files into the output folder
    for ii in range(len(observables.obs_list["TNState2File"])):
        if "/" not in observables.obs_list["TNState2File"].name[ii]:
            observables.obs_list["TNState2File"].name[ii] = os.path.join(
                io_info.outPATH, observables.obs_list["TNState2File"].name[ii]
            )

    # Checks for parallel implementation
    if backend.mpi_approach not in ("SR", "PF"):
        if where_barriers <= 0:
            raise ValueError(
                "To obtain a correct result in a parallel approach the \
                where_barriers parameters must be greater then 0"
            )
        if backend.mpi_approach == "MW":
            if where_barriers != 1:
                raise ValueError(
                    "To obtain a correct result with the MW approach \
                    where_barrier must be 1."
                )
    if isinstance(circ, Qcircuit):
        preprocessed_circ = circ
        if backend.backend == "FR":
            raise ValueError("Qcircuit simulations not implemented in fortran")
    else:
        # Preprocess the circuit to adapt it to the MPS constraints (linearity)
        preprocessed_circ = preprocess(circ, qk_params=transpilation_parameters)

        # If required order the circuit in a layered way and apply barriers
        if where_barriers > 0:
            preprocessed_circ = to_layered_circ(
                preprocessed_circ, where_barriers=where_barriers
            )

    if backend.backend == "PY":
        circ_str = preprocessed_circ
        n_sites = preprocessed_circ.num_qubits
    else:
        # Write the circuit on file
        n_sites, operator_mapping, circ_str = pre_parser(
            preprocessed_circ,
            operators,
            io_info.inPATH,
            fock_cutoff=local_dim,
            sparse=io_info.sparse,
        )
        # Write the observables on file
        observables.write(io_info.inPATH, {}, operator_mapping)

    # Prepare input dictionary
    input_dict = OrderedDict()
    input_dict["num_sites"] = n_sites
    input_dict["local_dim"] = local_dim
    input_dict["observables_filename"] = os.path.join(observables.filename_observables)

    dictionaries = [
        input_dict,
        convergence_parameters.to_dict(),
        io_info.to_dict(),
        checkpoints.to_dict(),
        backend.to_dict(),
        OrderedDict({"state_string_len": 0}),
    ]
    temp_input_dict = merge_ordered_dicts(dictionaries)
    # Add "settings%" on front for ease fortran reading
    input_dict = OrderedDict()
    for key, val in temp_input_dict.items():
        input_dict[f"settings%{key}"] = val

    # Save input parameters on namelist file
    write_nml("INPUT", input_dict, os.path.join(io_info.inPATH, io_info.input_namelist))

    # Setting checkpoints if required
    if checkpoints.frequency > 0:
        checkpoints.set_up(input_dict, operators, observables, circ_str)

    # If the approach is pure python, do not go through all the steps for
    # the usual simulation setting
    if backend.backend == "PY":
        # Write all the information of the simulation as json
        to_write = [convergence_parameters, backend, io_info, checkpoints]
        for cls_to_write in to_write:
            cls_to_write.to_json(io_info.inPATH)
        result = run_py_simulation(
            preprocessed_circ,
            local_dim,
            convergence_parameters,
            operators,
            observables,
            backend=backend,
            initial_state=io_info.initial_state,
            checkpoints=checkpoints,
        )
    else:
        # Run the fortran program with the namelist name as argument
        res = subprocess.run(io_info.exe_file, capture_output=True)
        if res.stderr:
            print("--------------------------------------------")
            print("Program terminated with the following error:")
            print(res.stderr.decode())
            print("--------------------------------------------")
            sys.exit(1)
        result = SimulationResults(input_dict, observables)

        # Retrieve results
        result._get_results()

    return result


def restart_from_checkpoint(io_info, checkpoint_number=-1):
    """
    Restart a simulation starting from a checkpoint. Remember not to move checkpoints around,
    since it is expected the following directory tree

    .. code-block::bash
        checkpoints/
        |-general_setting_files
        |-checkpoint_1/
        |-...
        ...
        |-checkpoint_n/

    Parameters
    ----------
    io_info : :py:class:`QCIO`
        IO information for the checkpoints. The INPATH is the folder where
        the checkpoints are saved, the OUTPATH is the folder where the results
        of the simulation, starting from that checkpoint, will be saved.
    checkpoint_number: int
        Number of the directory you want to restart from. If `-1` restart from the last one.
        Default to -1.

    Returns
    -------
    result: qmatchatea.SimulationResults
        Results of the simulation
    """
    if not isinstance(io_info, QCIO):
        raise TypeError("io_info must be of type QCIO")

    PATH = io_info.inPATH
    if not os.path.isdir(PATH):
        raise IOError("Selected checkpoint directory does not exists")

    # Search all the directories in PATH that have 'checkpoint' in the name
    checkpoints = np.array(
        [
            o
            for o in os.listdir(PATH)
            if (os.path.isdir(os.path.join(PATH, o)) and "checkpoint" in o)
        ]
    )

    if len(checkpoints) == 0:
        raise RuntimeError("No checkpoints founded in the given PATH")
    # Order them by the number after the '_'
    checkpoints_numbers = [int(ck[ck.rfind("_") + 1 :]) for ck in checkpoints]
    order = np.argsort(checkpoints_numbers)
    checkpoints = checkpoints[order]
    # Pick the one selected by the user
    checkpoint_dir = str(checkpoints[checkpoint_number])
    # Select file
    checkpoint_file = os.listdir(os.path.join(PATH, checkpoint_dir))[0]
    checkpoint_file = os.path.join(checkpoint_dir, checkpoint_file)
    # The trailing number in the checkpoint file is the starting line for the circuit file
    starting_line = int(checkpoint_file[checkpoint_file.rfind("_") + 1 :])

    io_info.setup()
    io_info.set_initial_state(checkpoint_file)

    # Retrieve input dictionary
    namelist_name, input_dict = read_nml(os.path.join(PATH, io_info.input_namelist))
    # Retrieve observables class
    with open(os.path.join(PATH, "observables.pk"), "rb") as fh:
        observables = pickle.load(fh)
    obs_out_path = os.path.join(io_info.outPATH, observables.folder_observables)
    if not os.path.isdir(obs_out_path):
        os.mkdir(obs_out_path)
    # Modify the input dict to add the new informations
    input_dict["settings%initial_state"] = checkpoint_file
    input_dict["settings%initial_line"] = starting_line
    input_dict["settings%outPATH"] = io_info.outPATH

    # Save input parameters on namelist file
    write_nml(namelist_name, input_dict, os.path.join(PATH, io_info.input_namelist))

    # Run the fortran program with the namelist name as argument
    res = subprocess.run(io_info.exe_file, capture_output=True)
    if res.stderr:
        print("--------------------------------------------")
        print("Program terminated with the following error:")
        print(res.stderr.decode())
        print("--------------------------------------------")
        sys.exit(1)
    result = SimulationResults(input_dict, observables)

    # Retrieve results
    result._get_results()

    return result
