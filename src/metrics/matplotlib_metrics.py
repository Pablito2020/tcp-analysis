from src.metrics.metrics import TcpMetrics, CongestionWindowMetrics, TimeoutMetrics
import matplotlib.pyplot as plt


def print_congestion_window_metrics(metrics: CongestionWindowMetrics) -> None:
    plt.title('Congestion window x Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Congestion window (MSS)')
    plt.legend(loc='upper right')
    plt.savefig("congestion_window_plot.png")
    plt.figure(figsize=(12, 8))
    plt.plot(metrics.time, metrics.value, color='blue')
    plt.show()


def print_timeout_metrics(metrics: TimeoutMetrics) -> None:
    plt.title('Timeout x Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Timeout (s)')
    plt.legend(loc='upper right')
    plt.savefig("timeout_plot.png")
    plt.figure(figsize=(12, 8))
    plt.plot(metrics.time, metrics.value, color='blue')
    plt.show()


def print_metrics(metrics: TcpMetrics) -> None:
    print_congestion_window_metrics(metrics.congestion_window_metrics)
    print_timeout_metrics(metrics.timeout_metrics)
