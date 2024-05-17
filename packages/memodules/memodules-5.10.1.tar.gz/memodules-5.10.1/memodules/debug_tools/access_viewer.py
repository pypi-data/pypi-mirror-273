from typing import Any, ParamSpec, Self, TextIO, Callable, TypeVar
import sys

__all__ = [
    "AccessObserver",
    "StdIOTestSpace",
    "CallFollowerMeta",
]


class AccessObserver:
    def __init__(self, name: str, target_object: object, o_out: TextIO = sys.stdout, chain_observe: bool = True) -> None:
        self.name = name
        self.target = target_object
        self.stdout = o_out
        self.chain = chain_observe

    def __getattr__(self, name: str):
        if self.chain:
            def args_viewer(*args: Any, **kwargs: Any):
                result = None
                if name == 'fileno':
                    result = 0
                elif name == 'readline':
                    result = 'test line'
                print(f'{self.name}\nAccessName: {name}\nArgs: {args}\nKwArgs: {kwargs}', file=self.stdout)
                result = self if result is None else result
                return result
            return args_viewer
        else:
            print(f'AccessName: {name}')
            return getattr(self.target, name)


class StdIOTestSpace:
    def __enter__(self) -> Self:
        self.o_in = sys.stdin
        self.o_out = sys.stdout
        self.o_err = sys.stderr
        sys.stdin = AccessObserver('sys.stdin', self.o_out)
        sys.stdout = AccessObserver('sys.stdout', self.o_out)
        sys.stderr = AccessObserver('sys.stderr', self.o_out)
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        sys.stdin = self.o_in
        sys.stdout = self.o_out
        sys.stderr = self.o_err
        return False


_P = ParamSpec('_P')
_R = TypeVar('_R')


def printer(func: Callable[_P, _R]) -> Callable[_P, _R]:
    def wrapper(*arg: _P.args, **kw: _P.kwargs) -> _R:
        try:
            print(f'CALL: {func.__qualname__}')
        except AttributeError:
            print(f'CALL: Unknown.{func.__name__}')
        return func(*arg, **kw)
    return wrapper


def wrapping_machine(dic: dict[str, Any]) -> dict[str, Any]:
    for k, v in object.__dict__.items():
        if k not in dic and v is not object.__new__:
            dic[k] = v
    for k, v in dic.items():
        dic[k] = printer(v) if callable(v) else v
    return dic


class CallFollowerMeta(type):
    """Usage:
```python
class MyClass(metaclass=CallFollowerMeta):
    def __init__(self, value):
        self.value = value

instance = MyClass('string')
# CALL: MyClass.__init__
# CALL: object.__setattr__
print(instance)
# CALL: object.__str__
# CALL: object.__repr__
```"""
    def __new__(cls, name: str, bases: tuple[type, ...], dic: dict[str, Any]):
        return super().__new__(cls, name, bases, wrapping_machine(dic))
