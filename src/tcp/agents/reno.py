import logging

from src.tcp.common.fast_retransmit import FastRetransmitState
from src.tcp.common.tcp_state import TcpState
from src.tcp.congestion_window.slow_start import SlowStart, CWND_ACTION
from src.tcp.timeout.jacobson_karels import JacobsonKarelsTimeoutEstimator
from src.tcp.agents.tcp_agent import TcpAgent, timeout_func
from src.tcp.timeout.timeout import Timeout
from src.trace.trace_file import Time, PacketEvent


class TcpReno(TcpAgent):

    def __init__(self, initial_timeout: str = "3.0", fast_retransmit_threshold: int = 3, initial_value: int = 1,
                 slow_start_threshold: int = 20, mss: int = 1000):
        super().__init__()
        self.timeout_metric.timeout_value_type = "s"
        self.state = TcpState()
        estimator = JacobsonKarelsTimeoutEstimator(Time.from_str(initial_timeout))
        self.timeout_service = Timeout(estimator=estimator, timeout_func=timeout_func(self))
        self.cw = SlowStart(initial_value=initial_value, slow_start_threshold=slow_start_threshold, mss=mss)
        self.fast_retransmit = FastRetransmitState(start_fast_retransmit_threshold=fast_retransmit_threshold)

    def recv_packet(self, packet: PacketEvent):
        self.timeout_service.schedule(packet.time)
        if self.state.is_new_ack(packet):
            self.__new_timer(packet)
            self.cw.recv_ack()
            self.fast_retransmit = self.fast_retransmit.ack()
            self.state = self.state.update_last_received_ack(packet)
            self.timeout_service.received_ack(packet)
        elif self.state.is_dup_ack(packet):
            self.fast_retransmit = self.fast_retransmit.duplicate_ack()
            if self.fast_retransmit.should_start_fast_retransmit:
                self.dupack_action(packet)
        self.add_metrics(packet.time)

    def dupack_action(self, packet: PacketEvent):
        if self.allow_fast_retrans:
            self.fast_retransmit = self.fast_retransmit.set_recover(self.state.highest_package_sent)
            self.cw.slowdown()
            self.timeout_service.reset_timer(packet.time)

    @property
    def allow_fast_retrans(self) -> bool:
        return self.fast_retransmit.we_recovered(
            self.state.last_recv_ack) or self.cw.state == CWND_ACTION.CWND_ACTION_DUPACK

    def send_packet(self, packet: PacketEvent):
        self.timeout_service.schedule(packet.time)
        force_set_rtx_timer = self.state.has_everything_acknowledged
        if self.state.is_new_package_sent(packet):
            self.state = self.state.update_highest_package_sent(packet)
            self.timeout_service.update_timer_with_new_package(packet)
        if self.timeout_service.is_doing_nothing(packet) or force_set_rtx_timer:
            self.timeout_service.set_timer(packet.time)
        self.add_metrics(packet.time)

    def __new_timer(self, packet: PacketEvent):
        if self.state.is_retransmit(packet):
            self.timeout_service.set_timer(packet.time)
        else:
            self.timeout_service.inactivate()

    def timeout(self, timeout_time: Time):
        logging.debug(f'[TIMEOUT] Timeout on {timeout_time}')
        self.congestion_window_metric.add_metric(timeout_time + Time.from_str('0.02'), self.cw.cw)
        self.fast_retransmit = self.fast_retransmit.ack()
        self.cw.has_timed_out()
        self.timeout_service.reset_timer(timeout_time)
        self.timeout_service.multiply_timeout_by(2)
        self.add_metrics(timeout_time)

    def add_metrics(self, time: Time):
        self.timeout_metric.add_metric(time + Time.from_str('0.02'),
                                       (self.timeout_service.timeout + Time.from_str('0.02')))
        self.congestion_window_metric.add_metric(time + Time.from_str('0.02'), self.cw.cw)
