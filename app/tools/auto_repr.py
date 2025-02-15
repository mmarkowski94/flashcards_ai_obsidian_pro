import inspect
from types import MappingProxyType
from typing import Any, TypeVar

T = TypeVar("T", bound=type[Any])


def auto_repr(cls: T) -> T:
    members: MappingProxyType[str, Any] = vars(cls)

    if "__repr__" in members:
        raise TypeError(f"{cls.__name__} already has __repr__ method.")

    if "__init__" not in members:
        raise TypeError(f"{cls.__name__} does not override __init__ method.")

    signature: inspect.Signature = inspect.signature(cls.__init__)
    parameter_names: list[str] = list(signature.parameters)[1:]

    # TODO check object members
    if not all(members.get(name, None) for name in parameter_names):
        raise TypeError(
            f"Cannot apply auto_repr to {cls.__name__} because not all__init__ parameters have matching properties."
        )

    def synthesized_repr(self: T) -> str:
        return "{type_class}({args})".format(
            type_class=type(self).__name__,
            args=", ".join(f"{name}={getattr(self, name)!r}" for name in parameter_names),
        )

    setattr(cls, "__repr__", synthesized_repr)

    return cls
