# qcentroid-runtime-qiskit

![deploy to pypi](https://github.com/QCentroid/qcentroid-runtime-qiskit/actions/workflows/publish.yml/badge.svg)
[![Python](https://img.shields.io/pypi/pyversions/qcentroid-runtime-qiskit.svg)](https://badge.fury.io/py/qcentroid-runtime-qiskit)
[![PyPI](https://badge.fury.io/py/qcentroid-runtime-qiskit.svg)](https://badge.fury.io/py/qcentroid-runtime-qiskit)
 
QCentroid library to interact with Qiskit




## Install

```bash
pip install qcentroid-runtime-qiskit
```


## Use

### Simple example

As easy as this:

```python
from qcentroid_runtime_qiskit import QCentroidRuntimeQiskit
import logging

logging.basicConfig(level=logging.DEBUG)

def main():
    
    # Get the solver details
    qcentroid_qiskit = QCentroidRuntimeQiskit.get_instance() # with optional params

    print(f"currentVersion:{QCentroidRuntimeQiskit.getVersion()}")
    QCentroidRuntimeQiskit.execute(circuit)
    
    
if __name__ == "__main__":
    main() 
```

