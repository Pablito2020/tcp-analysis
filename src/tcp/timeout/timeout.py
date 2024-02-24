import logging
from dataclasses import field, dataclass, InitVar

from src.tcp.timeout.jacobson_karels import JacobsonKarelsTimeoutEstimator
from src.tcp.timeout.scheduler import Scheduler, TimeoutFunc
from src.trace.trace_file import SequenceNumber, Time, PacketEvent, TimeInterval


@dataclass
class Timeout:
    estimator: JacobsonKarelsTimeoutEstimator
    seq_number_to_timeout: SequenceNumber | None = None  # rtt_seq number of sequence being timed if rtt_active_ is 1
    time_seq_number_was_sent: Time = Time.from_str("0")  # rtt_ts
    is_active: bool = False  # rtt_active
    timeout_func: InitVar[TimeoutFunc | None] = None
    scheduler: Scheduler = field(init=False)

    def __post_init__(self, timeout_func: TimeoutFunc | None):
        if not timeout_func:
            raise ValueError("Specify a timeout function!")
        self.scheduler = Scheduler(timeout_action=timeout_func)

    def received_ack(self, packet: PacketEvent):
        if self.is_active and (not self.seq_number_to_timeout or packet.sequence_number >= self.seq_number_to_timeout):
            self.is_active = False
            interval = TimeInterval(begin=self.time_seq_number_was_sent, end=packet.time)
            self.estimator.recalculate_timeout(ack_recv_time=interval)

    def update_timer_with_new_package(self, packet: PacketEvent):
        if not self.is_active:
            assert not self.seq_number_to_timeout or packet.sequence_number > self.seq_number_to_timeout, "If we're doing a timeout, the new one should have a bigger #seq"
            self.force_update_timer_with_new_package(packet)

    def force_update_timer_with_new_package(self, packet: PacketEvent):
        self.is_active = True
        self.seq_number_to_timeout = packet.sequence_number
        self.time_seq_number_was_sent = packet.time
        logging.debug(f'[TIMER] Setting rtt_ts to {packet.time}, with seq_no: {packet.sequence_number}')

    def set_timer(self, current_time: Time) -> None:
        """
        Sets a timer from the current time to the current estimated timeout
        :param current_time: The time we're right now
        """
        timeout = self.estimator.timeout
        current_timeout = current_time + timeout
        logging.debug(f'[TIMER] Setting from ({current_time} to {current_time + timeout})')
        self.scheduler.set_timer(current_timeout)

    def reset_timer(self, curr_time: Time):
        self.set_timer(current_time=curr_time)
        self.is_active = False

    def inactivate(self):
        self.scheduler.inactivate()

    def is_doing_nothing(self, packet: PacketEvent):
        return not self.scheduler.is_pending(packet.time)

    def schedule(self, curr_time: Time):
        self.scheduler.schedule(curr_time)

    @property
    def timeout(self) -> Time:
        return self.estimator.timeout

    def multiply_timeout_by(self, value: int):
        self.estimator.timeout *= value
