# cspell:ignore mkey, mfour
"""Test the tree generator."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pip4a.tree import Tree


if TYPE_CHECKING:
    import pytest

    from pip4a.tree import JSONVal


sample: JSONVal = {
    "key_one": "one",
    "key_two": 42,
    "key_three": True,
    "key_four": None,
    "key_five": ["one", "two", "three"],
    "key_six": {
        "key_one": "one",
        "key_two": 42,
        "key_three": True,
        "key_four": None,
        "key_five": ["one", "two", "three"],
        "key_six": {
            "key_one": "one",
            "key_two": 42,
            "key_three": True,
            "key_four": None,
            "key_five": ["one", "two", "three"],
            "key_six": {
                "key_one": "one",
                "key_two": 42,
                "key_three": True,
                "key_four": None,
                "key_five": ["one", "two", "three"],
            },
        },
    },
}

result = """key_one
└──one
key_two
└──42
key_three
└──True
key_four
└──None
key_five
├──one
├──two
└──three
key_six
├──key_one
│  └──one
├──key_two
│  └──42
├──key_three
│  └──True
├──key_four
│  └──None
├──key_five
│  ├──one
│  ├──two
│  └──three
└──key_six
   ├──key_one
   │  └──one
   ├──key_two
   │  └──42
   ├──key_three
   │  └──True
   ├──key_four
   │  └──None
   ├──key_five
   │  ├──one
   │  ├──two
   │  └──three
   └──key_six
      ├──key_one
      │  └──one
      ├──key_two
      │  └──42
      ├──key_three
      │  └──True
      ├──key_four
      │  └──None
      └──key_five
         ├──one
         ├──two
         └──three
"""


def test_tree_large(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the tree generator."""
    monkeypatch.setenv("NO_COLOR", "true")
    assert Tree(sample).render() == result


sample = {
    "key_one": True,
    "key_two": 42,
    "key_three": None,
    "key_four": "four",
    "key_five": [{"a": 1}, {"b": 2}],
}

expected = [
    "\x1b[34mkey_one\x1b[0m",
    "└──\x1b[32mTrue\x1b[0m",
    "\x1b[34mkey_two\x1b[0m",
    "└──\x1b[32m42\x1b[0m",
    "\x1b[34mkey_three\x1b[0m",
    "└──\x1b[32mNone\x1b[0m",
    "\x1b[34mkey_four\x1b[0m",
    "└──\x1b[32mfour\x1b[0m",
    "key_five\x1b[0m",
    "├──\x1b[3m0\x1b[0m\x1b[0m",
    "│  └──a\x1b[0m",
    "│     └──1\x1b[0m",
    "└──\x1b[3m1\x1b[0m\x1b[0m",
    "   └──b\x1b[0m",
    "      └──2\x1b[0m",
]


def test_tree_color() -> None:
    """Test the tree generator."""
    tree = Tree(sample)
    tree.blue = ["key_one", "key_two", "key_three", "key_four"]
    tree.green = [True, 42, None, "four"]
    rendered = tree.render().splitlines()
    assert rendered == expected
