# This code is part of qmatchatea.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import os
import os.path
import unittest
from shutil import rmtree
import subprocess

try:
    import mpi4py

    mpi_is_present = True
except ModuleNotFoundError:
    mpi_is_present = False


class TestSimulationParallelization(unittest.TestCase):
    """
    Since it is not possible to directly run this test we perform a workaround:
    through subprocess the unittest calls the actual test
    """

    def setUp(self):
        self.mpi_command = os.environ.get("QMATCHATEA_MPI_COMMAND", "mpiexec")
        if not os.path.isdir("mpi/TMP_TEST"):
            os.makedirs("mpi/TMP_TEST")

    def tearDown(self):
        if os.path.isdir("mpi/TMP_TEST"):
            rmtree("mpi/TMP_TEST/")

    @unittest.skipIf(not mpi_is_present, "MPI is nor present")
    def test_mpi_data_patallelism(self):
        """
        Test if the parallelization of multiple simulations is working using GHZ states.
        """

        result = subprocess.run(
            [
                self.mpi_command,
                "-n",
                "4",
                "python3",
                "python/tests/mpi/_testmpi_data_patallelism.py",
            ],
            capture_output=True,
        )

        out = str(result.stdout).split("\n")
        condition = bool(out[-1])

        self.assertTrue(
            condition,
            msg="GHZ circuits simulated parallely on multiple processes correts",
        )

        return

    @unittest.skipIf(not mpi_is_present, "MPI is nor present")
    def test_mpimps_ghz(self):
        """
        Test if the parallelization of multiple simulations is working using GHZ states.
        """

        result = subprocess.run(
            [
                self.mpi_command,
                "-n",
                "4",
                "python3",
                "python/tests/mpi/_testmpimps_ghz.py",
            ],
            capture_output=True,
        )

        out = str(result.stdout).split("\n")
        condition = bool(out[-1])

        self.assertTrue(
            condition,
            msg="GHZ circuits simulated parallely on multiple processes correts",
        )

        return

    @unittest.skipIf(not mpi_is_present, "MPI is nor present")
    def test_mpimps_qft(self):
        """
        Test if the parallelization of multiple simulations is working using GHZ states.
        """

        result = subprocess.run(
            [
                self.mpi_command,
                "-n",
                "4",
                "python3",
                "python/tests/mpi/_testmpimps_qft.py",
            ],
            capture_output=True,
        )

        out = str(result.stdout).split("\n")
        condition = bool(out[-1])

        self.assertTrue(
            condition,
            msg="GHZ circuits simulated parallely on multiple processes correts",
        )

        return
