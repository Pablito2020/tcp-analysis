import logging
import os
from argparse import ArgumentParser, RawTextHelpFormatter
from dataclasses import dataclass

from src.config.logging import configure_logging
from src.metrics.metrics import TcpMetrics
from src.tcp.agents.reno import TcpReno
from src.tcp.agents.rfc_793 import TcpRfc793Agent
from src.tcp.congestion_window.original_algorithm import Rfc793CongestionControl
from src.tcp.congestion_window.slow_start import SlowStart
from src.tcp.tcp import Tcp
from src.tcp.agents.tcp_agent import TcpAgent
from src.trace.congestion_window_file import CongestionWindowTraceFile
from src.trace.timeout_file import TimeoutTraceFile
from src.trace.trace_file import TraceFile, Node


@dataclass(frozen=True)
class Config:
    tcp: Tcp
    folder: str
    original_metrics: TcpMetrics | None
    trace: TraceFile | None

    def __post_init__(self):
        assert isinstance(self.tcp, Tcp)
        assert isinstance(self.folder, str)
        assert self.folder != '', "Folder cannot be empty."
        assert os.path.exists(self.folder), "Folder does not exist."


def get_agent_from(args) -> TcpAgent:
    match args.implementation:
        case 'rfc793':
            use_karn_rtt = args.karn_rtt
            initial_timeout = args.initial_timeout
            initial_cw = args.initial_cw
            mss = args.mss
            max_cw = args.max_cw if args.original_cw_algorithm else args.ssthreshold
            congestion_window_str = f"\t - max. congestion window: {max_cw}" if args.original_cw_algorithm else f"\t - slow start threshold: {max_cw}"
            algorithm_cw = Rfc793CongestionControl(initial_value=initial_cw, max_congestion_window=max_cw, mss=mss) if args.original_cw_algorithm else SlowStart(initial_value=initial_cw, slow_start_threshold=max_cw, mss=mss)
            logging.info(f"Using RFC 793 with:\n"
                         f"\t - karn rtt: {use_karn_rtt}\n"
                         f"\t - initial timeout: {initial_timeout}\n"
                         f"\t - initial congestion window: {initial_cw}\n"
                         f"\t - mss: {mss}\n"
                         f"{congestion_window_str}\n"
                         f"\t - using original cw algorithm: {args.original_cw_algorithm}\n"
                         f"\t - using slow start: {not args.original_cw_algorithm}\n"
                         )
            return TcpRfc793Agent(cw_algorithm=algorithm_cw, initial_timeout=initial_timeout, karn_rtt=use_karn_rtt)
        case 'reno':
            initial_timeout = args.initial_timeout
            initial_cw = args.initial_cw
            mss = args.mss
            slow_start_threshold = args.ssthreshold
            fast_retransmit_threshold = args.frthreshold
            logging.info(f"Using Reno with:\n"
                         f"\t - initial timeout: {initial_timeout}\n"
                         f"\t - initial congestion window: {initial_cw}\n"
                         f"\t - mss: {mss}\n"
                         f"\t - slow start threshold: {slow_start_threshold}\n"
                         f"\t - fast retransmit threshold: {fast_retransmit_threshold}"
                         )
            return TcpReno(initial_timeout=initial_timeout, fast_retransmit_threshold=fast_retransmit_threshold,
                           initial_value=initial_cw,
                           slow_start_threshold=slow_start_threshold, mss=mss)
        case _:
            raise ValueError(f"Invalid implementation: {args.implementation}")


def parse_args() -> Config:
    parser = ArgumentParser(prog="NS TCP Simulator",
                            description="Program that reads a trace from ns (network simulator version 2) and "
                                        "simulates the timeouts and congestion window of a TCP agent.",
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument('-f', '--file', type=str, help='File name of the trace.')
    parser.add_argument('-t', '--timeout-file', type=str, help='File name of the timeout trace')
    parser.add_argument('-c', '--congestion-file', type=str, help='File name of the congestion window trace')
    parser.add_argument('-node',
                        '--node',
                        default=1,
                        type=int,
                        help='Node identifier of the TCP sender. Default is 1.')
    parser.add_argument('-k',
                        '--karn-rtt',
                        default=True,
                        type=bool,
                        help='Weather to use karn rtt or not (only for RFC793)')
    parser.add_argument('--initial-timeout',
                        default="3.0",
                        type=str,
                        help='Initial timeout value (in seconds)')
    parser.add_argument('--initial-cw',
                        default=1,
                        type=int,
                        help='Initial congestion window value')
    parser.add_argument('--ssthreshold',
                        default=10,
                        type=int,
                        help='Slow start threshold')
    parser.add_argument('--frthreshold',
                        default=3,
                        type=int,
                        help='Fast Retransmit threshold (only for Reno)')
    parser.add_argument('--mss',
                        default=1000,
                        type=int,
                        help='Maximum Segment Size (in bytes)')
    parser.add_argument('--max-cw',
                        default=10,
                        type=int,
                        help='Maximum congestion window (only for RFC793 with original cw algorithm)')
    parser.add_argument('--original-cw-algorithm',
                        default=False,
                        type=bool,
                        help='Weather to use the original congestion window algorithm or not (only for RFC793)')
    parser.add_argument('-i',
                        '--implementation',
                        default='rfc793',
                        help='Provide the implementation of the TCP agent. Default is rfc793.')
    parser.add_argument(
        "-log",
        "--loglevel",
        default="info",
        help="Provide logging level. Example --loglevel debug",
    )
    parser.add_argument('-s',
                        '--save-folder',
                        default='./images',
                        help='Folder to save the images. Default is ./images.')
    args = parser.parse_args()
    configure_logging(args.loglevel.upper())
    node = Node(identifier=args.node)
    tcp_agent = get_agent_from(args)
    tcp_ = Tcp(agent=tcp_agent, node=node)
    if args.file:
        trace = TraceFile(file_name=args.file)
    else:
        trace = None
    if args.timeout_file and args.congestion_file:
        type_of_value_seconds = "ms" if isinstance(tcp_agent, TcpRfc793Agent) else "s"
        timeout = TimeoutTraceFile(file_name=args.timeout_file).get_metrics()
        timeout.timeout_value_type = type_of_value_seconds
        congestion = CongestionWindowTraceFile(file_name=args.congestion_file).get_metrics()
        tcp_original_metrics = TcpMetrics(timeout_metrics=timeout, congestion_window_metrics=congestion)
    else:
        tcp_original_metrics = None
    folder = args.save_folder
    return Config(trace=trace, tcp=tcp_, original_metrics=tcp_original_metrics, folder=folder)
