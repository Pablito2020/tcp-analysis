from abc import ABC, abstractmethod

from src.metrics.metrics import TcpMetrics, CongestionWindowMetrics, TimeoutMetrics
from src.trace.filters import filter_packets_from_node
from src.trace.trace_file import Node, TraceFile


class TcpAgent(ABC):
    """
    Abstract class for TCP agents
    """
    def __init__(self):
        self.congestion_window_metric = CongestionWindowMetrics()
        self.timeout_metric = TimeoutMetrics()

    def reset_metrics(self):
        self.congestion_window_metric = CongestionWindowMetrics()
        self.timeout_metric = TimeoutMetrics()

    @abstractmethod
    def send_packet(self, packet):
        pass

    @abstractmethod
    def recv_packet(self, packet):
        pass

    @abstractmethod
    def get_timeout(self):
        pass

    @abstractmethod
    def get_congestion_window(self):
        pass


class Tcp:

    def __init__(self, agent: TcpAgent, node: Node):
        self.agent = agent
        self.node = node

    def get_metrics(self, trace: TraceFile) -> TcpMetrics:
        self.agent.reset_metrics()
        packets_from_tcp_sender = list(filter_packets_from_node(node=self.node, trace=trace))
        print(packets_from_tcp_sender)
        # for each, do send or recv, etc.
        # return the metrics
        return TcpMetrics(self.agent.timeout_metric, self.agent.congestion_window_metric)
