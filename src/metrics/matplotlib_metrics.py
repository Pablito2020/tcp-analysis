import logging

from src.metrics.metrics import TcpMetrics, CongestionWindowMetrics, TimeoutMetrics
import matplotlib.pyplot as plt

logging.getLogger('matplotlib').setLevel(logging.CRITICAL)


def print_congestion_window_metrics(metrics: CongestionWindowMetrics, file: str) -> None:
    plt.title('Congestion window x Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Congestion window (MSS)')
    plt.legend(loc='upper right')
    plt.plot(metrics.time, metrics.value, color='blue')
    plt.savefig(file, bbox_inches='tight')
    plt.clf()
    logging.info(f"Saved congestion window metrics. Image path: {file}")


def print_timeout_metrics(metrics: TimeoutMetrics, file: str) -> None:
    plt.title('Timeout x Time')
    plt.xlabel('Time (s)')
    plt.ylabel(f'Timeout ({metrics.timeout_value_type})')
    plt.legend(loc='upper right')
    plt.plot(metrics.time, metrics.value, color='blue')
    plt.savefig(file, bbox_inches='tight')
    plt.clf()
    logging.info(f"Saved timeout metrics. Image path: {file}")


def versus_congestion_windows(original: CongestionWindowMetrics, program: CongestionWindowMetrics, file: str) -> None:
    plt.title('Congestion window x Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Congestion window (MSS)')
    plt.legend(loc='upper right')
    plt.plot(original.time, original.value, color='blue')
    plt.plot(program.time, program.value, color='red')
    plt.legend(['Original', 'Program'], loc='lower right')
    plt.savefig(file, bbox_inches='tight')
    plt.clf()
    logging.info(f"Saved congestion window diff. Image path: {file}")


def versus_timeouts(original: TimeoutMetrics, program: TimeoutMetrics, file: str) -> None:
    plt.title('Timeout x Time')
    plt.xlabel('Time (s)')
    plt.ylabel(f'Timeout ({program.timeout_value_type})')
    plt.plot(original.time, original.value, color='blue')
    plt.plot(program.time, program.value, color='red')
    plt.legend(['Original', 'Program'], loc='lower right')
    plt.savefig(file, bbox_inches='tight')
    plt.clf()
    logging.info(f"Saved timeout diff. Image path: {file}")


def print_metric(metrics: TcpMetrics, folder: str, type: str) -> None:
    logging.info(f"Saving metrics for {type} on folder {folder}")
    print_congestion_window_metrics(metrics.congestion_window_metrics,
                                    file=f'{folder}/congestion_window_{type}_plot.png')
    print_timeout_metrics(metrics.timeout_metrics, file=f'{folder}/timeout_{type}_plot.png')


def print_metrics(original: TcpMetrics, program: TcpMetrics, folder: str = "./images"):
    print_metric(original, folder=f"{folder}", type="original")
    print_metric(program, folder=f"{folder}", type="program")
    logging.info(f"Saving diff metrics between original and program on folder {folder}")
    versus_timeouts(original=original.timeout_metrics, program=program.timeout_metrics,
                    file=f'{folder}/timeout_plot.png')
    versus_congestion_windows(original=original.congestion_window_metrics,
                              program=program.congestion_window_metrics,
                              file=f'{folder}/congestion_window_plot.png')
