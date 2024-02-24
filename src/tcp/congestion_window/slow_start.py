from enum import Enum

from src.tcp.congestion_window.cw import CongestionWindow
from src.tcp.congestion_window.cw_algorithm import CWAlgorithm


class CWND_ACTION(Enum):
    CWND_ACTION_DUPACK = 1  # dup acks/fast retransmit
    CWND_ACTION_TIMEOUT = 2  # retransmission timeout
    CWND_ACTION_EXITED = 4  # congestion recovery has ended


class SlowStart(CWAlgorithm):

    def __init__(self, initial_value: int = 1, slow_start_threshold: int = 20, mss: int = 1000):
        self.initial_congestion_window: CongestionWindow = CongestionWindow(initial_value, mss=mss)
        self.congestion_window: CongestionWindow = CongestionWindow(initial_value, mss=mss)
        self.slow_start_threshold: CongestionWindow = CongestionWindow(slow_start_threshold, mss=mss)
        self.CWMAX = CongestionWindow(slow_start_threshold, mss=mss)
        self.state: CWND_ACTION | None = None

    def recv_ack(self):
        if self.state == CWND_ACTION.CWND_ACTION_DUPACK:
            self.state = CWND_ACTION.CWND_ACTION_EXITED
        if self.should_enter_congestion_avoidance:
            self.congestion_window = self.congestion_window.linear_increase()
            self.slow_start_threshold = min(self.CWMAX, self.congestion_window)
        else:
            self.congestion_window = self.congestion_window.exponential_increase()

    @property
    def should_enter_congestion_avoidance(self):
        return self.congestion_window >= self.slow_start_threshold

    def has_timed_out(self):
        self.congestion_window = self.initial_congestion_window
        self.slow_start_threshold = max(self.initial_congestion_window, self.slow_start_threshold.make_half())

    def slowdown(self):
        """
        Apply fast retransmit and fast recovery (dup acknowledges, only for reno)
        """
        self.state = CWND_ACTION.CWND_ACTION_DUPACK
        self.slow_start_threshold = max(self.initial_congestion_window, self.slow_start_threshold.make_half())
        self.congestion_window = min(self.congestion_window.make_half(), self.CWMAX.make_half())

    @property
    def cw(self) -> float:
        return self.congestion_window.value

    def get_cw(self) -> float:
        return self.cw
