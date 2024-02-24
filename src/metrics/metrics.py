from dataclasses import dataclass
from typing import List, Tuple

from src.trace.trace_file import Time


class TimeoutMetrics:

    def __init__(self):
        self.metrics: List[Tuple[Time, float]] = []

    def add_metric(self, time: Time, timeout: Time):
        self.metrics.append((time, timeout.value))

    @property
    def time(self) -> List[float]:
        return [time.value for time, _ in self.metrics]

    @property
    def value(self) -> List[float]:
        return [value for _, value in self.metrics]


class CongestionWindowMetrics:

    def __init__(self):
        self.metrics: List[Tuple[Time, int]] = []

    def add_metric(self, time: Time, metric: int):
        self.metrics.append((time, metric))

    @property
    def time(self) -> List[float]:
        return [time.value for time, _ in self.metrics]

    @property
    def value(self) -> List[int]:
        return [value for _, value in self.metrics]


@dataclass(frozen=True)
class TcpMetrics:
    timeout_metrics: TimeoutMetrics
    congestion_window_metrics: CongestionWindowMetrics
