from src.trace.trace_file import Node, TraceFile, EventType, PacketEvent


def send_from(node: Node, packet: PacketEvent):
    return packet.source == node and packet.event_type == EventType.PutQueue


def received(node: Node, packet: PacketEvent):
    return packet.destination == node and packet.event_type == EventType.Received


def filter_packets_from_node(node: Node, trace: TraceFile):
    """
    Filters the packets from a given node (sent and received) in the trace file
    """
    for packet in trace:
        if send_from(node, packet) or received(node, packet):
            yield packet
