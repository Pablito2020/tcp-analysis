from argparse import ArgumentParser, RawTextHelpFormatter
from typing import Tuple

from src.metrics.matplotlib_metrics import print_metrics
from src.tcp.rfc_793 import Rfc793
from src.tcp.tcp import Tcp
from src.trace.trace_file import Node, TraceFile


def parse_args() -> Tuple[Tcp, TraceFile]:
    parser = ArgumentParser(prog="NS TCP Simulator",
                            description="Program that reads a trace from ns (network simulator version 2) and "
                                        "simulates the timeouts and congestion window of a TCP agent.",
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument('-f', '--file', type=str, help='File name of the trace.', default="./data/trace_file.res")
    parser.add_argument('-node',
                        '--node',
                        default=1,
                        type=int,
                        help='Node identifier of the TCP sender. Default is 1.')
    parser.add_argument('-i',
                        '--implementation',
                        default='rfc793',
                        help='Provide the implementation of the TCP agent. Default is rfc793.')
    args = parser.parse_args()
    node = Node(identifier=args.node)
    tcp_agent = Rfc793() if args.implementation == 'rfc793' else None
    return Tcp(agent=tcp_agent, node=node), TraceFile(file_name=args.file)


if __name__ == '__main__':
    try:
        tcp, trace_file = parse_args()
        metrics = tcp.get_metrics(trace=trace_file)
        print_metrics(metrics)
    except Exception as e:
        print(f'Error: {e}')
