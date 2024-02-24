import logging
from typing import List

from src.metrics.metrics import TcpMetrics
from src.tcp.agents.tcp_agent import TcpAgent
from src.trace.filters import filter_packets_from_node, assert_tcp_packets, dequeue_packet_on
from src.trace.trace_file import Node, TraceFile, PacketType, PacketEvent


class Tcp:

    def __init__(self, agent: TcpAgent, node: Node, assert_only_tcp: bool = True,
                 assert_same_enqueue_as_dequeue: bool = True):
        self.agent = agent
        self.node = node
        self.assert_only_tcp = assert_only_tcp
        self.assert_same_enq_as_deq = assert_same_enqueue_as_dequeue

    def get_metrics(self, trace: TraceFile) -> TcpMetrics:
        self.agent.reset_metrics()
        packets_from_tcp_sender = self.get_packages(trace=trace)
        for packet in packets_from_tcp_sender:
            logging.debug(f'Packet: {packet}')
            if packet.packet_type == PacketType.Tcp:
                self.agent.send_packet(packet)
            elif packet.packet_type == PacketType.Ack:
                self.agent.recv_packet(packet)
            else:
                logging.error(f"Not recognized package: {packet.packet_type}")
        return TcpMetrics(self.agent.timeout_metric, self.agent.congestion_window_metric)

    def get_packages(self, trace: TraceFile) -> List[PacketEvent]:
        packets_enqueued_tcp_sender = list(filter_packets_from_node(node=self.node, trace=trace))
        if self.assert_only_tcp:
            assert_tcp_packets(packets_enqueued_tcp_sender)
            received_packages = [packet for packet in packets_enqueued_tcp_sender if packet.destination == self.node]
            received_packages = [packet for packet in received_packages if packet.packet_type != PacketType.Ack]
            assert len(received_packages) == 0, "There are non-Ack packets received by the TCP sender."
            sent_packages = [packet for packet in packets_enqueued_tcp_sender if packet.source == self.node]
            sent_packages = [packet for packet in sent_packages if packet.packet_type != PacketType.Tcp]
            assert len(sent_packages) == 0, "There are non-TCP packets sent by the TCP sender."
        if self.assert_same_enq_as_deq:
            packets_dequeued = list(filter_packets_from_node(node=self.node, trace=trace, send_func=dequeue_packet_on))
            assert len(packets_enqueued_tcp_sender) == len(packets_dequeued), ("Length of packets enqueued and "
                                                                               "dequeued are not the same.")
        sorted_packets_enqueued_tcp_sender = sorted(packets_enqueued_tcp_sender, key=lambda packet: packet.time)
        assert sorted_packets_enqueued_tcp_sender == packets_enqueued_tcp_sender, "Packets are not sorted by time."
        return packets_enqueued_tcp_sender
