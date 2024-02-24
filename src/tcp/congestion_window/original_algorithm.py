from src.tcp.congestion_window.cw import CongestionWindow
from src.tcp.congestion_window.cw_algorithm import CWAlgorithm


class Rfc793CongestionControl(CWAlgorithm):

    def __init__(self, initial_value: int = 1, max_congestion_window: int = 20, mss: int = 1000):
        self.initial_congestion_window: CongestionWindow = CongestionWindow(initial_value, mss=mss)
        self.congestion_window: CongestionWindow = CongestionWindow(initial_value, mss=mss)
        self.max_congestion_window: CongestionWindow = CongestionWindow(max_congestion_window, mss=mss)

    def recv_ack(self):
        self.congestion_window = self.max_congestion_window

    def has_timed_out(self):
        self.congestion_window = self.initial_congestion_window

    @property
    def cw(self) -> float:
        return self.congestion_window.value

    def get_cw(self) -> float:
        return self.cw
