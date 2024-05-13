# This code is part of qmatchatea.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import unittest
import subprocess
import os
import io
import warnings
from contextlib import redirect_stdout
from shutil import rmtree, copy
import numpy as np
from qtealeaves.tensors.tensor import GPU_AVAILABLE


from examples.get_started import main as get_started
from examples.advanced.checkpoints import main as checkpoints
from examples.advanced.io_settings import main as io_settings
from examples.advanced.qcemulator import main as qcemulator
from examples.advanced.qudits import main as qudits
from examples.backend.argparse_selector import main as argparse_selector
from examples.backend.device import main as device
from examples.backend.mps_ttn_comparison import main as mps_ttn_comparison
from examples.backend.precisions import main as precisions
from examples.circuits.quantum_fourier_transform import (
    main as quantum_fourier_transform,
)
from examples.circuits.random_quantum_circuit import main as random_quantum_circuit
from examples.circuits.teleportation import main as teleportation
from examples.circuits.variational_quantum_eigensolver import (
    main as variational_quantum_eigensolver,
)
from examples.convergence.bond_dimension import main as bond_dimension
from examples.convergence.convergence_analysis import main as convergence_analysis
from examples.convergence.svd_methods import main as svd_methods
from examples.observables.bond_entropy import main as bond_entropy
from examples.observables.local import main as local
from examples.observables.mid_circuit_measurement import main as mid_circuit_measurement
from examples.observables.probabilities import main as probabilities
from examples.observables.projective import main as projective
from examples.observables.save_read_results import main as save_read_results
from examples.observables.save_state import main as save_state
from examples.observables.tensor_product import main as tensor_product
from examples.observables.weighted_sum import main as weighted_sum


try:
    import mpi4py

    has_mpi = True
except ImportError:
    has_mpi = False

warnings.filterwarnings("ignore")


class TestExamples(unittest.TestCase):
    """Test that all the examples works correctly"""

    def setUp(self):
        """Define 'global' variables"""
        self.examples_names = [
            "mpi/data_parallelism_mpi_example.py",
            "mpi/mpi_mps.py",
        ]
        self.examples_folder = "tests/"
        if not os.path.isdir(self.examples_folder):
            os.makedirs(self.examples_folder)
        for filename in self.examples_names:
            filename = filename.split("/")
            pathname = self.examples_folder + filename[-1]
            filename = "/".join(filename)
            copy(f"examples/{filename}", pathname)
        self.num_sites = 4
        # Set seed
        np.random.seed(123)

        self.data_dir = "data"

    def tearDown(self):
        if os.path.isdir("TMP_TEST"):
            rmtree("TMP_TEST")
        if os.path.isdir("TMP_MPI"):
            rmtree("TMP_MPI")
        if os.path.isdir("mpi"):
            rmtree("mpi")
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        for file in self.examples_names:
            file = file.split("/")[-1]
            file = self.examples_folder + file
            if os.path.isfile(file):
                os.remove(file)
        return

    def test_advanced_checkpoints(self):
        """
        Test the checkpoints example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)

        f = io.StringIO()
        with redirect_stdout(f):
            checkpoints()

    def test_advanced_io_settings(self):
        """
        Test the io_settings example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        f = io.StringIO()
        with redirect_stdout(f):
            io_settings()

    def test_advanced_qcemulator(self):
        """
        Test the qcemulator example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        f = io.StringIO()
        with redirect_stdout(f):
            qcemulator()

    def test_advanced_qudits(self):
        """
        Test the qudits example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        f = io.StringIO()
        with redirect_stdout(f):
            qudits()

    def test_backend_argparse_selector(self):
        """
        Test the argparse_selector example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        f = io.StringIO()
        with redirect_stdout(f):
            argparse_selector()

    @unittest.skipIf(not GPU_AVAILABLE, "GPU is not available")
    def test_backend_device(self):
        """
        Test the device example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        f = io.StringIO()
        with redirect_stdout(f):
            device()

    def test_backend_mps_ttn_comparison(self):
        """
        Test the mps_ttn_comparison example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        f = io.StringIO()
        with redirect_stdout(f):
            mps_ttn_comparison()

    def test_backend_precisions(self):
        """
        Test the precisions example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        f = io.StringIO()
        with redirect_stdout(f):
            precisions()

    def test_circuits_quantum_fourier_transform(self):
        """
        Test the quantum_fourier_transform example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        f = io.StringIO()
        with redirect_stdout(f):
            quantum_fourier_transform()

    def test_circuits_random_quantum_circuit(self):
        """
        Test the random_quantum_circuit example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        f = io.StringIO()
        with redirect_stdout(f):
            random_quantum_circuit()

    def test_circuits_teleportation(self):
        """
        Test the teleportation example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        f = io.StringIO()
        with redirect_stdout(f):
            teleportation()

    def test_circuits_variational_quantum_eigensolver(self):
        """
        Test the variational_quantum_eigensolver example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        f = io.StringIO()
        with redirect_stdout(f):
            variational_quantum_eigensolver()

    def test_convergence_bond_dimension(self):
        """
        Test the bond_dimension example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        f = io.StringIO()
        with redirect_stdout(f):
            bond_dimension()

    def test_convergence_convergence_analysis(self):
        """
        Test the convergence_analysis example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        f = io.StringIO()
        with redirect_stdout(f):
            convergence_analysis()

    def test_convergence_svd_methods(self):
        """
        Test the svd_methods example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        f = io.StringIO()
        with redirect_stdout(f):
            svd_methods()

    @unittest.skipIf(not has_mpi, "mpi4py not installed")
    def test_mpi_data_parallelism(self):
        """
        Test the mpi_example example
        """
        try:
            res = subprocess.run(
                [
                    "mpiexec",
                    "-n",
                    "4",
                    "python3",
                    f"{self.examples_folder}data_parallelism_mpi_example.py",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as ex:
            self.fail(ex.stderr)

    @unittest.skipIf(not has_mpi, "mpi4py not installed")
    def test_mpi_mpi_mps(self):
        """
        Test the mpi_example example
        """
        try:
            res = subprocess.run(
                ["mpiexec", "-n", "4", "python3", f"{self.examples_folder}mpi_mps.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as ex:
            self.fail(ex.stderr)

    def test_observables_bond_entropy(self):
        """
        Test the bond_entropy example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        f = io.StringIO()
        with redirect_stdout(f):
            bond_entropy()

    def test_observables_local(self):
        """
        Test the local example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        f = io.StringIO()
        with redirect_stdout(f):
            local()

    def test_observables_mid_circuit_measurement(self):
        """
        Test the mid_circuit_measurement example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        f = io.StringIO()
        with redirect_stdout(f):
            mid_circuit_measurement()

    def test_observables_probabilities(self):
        """
        Test the probabilities example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        f = io.StringIO()
        with redirect_stdout(f):
            probabilities()

    def test_observables_projective(self):
        """
        Test the projective example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        f = io.StringIO()
        with redirect_stdout(f):
            projective()

    def test_observables_save_read_results(self):
        """
        Test the save_read_results example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        f = io.StringIO()
        with redirect_stdout(f):
            save_read_results()

    def test_observables_save_state(self):
        """
        Test the save_state example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        f = io.StringIO()
        with redirect_stdout(f):
            save_state()

    def test_observables_tensor_product(self):
        """
        Test the tensor_product example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        f = io.StringIO()
        with redirect_stdout(f):
            tensor_product()

    def test_observables_weighted_sum(self):
        """
        Test the weighted_sum example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        f = io.StringIO()
        with redirect_stdout(f):
            weighted_sum()

    def test_get_started(self):
        """
        Test the get_started example
        """
        if os.path.isdir(self.data_dir):
            rmtree(self.data_dir)
        f = io.StringIO()
        with redirect_stdout(f):
            get_started()
