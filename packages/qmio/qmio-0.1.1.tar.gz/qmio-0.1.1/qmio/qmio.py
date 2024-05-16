from qmio.services import QmioRuntimeService

circuit = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[4];
    creg c[4];
    rx(0.01) q[0];
    measure q[0]->c[0];
    measure q[1]->c[1];
    measure q[2]->c[2];
    measure q[3]->c[3];
    """

config = '{"$type": "<class \'qat.purr.compiler.config.CompilerConfig\'>", "$data": {"repeats": 1, "repetition_period": null, "results_format": {"$type": "<class \'qat.purr.compiler.config.QuantumResultsFormat\'>", "$data": {"format": {"$type": "<enum \'qat.purr.compiler.config.InlineResultsProcessing\'>", "$value": 1}, "transforms": {"$type": "<enum \'qat.purr.compiler.config.ResultsFormatting\'>", "$value": 3}}}, "metrics": {"$type": "<enum \'qat.purr.compiler.config.MetricsType\'>", "$value": 6}, "active_calibrations": [], "optimizations": null}}'

# service = QmioRuntimeService()

# backend = service.backend(name="qpu")
# backend.connect()
# result = backend.run(program, config)
# backend.disconnect()

# with service.backend(name="qpu") as backend:
#     result = backend.run(program=program, config=config)

# print(result)
