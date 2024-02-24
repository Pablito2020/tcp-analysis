from decimal import Decimal

from src.trace.trace_file import Time, TimeInterval


class JacobsonKarelsTimeoutEstimator:

    def __init__(self, initial_timeout: Time):
        self.estimated_rtt: Time | None = None
        self.deviation: Time | None = None
        self.timeout: Time = initial_timeout

    def recalculate_timeout(self, ack_recv_time: TimeInterval):
        rtt = ack_recv_time.end - ack_recv_time.begin
        ALPHA = Decimal("0.125")
        BETA = Decimal("0.25")
        if not self.estimated_rtt:
            self.estimated_rtt = rtt
            self.deviation = rtt.half()
        else:
            diff = rtt - self.estimated_rtt
            self.estimated_rtt = self.estimated_rtt + diff * ALPHA
            self.deviation = self.deviation + (abs(diff) - self.deviation) * BETA
        self.timeout = Time(self.estimated_rtt.value + 4 * self.deviation.value)
