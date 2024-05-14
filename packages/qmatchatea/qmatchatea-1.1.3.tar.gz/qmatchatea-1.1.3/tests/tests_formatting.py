# This code is part of qmatchatea.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import pathlib
import unittest
import subprocess


class TestBlackFormatting(unittest.TestCase):
    def test_black_formatting(self):
        # Enter the following folders up to a defined depth
        folders_depth = {
            "qmatchatea": 2,
            "tests": 1,
        }

        # Get the root path of the repository based on the current file
        root = str(pathlib.Path(__file__).parent.parent.resolve())

        paths = [root + "/*.py"]
        for elem, depth in folders_depth.items():
            fill_path = "/"
            for ii in range(depth):
                paths.append(root + "/" + elem + fill_path + "*.py")

                fill_path += "*/"

        cmd_call = ["black", "--check", "--exclude=Examples"] + paths
        result = subprocess.call(" ".join(cmd_call), shell=True)
        success = int(result) == 0

        self.assertTrue(success, "Repository did not pass Black formatting.")
