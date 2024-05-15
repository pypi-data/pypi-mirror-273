import math
from ._utils import NDArrays
import numpy as np
from .armisticeai import UploadRequest


class DapConfig:
    def __init__(
        self,
        *,
        leader_url="https://leader-test.armistice.ai",
        helper_url="https://helper-test.armistice.ai",
        time_precision=14400,
        vdaf_bits=32,
        vdaf_type="Prio3SumVec",
        vdaf_length: int,
    ):
        self.leader_url = leader_url
        self.helper_url = helper_url
        self.time_precision = time_precision
        self.vdaf_bits = vdaf_bits
        self.vdaf_type = vdaf_type
        self.vdaf_length = vdaf_length
        self.chunk_length = optimal_chunk_length(vdaf_length * vdaf_bits)

    def upload_measurement(self, task_id: str, measurement: NDArrays):
        ser_measurement = serialize_for_pyo3(measurement)
        task_config = {
            "task_id": task_id,
            "leader": self.leader_url,
            "helper": self.helper_url,
            "bits": self.vdaf_bits,
            "length": len(ser_measurement),
            "chunk_length": optimal_chunk_length(len(measurements) * int(vdaf["bits"])),
            "time_precision": self.time_precision,
        }
        req = UploadRequest(task_config, measurements)
        _ = req.run()


def optimal_chunk_length(measurement_length):
    if measurement_length <= 1:
        return 1

    class Candidate:
        def __init__(self, gadget_calls, chunk_length):
            self.gadget_calls = gadget_calls
            self.chunk_length = chunk_length

    max_log2 = math.floor(math.log2(measurement_length + 1))
    best_opt = min(
        (
            Candidate(
                (1 << log2) - 1,
                (measurement_length + (1 << log2) - 2) // ((1 << log2) - 1),
            )
            for log2 in range(max_log2, 0, -1)
        ),
        key=lambda candidate: (candidate.chunk_length * 2)
        + 2 * (2 ** math.ceil(math.log2(1 + candidate.gadget_calls)) - 1),
    )

    return best_opt.chunk_length


def serialize_for_pyo3(ndarrays: NDArrays):
    # flatten
    flattened = [arr.ravel() for arr in ndarrays]

    # rescale
    original_range = (-1, 1)
    target_range = (0, 2**32 - 1)
    rescaled = [
        np.interp(arr, original_range, target_range)
        .astype(np.uint32)
        .astype(str)
        .tolist()
        for arr in flattened
    ]

    # flatter
    flat = [item for sublist in rescaled for item in sublist]

    return flat
