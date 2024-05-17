"Event constants for tkinter.ttk"
from dataclasses import dataclass
from typing import Literal

__all__ = [
    'Combobox',
]


@dataclass(frozen=True)
class ComboboxWidget:
    ChangeValueByList: Literal['<<ComboboxSelected>>'] = '<<ComboboxSelected>>'
    "An event when a value is changed from the dropdown list."
    ItemSelected: Literal['<<ComboboxSelected>>'] = '<<ComboboxSelected>>'
    "An event when a value is changed from the dropdown list."
    SelectionChange: Literal['<<ComboboxSelected>>'] = '<<ComboboxSelected>>'
    "An event when a value is changed from the dropdown list."


Combobox = ComboboxWidget()
