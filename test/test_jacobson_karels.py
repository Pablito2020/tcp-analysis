from src.tcp.timeout.jacobson_karels import JacobsonKarelsTimeoutEstimator
from src.trace.trace_file import TimeInterval, Time


# |-------------------------------------------------|
# | RTT (s) | rtt | srtt | rttvar | timeout (aprox) |
# |-------------------------------------------------|
# |   0.14  | 14  | 112  |   28   |      42         |
# |   0.15  | 15  | 113  |   22   |      36         |
# |   0.15  | 15  | 114  |   18   |      32         |
# |   0.15  | 15  | 115  |   15   |      29         |
# |-------------------------------------------------|
def test_jacobson_karels():
    estimator = JacobsonKarelsTimeoutEstimator(initial_timeout=Time.from_str("3.0"))
    estimator.recalculate_timeout(TimeInterval(Time.from_str("0"), Time.from_str("0.14")))  # 14
    assert estimator.timeout == Time.from_str("0.42")
    estimator.recalculate_timeout(TimeInterval(Time.from_str("0.14"), Time.from_str("0.29")))  # 15
    assert estimator.timeout == Time.from_str("0.36125")
    estimator.recalculate_timeout(TimeInterval(Time.from_str("0.29"), Time.from_str("0.44")))  # 15
    assert estimator.timeout == Time.from_str("0.31609375")
    estimator.recalculate_timeout(TimeInterval(Time.from_str("0.44"), Time.from_str("0.59")))  # 15
    assert estimator.timeout == Time.from_str("0.28126953125")
