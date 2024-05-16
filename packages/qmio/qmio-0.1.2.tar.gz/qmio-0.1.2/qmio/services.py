from qmio.backends import QPUBackend

class QmioRuntimeService():

    def backend(self, name):
        if name == "qpu":
            return QPUBackend()
        # if name == "qulacs":
        #     pass
        else:
            raise ValueError(f"Backend unknown: {name}")
