# This code is part of qmatchatea.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import setuptools
import os
import os.path
import importlib.util

# Parse the version file
spec = importlib.util.spec_from_file_location("qmatchatea", "./qmatchatea/version.py")
version_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(version_module)

# Parse requirements
requirement_path = "requirements.txt"
if os.path.isfile(requirement_path):
    with open(requirement_path) as fh:
        install_requires = list(fh.read().splitlines())
    install_requires.remove("mpi4py")
else:
    install_requires = []

install_requires = [
    "numpy>=1.18.1",
    "scipy>=1.4.1",
    "matplotlib>=3.1.3",
    "qtealeaves>=1.1.6",
    "qiskit==0.38.0",
    "mpi4py",
    "joblib",
]

# Get the readme file
if os.path.isfile("README.md"):
    with open("README.md", "r") as fh:
        long_description = fh.read()
else:
    long_description = ""

setuptools.setup(
    name="qmatchatea",
    version=version_module.__version__,
    author="Marco Ballarin",
    author_email="marco97.ballarin@gmail.com",
    description="Quantum matcha TEA python library for tensor network emulation of quantum circuits.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://baltig.infn.it/quantum_matcha_tea/py_api_quantum_matcha_tea",
    project_urls={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={
        "qmatchatea": "qmatchatea",
        "qmatchatea.circuit": "qmatchatea/circuit",
        "qmatchatea.utils": "qmatchatea/utils",
    },
    packages=["qmatchatea", "qmatchatea.circuit", "qmatchatea.utils"],
    python_requires=">=3.8",
    install_requires=install_requires,
    # entry_points = { 'console_scripts': ['build_exec = qmatchatea.bin.compiler:main', ], },
    # These packages are not mandatory for a pip installation. If they are not there
    # they will simply be ignored.
    package_data={"qmatchatea": ["bin/qmatchatea.exe", "bin/par_qmatchatea.exe"]},
)
