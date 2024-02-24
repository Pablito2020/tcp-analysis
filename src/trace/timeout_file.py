from dataclasses import dataclass

from src.metrics.metrics import TimeoutMetrics
from src.trace.trace_file import Time


@dataclass(frozen=True)
class TimeoutTraceEntity:
    time: Time
    rto: Time
    rtt: Time | None
    srtt: Time | None
    rttvar: Time | None

    @staticmethod
    def from_str(line: str) -> 'TimeoutTraceEntity':
        try:
            time, rto, rtt, srtt, rttvar = line.split()
            return TimeoutTraceEntity(time=Time.from_str(time),
                                      rto=Time.from_str(rto),
                                      rtt=Time.from_str(rtt),
                                      srtt=Time.from_str(srtt),
                                      rttvar=Time.from_str(rttvar))
        except ValueError:
            time, rto = line.split()
            return TimeoutTraceEntity(time=Time.from_str(time),
                                      rto=Time.from_str(rto),
                                      rtt=None,
                                      srtt=None,
                                      rttvar=None)


class TimeoutTraceFile:

    def __init__(self, file_name: str):
        self.file_name = file_name

    def __iter__(self) -> TimeoutTraceEntity:
        with open(self.file_name) as file:
            for line in file:
                yield TimeoutTraceEntity.from_str(line)

    def get_metrics(self) -> TimeoutMetrics:
        metrics = TimeoutMetrics()
        for x in self:
            metrics.add_metric(x.time, x.rto)
        return metrics
