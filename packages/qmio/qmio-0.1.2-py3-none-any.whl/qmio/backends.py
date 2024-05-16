from qmio.clients import ZMQClient
import json

def _config_build(shots: int, repetition_period=None):
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
            "optimizations": {
                "$type": "<enum \'qat.purr.compiler.config.TketOptimizations\'>",
                "$value": 1
            }
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

    # def run(self, circuit, config):
    #     if not self.client:
    #         raise RuntimeError("Not connected to the server")

    #     job = (circuit, config)
    #     self.client._send(job)
    #     result = self.client._await_results()
    #     return result

    def run(self, circuit, shots):
        if not self.client:
            raise RuntimeError("Not connected to the server")

        config = _config_build(shots)
        job = (circuit, config)
        self.client._send(job)
        result = self.client._await_results()
        return result
