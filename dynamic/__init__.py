from typing import Any, ItemsView, Iterator, KeysView, Union, ValuesView

ValueTypes = Union[bool, int, float, str, list, dict, None]


class _noop:  # pylint: disable=C0115,C0116 ; coverage: disable
    def __init__(self):
        pass

    def resolve(self):
        return self

    def __getattr__(self, _):
        return self

    def __setattr__(self, _n, _v):
        pass


NoOp = _noop()


class ImmutabilityError(Exception):
    """
    An `ImmutabilityError` is raised by dynamics when a user tries to set an
    attribute. Dynamics are immutable.
    """

    pass


class Dynamic:
    """
    Dynamics are wrappers around basic data structures. They are used to quickly
    dot-path your way through nested data, especially JSON:

        >>> from dynamic import Dynamic
        >>> json = Dynamic({"first": {"second": {"third": "value"}}})
        >>> print(json.first.second.third.resolve())
        value

    They also implement wrappers around iterating lists and dicts, as well as testing
    for membership:

        >>> from dynamic import Dynamic
        >>> json = Dynamic({"results": [{"name": "first"}, {"name": "second"}, {"name": "third"}]})
        >>> for item in json.results:
        ...     print(item.name.resolve())
        ...
        first
        second
        third
        >>> print(json.results[1].resolve())
        {'name': 'second'}

    Getting attributes of dynamics always returns a new dynamic. When you've reached
    the attribute that you want, you need to ".resolve()" that value:

        >>> from dynamic import Dynamic
        >>> json = Dynamic({"first": {"second": {"third": "value"}}})
        >>> print(json.first.second.third)
        <dynamic.Dynamic object at 0x101b2b9d0>
        >>> print(json.first.second.third.resolve())
        value

    Dynamics are also immutable: you cannot manipulate their internal data -- this is
    done so that the original structure is intact for repeated use:

        >>> from dynamic import Dynamic
        >>> json = Dynamic({"name": "vince"})
        >>> json.name = "Vince"
        Traceback (most recent call last):
        File ..., line ..., in ...
        File ..., line 62, in __setattr__
            raise ImmutabilityError(f"Dynamics are immutable: cannot set {name!r}")
        dynamic.ImmutabilityError: Dynamics are immutable: cannot set 'name'

        >>> del json.name
        Traceback (most recent call last):
        File ..., line ..., in ...
        File ..., line 65, in __delattr__
            raise ImmutabilityError(f"Dynamics are immutable: cannot delete {name!r}")
        dynamic.ImmutabilityError: Dynamics are immutable: cannot delete 'name'

    Args:
        - value (bool, int, float, str, list, dict, None): the data you want to wrap;
            most typically this is a parsed JSON response from an API request

    Exceptions:
        - ImmutabilityError: raised when you try to either set or delete an attribute
            of the dynamic

    Implements:
        - __iter__ and __next__ for iteration; i.e. `for item in json.results: ...`
        - __contains__ for testing item membership; i.e. `if "awesome" in json.tags: ...`
        - items for iterating dictionary key-value pairs; i.e. `for k, v in json.items(): ...`
        - keys for iterating dictionary keys; i.e. `for key in json.keys(): ...`
        - values for iterating dictionary values; i.e. `for value in json.values(): ...`
    """

    value: ValueTypes
    i: int
    length: int
    iterable: list

    def __init__(self, value: ValueTypes) -> None:
        object.__setattr__(self, "value", value)

    def resolve(self) -> ValueTypes:
        """
        Returns the innder data value for the dynamic. This is used at the end
        of a call chain so that the expected value is returned instead of another
        dynamic object.

        Example:

            >>> from dynamic import Dynamic
            >>> json = Dynamic({"first": {"second": {"third": "value"}}})
            >>> print(json.first.second.third)
            <dynamic.Dynamic object at 0x101b2b9d0>
            >>> print(json.first.second.third.resolve())
            value
        """
        return self.value

    def __setattr__(self, name: str, _: Any) -> None:
        raise ImmutabilityError(f"Dynamics are immutable: cannot set {name!r}")

    def __delattr__(self, name: str) -> None:
        raise ImmutabilityError(f"Dynamics are immutable: cannot delete {name!r}")

    def __getattr__(self, name: str) -> Union["Dynamic", _noop]:
        if isinstance(self.value, dict) and name in self.value:
            return Dynamic(self.value[name])
        return NoOp

    def __getitem__(self, index: int) -> Union["Dynamic", _noop]:
        if isinstance(self.value, list) and index < len(self.value):
            return Dynamic(self.value[index])
        return NoOp

    def __iter__(self) -> Iterator[Any]:  # pylint: disable=W0201
        if self.value is None or isinstance(self.value, (bool, int, float)):
            object.__setattr__(self, "i", 1)
            object.__setattr__(self, "length", 0)
        else:
            object.__setattr__(self, "i", 0)
            object.__setattr__(self, "length", len(self.value))
            object.__setattr__(self, "iterable", list(iter(self.value)))

        return self

    def __next__(self) -> "Dynamic":
        if self.i >= self.length:
            raise StopIteration

        value = Dynamic(self.iterable[self.i])
        object.__setattr__(self, "i", self.i + 1)
        return value

    def __contains__(self, value: Any) -> bool:
        if self.value is None or isinstance(self.value, (bool, int, float)):
            return False

        return value in self.value

    def items(self) -> ItemsView:  # pylint: disable=C0116
        if isinstance(self.value, dict):
            return self.value.items()
        return {}.items()

    def keys(self) -> KeysView:  # pylint: disable=C0116
        if isinstance(self.value, dict):
            return self.value.keys()
        return {}.keys()

    def values(self) -> ValuesView:  # pylint: disable=C0116
        if isinstance(self.value, dict):
            return self.value.values()
        return {}.values()
