# Dynamic

TIL C# actually has something I don't think is pointless ceremony

## Usage

Dynamics are wrappers around basic data structures. They are used to quickly dot-path your way through nested data, especially JSON:

```python
from dynamic import Dynamic
json = Dynamic({"first": {"second": {"third": "value"}}})
print(json.first.second.third.resolve())
# value
```

They also implement wrappers around iterating lists and dicts, as well as testing for membership:

```python
from dynamic import Dynamic
json = Dynamic({"results": [{"name": "first"}, {"name": "second"}, {"name": "third"}]})
for item in json.results:
    print(item.name.resolve())
# first
# second
# third

print(json.results[1].resolve())
# {'name': 'second'}
```

Getting attributes of dynamics always returns a new dynamic. When you've reached the attribute that you want, you need to `.resolve()` that value:

```python
from dynamic import Dynamic
json = Dynamic({"first": {"second": {"third": "value"}}})
print(json.first.second.third)
# <dynamic.Dynamic object at 0x101b2b9d0>

print(json.first.second.third.resolve())
# value
```

Dynamics are also immutable: you cannot manipulate their internal data -- this is done so that the original structure is intact for repeated use:

```python
from dynamic import Dynamic
json = Dynamic({"name": "vince"})
json.name = "Vince"
# Traceback (most recent call last):
# File ..., line ..., in ...
# File ..., line 62, in __setattr__
#     raise ImmutabilityError(f"Dynamics are immutable: cannot set {name!r}")
# dynamic.ImmutabilityError: Dynamics are immutable: cannot set 'name'

del json.name
# Traceback (most recent call last):
# File ..., line ..., in ...
# File ..., line 65, in __delattr__
#     raise ImmutabilityError(f"Dynamics are immutable: cannot delete {name!r}")
# dynamic.ImmutabilityError: Dynamics are immutable: cannot delete 'name'
```
