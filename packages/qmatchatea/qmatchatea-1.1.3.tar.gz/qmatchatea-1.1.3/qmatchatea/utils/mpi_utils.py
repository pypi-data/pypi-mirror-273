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
Function to help in the MPI protocol. Here you insert barriers, which means
canonization of the state each where_barriers layers. In particular, it is
important because at each layer in the circuit description is connected a
canonization in the MPS simulation. If the canonization are not often enough
the simulation might not converge.

Functions and classes
---------------------

"""

try:
    from strawberryfields import Program

    SF_IS_IMPORTED = True
except ModuleNotFoundError:
    SF_IS_IMPORTED = False
try:
    from qiskit.visualization.utils import _get_layered_instructions
except ImportError:
    # This try except makes the code compatible also with the latest version of
    # qiskit, where the _get_layered_instructions changed path
    from qiskit.visualization.circuit._utils import _get_layered_instructions
from qiskit import QuantumCircuit
import numpy as np
from .sf_utils import Barrier

__all__ = ["MPISettings", "to_layered_circ"]


class MPISettings:
    """
    Settings for using the library on multiple processes using MPI.
    The default settings use no MPI, i.e. a serial execution of the algorithm.

    Parameters
    ----------
    mpi_approach: str, optional
        Approach for the MPI simulation.
        Available:
        - "SR": serial, the algorithm is run serially on the TN ansatz
        - "CT": cartesian, the MPS is divided between different processes,
                and the algorithm is done in parallel. MPS ONLY.
        - "MW": master-worker. The MPS is stored ona single process (the master)
                but the operations are done on the worker processes. It requires
                a lot of communications. FORTRAN ONLY, MPS ONLY.
        Default to "SR".
    isometrization: int | List[int], optional
        How to perform the isometrization.
        - `-1` is a serial isometrization step
        - A `int` is a parallel isometrization step with that number of layers
        - A `List[int]` is a parallel isometrization step where each entry is
          the number of layers for the `i`-th isometrization. If the number of
          isometrization steps is greater than the length of the array, the array
          is repeated.
        Default to `-1`
    num_procs: int, optional, FORTRAN ONLY
        Number of processes for the MPI simulation. Default to 1.
    mpi_command : List[str], optional, FORTRAN ONLY
        MPI command that should be called when launching MPI from fortran.
        The "-n" for the number of processes is already taken into account.
        Default to ["mpi_exec"].
    """

    def __init__(
        self, mpi_approach="SR", isometrization=-1, num_procs=1, mpi_command=None
    ):
        self.num_procs = num_procs
        self.mpi_approach = mpi_approach.upper()
        self.isometrization = isometrization
        if mpi_command is None:
            mpi_command = ["mpiexec"]
        self.mpi_command = list(mpi_command)

    def __getitem__(self, idx):
        """
        Get the settings of the isometrization for the idx-th isometrization
        """
        if np.isscalar(self.isometrization):
            return self.isometrization

        return self.isometrization[idx % len(self.isometrization)]

    def print_isometrization_type(self, idx):
        """
        print which type of isometrization we have at index idx

        Parameters
        ----------
        idx : int
            Index of the isometrization
        """

        iso_type = self[idx]
        if iso_type < 0:
            print(f"At step {idx} serial isometrization")
        else:
            print(f"At step {idx} parallel isometrization with {iso_type} layers")


def _to_layered_circ_qk(qc, where_barriers=1):
    """
    Transform a quantum circuit in another, where the instruction are ordered by layers.
    Apply a barrier every where_barriers layers.

    Parameters
    ----------
    qc: qiskit.QuantumCircuit
        Quantum circuit
    where_barriers: int
        Apply a barrier every where_barriers layers.

    Returns
    -------
    layered_qc: qiskit.QuantumCircuit
            Ordered quantum circuit with barriers
    """
    layered_qc = QuantumCircuit(qc.num_qubits)

    layered_instructions = _get_layered_instructions(qc)[2]
    for ii, layer in enumerate(layered_instructions):
        for instruction in layer:
            layered_qc.append(instruction.op, instruction.qargs, instruction.cargs)
        if ii % where_barriers == 0:
            layered_qc.barrier()

    return layered_qc


def _obtain_layers_sf(program):
    """
    Obtain the different layers of a sf program to optimize the MPI process

    Parameters
    ----------
    program: sf.Program
        Strawberry fields program

    Returns
    -------
    layers: list
        A list of lists. Each sublist is a layer of the program, containing the commands
    """
    if not SF_IS_IMPORTED:
        raise ImportError("Strawberryfields library is not imported or installed.")
    layers = []
    # Current_idxs contains the "position" of the last gate on each wire (qumode)
    current_idxs = np.zeros(program.num_subsystems, dtype=int)
    for com in program.circuit:
        if max(current_idxs) >= len(layers):
            layers.append([])
        idxs = [rg.ind for rg in com.reg]
        idx = min(idxs)
        layers[current_idxs[idx]].append(com)
        # You apply a gate, so the first available position shifts right (+1)
        current_idxs[idxs] += 1

    # Drop last empty layer
    layers = layers[:-1]

    return layers


def _to_layered_circ_sf(program, where_barriers=1):
    """
    Transform a strawberry fields program in another,
    where the instruction are ordered by layers.
    Apply a barrier every where_barriers layers.

    Parameters
    ----------
    program: sf.Program
        strawberry fields program
    where_barriers: int
        Apply a barrier every where_barriers layers.

    Returns
    -------
    layered_program: sf.Program
        Ordered sf program with barriers
    """
    if not SF_IS_IMPORTED:
        raise ImportError("Strawberryfields library is not imported or installed.")
    layered_program = Program(program.num_subsystems)
    layers = _obtain_layers_sf(program)

    for ii, layer in enumerate(layers):
        for comm in layer:
            idxs = [rg.ind for rg in comm.reg]
            regs = [layered_program.register[idx] for idx in idxs]

            layered_program.append(comm.op, regs)
        if ii % where_barriers == 0:
            layered_program.append(Barrier(), layered_program.register)

    return layered_program


def to_layered_circ(circ, where_barriers=1):
    """
    Interface for the transformation of qiskit and strawberry fields circuit
    into layered ones, the correct order for the MPI protocols.
    You also insert barriers, i.e. canonization procedures

    Parameters
    ----------
    circ: strawberryfields.program.Program or qiskit.circuit.quantumcircuit.QuantumCircuit
        Quantum circuit instance
    where_barriers: int
        Apply a barrier every where_barriers layers.

    Returns
    -------
    layered_circ: strawberryfields.program.Program or qiskit.circuit.quantumcircuit.QuantumCircuit
        Ordered circuit program with barriers
    """

    if isinstance(circ, QuantumCircuit):
        layered_circ = _to_layered_circ_qk(circ, where_barriers)
    elif SF_IS_IMPORTED and isinstance(circ, Program):
        layered_circ = _to_layered_circ_sf(circ, where_barriers)
    else:
        raise TypeError(
            "Only qiskit quantum circuit of strawberry fields programs\
             are implemented. Your circuit is of type:"
            + str(type(circ))
        )

    return layered_circ
