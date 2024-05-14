[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)

# Quantum Matcha Tea

Quantum Matcha Tea is a Tensor Network emulator for quantum circuits and linear optics circuits.
You can define your circuits in either:

- [qiskit](https://github.com/Qiskit), for quantum circuits;
- [strawberry fields](https://github.com/XanaduAI/strawberryfields), for linear optics circuits.

If you use another quantum information library (as [cirq](https://quantumai.google/cirq)) we suggest to save your circuit in `qasm`
format and then load it in qiskit.

The circuits ca be ran using the following backends:

- [numpy](https://numpy.org/), using the CPU in python;
- [cupy](https://cupy.dev/), using the GPU in python;
- fortran, using either the CPU or GPU and MPI multiprocessing;

## Documentation

[Here](https://quantum_matcha_tea.baltig-pages.infn.it/py_api_quantum_matcha_tea) is the documentation.
The documentation can also be built locally with sphinx with the following python packages:

- `sphinx`
- `sphinx_rtd_theme`
- `sphinx-gallery`

and running the command `make html` in the `docs/` folder.

## Installation

Independent of the use-case, you have to install the dependencies. Then,
there are the options using it as a stand-alone package,
or as a python interface for the fortran backend of quantum matcha TEA.

### Installation via pip

The package is available via PyPi and `pip install qmatchatea`.
After cloning the repository, a local installation via pip is
also possible via `pip install .`.

### Dependencies

Notice that, even though the library could be run with a GPU with `cupy`, the latter package is not installed
by default in the machine, since it could give problems
for machines that have no access to a gpu.
If you have access to a GPU and you want to use it,
please proceed to the installation as described in [cupy website](https://docs.cupy.dev/en/stable/install.html).

Furthermore, also [strawberry fields](https://github.com/XanaduAI/strawberryfields) is not installed by default.

## Testing the package

To test the python package `qmatchatea` simply run from the command:
``
python3 -m unittest
``

## License

The project `qmatchatea` from the repository `py_api_quantum_matcha_tea`
is licensed under the following license:

[Apache License 2.0](LICENSE)

The license applies to the files of this project as indicated
in the header of each file, but not its dependencies.
