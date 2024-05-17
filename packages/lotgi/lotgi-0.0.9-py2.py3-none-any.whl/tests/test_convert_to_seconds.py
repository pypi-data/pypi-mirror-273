"""
Written by our favorite chat bot.
"""

# The test functions (save as test_convert_to_seconds.py)
import pytest
import lotgi.convert_to_seconds
from lotgi.convert_to_seconds import convert_to_seconds

def test_full_format():
    assert convert_to_seconds("1d10h3m2s") == 122582

def test_only_days():
    assert convert_to_seconds("1d") == 86400

def test_only_hours():
    assert convert_to_seconds("10h") == 36000

def test_only_minutes():
    assert convert_to_seconds("3m") == 180

def test_only_seconds():
    assert convert_to_seconds("2s") == 2

def test_days_and_hours():
    assert convert_to_seconds("1d10h") == 122400

def test_hours_and_minutes():
    assert convert_to_seconds("10h3m") == 36180

def test_minutes_and_seconds():
    assert convert_to_seconds("3m2s") == 182

def test_empty_string():
    with pytest.raises(ValueError):
        convert_to_seconds("")

def test_invalid_format():
    with pytest.raises(ValueError):
        convert_to_seconds("10x5y")
