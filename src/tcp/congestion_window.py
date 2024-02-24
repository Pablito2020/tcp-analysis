from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class CongestionWindow:
    value: int
    slow_start_threshold: int

    def __post_init__(self):
        if self.value < 1:
            raise ValueError("Congestion window should be at least 1")
        if self.slow_start_threshold < 1:
            raise ValueError("Slow start threshold must be at least 1")
