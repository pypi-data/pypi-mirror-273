# Qmio
Python module to interact with the different backends available in the Qmio system at CESGA.

## Usage
```python
from qmio import QmioRuntimeService

circuit = 'OPENQASM 3.0;\ninclude "qelib1.inc";\nqreg q[32];\ncreg c[32];\nx q[0];\nmeasure q[0]->c[0];'

service = QmioRuntimeService()
with service.backend(name="qpu") as backend:
    result = backend.run(circuit=circuit, shots=1000)

print(result)
```
