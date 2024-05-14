import time
from typing import Optional, Iterable, Sized

from .progress_bar import ProgressBar
from .progress_bar_pool import ProgressBarPool
from ..print_ import bprint


class AsciiProgressBar(ProgressBar):

    def __init__(
            self,
            iterable: Iterable,
            position: int,
            *,
            total: Optional[float] = None,
            desc: str = "",
            leave: bool = True,
            num_bars: int = 1,
            ncols: int = 50,
            pool: Optional = None,
            **kwargs
    ):
        total_ = 1
        if isinstance(iterable, Sized):
            total_ = len(iterable)
        if total is not None:
            total_ = total
        ProgressBar.__init__(self, total_, position)
        self.iterable: Iterable = iterable
        self.pool: ProgressBarPool = pool
        self.num_bars: int = num_bars
        self.leave: bool = leave
        self.desc: str = desc
        self.initial_value: float = 0
        self.current_value: float = 0
        self.ncols: int = ncols
        self.unit: str = "it"
        self.pbar_format = "{l_bar} |{bar}| {n_fmt:.2f}/{total_fmt:.2f}{unit}" \
                           " [{elapsed:.2f}<{remaining}, {rate_fmt:.2f}{unit}{postfix}]"
        self.__dict__.update(kwargs)
        self.initial_start_time = time.time()
        self.prev_update: float = self.initial_start_time
        self.delta: float = 0
        self.prev_value: float = self.initial_value
        self.bprint_row_index = bprint.current_row

    def __iter__(self):
        self.bprint_row_index = bprint.current_row
        for v in self.iterable:
            self.update(0)
            yield v
            bprint.move_up()
            bprint.clear_line()
            bprint.rows.pop()
            self.update(1)
            bprint.move_up()
            bprint.clear_line()
            bprint.rows.pop()
        if self.position > 0:
            self.reset()
        else:
            self.draw()

    def draw(self, *, refresh: bool = False) -> None:
        percent = self.current_value / self.total
        num_to_fill = int(percent * self.ncols)
        progress_str = num_to_fill * "#" + (self.ncols - num_to_fill) * " "
        to_print = self.pbar_format.format(
            l_bar=self.desc,
            bar=progress_str,
            n_fmt=self.current_value,
            total_fmt=self.total,
            elapsed=self.prev_update - self.initial_start_time,
            remaining="?",
            rate_fmt=(self.current_value - self.prev_value) /
                     self.delta if self.delta != 0 else 0,
            postfix="/s",
            unit=self.unit
        )
        if refresh and self.pool is not None and len(self.pool.bars) > 1:
            for w in self.writes:
                bprint(w, end="")
        bprint(to_print)

    def update(self, amount: float = 1, refresh: bool = False):
        self.prev_value = self.current_value
        self.current_value = min(
            self.current_value + amount, self.total)  # type:ignore
        current_time = time.time()
        self.delta = current_time - self.prev_update
        self.prev_update = current_time
        self.draw(refresh=refresh)

    def _write(self, *args: str, sep: str = " ", end: str = "\n") -> None:
        if not end.endswith("\n"):
            end += "\n"
        if self.pool is not None and len(self.pool.bars) > 0:
            succeeding_bars = self.pool.bars[self.position + 1:]
            if succeeding_bars:
                for succeeding_bar in succeeding_bars:
                    # clear child
                    bprint.move_up()
                    bprint.clear_line()
                    bprint.rows.pop()
                    for _ in range(succeeding_bar.num_writes):
                        # clear child's writes
                        bprint.move_up()
                        bprint.clear_line()
                        bprint.rows.pop()
                # clear self
                bprint.move_up()
                bprint.clear_line()
                bprint.rows.pop()
                bprint(sep.join(map(str, args)), end=end)
                self.draw()
                for succeeding_bar in succeeding_bars:
                    succeeding_bar.update(0, refresh=True)
                return

        bprint.move_up()
        bprint.clear_line()
        bprint.rows.pop()
        bprint(sep.join(map(str, args)), end=end)
        self.draw()

    def reset(self) -> None:
        self.current_value = self.initial_value
        self.initial_start_time = time.time()
        self.delta = 0
        self.prev_value = self.initial_value
        for _ in range(self.num_writes):
            bprint.move_up()
            bprint.clear_line()
            bprint.rows.pop()
        self.writes.clear()


__all__ = [
    'AsciiProgressBar'
]
