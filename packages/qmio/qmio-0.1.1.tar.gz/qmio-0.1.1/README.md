
# Table of Contents

1.  [Intro](#orgf9aa4ec)
2.  [Estructure](#org6bcf005)
3.  [Qmio module](#org9f6e788)
    1.  [qmio.py](#orgdcf0a4d)
        1.  [services.py](#orgfb7ed10)
        2.  [backends.py](#org006d051)
        3.  [clients.py](#orga1d17e8)
4.  [tests](#orgeeaa0cc)
    1.  [test<sub>clients</sub>](#orgae61544)
    2.  [test<sub>backends</sub>](#org40f4db8)
    3.  [test<sub>services</sub>](#org32b9d24)
    4.  [test<sub>qmio</sub>](#org7c42007)



<a id="orgf9aa4ec"></a>

# Intro

Proyecto de Integración del computador cuántico del cesga. Ejemplo de uso en qmio.py


<a id="org6bcf005"></a>

# Estructure

    .
    ├── config
    │   ├── development.py
    │   ├── __init__.py
    │   └── production.py
    ├── LICENSE
    ├── main.org
    ├── main.pdf
    ├── main.tex
    ├── notes.org
    ├── qmio
    │   ├── backends.py
    │   ├── clients.py
    │   ├── __init__.py
    │   ├── qmio.py
    │   └── services.py
    ├── README.md
    ├── requirements-dev.txt
    ├── requirements.txt
    ├── setup.cfg
    ├── setup.py
    └── user_test.py
    
    3 directories, 19 files


<a id="org9f6e788"></a>

# Qmio module


<a id="orgdcf0a4d"></a>

## qmio.py

    from qmio.services import QmioRuntimeService
    
    program = """OPENQASM 2.0;
        include "qelib1.inc";
        qreg q[4];
        creg c[4];
        rx(0.01) q[0];
        measure q[0]->c[0];
        measure q[1]->c[1];
        measure q[2]->c[2];
        measure q[3]->c[3];
        """
    
    # config = '{"$type": "<class \'qat.purr.compiler.config.CompilerConfig\'>", "$data": {"repeats": 1, "repetition_period": null, "results_format": {"$type": "<class \'qat.purr.compiler.config.QuantumResultsFormat\'>", "$data": {"format": {"$type": "<enum \'qat.purr.compiler.config.InlineResultsProcessing\'>", "$value": 1}, "transforms": {"$type": "<enum \'qat.purr.compiler.config.ResultsFormatting\'>", "$value": 3}}}, "metrics": {"$type": "<enum \'qat.purr.compiler.config.MetricsType\'>", "$value": 6}, "active_calibrations": [], "optimizations": null}}'
    
    service = QmioRuntimeService()
    
    shots = 100
    
    # You can user with explicit connect and disconnect
    # backend = service.backend(name="qpu")
    # backend.connect()
    # result = backend.run(program, shots=shots)
    # backend.disconnect()
    
    # Recommended usage
    with service.backend(name="qpu") as backend:
        result = backend.run(program=program, shots=shots)
    
    print(result)


<a id="orgfb7ed10"></a>

### services.py

    from qmio.backends import QPUBackend
    
    class QmioRuntimeService():
    
        def backend(self, name):
            if name == "qpu":
                return QPUBackend()
            else:
                raise ValueError(f"Backend desconocido: {name}")


<a id="org006d051"></a>

### backends.py

    from qmio.clients import ZMQClient
    import json
    
    def _config_build(shots: int, repetition_period=None, optimizations=None):
        config = {
            "$type": "<class \'qat.purr.compiler.config.CompilerConfig\'>",
            "$data": {
                "repeats": shots,
                "repetition_period": repetition_period,
                "results_format": {
                    "$type": "<class \'qat.purr.compiler.config.QuantumResultsFormat\'>",
                    "$data": {
                        "format": {
                            "$type": "<enum \'qat.purr.compiler.config.InlineResultsProcessing\'>",
                            "$value": 1
                        },
                        "transforms": {
                            "$type": "<enum \'qat.purr.compiler.config.ResultsFormatting\'>",
                            "$value": 3
                        }
                    }
                },
                "metrics": {
                    "$type": "<enum \'qat.purr.compiler.config.MetricsType\'>",
                    "$value": 6
                },
                "active_calibrations": [],
                "optimizations": optimizations
            }
        }
        config_str = json.dumps(config)
        return config_str
    
    
    class QPUBackend:
        def __init__(self):
            self.client = None
    
        def __enter__(self):
            self.client = ZMQClient()
            return self
    
        def __exit__(self, exc_type, exc_value, traceback):
            if self.client:
                self.client.close()
                self.client = None
    
        def connect(self):
            self.client = ZMQClient()
    
        def disconnect(self):
            self.client.close()
            self.client = None
    
        # def run(self, program, config):
        #     if not self.client:
        #         raise RuntimeError("Not connected to the server")
    
        #     job = (program, config)
        #     self.client._send(job)
        #     result = self.client._await_results()
        #     return result
    
        def run(self, program, shots):
            if not self.client:
                raise RuntimeError("Not connected to the server")
    
            config = _config_build(shots)
            job = (program, config)
            self.client._send(job)
            result = self.client._await_results()
            return result


<a id="orga1d17e8"></a>

### clients.py

    from time import time
    from typing import Union
    from config.development import ZMQ_SERVER
    import zmq
    
    class ZMQBase:
        def __init__(self, socket_type):
            self._context = zmq.Context()
            self._socket = self._context.socket(socket_type)
            self._timeout = 30.0
            self._address = ZMQ_SERVER
    
        def _check_recieved(self):
            try:
                msg = self._socket.recv_pyobj()
                return msg
            except zmq.ZMQError:
                return None
    
        def _send(self, message) -> None:
            sent = False
            t0 = time()
            while not sent:
                try:
                    self._socket.send_pyobj(message)
                    sent = True
                except zmq.ZMQError as e:
                    if time() > t0 + self._timeout:
                        raise TimeoutError(
                            "Sending %s on %s timedout" % (message, self._address)
                        )
            return
    
        def close(self):
            """Disconnect the link to the socket."""
            if self._socket.closed:
                return
            self._socket.close()
            self._context.destroy()
    
        def __del__(self):
            self.close()
    
    
    class ZMQClient(ZMQBase):
        def __init__(self):
            super().__init__(zmq.REQ)
            self._socket.setsockopt(zmq.LINGER, 0)
            self._socket.connect(self._address)
    
        def _await_results(self):
            result = None
            while result is None:
                result = self._check_recieved()
            return result


<a id="orgeeaa0cc"></a>

# tests


<a id="orgae61544"></a>

## test<sub>clients</sub>


<a id="org40f4db8"></a>

## test<sub>backends</sub>


<a id="org32b9d24"></a>

## test<sub>services</sub>


<a id="org7c42007"></a>

## test<sub>qmio</sub>

