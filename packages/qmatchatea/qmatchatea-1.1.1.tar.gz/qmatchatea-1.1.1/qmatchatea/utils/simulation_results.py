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
Class to handle the results of a qmatchatea simulation
"""

# pylint: disable=too-many-instance-attributes
import os
import pickle
from datetime import datetime
import numpy as np
from qtealeaves.emulator import MPS, TTN
from qtealeaves.tensors import TensorBackend

from .tn_utils import read_mps

__all__ = ["SimulationResults"]


class SimulationResults:
    """
    Class to store and retrieve the result of a qmatchatea simulation
    """

    def __init__(self, input_params=None, observables=None):
        """
        Initialization. Provide a input params dictionary only if you want to retrieve
        the result directly from the Fortran working folder.
        Otherwise, if you want to load previous results, just initialize the class
        without parameters.

        Parameters
        ----------
        input_params: dict, optional
            If provided contains all the input parameters of the simulation.
            If it is empty than you should use this class to upload a previous experiment
        observables: TNObservables, optional
            observables used in the simulation
        """
        # Name of the input parameters in a simulation
        self._input_params_names = [
            "num_sites",
            "local_dim",
            "approach",
            "observables_filename",
            "max_bond_dimension",
            "cut_ratio",
            "trunc_tracking_mode",
            "inPATH",
            "outPATH",
            "sparse",
            "initial_state",
            "checkpoint_PATH",
            "checkpoint_frequency",
            "initial_line",
        ]

        self._input_params = {} if input_params is None else input_params
        self._from_simulation = (
            False  # flag set to True if you have to obtain data from Fortran,
        )
        # i.e. if you provide a suitable input parameter dictionary

        if all("settings%" + k in self._input_params for k in self._input_params_names):
            self.inPATH = input_params["settings%inPATH"]
            self.outPATH = input_params["settings%outPATH"]
            assert os.path.isdir(self.inPATH), "Input PATH is not a folder"
            assert os.path.isdir(self.outPATH), "Output PATH is not a folder"
            self._from_simulation = True

        self._datetime = datetime.today().strftime("%Y-%m-%d-%H:%M:%S")

        # Set to None all the variables
        self._initial_state = "Vacuum"
        if "settings%initial_state" in self._input_params:
            if self._input_params["settings%initial_state"] == "Vacuum":
                pass
            elif int(self._input_params["settings%initial_line"]) == 1:
                self._initial_state = read_mps(
                    os.path.join(
                        self.inPATH, self._input_params["settings%initial_state"]
                    )
                )
            else:
                self._initial_state = read_mps(
                    os.path.join(
                        self._input_params["settings%checkpoint_PATH"],
                        self._input_params["settings%initial_state"],
                    )
                )

        self._observables = {} if observables is None else observables
        self._singular_values_cut = None
        self._statevector = None

    def _get_results(self):
        """
        Load the results on python from the output files
        """

        assert (
            self._from_simulation
        ), "Cannot retrieve results if no input parameters are provided"

        if self._observables is not None:
            self._observables = self._observables.read(
                self._input_params["settings%observables_filename"],
                self.outPATH,
                {},
            )

            tn_state_path = None
            for key, value in self._observables.items():
                # The only key with the '/' is the MPS state
                if "/" in key:
                    tn_state_path = value

            if tn_state_path is not None:
                self._observables["tn_state_path"] = tn_state_path
            self.load_state()

        self._singular_values_cut = np.loadtxt(
            os.path.join(self.outPATH, "singular_values_cut.txt")
        )

    # ----------------------------
    # Methods to save/load results
    # ----------------------------
    def _store_attr_for_pickle(self):
        """Return dictionary with attributes that cannot be pickled and unset them."""
        storage = {
            "tn_state": self._observables.get("tn_state", None),
            "initial_state": self._initial_state,
            "statevector": self._statevector,
        }

        self._observables["tn_state"] = None
        self._initial_state = None
        self._statevector = None

        return storage

    def _restore_attr_for_pickle(self, storage):
        """Restore attributed removed for pickle from dictionary."""
        # Reset temporary removed attributes
        self._observables["tn_state"] = storage["tn_state"]
        self._initial_state = storage["initial_state"]
        self._statevector = storage["statevector"]

    def save_pickle(self, filename):
        """
        Save class via pickle-module.

        Parameters
        ----------
        filename : str
            path where to save the file

        **Details**

        The following attributes have a special treatment and are not present
        in the copied object.

        * initial state tensor network
        * final state tensor network
        * statevector
        """
        # Temporary remove objects which cannot be pickled which
        # included convergence parameters for lambda function and
        # parameterized variables, the log file as file handle and
        # the MPI communicator
        storage = self._store_attr_for_pickle()

        ext = "pkl"
        if not filename.endswith(ext):
            filename += "." + ext

        with open(filename, "wb") as fh:
            pickle.dump(self, fh)

        self._restore_attr_for_pickle(storage)

    @classmethod
    def read_pickle(cls, filename):
        """
        Load the results of a previous simulation

        Parameters
        ----------
        path: str
            PATH to the file from which we want to load the results

        Returns
        -------
        readme: str
            The text contained in the readme file inside the folder
        """
        ext = "pkl"
        if not filename.endswith(ext):
            raise Exception(
                f"Filename {filename} not valid, extension should be {ext}."
            )

        with open(filename, "rb") as fh:
            obj = pickle.load(fh)

        if not isinstance(obj, cls):
            raise TypeError(
                f"Loading wrong tensor network ansatz: {type(obj)} vs {cls}."
            )

        return obj

    def set_results(self, result_dict, singvals_cut):
        """Set the results of a simulation

        Parameters
        ----------
        result_dict: dict
            Dictionary of the attribute to be set
        singvals_cut: array-like
            Array of singular values cut through the simulation
        """
        self._observables = result_dict.copy()
        self._singular_values_cut = np.array(singvals_cut)

        tn_state_path = None
        for key, value in result_dict.items():
            # The only key with the '.' is the MPS state
            if "/" in key:
                tn_state_path = value

        if tn_state_path is not None:
            self._observables["tn_state_path"] = tn_state_path
        self.load_state()

    def load_state(self, tensor_backend=TensorBackend()):
        """
        Loads the state located in `tn_state_path`,
        saving it in `tn_state`

        Parameters
        ----------
        tensor_backend : TensorBackend, optional
            Tensor backend of the state if it is
            saved in a formatted format.
            Default to TensorBackend().
        """
        key = self.observables.get("tn_state_path", None)
        if key is None:
            return

        if key.endswith("pklmps"):
            state = MPS.read_pickle(key)
        elif key.endswith("mps"):
            state = MPS.read(key, tensor_backend=tensor_backend)
        elif key.endswith("pklttn"):
            state = TTN.read_pickle(key)
        elif key.endswith("ttn"):
            state = TTN.read(key, tensor_backend=tensor_backend)
        else:
            raise IOError(f"File extension {key} not supported")

        self._observables["tn_state"] = state

    # -----------------------------
    # Methods to access the results
    # -----------------------------
    @property
    def fidelity(self):
        """
        Return the lower bound for the fidelity of the simulation,
        using the method described in
        If you are interested in the evolution of the fidelity through
        the simulation compute it yourself using `np.cumprod(1-self.singular_values_cut)`.

        Returns
        -------
        float
            fidelity of the final state
        """

        fid = np.prod(1 - np.array(self.singular_values_cut))
        return fid

    @property
    def measures(self):
        """Obtain the measures of the simulation as a dictionary.
        The keys are the measured states, the values the number of occurrencies

        Returns
        -------
        measures: dict
            Measures of the simulation
        """
        return self.observables.get("projective_measurements", None)

    @property
    def statevector(self):
        """Obtain the statevector as a complex numpy array

        Returns
        -------
        statevector: np.array or None
            The statevector of the simulation
        """
        if self._statevector is None:
            if "tn_state" in self.observables.keys():
                tn_state = self.observables["tn_state"]
                if tn_state.num_sites < 30:
                    self._statevector = tn_state.to_statevector(qiskit_order=True)
        return self._statevector.elem

    @property
    def singular_values_cut(self):
        """Obtain the singular values cutted through the simulation, depending on the mode
        chosen. If 'M' for maximum (default), 'C' for cumulated.

        Returns
        -------
        np.ndarray[float]
            Singular values cut during the simulation
        """
        return self._singular_values_cut

    @property
    def computational_time(self):
        """Obtain the computational time of the simulation

        Returns
        -------
        float
            computational time of the simulation
        """
        return self.observables.get("time", None)

    @property
    def entanglement(self):
        """Obtain the bond entanglement entropy measured along each bond of the MPS at
        the end of the simulation

        Returns
        -------
        entanglement: np.array or None
            Bond entanglement entropy
        """
        if "bond_entropy" in self.observables.keys():
            entanglement = self.observables["bond_entropy"]
        elif "bond_entropy0" in self.observables.keys():
            entanglement = self.observables["bond_entropy0"]
        else:
            entanglement = None
        return entanglement

    @property
    def measure_probabilities(self):
        """Return the probability of measuring a given state, which is computed using a
        binary tree by eliminating all the branches with probability under a certain threshold.

        Returns
        -------
        measure_probabilities: Dict[Dict | None]
            probability of measuring a certain state if it is greater than a threshold
        """
        keys = ["unbiased_probability", "even_probability", "greedy_probability"]
        new_keys = ["U", "E", "G"]
        probs = {}
        for key, new_key in zip(keys, new_keys):
            if key in self.observables.keys():
                probs[new_key] = self.observables[key]
            else:
                probs[new_key] = [None]
        return probs

    @property
    def date_time(self):
        """Obtain the starting date and time of the simulation, in the format
        ``Year-month-day-Hour:Minute:Second``

        Returns
        -------
        datetime: string
            The date-time when the simulation started
        """
        return self._datetime

    @property
    def input_params(self):
        """Obtain the input parameters used in the simulation, which are the following:
            - 'num_sites',              number of sites of the mps
            - 'local_dim',              local dimension of the single site
            - 'max_bond_dim',           maximum bond dimension of the mps
            - 'cut_ratio',              cut ration used in the SVD truncation
            - 'in_name',                path to the fortran input folder
            - 'out_name',               path to the Fortran output folder
            - 'trunc_tracking_mode',           mode to save the singular values cut
            - 'sparse',                 if the input gate tensors are saved as sparse
            - 'par_approach',           parallel approach of the simulation. Can be
                'SR' (serial), 'MW' (master/workers) or 'CT' (cartesian)
            - 'initial_state',          initial state of the simulation. 'Vacuum' or
                the PATH to the initial state
            - 'do_observables',         True if there are some observables to compute at
                the end

        Returns
        -------
        input_params: dict or None
            Input parameters
        """
        return self._input_params

    @property
    def tn_state(self):
        """
        Returns the tensor network class, either TTN or MPS

        Returns
        -------
        _AbstractTN
            The tensor network class
        """
        return self.observables.get("tn_state", None)

    @property
    def tn_state_path(self):
        """
        Returns the tensor list in row-major format.
        The indexing of the single tensor is as follows:

        .. code-block::

            1-o-3
             2|

        Returns
        -------
        mps: list
            list of np.array tensors
        """
        return self.observables.get("tn_state_path", None)

    @property
    def initial_state(self):
        """Returns the initial state of the simulation, as an MPS in row-major format or as
        a string if starting from the Vacuum state

        Returns
        -------
        initial_state: list or str
            list of np.array tensors or Vacuum
        """
        return self._initial_state

    @property
    def observables(self):
        """Returns the expectation values of the observables as a dict with the format
            observable_name : observable_expectation_value

        Returns
        -------
        observables: dict or None
            Expectation values of the observables
        """
        return self._observables
