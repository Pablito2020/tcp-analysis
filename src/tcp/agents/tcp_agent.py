from abc import ABC, abstractmethod

from src.metrics.metrics import CongestionWindowMetrics, TimeoutMetrics
from src.trace.trace_file import Time


class TcpAgent(ABC):
    """
    Abstract class for TCP agents
    """

    def __init__(self):
        self.congestion_window_metric = CongestionWindowMetrics()
        self.timeout_metric = TimeoutMetrics()

    def reset_metrics(self):
        self.congestion_window_metric.reset()
        self.timeout_metric.reset()

    @abstractmethod
    def send_packet(self, packet):
        pass

    @abstractmethod
    def recv_packet(self, packet):
        pass

    @abstractmethod
    def timeout(self, time: Time):
        pass


def timeout_func(tcp_agent: TcpAgent):
    def timeout_action(timeout_time: Time):
        tcp_agent.timeout(timeout_time)

    return timeout_action
