from dataclasses import dataclass
from decimal import Decimal
from typing import List, Tuple

from src.trace.trace_file import Time


class TimeoutMetrics:

    def __init__(self):
        self.metrics: List[Tuple[Time, Decimal]] = []
        self.timeout_value_type: str = "ms"  # ms (milliseconds) or s (seconds)

    def add_metric(self, time: Time, timeout: Time):
        self.metrics.append((time, timeout.value))

    def reset(self):
        self.metrics = []

    @property
    def time(self) -> List[Decimal]:
        return [time.value for time, _ in self.metrics]

    @property
    def value(self) -> List[Decimal]:
        return [value for _, value in self.metrics]


class CongestionWindowMetrics:

    def __init__(self):
        self.metrics: List[Tuple[Time, float]] = []

    def add_metric(self, time: Time, metric: float):
        self.metrics.append((time, metric))

    @property
    def time(self) -> List[Decimal]:
        return [time.value for time, _ in self.metrics]

    @property
    def value(self) -> List[float]:
        return [value for _, value in self.metrics]

    def reset(self):
        self.metrics = []


@dataclass(frozen=True)
class TcpMetrics:
    timeout_metrics: TimeoutMetrics
    congestion_window_metrics: CongestionWindowMetrics
