from abc import ABC, abstractmethod

from src.tcp.congestion_window.cw import CongestionWindow


class CWAlgorithm(ABC):

    @abstractmethod
    def recv_ack(self):
        pass

    @abstractmethod
    def has_timed_out(self):
        pass

    @abstractmethod
    def get_cw(self) -> float:
        pass
