# pylint: disable=C0116

import pytest

from dynamic import Dynamic, ImmutabilityError, NoOp


def describe_dotting_through_dicts():
    json = Dynamic({
        "results": {
            "name": {
                "en": "One",
                "es": "Uno",
                "fr": "Une",
            }
        }
    })

    def test_good_path():  # pylint: disable=W0612
        assert json.results.name.en.resolve() == "One"

    def test_bad_path():  # pylint: disable=W0612
        assert json.foo.bar.baz.resolve() == NoOp


def describe_dynamics_are_immutable():
    json = Dynamic({"name": "vince"})

    def test_setattr():  # pylint: disable=W0612
        with pytest.raises(ImmutabilityError):
            json.age = 35

    def test_delattr():  # pylint: disable=W0612
        with pytest.raises(ImmutabilityError):
            del json.name


def describe_iterating_list():
    json = Dynamic([
        {"name": "vince"},
    ])

    def test_good_list_path():  # pylint: disable=W0612
        assert json[0].name.resolve() == "vince"

    def test_index_error():  # pylint: disable=W0612
        assert json[99].resolve() == NoOp

    def test_not_a_list():  # pylint: disable=W0612
        j = Dynamic({"foo": "bar"})
        assert j[0].resolve() == NoOp


def describe_iterating():
    def test_list():  # pylint: disable=W0612
        json = Dynamic([
            {"name": "vince"},
            {"name": "hana"},
            {"name": "leo"},
        ])
        for item in json:
            assert "name" in item

    def test_dict():  # pylint: disable=W0612
        json = Dynamic({"name": "vince"})
        items = [x.resolve() for x in json]
        assert items == ["name"]

    def test_str():  # pylint: disable=W0612
        json = Dynamic("abc")
        items = [x.resolve() for x in json]
        assert items == ["a", "b", "c"]

    def test_int():  # pylint: disable=W0612
        json = Dynamic(1)
        items = [x.resolve() for x in json]
        assert items == []


def describe_in():
    def test_list():  # pylint: disable=W0612
        json = Dynamic(["a", "b"])
        assert "a" in json

    def test_dict():  # pylint: disable=W0612
        json = Dynamic({"name": "vince"})
        assert "name" in json

    def test_str():  # pylint: disable=W0612
        json = Dynamic("abc")
        assert "a" in json

    def test_int():  # pylint: disable=W0612
        json = Dynamic(1)
        assert "a" not in json


def describe_items():
    def test_dict():  # pylint: disable=W0612
        json = Dynamic({"one": "uno", "two": "dos"})
        assert len(json.items()) == 2

    def test_not_dict():  # pylint: disable=W0612
        json = Dynamic(["one", "two"])
        assert len(json.items()) == 0


def describe_keys():
    def test_dict():  # pylint: disable=W0612
        json = Dynamic({"one": "uno", "two": "dos"})
        assert len(json.keys()) == 2

    def test_not_dict():  # pylint: disable=W0612
        json = Dynamic(["one", "two"])
        assert len(json.keys()) == 0


def describe_values():
    def test_dict():  # pylint: disable=W0612
        json = Dynamic({"one": "uno", "two": "dos"})
        assert len(json.values()) == 2

    def test_not_dict():  # pylint: disable=W0612
        json = Dynamic(["one", "two"])
        assert len(json.values()) == 0
