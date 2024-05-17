from copy import deepcopy
import tkinter as tk
from tkinter import font
from typing import Any, Iterable, Self, Sized
AUTO = -1


class Counter:
    def __init__(self, *, item: Sized | None = None, min_max: tuple[int, int] = (0, 0), start_count: int = 0, loopable: bool = False) -> None:
        if item is None:
            self.min = min_max[0]
            self.max = min_max[1]
        else:
            self.min = 0
            self.max = len(item) - 1
        self._loopable = loopable
        self._current = start_count if start_count >= self.min and start_count <= self.max else self.min

    def __str__(self):
        return str(self._current)

    def __repr__(self):
        return f'{self._current!r}'

    def __int__(self):
        return self._current

    def __add__(self, value: int) -> 'Counter':
        if self.ulimit:
            return self
        else:
            aself = deepcopy(self)
            if aself.over_ulimit(value):
                if aself._loopable:
                    aself._current = (aself._current + value - aself.max - 1)
                else:
                    aself._current = aself.max
            else:
                aself._current += value
            return aself

    def __iadd__(self, value: int) -> Self:
        if self.ulimit:
            return self
        else:
            if self.over_ulimit(value):
                if self._loopable:
                    self._current = (self._current + value - self.max - 1)
                else:
                    self._current = self.max
            else:
                self._current += value
            return self

    def __sub__(self, value: int) -> 'Counter':
        if self.llimit:
            return self
        else:
            aself = deepcopy(self)
            if aself.over_llimit(value):
                if aself._loopable:
                    aself._current = aself.max + (aself._current - value - aself.min + 1)
                else:
                    aself._current = aself.min
            else:
                aself._current -= value
            return aself

    def __isub__(self, value: int) -> Self:
        if self.llimit:
            return self
        else:
            if self.over_llimit(value):
                if self._loopable:
                    self._current = self.max + (self._current - value - self.min + 1)
                else:
                    self._current = self.min
            else:
                self._current -= value
            return self

    def __index__(self) -> int:
        return self._current

    def over_ulimit(self, value: int) -> bool:
        return self.max < self._current + value

    def over_llimit(self, value: int) -> bool:
        return self.min > self._current - value

    def inc(self):
        self += 1

    def dec(self):
        self -= 1

    @property
    def ulimit(self) -> bool:
        return self._current == self.max and not self._loopable

    @property
    def llimit(self) -> bool:
        return self._current == self.min and not self._loopable


class Transition(tk.Frame):
    def __init__(self, master: tk.Misc | None = None, *arg, loop: bool = False, **kw) -> None:
        super().__init__(master, *arg, **kw)
        self._widgets: list[tk.Widget] = []
        self.current: Counter | None = None
        self._packing: tuple[tuple[Any, ...], dict[str, Any]] | None = None
        self._loop = loop

    def __getitem__(self, id: int):
        return self._widgets[id]

    def __add__(self, value: tk.Widget | Iterable[tk.Widget]):
        aself = deepcopy(self)
        aself.register_widget(value)
        return aself

    def __iadd__(self, value: tk.Widget | Iterable[tk.Widget]):
        self.register_widget(value)
        return self

    def register_widget(self, widget: tk.Widget | Iterable[tk.Widget], *, id: int | slice = AUTO):
        if isinstance(id, slice):
            if any(n >= len(self._widgets) for n in [id.start, id.stop]):
                raise IndexError('不正なID指定です。')
            else:
                item = [widget] if not isinstance(widget, Iterable) else widget
                self._widgets[id] = item
        elif id >= 0:
            if id >= len(self._widgets):
                raise IndexError('不正なID指定です。')
            elif isinstance(widget, Iterable):
                key = slice(id, id)
            else:
                key = id
            self._widgets[key] = widget
        else:
            self._widgets += widget if isinstance(widget, Iterable) else [widget]

    def prepack(self, *arg: Any, **kw: Any):
        self._packing = (arg, kw)

    def initial_pack(self, id: int = 0):
        if self._packing is None:
            raise ValueError('パックオプションが未設定です。\nprepackメソッドでパックオプションをあらかじめ設定してください。')
        self._widgets[id].pack(*self._packing[0], **self._packing[1])
        self.current = Counter(item=self._widgets, loopable=self._loop, start_count=id)

    def next(self):
        if self.current is None:
            self.current = Counter(item=self._widgets, loopable=self._loop)
        elif self.current.ulimit:
            return
        else:
            self._widgets[self.current].pack_forget()
            self.current.inc()
        self._widgets[self.current].pack(*self._packing[0], **self._packing[1])

    def prev(self):
        if self.current is None:
            self.current = Counter(item=self._widgets, loopable=self._loop)
        elif self.current.llimit:
            return
        else:
            self._widgets[self.current].pack_forget()
            self.current.dec()
        self._widgets[self.current].pack(*self._packing[0], **self._packing[1])


def sample(loop: bool = True, widget_number: int = 3):
    root = tk.Tk()
    root.geometry('250x250')
    trans = Transition(root, loop=loop)
    trans.pack(side=tk.TOP, anchor=tk.S, fill=tk.BOTH, expand=True)
    trans.prepack(fill=tk.BOTH, expand=True)

    for i in range(1, widget_number + 1):
        _tmp_ = tk.Frame(trans)
        tk.Label(_tmp_, text=f'LABEL{i}', font=font.Font(size=20)).pack(fill=tk.BOTH, expand=True)
        trans.register_widget(_tmp_)

    bf = tk.Frame(root)
    bf.pack(side=tk.TOP, anchor=tk.S, fill=tk.X, expand=True)
    tk.Button(bf, text='NEXT', command=trans.next).pack(side=tk.RIGHT, anchor=tk.E)
    tk.Button(bf, text='PREV', command=trans.prev).pack(side=tk.RIGHT, anchor=tk.E, padx=5)
    trans.initial_pack()
    root.mainloop()


if __name__ == '__main__':
    sample(widget_number=5)
