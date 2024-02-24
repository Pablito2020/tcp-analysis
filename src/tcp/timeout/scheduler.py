from typing import Callable

from src.trace.trace_file import Time

TimeoutFunc = Callable[[Time], None]


class Scheduler:

    def __init__(self, timeout_action: TimeoutFunc):
        self.action = timeout_action
        self.time_to_execute_action: Time | None = None

    def inactivate(self):
        self.time_to_execute_action = None

    def set_timer(self, time: Time):
        self.time_to_execute_action = time

    def schedule(self, time: Time):
        if self.time_to_execute_action and self.time_to_execute_action <= time:
            self.action(self.time_to_execute_action)

    def is_pending(self, current_time: Time):
        return self.time_to_execute_action and self.time_to_execute_action > current_time
