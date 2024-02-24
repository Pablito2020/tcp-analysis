from dataclasses import dataclass, InitVar, field


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class CongestionWindow:
    initial_value: InitVar[int | None] = None
    initial_bytes: InitVar[int | None] = None
    bytes: int = field(init=False)
    mss: int = field(default=1000, compare=False)

    def __post_init__(self, initial_value: int | None = None, initial_bytes: int | None = None):
        assert (initial_value is None) != (initial_bytes is None), "Initial value or initial bytes should be provided"
        if initial_value is not None:
            assert initial_value > 0, "Initial value should be at least 1"
            object.__setattr__(self, "bytes", initial_value * self.mss)
        if initial_bytes is not None:
            assert initial_bytes > 0, "Initial bytes should be at least 1"
            object.__setattr__(self, "bytes", initial_bytes)

    @property
    def value(self) -> float:
        return self.bytes / self.mss

    def exponential_increase(self) -> 'CongestionWindow':
        new_bytes = self.bytes + self.mss
        return CongestionWindow(initial_bytes=new_bytes, mss=self.mss)

    def linear_increase(self) -> 'CongestionWindow':
        new_bytes = self.bytes + int((self.mss / self.bytes) * self.mss)
        return CongestionWindow(initial_bytes=new_bytes, mss=self.mss)

    def make_half(self) -> 'CongestionWindow':
        new_bytes = self.bytes // 2
        return CongestionWindow(initial_bytes=new_bytes, mss=self.mss)

    def __ge__(self, other: 'CongestionWindow') -> bool:
        return self.value >= other.value

    def __lt__(self, other: 'CongestionWindow') -> bool:
        return self.value < other.value

    def make_third(self):
        new_bytes = self.bytes // 3
        return CongestionWindow(initial_bytes=new_bytes, mss=self.mss)
