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
General utility functions and classes for the simulation
"""

# Import necessary packages
import os
import pickle
import shutil
import json
import time
from warnings import warn
from typing import OrderedDict
import numpy as np
from qiskit.circuit import QuantumCircuit
import qiskit.qpy as qpy_serialization
from qtealeaves import write_nml
from qtealeaves.convergence_parameters import TNConvergenceParameters
from qtealeaves.emulator import _AbstractTN
from qtealeaves.observables import TNObservables
from qtealeaves.tensors.tensor import GPU_AVAILABLE

from .tn_utils import QCOperators
from .mpi_utils import MPISettings

EXE_PATH_DIR = os.path.dirname(__file__)
EXE_PATH = os.path.join(EXE_PATH_DIR, "bin/qmatchatea.exe")

__all__ = [
    "print_state",
    "fidelity",
    "QCCheckpoints",
    "QCIO",
    "QCConvergenceParameters",
    "QCBackend",
    "SimpleHamiltonian",
]


class SimpleHamiltonian(dict):
    """
    Simple class for an Hamiltonian that extends a normal dictionary.
    The keys are the pauli strings, the values the coefficients.
    It is used for simplicity, since it has a `to_pauli_dict` method
    equivalent to qiskit and other methods to ease the construction.
    """

    def set_num_qubits(self, num_qubits):
        """
        Set the number of qubits the Hamiltonian is describing

        Parameters
        ----------
        num_qubits : int
            Number of qubits
        """
        self["num_qubits"] = num_qubits

    def add_term(self, hterms, qubits, coeff):
        """
        Add a term to the Hamiltonian acting on the
        qubits qubits. You do not need to specify the identities

        Parameters
        ----------
        hterms : str or array-like
            Pauli matrices to apply
        qubits : int or array-like
            Qubits where the terms acts
        coeff : complex
            Coefficient of the term

        Returns
        -------
        None
        """
        if np.isscalar(qubits):
            qubits = np.array([qubits])
            hterms = np.array([hterms])
        ordering = np.argsort(qubits)
        qubits = qubits[ordering]
        hterms = hterms[ordering]

        pauli_string = ""
        for hterm, qubit in zip(hterms, qubits):
            last_qubit = len(pauli_string)
            pauli_string += "I" * (qubit - last_qubit)
            pauli_string += hterm
        last_qubit = len(pauli_string)
        pauli_string += "I" * (self["num_qubits"] - last_qubit)

        self[pauli_string[::-1]] = coeff

    def to_pauli_dict(self):
        """
        Get the qiskit pauli dict representation, that can be later
        used in the observable class

        Returns
        -------
        dict
            dictionary with qiskit pauli_dict old format
        """
        pauli_dict = {"paulis": []}
        for key, val in self.items():
            if key == "num_qubits":
                continue

            pauli_dict["paulis"].append(
                {"label": key, "coeff": {"real": np.real(val), "imag": np.imag(val)}}
            )
        return pauli_dict


class QCCheckpoints:
    """
    Class to handle checkpoint parameters

    Parameters
    ----------
    PATH: str, optional
        PATH to the checkpoint directory. Default `data/checkpoints/`.
    frequency: float, optional
        Decide the frequency, in **hours**, of the checkpoints.
        If negative no checkpoints are present. Default to -1.
    input_nml: str, optional
        Name of the input namelist. Default 'input.nml'
    restart: int, optional
        If an int is provided, it is the checkpoint counter from which the user wants to restart.
        Default to None.
    """

    def __init__(
        self,
        PATH="data/checkpoints/",
        frequency=-1,
        input_nml="input.nml",
        restart=None,
    ):
        self._PATH = PATH if (PATH.endswith("/")) else PATH + "/"
        self._frequency = frequency
        self._input_nml = input_nml
        self.restart = restart
        self._checkpoint_cnt = 0
        self._initial_line = 0
        self._initial_time = -1

    def set_up(
        self,
        input_dict,
        operators=QCOperators(),
        observables=TNObservables(),
        circ="",
    ):
        """Set up the checkpoints directory

        Parameters
        ----------
        input_dict : dict
            Input parameter dictionary
        operators : :py:class:`QCOperators`, optional
            Tensor operators
        obervables : :py:class: `TNObservables`, optional
            Tensor observables
        circ_str: str or QuantumCircuit
            String representing the quantum circuit (fortran) or
            the qiskit quantum circuit (python)
        """
        if not isinstance(operators, QCOperators):
            raise TypeError("Operators must be QCOperators type")
        elif not isinstance(observables, TNObservables):
            raise TypeError("observables must be TNObservables type")

        if not os.path.isdir(self.PATH):
            os.mkdir(self.PATH)

        # Modify for new PATH
        input_dict["inPATH"] = self.PATH

        # Write files that can be already written
        with open(os.path.join(self.PATH, "observables.pk"), "wb") as fh:
            pickle.dump(observables, fh)
        _, operator_mapping = operators.write_input_3(self.PATH)
        observables.write(self.PATH, {}, operator_mapping)
        write_nml("INPUT", input_dict, os.path.join(self.PATH, self.input_nml))

        # We save extra infos for checkpoints, i.e. the quantum circuit
        if isinstance(circ, str):
            with open(os.path.join(self.PATH, "circuit.dat"), "w") as fh:
                fh.write(circ)
        elif isinstance(circ, QuantumCircuit):
            with open(os.path.join(self.PATH, "circuit.qpy"), "wb") as fd:
                qpy_serialization.dump(circ, fd)
        else:
            raise ValueError(f"Impossible to handle circuit of type {type(circ)}")

        self._initial_time = time.time()

    @property
    def PATH(self):
        """PATH property"""
        return self._PATH

    @property
    def frequency(self):
        """Checkpoint frequency property"""
        return self._frequency

    @property
    def input_nml(self):
        """Input namelist property"""
        return self._input_nml

    def save_checkpoint(self, operation_idx, emulator):
        """
        Save the state for the checkpoint if the
        `operation_idx` exceeded the frequency of the
        checkpoints

        Parameters
        ----------
        operation_idx : int
            Index of the current operation in the quantum circuit
        emulator: _AbstractTN
            Tensor network class

        Returns
        -------
        None
        """
        elapsed_time = (time.time() - self._initial_time) / 3600
        if elapsed_time > self.frequency > 0:
            dir_path = os.path.join(self.PATH, str(self._checkpoint_cnt))

            # Create directory if not accessible
            if not os.path.isdir(dir_path):
                os.makedirs(dir_path)

            # Save the TN state on file.
            file_path = os.path.join(dir_path, "tn_state.npy")
            tensor_list = emulator.to_tensor_list()
            np.save(file_path, np.array(tensor_list, dtype=object), allow_pickle=True)

            # Save the index of the line on file
            # The +1 is because that operation has already been applied
            with open(os.path.join(dir_path, "index.txt"), "w") as fh:
                fh.write(str(operation_idx + 1))

            # Update the counter
            self._checkpoint_cnt += 1

            # Restart the countdown to the next checkpoint
            self._initial_time = time.time()

    def restart_from_checkpoint(self, initial_state):
        """
        Restart from the checkpoint passed in the initialization. Python only.

        Parameters
        ----------
        initial_state: str | List[Tensors] | _AbstractTN
            The initial state of the simulation. Might be overwritten on exit.

        Returns
        -------
        str | List[Tensors] | _AbstractTN
            The new initial state. If `self.restart` is None, it is the old
            initial state.
        """
        # Default value, no restart was requested
        if self.restart is None:
            return initial_state

        # If the value is -1, restart from the last one
        if self.restart == -1:
            self.restart = 0
            while os.path.isdir(os.path.join(self.PATH, str(self.restart))):
                self.restart += 1
            self.restart -= 1

        dir_path = os.path.join(self.PATH, str(self.restart))

        # Save the index of the line on file
        with open(os.path.join(dir_path, "index.txt"), "r") as fh:
            self._initial_line = int(fh.read())

        # Read the TN state
        initial_state = np.load(
            os.path.join(dir_path, "tn_state.npy"), allow_pickle=True
        )

        return initial_state

    def to_dict(self):
        """Return the ordered dictionary of the properties of
        the class for fortran

        Returns
        -------
        dictionary: OrderedDict
            Ordered dictionary of the class properties
        """
        dictionary = OrderedDict()

        dictionary["checkpoint_PATH"] = self.PATH
        dictionary["checkpoint_frequency"] = self.frequency
        dictionary["initial_line"] = 1

        return dictionary

    def to_json(self, path):
        """
        Write the class as a json on file
        """
        path = os.path.join(path, "checkpoints.json")
        with open(path, "w") as fp:
            json.dump(self.to_dict(), fp, indent=4)

    @classmethod
    def from_json(cls, path):
        """
        Initialize the class from a json file
        """
        path = os.path.join(path, "checkpoints.json")
        with open(path, "r") as fp:
            dictionary = json.load(fp)[0]

        return cls(**dictionary)


class QCIO:
    """
    Class to handle Input/Output parameters

    Parameters
    ----------
    inPATH: str, optional
        PATH to the directory containing the input files.
        Default to 'data/in/'
    outPATH: str, optional
        PATH to the directory containing the output files.
        Default to 'data/out/'
    input_namelist: str, optional
        Name of the input namelist file. Name, NOT PATH.
        Default to 'input.nml'
    exe_file: list of str, optional
        Path to the executable plus additional commands
        Default to `[EXE_PATH_SERIAL]`.
    initial_state: str or :py:class:`MPS`, optional
        If an MPS, then the list of tensors is used as initial state for
        a starting point of the FORTRAN simulation, saving the file to
        inPATH/initial_state.dat. If 'Vacuum' start from |000...0>. Default to 'Vacuum'.
        If a PATH it is a PATH to a saved MPS.
    sparse: bool, optional
        Weather to write operators in a semi-sparse format or not.
        Default to False
    """

    initial_states_keywords = ("vacuum", "random")

    def __init__(
        self,
        inPATH="data/in/",
        outPATH="data/out/",
        input_namelist="input.nml",
        exe_file=None,
        initial_state="Vacuum",
        sparse=False,
    ):
        self._inPATH = inPATH if inPATH.endswith("/") else inPATH + "/"
        self._outPATH = outPATH if outPATH.endswith("/") else outPATH + "/"
        self._input_namelist = input_namelist

        if exe_file is None:
            self._exe_file = [EXE_PATH]
        # Check if people don't read docstring
        # and use strings nevertheless
        elif isinstance(exe_file, str):
            self._exe_file = [exe_file]
        else:
            self._exe_file = exe_file
        self._sparse = sparse
        self._initial_state = initial_state

    def setup(self, fortran=False):
        """
        Setup the io files

        Parameters
        ----------
        fortran: bool, optional
            If True, the simulation will be run by fortran.
            Default to False.
        """

        # Directories
        if not os.path.isdir(self.inPATH):
            os.makedirs(self.inPATH)
        if not os.path.isdir(self.outPATH):
            os.makedirs(self.outPATH)

        # Executable. Not used for python simulations
        if self.exe_file[-1] != os.path.join(self.inPATH, self.input_namelist):
            self._exe_file += [os.path.join(self.inPATH, self.input_namelist)]

        # Initial state

        # First, check if it is a string.
        if isinstance(self.initial_state, str):
            if self.initial_state.lower() not in self.initial_states_keywords:
                # Handle the string case assuming it is a path
                if not os.path.isfile(self.initial_state):
                    raise Exception("Path to input file does not exist.")

                # Move it to the input folder if fortran is involved
                if fortran:
                    new_path = os.path.join(
                        self.inPATH, os.path.basename(self.initial_state)
                    )
                    shutil.copy(self.initial_state, new_path)
                    self._initial_state = os.path.basename(self.initial_state)
        else:
            # Assume it is an _AbstractTN that we can write in a formatted way
            if hasattr(self.initial_state, "write"):
                self.initial_state.write(os.path.join(self.inPATH, "initial_state"))
            elif hasattr(self.initial_state, "save_pickle"):
                self.initial_state.save_pickle(
                    os.path.join(self.inPATH, "initial_state")
                )
            # Assume it is a list and use numpy save
            else:
                np.save(
                    os.path.join(self.inPATH, "initial_state"),
                    np.array(self.initial_state, dtype=object),
                    allow_pickle=True,
                )
            if fortran:
                self._initial_state = "initial_state.dat"

    @property
    def inPATH(self):
        """Input PATH property"""
        return self._inPATH

    @property
    def exe_cmd(self):
        """Executable command to run on the terminal"""
        return [self.exe_file, self._inPATH + self._input_namelist]

    @property
    def outPATH(self):
        """Output PATH property"""
        return self._outPATH

    @property
    def input_namelist(self):
        """Input namelist property"""
        return self._input_namelist

    @property
    def exe_file(self):
        """Executable file and commands property"""
        return self._exe_file

    @property
    def sparse(self):
        """Tensor sparsity property"""
        return self._sparse

    @property
    def initial_state(self):
        """Initial state property"""
        return self._initial_state

    # @initial_state.setter
    def set_initial_state(self, initial_state):
        """Modify the initial state property"""
        if not isinstance(initial_state, str):
            if not isinstance(initial_state, _AbstractTN):
                raise TypeError(
                    "A non-str initial state must be initialized as an _AbstractTN class"
                )
        self._initial_state = initial_state

    # @exe_file setter
    def set_exe_file(self, exe_file):
        """Modify exe file"""
        if not isinstance(exe_file, list):
            raise TypeError(f"exe_file must be a list of strings, not {type(exe_file)}")
        self._exe_file = exe_file

    def to_dict(self):
        """Return the ordered dictionary of the properties of
        the class for fortran

        Returns
        -------
        dictionary: OrderedDict
            Ordered dictionary of the class properties
        """
        dictionary = OrderedDict()
        for prop, value in vars(self).items():
            if prop in ("_exe_file", "_input_namelist"):
                continue
            if prop == "_initial_state" and not isinstance(value, str):
                value = "initial_state.dat"
            dictionary[prop[1:]] = value

        return dictionary

    def to_json(self, path):
        """
        Write the class as a json on file
        """
        path = os.path.join(path, "io_info.json")
        with open(path, "w") as fp:
            json.dump(self.to_dict(), fp, indent=4)

    @classmethod
    def from_json(cls, path):
        """
        Initialize the class from a json file
        """
        path = os.path.join(path, "io_info.json")
        with open(path, "r") as fp:
            dictionary = json.load(fp)[0]

        return cls(**dictionary)


class QCConvergenceParameters(TNConvergenceParameters):
    """Convergence parameter class, inhereting from the
    more general Tensor Network type. Here the convergence
    parameters are only the bond dimension and the cut ratio.

    Parameters
    ----------
    max_bond_dimension : int, optional
        Maximum bond dimension of the problem. Default to 10.
    cut_ratio : float, optional
        Cut ratio for singular values. If :math:`\\lambda_n/\\lambda_1 <` cut_ratio then
        :math:`\\lambda_n` is neglected. Default to 1e-9.
    trunc_tracking_mode : str, optional
        Modus for storing truncation, 'M' for maximum, 'C' for
        cumulated (default).
    svd_ctrl : character, optional
        Control for the SVD algorithm. Available:
        - "A" : automatic. Some heuristic is run to choose the best mode for the algorithm.
                The heuristic can be seen in qtealeaves/tensors/tensors.py
                in the function _process_svd_ctrl.
        - "V" : gesvd. Safe but slow method. Recommended in Fortran simulation
        - "D" : gesdd. Fast iterative method. It might fail. Resort to gesvd if it fails
        - "E" : eigenvalue decomposition method. Faster on GPU. Available only when
                contracting the singular value to left or right
        - "X" : sparse eigenvalue decomposition method. Used when you reach the maximum
                bond dimension. Only python.
        - "R" : random svd method. Used when you reach the maximum bond dimension.
                Only python.
        Default to 'A'.
    ini_bond_dimension: int, optional
        Initial bond dimension of the simulation. It is used if the initial state is random.
        Default to 1.

    """

    def __init__(
        self,
        max_bond_dimension=10,
        cut_ratio=1e-9,
        trunc_tracking_mode="C",
        svd_ctrl="A",
        ini_bond_dimension=1,
    ):
        TNConvergenceParameters.__init__(
            self,
            max_bond_dimension=max_bond_dimension,
            cut_ratio=cut_ratio,
            trunc_tracking_mode=trunc_tracking_mode,
            svd_ctrl=svd_ctrl,
            ini_bond_dimension=ini_bond_dimension,
        )

    def to_dict(self):
        """Return the ordered dictionary of the properties of
        the class

        Returns
        -------
        dictionary: OrderedDict
            Ordered dictionary of the class properties
        """
        dictionary = OrderedDict()
        dictionary["max_bond_dimension"] = self.max_bond_dimension
        dictionary["cut_ratio"] = self.cut_ratio
        dictionary["trunc_tracking_mode"] = self.trunc_tracking_mode

        return dictionary

    def pretty_print(self):
        """
        Print the convergence parameters.
        (Implemented to avoid too few public methods)
        """
        print("-" * 50)
        print(
            "-" * 10 + f" Maximum bond dimension: {self.max_bond_dimension} " + "-" * 10
        )
        print("-" * 10 + f" Cut ratio: {self.cut_ratio} " + "-" * 10)
        print(
            "-" * 10
            + f" Truncation tracking mode: {self.trunc_tracking_mode} "
            + "-" * 10
        )
        print("-" * 50)

    def to_json(self, path):
        """
        Write the class as a json on file
        """
        path = os.path.join(path, "convergence_parameters.json")
        with open(path, "w") as fp:
            dictionary = self.to_dict()
            dictionary["svd_ctrl"] = self.svd_ctrl
            json.dump(dictionary, fp, indent=4)

    @classmethod
    def from_json(cls, path):
        """
        Initialize the class from a json file
        """
        path = os.path.join(path, "convergence_parameters.json")
        with open(path, "r") as fp:
            dictionary = json.load(fp)[0]

        return cls(**dictionary)


class QCBackend:
    """
    Backend for the simulation. Contains all the informations about
    which executable you want to run

    Parameters
    ----------
    backend : str, optional
        First backend definition. Either "PY" (python) or "FR" (fortran).
        Default to "PY".
    precision: str, optional
        Precision of the simulation.
        Select a real precision ONLY if you use ONLY real gates.
        Available:
        - "A": automatic. For the heuristic see `self.resolve_precision`.
        - "Z": double precision complex;
        - "C": single precision complex;
        - "D": double precision real;
        - "S": single precision real.
        Default to "A".
    device: str, optional
        Device of the simulation.
        Available:
        - "A" : automatic. For the heuristic see `self.resolve_device`
        - "cpu": use the cpu
        - "gpu": use the gpu if it is available
        Defailt to "A"
    ansatz : str, optional
        Weather to run the circuit with MPS or TTN tensor network ansatz.
        Default to "MPS".
    mpi_settings : MPISettings | None, optional
        Settings for running the simulation multi-node.
        Default to None, i.e. no MPI.
    """

    def __init__(
        self,
        backend="PY",
        precision="A",
        device="cpu",
        ansatz="MPS",
        mpi_settings=None,
    ):
        if backend == "FR" and device == "gpu" and precision == "C":
            raise ValueError(
                "Only double precision complex available "
                + "in fortran with the GPU device"
            )

        self._backend = backend.upper()
        self._precision = precision.upper()
        self._device = device
        if backend == "FR" and ansatz.upper() != "MPS":
            warn(
                f"Only MPS ansatz available on fortran simulation, not {ansatz}."
                + "The ansatz is set back to MPS."
            )
            ansatz = "MPS"
        self._ansatz = ansatz.upper()
        self.mpi_settings = MPISettings() if mpi_settings is None else mpi_settings

    def to_dict(self):
        """
        Map the backend to a dictionary for fortran
        """
        dictionary = OrderedDict({})
        mpi = "T" if self.num_procs > 1 else "F"
        gpu = "T" if self.device == "gpu" else "F"
        dictionary["simulation_mode"] = self.precision + mpi + gpu
        dictionary["approach"] = self.mpi_approach
        # dictionary["ansatz"] = self.ansatz

        return dictionary

    def resolve_precision(self, min_fidelity, tol=1e-7):
        """
        Resolve the precision of the simulation.
        Heuristic if `self._precision=`"A"`.

        Parameters
        ----------
        min_fidelity: float
            Lower bound of the fidelity of the simulation at the moment
        tol: float, optional
            Tolerance after which you switch to single precision.
            Default to 1e-7

        Returns
        -------
        str
            The selected precision
        """
        if self._precision != "A":
            return self.precision

        # For fortran, automatic means Z
        if self.backend == "FR":
            return "Z"

        # The lower bound of the fidelity of our state is
        # below the number of digits of a single
        # precision
        if 1 - min_fidelity > tol:
            return "C"

        return "Z"

    def resolve_device(self, bond_dimension, previous_device, exp_gpu=7):
        """
        Resolve the device if it set on automatic.

        Parameters
        ----------
        bond_dimension : int
            Maximum bond dimension of the system
        previous_device : str
            Device where the system is currently. This is used
            to ensure we do not keep exchanging data back and
            forth.
        exp_gpu : int, optional
            Exponent of the bond dimension after which you switch
            to the gpu, i.e:
            - if chi >= 2**exp_gpu -> use gpu
            - if chi <= 2**(exp_gpu-1) -> use cpu
            Default to 7. (switch at 128)

        Returns
        -------
        str
            Device where to move (or keep) the system
        """
        if self._device != "A":
            if self._device == "cgpu":
                return "cpu"
            return self._device

        # For fortran, automatic means cpu
        if self.backend == "FR":
            return "cpu"

        if bond_dimension >= 2**exp_gpu and GPU_AVAILABLE:
            return "gpu"
        # The condition on the CPU is here because we want
        # to avoid keep exchanging informations if the bond
        # dimension oscillates between 129 and 120
        if bond_dimension <= 2 ** (exp_gpu - 1):
            return "cpu"

        return previous_device

    @property
    def backend(self):
        """Backend property"""
        return self._backend

    @property
    def precision(self):
        """Precision property"""
        # For fortran, automatic means Z
        if self.backend == "FR":
            return "Z"
        return self._precision

    @property
    def device(self):
        """Device property"""
        # For fortran, automatic means cpu
        if self.backend == "FR":
            return "cpu"
        return self._device

    @property
    def num_procs(self):
        """Number of processes property"""
        return self.mpi_settings.num_procs

    @property
    def mpi_approach(self):
        """mpi_approach property"""
        return self.mpi_settings.mpi_approach.upper()

    @property
    def ansatz(self):
        """ansatz property"""
        return self._ansatz

    @property
    def mpi_command(self):
        """mpi_command property"""
        return self.mpi_settings.mpi_command

    @property
    def identifier(self):
        """Identifier combining all properties."""
        return ":".join(
            [
                self.backend,
                self.resolve_precision(1),
                self.resolve_device(1, "cpu"),
                str(self.num_procs),
                self.mpi_approach,
                self.ansatz,
            ]
        )

    def to_json(self, path):
        """
        Write the class as a json on file as
        backend.json in the flder path
        """
        path = os.path.join(path, "backend.json")
        dictionary = OrderedDict()
        dictionary["backend"] = self.backend
        dictionary["device"] = self.device
        dictionary["precision"] = self.precision
        dictionary["num_procs"] = self.num_procs
        dictionary["ansatz"] = self.ansatz
        dictionary["mpi_approach"] = self.mpi_approach
        dictionary["mpi_command"] = self.mpi_command

        with open(path, "w") as fp:
            json.dump(dictionary, fp, indent=4)

    @classmethod
    def from_json(cls, path):
        """
        Initialize the class from a json file called
        "backend.json" in the folder path
        """
        path = os.path.join(path, "backend.json")
        with open(path, "r") as fp:
            dictionary = json.load(fp)[0]

        return cls(**dictionary)


def merge_ordered_dicts(dicts):
    """Merge ordered dicts together, concatenating them in the order provided in the list

    Parameters
    ----------
    dicts : list of OrderedDict
        OrderedDict to concatenate

    Return
    ------
    final_dict: OrderedDict
        Concatenated OrderedDict
    """
    for dictionary in dicts:
        if not isinstance(dictionary, OrderedDict):
            raise TypeError("Only OrderedDict can be concatenated using this function")

    final_dict = dicts[0]
    for dictionary in dicts[1:]:
        final_dict.update(dictionary)

    return final_dict


def print_state(dense_state):
    """
    Prints a *dense_state* with kets. Compatible with quimb states.

    Parameters
    ----------
    dense_state: array_like
            Dense representation of a quantum state

    Returns
    -------
    None: None
    """

    NN = int(np.log2(len(dense_state)))

    binaries = [bin(ii)[2:] for ii in range(2**NN)]
    binaries = ["0" * (NN - len(a)) + a for a in binaries]  # Pad with 0s

    ket = []
    for ii, coef in enumerate(dense_state):
        if not np.isclose(np.abs(coef), 0.0):
            if np.isclose(np.imag(coef), 0.0):
                if np.isclose(np.real(coef), 1.0):
                    ket.append("|{}>".format(binaries[ii]))
                else:
                    ket.append("{:.3f}|{}>".format(np.real(coef), binaries[ii]))
            else:
                ket.append("{:.3f}|{}>".format(coef, binaries[ii]))
    print(" + ".join(ket))


def fidelity(psi, phi):
    """
    Returns the fidelity bewteen two quantum states *psi*, *phi* defined as
    :math:`|\\langle\\psi|phi\\rangle|^2`

    Parameters
    ----------
    psi: complex np.array or quimb.core.qarray
            Quantum state
    phi: complex np.array or quimb.core.qarray
            Quantum state

    Returns
    -------
    Fidelity: double real
            Fidelity of the two quantum states
    """

    # Enforcing normalization
    psi /= np.sqrt(np.abs(np.sum(psi.conj() * psi)))
    phi /= np.sqrt(np.abs(np.sum(phi.conj() * phi)))

    return np.abs(np.vdot(psi, phi)) ** 2
