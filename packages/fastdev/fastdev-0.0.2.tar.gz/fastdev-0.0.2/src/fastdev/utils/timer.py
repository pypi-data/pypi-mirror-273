from contextlib import ContextDecorator
from time import perf_counter
from typing import Optional


class Timer(ContextDecorator):
    def __init__(self, start: bool = True, print_tmpl: Optional[str] = None):
        self.print_tmpl = print_tmpl if print_tmpl is not None else "{:.4f}"

        self._is_paused: bool = False
        self._total_paused: float = 0.0

        if start:
            self.start()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        print(self.print_tmpl.format(self.check()))

    def start(self) -> "Timer":
        if not self._is_paused:
            self._start = perf_counter()
        else:
            self._total_paused += perf_counter() - self._last
        self._last = perf_counter()
        self._is_paused = False
        return self

    def check(self):
        dur = perf_counter() - self._last
        self._last = perf_counter()
        return dur

    def pause(self):
        self._last = perf_counter()
        dur = perf_counter() - self._last
        self._is_paused = True
        return dur

    def seconds(self):
        if self._is_paused:
            end_time = self._last
        else:
            end_time = perf_counter()
        return end_time - self._start - self._total_paused
