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
from io import StringIO
import pylint.lint
from pylint.reporters.text import ParseableTextReporter


class TestPylint(unittest.TestCase):
    """
    Run pylint to check syntax in source files.

    **Details**

    We disable globally:

    * C0325: superfluous parenthesis
    * C0209: consider using fstring
    * W1514: unspecified encoding
    * R1711: useless returns (for allowing empty iterators with
      return-yield)
    * R1732: consider using with
    * Skip Unused argument errors when args
    * Skip Unused argument errors when kargs

    """

    def setUp(self):
        """
        Provide the test setup.
        """
        pattern_1 = (
            "[E0611(no-name-in-module), ] No name '_TNObsBase' in module"
            + " 'qtealeaves'"
        )
        pattern_2 = "[E0401(import-error), ] Unable to import 'strawberryfields'"
        pattern_3 = "[E0401(import-error), ] Unable to import 'strawberryfields.backends.fockbackend'"
        self.default_patterns = [pattern_1, pattern_2, pattern_3]
        self.pylint_args = {
            "good-names": "ii,jj,kk,nn,mm,fh,dx,dy,dz,dt,hh,qc,dl,gh,xp,PATH,inPATH,outPATH",
            "disable": "C0325,C0209,W1514,R1711,R1732"
            #'ignore_in_line' : pattern_1
        }

    def run_pylint(self, filename, local_settings={}):
        """
        Run linter test with our unit test settings for one specific
        filename.
        """
        args = []

        ignore_in_line = self.default_patterns
        if "ignore_in_line" in local_settings:
            ignore_in_line += local_settings["ignore_in_line"]
            del local_settings["ignore_in_line"]

        for elem in self.pylint_args.keys():
            args += ["--" + elem + "=" + self.pylint_args[elem]]

            if elem in local_settings:
                args[-1] = args[-1] + "," + local_settings[elem]
                del local_settings[elem]

        for elem in local_settings.keys():
            args += ["--" + elem + "=" + local_settings[elem]]

        args += [filename]

        obj = StringIO()
        reporter = pylint.reporters.text.ParseableTextReporter(obj)
        pylint.lint.Run(args, reporter=reporter, exit=False)

        error_list = []
        for elem in obj.getvalue().split("\n"):
            tmp = elem.replace("\n", "")

            if len(tmp) == 0:
                continue
            if tmp.startswith("***"):
                continue
            if tmp.startswith("---"):
                continue
            if tmp.startswith("Your code"):
                continue
            if "Unused argument 'args'" in tmp:
                continue
            if "Unused argument 'kwargs'" in tmp:
                continue

            do_continue = False
            for pattern in ignore_in_line:
                if pattern in tmp:
                    do_continue = True

            if do_continue:
                continue

            error_list.append(tmp)

        return error_list

    def test_folders_recursively(self):
        """
        Recursively run python linter test on all .py files of
        specified folders.
        """
        parent_folders = ["qmatchatea"]
        skip_files = []
        error_list = []

        for elem in parent_folders:
            for root, dirnames, filenames in os.walk(elem):
                for filename in filenames:
                    if not filename.endswith(".py"):
                        continue

                    if filename in skip_files:
                        continue

                    target_file = os.path.join(root, filename)

                    target_attr = "get_settings_" + filename.replace(".py", "")
                    if hasattr(self, target_attr):
                        target_setting = self.__getattribute__(target_attr)()
                    else:
                        target_setting = {}

                    error_list_ii = self.run_pylint(
                        target_file, local_settings=target_setting
                    )

                    error_list += error_list_ii

        if len(error_list) > 0:
            print("\n".join(error_list))

        self.assertEqual(len(error_list), 0, "\n".join(error_list))

    # --------------------------------------------------------------------------
    #                          Settings for qtealeaves
    # --------------------------------------------------------------------------

    @staticmethod
    def get_settings_mps_simulator():
        """
        Linter settings for mps simulator.

        **Details**

        We locally ignore:

        * R0913: too many arguments
        * R0914: too many locals
        * R1720: no-else-raise
        """
        return {
            "ignore_in_line": ["R0913", "R0914", "R1720"],
            "good-names": "ii, jj, kk, ss, fh, tSVD, UU, Vh, QQ, RR, op, xp",
        }

    @staticmethod
    def get_settings_sf_utils():
        """
        Linter settings for mps simulator.

        **Details**

        We locally ignore:

        * W0223: abstract-method
        * R0903: too few public methods
        * C0103: invalid name
        * W0106: expression not assigned
        """
        return {"disable": "W0223, R0903, C0103, W0106"}

    @staticmethod
    def get_settings_mpi_utils():
        """
        Linter settings for mps simulator.

        **Details**

        We locally ignore:

        * C0301: line-too-long
        """
        return {"disable": "C0301"}

    @staticmethod
    def get_settings_qk_utils():
        """
        Linter settings for mps simulator.

        **Details**

        We locally ignore:

        * C0103: invalid name
        * R1705: no-else-return
        """
        return {"disable": "C0103, R1705"}

    @staticmethod
    def get_settings_tn_utils():
        """
        Linter settings for mps simulator.

        **Details**

        We locally ignore:

        * R1732: consider-using-with
        * W0237: argument renamed
        * W0221: argument different
        """
        return {"disable": "R1732, W0237,W0221"}

    @staticmethod
    def get_settings_utils():
        """
        Linter settings for mps simulator.

        **Details**

        We locally ignore:

        * C0103: invalid name
        * C0302: too-many-lines
        * R1720: no-else-raise
        * R0902: too-many-instance-attributes
        * R0913: too-many-arguments
        """
        return {"disable": "C0103, C0302, R1720, R0902, R0913"}

    @staticmethod
    def get_settings_preprocessing():
        """
        Linter settings for mps simulator.

        **Details**

        We locally ignore:

        * R0914: too-many-locals
        """
        return {"disable": "R0914"}

    @staticmethod
    def get_settings_par_simulations():
        """
        Linter settings for mps simulator.

        **Details**

        We locally ignore:

        * C0103: invalid name
        * R1720: no-else-raise
        * E1120: no-value-parameter
        * R1705: no-else-return
        """
        return {"disable": "R1720, C0103, E1120, R1705"}

    @staticmethod
    def get_settings_py_emulator():
        """
        Linter settings for mps simulator.

        **Details**

        We locally ignore:

        * R1720: no-else-raise
        * R1724: no-else-continue
        * R0913: too-many-arguments
        * R0914: too-many-locals
        * R0912: too-many-branches
        * R0915: too-many-statements
        * E1121: too-many-function-args,
        """
        return {"disable": "R1720, R1724, R0913, R0912, R0914, R0915, E1121"}

    @staticmethod
    def get_settings_interface():
        """
        Linter settings for mps simulator.

        **Details**

        We locally ignore:


        * R1720: no-else-raise
        * R0913: too-many-arguments
        * W1510: subprocess-run-check
        * W0212: protected-access
        * R0912: too-many-branches
        * R0915: too-many-statements
        * R0914: too many locals
        * R0902: too-maby-instance-attributs
        * C0103: invalid name


        """
        return {"disable": "R1720,R0913, W1510,W0212,R0915,R0912,C0103,R0914,R0902"}

    @staticmethod
    def get_settings_circuit():
        """
        Linter settings for local observables.

        **Details**

        We locally ignore:

        C0103 : invalid-name
        C0302 : too-many-lines
        R1733 : unnecessary-dict-index-lookup
        R0913 : too-many-arguments
        R0904 : too-many-public-methods
        R0902 : too-maby-instance-attributes

        """
        pattern = (
            "[R0912(too-many-branches), Qcircuit.to_matrix] Too many branches (17/12)"
        )
        return {
            "disable": "C0103, C0302, R1733, R0913, R0902, R0904",
            "ignore_in_line": [pattern],
        }

    @staticmethod
    def get_settings___init__():
        """
        Linter settings for mps simulator.

        **Details**

        We locally ignore:


        * E0602 : undefined variable


        """
        return {"disable": "E0602"}
