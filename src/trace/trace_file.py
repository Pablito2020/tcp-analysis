from __future__ import annotations

import logging
import pathlib
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import Enum
from typing import Generator


class EventType(Enum):
    PutQueue = '+'
    DropQueue = '-'
    Received = 'r'
    Dropped = 'd'

    @staticmethod
    def from_value(value: str) -> 'EventType':
        for event_type in EventType:
            if event_type.value == value:
                return event_type
        raise ValueError(f'Invalid event type: {value}')


@dataclass(frozen=True, order=True)
class Time:
    value: Decimal

    @staticmethod
    def from_str(value: str) -> 'Time':
        try:
            return Time(Decimal(value))
        except ValueError:
            raise ValueError(f'Invalid time: {value}')
        except InvalidOperation:
            raise ValueError(f'Invalid decimal time: {value}')

    def __sub__(self, value: 'Time') -> 'Time':
        assert isinstance(value, Time)
        return Time(self.value - value.value)

    def __add__(self, other: 'Time') -> 'Time':
        assert isinstance(other, Time)
        return Time(self.value + other.value)

    def __mul__(self, other: int | Decimal | Time) -> 'Time':
        if isinstance(other, Time):
            return Time(self.value * other.value)
        return Time(self.value * other)

    def __abs__(self):
        return Time(abs(self.value))

    def half(self) -> 'Time':
        return Time(self.value / 2)


@dataclass(frozen=True, order=True)
class TimeInterval:
    begin: Time
    end: Time

    def __post_init__(self):
        if self.begin > self.end:
            raise ValueError("Begin time must be less than end time")

    def __contains__(self, time: Time) -> bool:
        assert isinstance(time, Time)
        return self.begin <= time <= self.end


@dataclass(frozen=True, order=True)
class Node:
    identifier: int

    def __post_init__(self):
        if self.identifier < 0:
            raise ValueError("Node identifier must be non-negative")

    @staticmethod
    def from_str(value: str) -> 'Node':
        try:
            return Node(int(value))
        except ValueError as e:
            raise ValueError(f'Invalid node: {value}, error: {e}')


class PacketType(Enum):
    Tcp = 'tcp'
    Ack = 'ack'
    Udp = 'udp'

    @staticmethod
    def from_value(value: str) -> 'PacketType':
        if value not in ['tcp', 'ack', 'cbr', 'exp']:
            raise ValueError(f'Invalid packet type: {value}')
        if value in ['cbr', 'exp']:
            return PacketType.Udp
        # TODO: is this correct?
        return PacketType(value)


@dataclass(frozen=True, order=True)
class PacketSize:
    value: int

    @staticmethod
    def from_str(value: str) -> 'PacketSize':
        try:
            return PacketSize(int(value))
        except ValueError:
            raise ValueError(f'Invalid packet size: {value}')


@dataclass(frozen=True, unsafe_hash=True)
class Flags:
    value: str

    @staticmethod
    def from_str(value: str) -> 'Flags':
        return Flags(value)


@dataclass(frozen=True, order=True)
class FlowIdentifier:
    value: int

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Flow identifier must be non-negative")

    @staticmethod
    def from_str(value: str) -> 'FlowIdentifier':
        try:
            return FlowIdentifier(int(value))
        except ValueError as e:
            raise ValueError(f'Invalid flow identifier: {value}, error: {e}')


@dataclass(frozen=True)
class Port:
    value: int

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Port must be non-negative")

    @staticmethod
    def from_str(value: str) -> 'Port':
        try:
            return Port(int(value))
        except ValueError as e:
            raise ValueError(f'Invalid port: {value}, error: {e}')


@dataclass(frozen=True)
class Address:
    node: Node
    port: Port

    @staticmethod
    def from_str(value: str) -> 'Address':
        try:
            node, port = value.split(".")
        except ValueError:
            raise ValueError(f'Invalid address: {value}, not in the format "node.port"')
        node = Node.from_str(node)
        port = Port.from_str(port)
        return Address(node, port)


@dataclass(frozen=True, order=True)
class SequenceNumber:
    value: int

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Sequence number must be non-negative")

    @staticmethod
    def from_str(value: str) -> 'SequenceNumber':
        try:
            return SequenceNumber(int(value))
        except ValueError as e:
            raise ValueError(f'Invalid sequence number: {value}, error: {e}')

    @staticmethod
    def syn_handshake() -> 'SequenceNumber':
        return SequenceNumber(0)

    def __add__(self, other: int) -> 'SequenceNumber':
        return SequenceNumber(self.value + other)


@dataclass(frozen=True, order=True)
class PacketIdentifier:
    value: int

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Packet identifier must be non-negative")

    @staticmethod
    def from_str(value: str) -> 'PacketIdentifier':
        try:
            return PacketIdentifier(int(value))
        except ValueError as e:
            raise ValueError(f'Invalid packet identifier: {value}, error: {e}')


@dataclass(frozen=True, unsafe_hash=True)
class PacketEvent:
    event_type: EventType
    time: Time
    source: Node
    destination: Node
    packet_type: PacketType
    packet_size: PacketSize
    flags: Flags
    flow_id: FlowIdentifier
    source_addr: Address
    destination_addr: Address
    sequence_number: SequenceNumber
    packet_identifier: PacketIdentifier

    @staticmethod
    def from_str(value: str) -> 'PacketEvent':
        parts = value.split(" ")
        if len(parts) != 12:
            raise ValueError(f'Invalid packet event: {value}, expected 12 parts, got {len(parts)}')
        event_type = EventType.from_value(parts[0])
        time = Time.from_str(parts[1])
        source = Node.from_str(parts[2])
        destination = Node.from_str(parts[3])
        packet_type = PacketType.from_value(parts[4])
        packet_size = PacketSize.from_str(parts[5])
        flags = Flags.from_str(parts[6])
        flow_id = FlowIdentifier.from_str(parts[7])
        source_addr = Address.from_str(parts[8])
        destination_addr = Address.from_str(parts[9])
        sequence_number = SequenceNumber.from_str(parts[10])
        packet_identifier = PacketIdentifier.from_str(parts[11])
        return PacketEvent(
            event_type=event_type,
            time=time,
            source=source,
            destination=destination,
            packet_type=packet_type,
            packet_size=packet_size,
            flags=flags,
            flow_id=flow_id,
            source_addr=source_addr,
            destination_addr=destination_addr,
            sequence_number=sequence_number,
            packet_identifier=packet_identifier)

    def __str__(self):
        return f'Packet: {self.packet_type} ({self.source} to {self.destination}. Time: {self.time}. Seq: {self.sequence_number}\n'

    def __repr__(self):
        return self.__str__()


class TraceFile:

    def __init__(self, file_name: str):
        if not pathlib.Path(file_name).is_file():
            raise ValueError(f'Trace file not found: {file_name}')
        self.file_name = file_name

    def __iter__(self) -> Generator[PacketEvent, None, None]:
        with open(self.file_name, 'r') as file:
            for line in file:
                yield PacketEvent.from_str(line)
