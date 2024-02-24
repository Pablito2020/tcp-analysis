from dataclasses import dataclass, replace

from src.trace.trace_file import SequenceNumber


@dataclass(frozen=True)
class FastRetransmitState:
    start_fast_retransmit_threshold: int
    duplicated_ack: int = 0
    recover: SequenceNumber | None = None

    def we_recovered(self, sequence_num: SequenceNumber):
        if not self.recover:
            return True
        return sequence_num > self.recover

    def duplicate_ack(self) -> 'FastRetransmitState':
        return replace(self, duplicated_ack=self.duplicated_ack + 1)

    @property
    def should_start_fast_retransmit(self) -> bool:
        return self.duplicated_ack == self.start_fast_retransmit_threshold

    def ack(self) -> 'FastRetransmitState':
        return replace(self, duplicated_ack=0)

    def set_recover(self, seq: SequenceNumber) -> 'FastRetransmitState':
        return replace(self, recover=seq)

