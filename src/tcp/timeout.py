from dataclasses import dataclass

from src.trace.trace_file import SequenceNumber, TimeInterval, PacketEvent, Time


@dataclass(frozen=True, order=True)
class TimeoutEvent:
    ack_allowed_interval: TimeInterval
    tcp_sequence_number: SequenceNumber

    def __contains__(self, time: Time) -> bool:
        return time in self.ack_allowed_interval

    @property
    def timeout_time(self) -> Time:
        return self.ack_allowed_interval.end


class TimeoutService:

    def __init__(self):
        self.timeout_event: TimeoutEvent | None = None

    def send_packet(self, packet: PacketEvent):
        # TODO: update timeout here if it is none
        pass

    def recv_packet(self, packet: PacketEvent):
        # TODO: update timeout here if it is none
        pass

    def has_timed_out(self, time: Time) -> bool:
        if allowed_window_time := self.timeout_event:
            return time not in allowed_window_time
        return False

    @property
    def sequence_number(self) -> SequenceNumber | None:
        if timeout_event := self.timeout_event:
            return timeout_event.tcp_sequence_number
        return None

    @property
    def next_timeout(self) -> Time | None:
        if timeout_event := self.timeout_event:
            return timeout_event.timeout_time
        return None
