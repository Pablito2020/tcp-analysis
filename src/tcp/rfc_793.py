from src.tcp.congestion_window import CongestionWindow
from src.tcp.tcp import TcpAgent
from src.tcp.timeout import TimeoutService


class Rfc793(TcpAgent):
    """
    Implementation of RFC 793 (the timeout and congestion window algorithm)
    """

    def __init__(self):
        self.congestion_window = CongestionWindow(value=1, slow_start_threshold=1)
        self.timeout_service = TimeoutService()

    def send_packet(self, packet):
        # update cw and timeout?
        pass

    def recv_packet(self, packet):
        # update cw and timeout?
        pass

    def get_timeout(self):
        return self.timeout_service.next_timeout

    def get_congestion_window(self):
        return self.congestion_window.value
