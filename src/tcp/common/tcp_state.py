from dataclasses import dataclass, replace

from src.trace.trace_file import SequenceNumber, PacketEvent


@dataclass(frozen=True)
class TcpState:
    last_recv_ack: SequenceNumber | None = None
    highest_package_sent: SequenceNumber | None = None

    def update_highest_package_sent(self, packet: PacketEvent) -> 'TcpState':
        return replace(self, highest_package_sent=packet.sequence_number)

    def is_new_ack(self, packet: PacketEvent) -> bool:
        if self.last_recv_ack is None:
            return True
        return packet.sequence_number > self.last_recv_ack

    def is_dup_ack(self, packet: PacketEvent) -> bool:
        return packet.sequence_number == self.last_recv_ack

    def is_new_package_sent(self, packet: PacketEvent) -> bool:
        if self.highest_package_sent is None:
            return True
        return packet.sequence_number > self.highest_package_sent

    def update_last_received_ack(self, packet: PacketEvent) -> 'TcpState':
        return replace(self, last_recv_ack=packet.sequence_number)

    def is_retransmit(self, packet: PacketEvent) -> bool:
        return packet.sequence_number < self.highest_package_sent

    @property
    def next_expected_ack(self):
        return self.last_recv_ack + 1

    @property
    def has_everything_acknowledged(self):
        return self.last_recv_ack == self.highest_package_sent
