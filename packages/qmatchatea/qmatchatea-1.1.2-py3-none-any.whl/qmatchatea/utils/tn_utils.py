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
I/O functions for tensors and mps (list of tensors).
Furthermore, the class :py:class:`QCOperators` for handling operators is provided.

Functions and classes
---------------------

"""

import os
import os.path
from ast import literal_eval
from typing import OrderedDict
import numpy as np
from qtealeaves import read_tensor
from qtealeaves.operators import TNOperators
from qtealeaves.tooling import StrBuffer

__all__ = ["write_tensor", "write_mps", "read_mps", "QCOperators"]


def read_nml(namelist_file):
    """
    Read a fortran namelist file

    Parameters
    ----------
    namelist_file : str
        PATH to the namelist

    Returns
    -------
    namelist_dict : OrderedDict
        Dictionary to be eventually passed to write_nml
    """
    if not os.path.isfile(namelist_file):
        raise IOError(f"{namelist_file} is not a file")
    with open(namelist_file, "r") as fh:
        file = fh.readlines()
    namelist_name = file[0].replace("&", "").replace("\n", "")

    namelist_dict = OrderedDict()
    for line in file[1:-2]:
        line = line.replace(" ", "").replace("\n", "")
        data = line.split("=")
        if data[1] == ".true.":
            namelist_dict[data[0]] = True
        elif data[1] == ".false.":
            namelist_dict[data[0]] = False
        else:
            namelist_dict[data[0]] = literal_eval(data[1])

    return namelist_name, namelist_dict


def write_tensor(tensor, dest, cmplx=True, sparse=False):
    """
    Write a tensor stored in a numpy matrix to a file. Conversion
    to column major is taken care of here.

    **Arguments**

    tensor : np.ndarray
        Tensor to be written to the file.

    dest : str, or filehandle
        If string, file will be created or overwritten. If filehandle,
        then data will be written there.

    sparse: bool
        If True write the tensor in a sparse format, i.e. each row is written as
        idx elem
        where idx is the position of the element elem in the tensor vector
    """
    if isinstance(dest, str):
        fh = open(dest, "w+")
    elif hasattr(dest, "write"):
        fh = dest

    # Number of links
    fh.write("%d \n" % (len(tensor.shape)))

    # Dimensions of links
    dl = " ".join(list(map(str, tensor.shape)))
    fh.write(dl + "\n")

    # Now we need to transpose
    tensor_colmajor = np.reshape(tensor, -1, order="F")
    if sparse:
        nonzero = np.nonzero(tensor_colmajor)[0]  # index of nonzero element
        tensor_colmajor = tensor_colmajor[nonzero]
        nonzero += 1  # from python to fortran indexing
        fh.write(f"{len(nonzero)} \n")

    for ii, elem in enumerate(tensor_colmajor):
        if cmplx:
            if sparse:
                fh.write(
                    "%d (%30.15E, %30.15E)\n"
                    % (nonzero[ii], np.real(elem), np.imag(elem))
                )
            else:
                fh.write("(%30.15E, %30.15E)\n" % (np.real(elem), np.imag(elem)))
        else:
            if sparse:
                fh.write("%d %30.15E\n" % (nonzero[ii], np.real(elem)))
            else:
                fh.write("%30.15E\n" % (np.real(elem)))
            imag_part = np.imag(elem)
            if np.abs(imag_part) > 1e-14:
                raise Exception("Writing complex valued tensor as real valued tensor.")

    if isinstance(dest, str):
        fh.close()

    return


def read_mps(filename, cmplx=True):
    """Read an MPS written by FORTRAN in a formatted way on file.
    Reads in column-major order but the output is in row-major

    Parameters
    ----------
    filename: str
            PATH to the file
    cmplx: bool, optional
            If True the MPS is complex, real otherwise. Default to True

    Returns
    -------
    mps: list
            list of np.array in row-major order
    """
    mps = []
    with open(filename, "r") as fh:
        num_sites = int(fh.readline())
        for _ in range(num_sites):
            tens = read_tensor(fh, cmplx=cmplx)
            mps.append(tens)

    return mps


def write_mps(filename, mps, cmplx=True):
    """Write an MPS in python format into a FORTRAN format, i.e.
    transforms row-major into column-major

    Parameters
    ----------
    filename: str
            PATH to the file
    mps: list
            List of tensors forming the mps
    cmplx: bool, optional
            If True the MPS is complex, real otherwise. Default to True

    Returns
    -------
    None
    """
    with open(filename, "w") as fh:
        fh.write(str(len(mps)) + " \n")
        for tens in mps:
            write_tensor(tens, fh, cmplx=cmplx)

    return None


class QCOperators(TNOperators):
    """
    Class to store and save to file operators. To add an operator to the list use
    self.ops['op_name'] = op_tensor.

    It starts with the pauli operators already defined, with keywords "X","Y","Z"
    """

    def __init__(self, folder_operators="TENSORS"):
        TNOperators.__init__(self, folder_operators=folder_operators)
        pauli_matrices = {
            "Z": np.array([[1, 0], [0, -1]]),
            "X": np.array([[0, 1], [1, 0]]),
            "Y": np.array([[0, -1j], [1j, 0]]),
            "I": np.array([[1, 0], [0, 1]]),
        }
        for key, val in pauli_matrices.items():
            self.ops[key] = val

    def write_operator(self, folder_dst, operator_name, params, sparse=False):
        """
        Write operator to file.

        Parameters
        ---------

        folder_dst : str or filehandle
            If filehandle, write there. If string, it defines the folder.
        operator_name : str
            Name of the operator.
        params : dictionary
                Contains the simulation parameters.
        kwargs : passed to write_symtensor

        """
        if operator_name not in self.ops:
            raise Exception("Operator `%s` not defined." % (operator_name))
        if hasattr(folder_dst, "write"):
            # filehandle
            full_filename = folder_dst
        else:
            full_filename = os.path.join(folder_dst, operator_name + ".dat")

        operator = self.get_operator(operator_name, params)

        write_tensor(operator, full_filename, sparse=sparse)

        return operator_name + ".dat"

        # tensor_backend is put to 2 since we only use non-symmetric tensors
        # Temporarily disabled quick inhereted way because of sparse tensors
        # return TNOperators.write_operator(self, folder_dst, operator_name,
        # params, tensor_backend=2, sparse=sparse)

    def write_input_3(self, folder_name, filename="operators.dat", sparse=False):
        """Write on file for fortran the operators used in the observable

        Parameters
        ----------
        folder_name: str
            PATH to the folder where we want to save the file
        filename: str, optional
            Name of the file. Default to 'operators.dat'
        sparse: bool, optional
            If True write the operators in a semi-sparse format, i.e. by writing
            only the non-zero elemnts and their position. Default to False.

        Returns
        -------
        relative_file: str
            Full PATH to the observable file 'observables.dat'
        operator_id_mapping: dict
            Dictionary which maps the operators names to their IDs
        """

        full_path = os.path.join(folder_name, self.folder_operators)
        if not os.path.isdir(full_path):
            os.makedirs(full_path)

        relative_file = os.path.join(full_path, filename)
        buffer_str = StrBuffer()

        operator_id_mapping = {}

        ii = 0
        for operator_ii in self.ops.keys():
            ii += 1
            # Write the operator on the buffer string
            _ = self.write_operator(buffer_str, operator_ii, None, sparse=sparse)
            # Mapping between the operator name and a number
            operator_id_mapping[operator_ii] = ii

        # Apriori length because operators are not written
        nn = len(operator_id_mapping)

        fh = open(relative_file, "w+")
        fh.write(str(nn) + "\n")
        fh.write(buffer_str())
        fh.close()

        return relative_file, operator_id_mapping
