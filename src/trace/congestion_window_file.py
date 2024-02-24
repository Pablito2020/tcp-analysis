from dataclasses import dataclass

from src.metrics.metrics import CongestionWindowMetrics
from src.trace.trace_file import Time


@dataclass(frozen=True)
class CongestionWindowEntity:
    time: Time
    congestion_window: float
    max_congestion_window: float

    @staticmethod
    def from_str(line: str) -> 'CongestionWindowEntity':
        time, cw, max_cw = line.split()
        return CongestionWindowEntity(time=Time.from_str(time),
                                      congestion_window=float(cw),
                                      max_congestion_window=float(max_cw))


class CongestionWindowTraceFile:

    def __init__(self, file_name: str):
        self.file_name = file_name

    def __iter__(self):
        with open(self.file_name) as file:
            for line in file:
                yield CongestionWindowEntity.from_str(line)

    def get_metrics(self) -> CongestionWindowMetrics:
        metrics = CongestionWindowMetrics()
        for x in self:
            metrics.add_metric(x.time, x.congestion_window)
        return metrics
