### Tests de las funciones del backend qpu ###
import pytest
from config.development import ZMQ_SERVER
from qmio.qmio import circuit
from qmio.backends import _config_build
import zmq


def test_config_build():
    result_config = _config_build(shots=100)
    assert result_config == '{"$type": "<class \'qat.purr.compiler.config.CompilerConfig\'>", "$data": {"repeats": 100, "repetition_period": null, "results_format": {"$type": "<class \'qat.purr.compiler.config.QuantumResultsFormat\'>", "$data": {"format": {"$type": "<enum \'qat.purr.compiler.config.InlineResultsProcessing\'>", "$value": 1}, "transforms": {"$type": "<enum \'qat.purr.compiler.config.ResultsFormatting\'>", "$value": 3}}}, "metrics": {"$type": "<enum \'qat.purr.compiler.config.MetricsType\'>", "$value": 6}, "active_calibrations": [], "optimizations": null}}'
