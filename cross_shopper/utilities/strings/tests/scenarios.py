"""Scenarios for for the utilities app string functions."""

import pytest

title_string_scenarios = pytest.mark.parametrize(
    "input_string, expected_string",
    [
        ("quick brown fox", "Quick Brown Fox"),
        (" quick brown fox", " Quick Brown Fox"),
        ("the quick brown fox", "The Quick Brown Fox"),
        ("jumps over a lazy dog", "Jumps Over a Lazy Dog"),
        ("an iPhone is a device", "An IPhone Is a Device"),
        ("...the end", "...The End"),
        ("isn't it lovely", "Isn't It Lovely"),
        ("", ""),
        ("a an the", "A an the"),
        ("mother-in-law's house", "Mother-In-Law's House"),
    ],
)
