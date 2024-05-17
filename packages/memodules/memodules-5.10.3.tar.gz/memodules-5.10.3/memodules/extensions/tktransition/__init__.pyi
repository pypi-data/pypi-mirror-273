import tkinter as tk
from typing import Any, Callable, Iterable, Literal, Self
from typing_extensions import override
AUTO = -1

type ScreenUnits = str | float
type Cursor = str | tuple[str] | tuple[str, str] | tuple[str, str, str] | tuple[str, str, str, str]
type Relief = Literal["raised", "sunken", "flat", "ridge", "solid", "groove"]
type TakeFocusValue = bool | Literal[0, 1, ""] | Callable[[str], bool | None]
def signeture[**Arg, Ret](f: Callable[Arg, Any]) -> Callable[[Callable[..., Ret]], Callable[Arg, Ret]]: ...

class Transition(tk.Frame):
    def __init__(self,
                 master: tk.Misc | None = None,
                 cnf: dict[str, Any] | None = {},
                 *,
                 loop: bool = False,
                 background: str = ...,
                 bd: ScreenUnits = 0,
                 bg: str = ...,
                 border: ScreenUnits = 0,
                 borderwidth: ScreenUnits = 0,
                 class_: str = "Frame",
                 colormap: tk.Misc | Literal['new', ''] = "",
                 container: bool = False,
                 cursor: Cursor = "",
                 height: ScreenUnits = 0,
                 highlightbackground: str = ...,
                 highlightcolor: str = ...,
                 highlightthickness: ScreenUnits = 0,
                 name: str = ...,
                 padx: ScreenUnits = 0,
                 pady: ScreenUnits = 0,
                 relief: Relief = "flat",
                 takefocus: TakeFocusValue = 0,
                 visual: str | tuple[str, int] = "",
                 width: ScreenUnits = 0) -> None: ...

    @override
    def __getitem__(self, id: int) -> tk.Widget: ...
    def __add__(self, value: tk.Widget | Iterable[tk.Widget]) -> Transition: ...
    def __iadd__(self, value: tk.Widget | Iterable[tk.Widget]) -> Self: ...
    def register_widget(self, widget: tk.Widget | Iterable[tk.Widget], *, id: int | slice = AUTO) -> None:
        """遷移するためのウィジェット登録メソッド
        idは__getitem__で取得できるようにするためだけの識別子
        既存のidを指定してregisterした場合は上書き。存在しないidを指定してregisterした場合はIndexError。
        .next(), .prev()の表示順は登録順"""
        ...
    @signeture(tk.Widget.pack)
    def prepack(self, *arg: Any, **kw: Any) -> None:
        """.next(), .prev()でパックするときのオプションをあらかじめセットしておくやつ"""
        ...
    def initial_pack(self, id: int = 0) -> None:
        "prepack()で指定したオプションに従って、引数で指定したidのウィジェットをあらかじめ配置してくれる"
        ...
    type isLastPage = bool
    def next(self) -> isLastPage:
        """今配置されてるウィジェットの次のIDのウィジェットを配置する
        loop = Falseのとき、今配置されてるウィジェットIDより後ろが無い場合return True
        それ以外はreturn False"""
        ...
    type isFirstPage = bool
    def prev(self) -> isFirstPage:
        """今配置されてるウィジェットの前のIDのウィジェットを配置する
        loop = Falseのとき、今配置されているウィジェットIDより前が無い場合return True
        それ以外はreturn False"""
        ...

def sample(loop: bool = True, widget_number: int = 3) -> None:
    """~~~markdown

    __Transition__ クラスがどんな感じに使えるかを見るサンプル
    以下関数内コード
    ======================================================
    ~~~

    ~~~python
    root = tk.Tk()
    root.geometry('250x250')
    trans = Transition(root, loop=loop)
    trans.pack(side=tk.TOP, anchor=tk.S, fill=tk.BOTH, expand=True)
    trans.prepack(fill=tk.BOTH, expand=True)

    for i in range(1, widget_number + 1):
        _tmp_ = tk.Frame(trans)
        tk.Label(_tmp_, text=f'LABEL{i}', font=font.Font(size=20)).pack(fill=tk.BOTH, expand=True)
        trans += _tmp_

    bf = tk.Frame(root)
    bf.pack(side=tk.TOP, anchor=tk.S, fill=tk.X, expand=True)
    tk.Button(bf, text='NEXT', command=trans.next).pack(side=tk.RIGHT, anchor=tk.E)
    tk.Button(bf, text='PREV', command=trans.prev).pack(side=tk.RIGHT, anchor=tk.E, padx=5)
    trans.initial_pack()
    root.mainloop()"""
