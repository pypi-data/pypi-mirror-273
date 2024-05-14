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
In order to simulate the quantum circuit we first need to preprocess it, to put it in a way
suitable for the MPS simulation. Afterwards, **if** a fortran backend is selected the parsing
process is applied, i.e. a suitable input file is generated for the fortran backend.
Thus, the two main processes explained here are:

1. Preprocessing of the circuit
2. Parsing the circuit for the Fortran I/O

Preprocessing
~~~~~~~~~~~~~

The tensor network ansatz that is used in the simulator is called Matrix Product States (MPS).
In this ansatz each degree of freedom (qubit, mode, particle) is treated as a rank-3 tensor.
We can only apply operators which are **local** or that applies to **nearest neighbors**.
This means that, when a circuit is passed to the preprocessing it is translated in an equivalent
circuit that follows these two properties. While for quantum optics these properties are already
ensured, for qubits quantum circuit we have to perform some transformations. We use qiskit for them,
and in particular we:

- Map the circuit using a pre-defined set of gates, called basis_gates.
  These gates can be passed to the function, to satisfy
  a particular constraint of a physical machine we want to simulate
- Map the circuit into a linear circuit. By an optimized application of *swap*
  gates we map non-local two-qubit gates into a series
  of local two-qubit gates.

These operations are automatically performed by the higher level function :py:func:`run_simulation`.
However, it is important to take into account that these operations require time, which is
proportional to the size of the circuit. For this reason, if the user has to perform multiple
simulation of the same circuit varing other parameres, e.g. the bond dimension, it is suggested to
perform the preprocessing only once, and then disable the mapping and the linearization of the
function.

.. warning::
    The preprocessing and linearization using qiskit modifies the order of the qubits.
    This is a behavior we don't want to experience, and such inside the preprocessing
    procedure the qubits are again ordered in the initial layout.

Parsing
~~~~~~~

These procedures are mirroring the Fortran procedure for the argument parsing. This means that,
if these are modified also the others **must** be modified and viceversa. However, the parsing
is not the only thing they do. Indeed, the quantum circuit from qiskit or the Program from
strawberry fields are analyzed, and the operators used inside them are saved into a file for
fortran under the form of tensors. The syntax that an input file must follow after the parsing
is the following:

.. code-block:: console

    total_num_sites
        total_num_classical_bits
        num_remaining_lines
        operator_name operator_idx num_sites
            first_site second_site
        operator_name operator_idx num_sites
            first_site

The *operator_idx* is a unique integer map to the operator tensor, stored in a different file.

"""


import os
import os.path
import warnings
from qiskit import QuantumCircuit, transpile, transpiler
import numpy as np
from qtealeaves import StrBuffer
from .utils.sf_utils import optical_gates
from .utils.qk_utils import get_index, qk_transpilation_params
from .tensor_compiler import tensor_compiler

try:
    from strawberryfields import Program

    SF_IS_IMPORTED = True
except ModuleNotFoundError:
    warnings.warn(
        "Not able to import strawberry-fields. Some functions will not be usable.",
        ImportWarning,
    )
    SF_IS_IMPORTED = False

__all__ = ["pre_parser", "preprocess"]
# Swap matrix
swap = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])


# Strawberry fields gates are contained in optical_gates.
def _pre_parser_qk(qc, operators, folder_dst):
    """
    Map a qiskit quantum circuit into a pair of text files to be read by the fortran
    simulator. The first one contains all the tensors that will be applied on the MPS as
    tensor structure, while the second the circuit structure with the following syntax:

    .. code-block::

        total_num_qubits
        total_num_bits
        num_remaining_lines
        gate_name gate_idx num_qubits
            first_qubit second_qubit
        gate_name gate_idx first num_qubits
            first_qubit

    Parameters
    ----------
    qc: qiskit.QuantumCircuit
        Quantum circuit instance
    operators: :py:class:`QCOperators`
        Operator class with the observables operators ALREADY THERE
    folder_dst: string
        path to the folder where the operators file `TENSORS/operator.dat` and
        `circuit.dat` will be saved

    Returns
    -------
    num_qubits: int
        Number of qubits
    id_mapping: dict
        Mapping between operator name and integer ID
    circ: str
        String containing the circuit
    """
    assert os.path.isdir(folder_dst), "Provided PATH does not exists"

    data = qc.data  # data structure of the quantum circuit
    qubits = []  # List of target qubits
    clbits = []  # List of used classical bits
    temp = 0  # Temporary variable for the definition of parametric gates names
    op_names = []
    basic_names = []
    conditions = []

    for instance in data:
        gate_name = instance[0].name
        basic_names.append(gate_name)
        if gate_name == "barrier":
            gate_mat = np.zeros(1)
        elif gate_name == "measure":
            gate_mat = np.zeros(1)
        else:
            gate_mat = instance[0].to_matrix()
        num_qubits = len(instance[1])
        num_params = len(instance[0].params)

        qubits.append(np.array([get_index(qc, instance[1][0])]))
        clbits.append([get_index(qc, cl) for cl in instance[2]])
        conditions.append(instance[0].condition)

        # If the gate has not yet been encountered we add it to the
        # name dictionary and the tensor list. Notice that this happens
        # in two cases: if the gate_name is new OR if the gate is parametric,
        # since parametric gates have different matric representation depending on the parameters
        if gate_name not in operators.ops.keys() or num_params > 0:
            if num_params > 0:
                gate_name = gate_name + str(temp)
                temp += 1
            # the transposition is due to an operation done inside the operator class
            # where it stores the state column-major order
            if num_qubits == 2 and gate_name != "barrier":
                gate_mat = gate_mat.reshape(2, 2, 2, 2)
            operators.ops[gate_name] = gate_mat

        if num_qubits == 2:
            qubits[-1] = np.append(qubits[-1], get_index(qc, instance[1][1]))

        op_names.append(gate_name)

    # Save tensors on file and retrieve ID mapping
    _, id_mapping = operators.write_input_3(folder_dst)

    # Save circuit on file
    circuit_dst = os.path.join(folder_dst, "circuit.dat")
    circ = StrBuffer()
    circ.write(str(qc.num_qubits) + "\n")
    circ.write(str(qc.num_clbits) + "\n")
    circ.write(str(len(op_names)) + "\n")
    for jj, name in enumerate(op_names):
        # +1 to be consistent with the fortran standard, where arrays start from 1
        circ.write(
            basic_names[jj]
            + " "
            + str(id_mapping[name])
            + " "
            + str(len(qubits[jj]))
            + " "
            + str(len(clbits[jj]))
            + f" {int(conditions[jj] is not None)}"
            + "\n"
        )
        circ.write("\t")
        for qub in qubits[jj]:
            circ.write(str(qub + 1) + " ")  # Qubit numbers
        for clbit in clbits[jj]:
            circ.write(str(clbit + 1) + " ")  # Classical bit numbers
        # Index of the interested classical bit and supposed vakye
        if conditions[jj] is not None:
            circ.write(f"{get_index(qc, conditions[jj][0])} {int(conditions[jj][1])} ")
        circ.write("\n")

    with open(circuit_dst, "w") as fh:
        fh.write(circ())

    return qc.num_qubits, id_mapping, circ()


def _pre_parser_sf(sf_program, operators, folder_dst, fock_cutoff, **kwargs):
    """
    Map a strawberry_fields program into a pair of text files to be read by the fortran
    simulator. The first one contains all the tensors that will be applied on the MPS as
    tensor structure, while the second the circuit structure with the following syntax:

    .. code-block::

        total_num_modes
        0
        num_remaining_lines
        gate_name gate_idx num_modes
            first_mode second_mode
        gate_name gate_idx num_modes
            first_mode

    Parameters
    ----------
    qc: sf.Program
        Strawberry fields program
    operators: :py:class:`QCOperators`
        Operator class with the observables operators ALREADY THERE
    folder_dst: string
        path to the folder where the operators file `TENSORS/operator.dat` and
        `circuit.dat` will be saved
    fock_cutoff: int
        cutoff of the fock space

    Returns
    -------
    num_modes: int
        Number of modes
    id_mapping: dict
        Mapping between operator name and integer ID
    circ: str
        String containing the circuit
    """
    if not SF_IS_IMPORTED:
        raise ImportError("Strawberryfields library is not imported.")
    assert os.path.isdir(folder_dst), "Provided PATH does not exists"

    data = sf_program.circuit  # data structure of the program
    modes = []  # List of target qubits
    temp = 0  # Temporary variable for the definition of parametric gates names
    op_names = []
    basic_names = []

    for instance in data:
        gate_name = type(instance.op).__name__
        basic_names.append(gate_name)
        modes_temp = [idx.ind for idx in instance.reg]
        params = instance.op.p
        gate_mat = optical_gates[gate_name](*params, fock_cutoff)

        num_modes = len(modes_temp)
        num_params = len(params)

        modes.append(modes_temp)

        # If the gate has not yet been encountered we add it to the
        # name dictionary and the tensor list. Notice that this happens
        # in two cases: if the gate_name is new OR if the gate is parametric,
        # since parametric gates have different matric representation depending on the parameters
        if gate_name not in operators.ops.keys() or num_params > 0:
            if num_params > 0:
                gate_name = gate_name + str(temp)
                temp += 1

            if num_modes == 2:
                gate_mat = np.transpose(gate_mat, [0, 2, 1, 3])

            operators.ops[gate_name] = gate_mat

        op_names.append(gate_name)

    # Save tensors on file and retrieve ID mapping
    _, id_mapping = operators.write_input_3(folder_dst, **kwargs)

    # Save circuit on file
    circuit_dst = os.path.join(folder_dst, "circuit.dat")
    circ = StrBuffer()
    circ.write(str(sf_program.num_subsystems) + "\n")
    circ.write("0 \n")  # 0 classical bits.
    # In this way we are consistent with the qiskit preprocessor
    # and thus need only a single reader in Fortran
    circ.write(str(len(op_names)) + "\n")
    for jj, name in enumerate(op_names):
        # +1 to be consistent with the fortran standard, where arrays start from 1
        circ.write(
            basic_names[jj]
            + " "
            + str(id_mapping[name])
            + " "
            + str(len(modes[jj]))
            + " "
            + str(0)
            + "\n"
        )  # At the moment no classical bit is present for quantum optics
        circ.write("\t")
        for qub in modes[jj]:
            circ.write(str(qub + 1) + " ")  # Mode numbers
        circ.write("\n")

    with open(circuit_dst, "w") as fh:
        fh.write(circ())

    return sf_program.num_subsystems, id_mapping, circ()


def pre_parser(circ, operators, folder_dst, **kwargs):
    """
    Interface for the preparser of qiskit and strawberry fields

    Parameters
    ----------
    circ: strawberryfields.program.Program or qiskit.circuit.quantumcircuit.QuantumCircuit
        Quantum circuit instance
    operators: :py:class:`QCOperators`
        Operator class with the observables operators ALREADY THERE
    folder_dst: str
        path to the folder where the operators file `TENSORS/operator.dat` and
        `circuit.dat` will be saved
    **kwargs: int
        The fock cutoff to be provided if type(circ)=strawberryfields.program.Program
        sparse, if to use sparse tensors for quantum optics

    Returns
    -------
    n_sites: int
        Number of sites of the MPS
    operator_mapping: dict
        Mapping between operator name and integer ID
    circ_str: str
        String containing the circuit
    """
    assert os.path.isdir(folder_dst), "Provided PATH does not exists"

    if isinstance(circ, QuantumCircuit):
        n_sites, operator_mapping, circ_str = _pre_parser_qk(
            circ, operators, folder_dst
        )
    elif SF_IS_IMPORTED and isinstance(circ, Program):
        n_sites, operator_mapping, circ_str = _pre_parser_sf(
            circ, operators, folder_dst, **kwargs
        )
    else:
        raise TypeError(
            "Only qiskit quantum circuit of strawberry fields programs are implemented.\
            Your circuit is of type:"
            + str(type(circ))
        )

    return n_sites, operator_mapping, circ_str


def _bubble_sort(nums):
    """Given an integer array sort it by only swapping nearest neighbors elements,
        and return the necessary swaps to bring the array into sorted shape

    Parameters
    ----------
    nums : list of int
        Array of integer to be sorted in ascendant order

    Returns
    -------
    swaps : list of tuples of int
        Indexes of the qubits that has to be swapped
    """
    # We set swapped to True so the loop looks runs at least once
    swapped = True
    swaps = []
    while swapped:
        swapped = False
        for ii in range(len(nums) - 1):
            if nums[ii] > nums[ii + 1]:
                # Swap the elements
                nums[ii], nums[ii + 1] = nums[ii + 1], nums[ii]
                # Set the flag to True so we'll loop again
                swapped = True
                swaps.append((ii, ii + 1))
    return swaps


def _reorder_qk(linearized_qc):
    """Qiskit transpiler does not control the final layout of the qubits, i.e.
        we don't know if they are ordered correctly. It takes care of this problem
        by rearrenging the measurements on the classical register. However, it is
        a problem for the mps simulator. We so reorder the qubit register by applying
        swap gates.

    Parameters
    ----------
    linearized_qc : :py:class:`qiskit.QuantumCircuit`
        Circuit linearized trhough the qiskit transpiler

    Returns
    -------
    linearized_qc : :py:class:`qiskit.QuantumCircuit`
        Circuit with the correct ending qubits
    """
    num_qub = linearized_qc.num_qubits
    # Read the final layout by the rearrengement of the measurements
    final_perm = [0] * num_qub
    for operator, qubits, clbits in linearized_qc.data[
        linearized_qc.size() - num_qub + 1 :
    ]:
        if operator.name == "measure":
            final_perm[get_index(linearized_qc, qubits[0])] = get_index(
                linearized_qc, clbits[0]
            )
    # Get the combination of swaps necessary trhough the bubble_sort algorithm,
    # which is O(num_qub^2)
    swaps = _bubble_sort(final_perm)
    # Perform the swapping operations
    linearized_qc.remove_final_measurements()
    for ii, jj in swaps:
        linearized_qc.swap(ii, jj)

    return linearized_qc


def _preprocess_qk(qc, qk_params=qk_transpilation_params()):
    """Transpile the circuit to adapt it to the linear structure of the MPS, with the constraint
    of having only the gates basis_gates

     Parameters
    ----------
    qc: QuantumCircuit
         qiskit quantum circuit
    linearize: bool, optional
        If True use qiskit transpiler to linearize the circuit. Default to True.
    basis_gate: list, optional
        If not empty decompose using qiskit transpiler into basis gate set
    optimization: intger, optional
        Level of optimization in qiskit transpiler. Default to 3.

    Returns
    -------
    linear_qc: QuantumCircuit
        Linearized quantum circuit
    """
    # Empty circuit case
    if len(qc.data) == 0:
        return qc
    basis_gates = [] if qk_params.basis_gates is None else qk_params.basis_gates
    n_qub = qc.num_qubits
    linear_map = transpiler.CouplingMap.from_line(n_qub)
    # Assure that final measurements are present, by first eliminating and adding them
    qc.remove_final_measurements()
    qc.measure_all()
    # Transpile the circuit
    if len(basis_gates) > 0 and qk_params.linearize:
        linear_qc = transpile(
            qc,
            coupling_map=linear_map,
            optimization_level=qk_params.optimization,
            basis_gates=basis_gates,
            initial_layout=list(range(n_qub)),
        )
    elif len(basis_gates) == 0 and qk_params.linearize:
        linear_qc = transpile(
            qc,
            coupling_map=linear_map,
            optimization_level=qk_params.optimization,
            initial_layout=list(range(n_qub)),
        )
    elif len(basis_gates) > 0:
        linear_qc = transpile(
            qc,
            optimization_level=qk_params.optimization,
            basis_gates=basis_gates,
            initial_layout=list(range(n_qub)),
        )
    else:
        linear_qc = qc

    # Reorder the circuit
    linear_qc = _reorder_qk(linearized_qc=linear_qc)

    # Use the tensor compiler if requested
    if qk_params.tensor_compiler:
        linear_qc = tensor_compiler(linear_qc)

    return linear_qc


def _preprocess_sf(sf_program):
    """
    Preprocess a strawberry fields program, decomposing it.
    TODO

    Parameters
    ----------
    sf_program: strawberryfields.Program
            Input strawberryfields program

    Results
    -------
    sf_program_new: strawberryfields.Program
            Preprocessed strawberryfields program
    """
    if not SF_IS_IMPORTED:
        raise ImportError("Strawberryfields library is not imported.")
    sf_program_new = sf_program

    return sf_program_new


def preprocess(circ, **kwargs):
    """
        Interface for the preprocessing of qiskit and strawberry fields

        Parameters
        ----------
        circ: strawberryfields.program.Program or qiskit.circuit.quantumcircuit.QuantumCircuit
            Quantum circuit instance
        **kwargs: int
            linearize: bool, optional
                If True use qiskit transpiler to linearize the circuit. Default to True.
            basis_gate: list, optional
                If not empty decompose using qiskit transpiler into basis gate set
            optimization: intger, optional
                Level of optimization in qiskit transpiler. Default to 3.

        Returns
        -------
        preprocessed_circ: strawberryfields.program.Program or \
            qiskit.circuit.quantumcircuit.QuantumCircuit
            Preprocessed quantum circuit instance
    """

    if isinstance(circ, QuantumCircuit):
        preprocessed_circ = _preprocess_qk(circ, **kwargs)
    elif SF_IS_IMPORTED and isinstance(circ, Program):
        preprocessed_circ = _preprocess_sf(circ)
    else:
        raise TypeError(
            "Only qiskit quantum circuit of strawberry fields programs\
             are implemented. Your circuit is of type:"
            + str(type(circ))
        )

    return preprocessed_circ
