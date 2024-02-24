from typing import List, Callable

from src.trace.trace_file import Node, TraceFile, EventType, PacketEvent, PacketType


def dequeue_packet_on(node: Node, packet: PacketEvent):
    return packet.source == node and packet.event_type == EventType.DropQueue


def enqueue_packet_on(node: Node, packet: PacketEvent):
    return packet.source == node and packet.event_type == EventType.PutQueue


def received(node: Node, packet: PacketEvent):
    return packet.destination == node and packet.event_type == EventType.Received


def filter_packets_from_node(node: Node, trace: TraceFile,
                             send_func: Callable[[Node, PacketEvent], bool] = enqueue_packet_on):
    """
    Filters the packets from a given node (sent and received) in the trace file
    What you consider as sent is defined by the send_func, which is enqueue_packet_on by default
    but can be changed to dequeue_packet_on if you want to consider the packet is sent when it is dequeued
    """
    for packet in trace:
        if send_func(node, packet) or received(node, packet):
            yield packet


def assert_tcp_packets(packets: List[PacketEvent]) -> None:
    """
    Asserts that the packets are all TCP
    """
    packets_not_tcp = [packet for packet in packets if packet.packet_type is PacketType.Udp]
    assert len(packets_not_tcp) == 0, "Packets are not all TCP."
