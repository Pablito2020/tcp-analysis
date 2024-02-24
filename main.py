import logging

from src.config.args import parse_args
from src.metrics.matplotlib_metrics import print_metrics, print_metric

if __name__ == '__main__':
    try:
        config = parse_args()
        if config.original_metrics and config.trace:
            program_metrics = config.tcp.get_metrics(trace=config.trace)
            print_metrics(original=config.original_metrics, program=program_metrics, folder=config.folder)
        elif config.trace:
            program_metrics = config.tcp.get_metrics(trace=config.trace)
            print_metric(metrics=program_metrics, folder=config.folder, type="program")
        elif config.original_metrics:
            print_metric(metrics=config.original_metrics, folder=config.folder, type="original")
        else:
            logging.error("Nothing specified....")
    except Exception as e:
        logging.error(f"Something very bad happened.\nError: {e}")
        exit(1)
