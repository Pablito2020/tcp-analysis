import logging

from src.tcp.congestion_window.cw_algorithm import CWAlgorithm
from src.tcp.timeout.jacobson_karels import JacobsonKarelsTimeoutEstimator
from src.tcp.agents.tcp_agent import TcpAgent, timeout_func
from src.tcp.common.tcp_state import TcpState
from src.tcp.timeout.timeout import Timeout
from src.trace.trace_file import Time, PacketEvent


class TcpRfc793Agent(TcpAgent):

    def __init__(self, cw_algorithm: CWAlgorithm, initial_timeout: str = "3.0", karn_rtt: bool = True):
        super().__init__()
        self.state = TcpState()
        estimator = JacobsonKarelsTimeoutEstimator(Time.from_str(initial_timeout))
        self.timeout_service = Timeout(estimator=estimator, timeout_func=timeout_func(self))
        self.cw = cw_algorithm
        self.karn_rtt = karn_rtt

    def recv_packet(self, packet: PacketEvent):
        self.timeout_service.schedule(packet.time)
        if self.state.is_new_ack(packet):
            self.__new_timer(packet)
            self.cw.recv_ack()
            self.state = self.state.update_last_received_ack(packet)
            self.timeout_service.received_ack(packet)
        self.add_metrics(packet.time)

    def send_packet(self, packet: PacketEvent):
        self.timeout_service.schedule(packet.time)
        seq_no = packet.sequence_number.value
        force_timer = self.state.has_everything_acknowledged
        if self.state.is_new_package_sent(packet):
            logging.debug(f'[SEND] Setting max_seq_ to {seq_no} on {packet.time}')
            self.state = self.state.update_highest_package_sent(packet)
            self.timeout_service.update_timer_with_new_package(packet)
        else:
            if not self.karn_rtt:
                logging.debug(f'[KANRTT] Forcing update on timer because karn rtt is disabled')
                self.timeout_service.force_update_timer_with_new_package(packet)
        if self.timeout_service.is_doing_nothing(packet) or force_timer:
            logging.debug(
                f'[TIMER] Setting timer on package {packet.sequence_number} because scheduling was not done yet')
            self.timeout_service.set_timer(packet.time)
        self.add_metrics(packet.time)

    def __new_timer(self, packet: PacketEvent):
        if self.state.is_retransmit(packet):
            logging.debug(f"[Ack]: {packet.sequence_number.value} on {packet.time}")
            self.timeout_service.set_timer(current_time=packet.time)
        else:
            self.timeout_service.inactivate()

    def timeout(self, timeout_time: Time):
        logging.debug(f'[TIMEOUT] Timeout on {timeout_time}')
        self.congestion_window_metric.add_metric(timeout_time + Time.from_str('0.02'), self.cw.get_cw())
        self.cw.has_timed_out()
        self.timeout_service.reset_timer(timeout_time)
        self.add_metrics(timeout_time)

    def add_metrics(self, time: Time):
        self.timeout_metric.add_metric(time + Time.from_str('0.02'),
                                       (self.timeout_service.timeout + Time.from_str('0.02')) * 100)
        self.congestion_window_metric.add_metric(time + Time.from_str('0.02'), self.cw.get_cw())
