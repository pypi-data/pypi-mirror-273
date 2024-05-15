import pytest
from antimatter.capabilities import CapabilityConverter

@pytest.mark.parametrize(
    "capabilities,expected,error_expected",
    [
        # Test with empty capabilities
        ([], {}, False),
        # Test with capabilities as a list of dictionaries containing name, value pairs
        ([{"name": "capability1", "value": "value1"}], {"capability1": "value1"}, False),
        # Test with capabilities as a list of dictionaries containing key:value pairs
        ([{"capability1": "value1"}], {"capability1": "value1"}, False),
        # Test with capabilities as a list of strings containing equal signs
        (["capability1=value1"], {"capability1": "value1"}, False),
        # Test with capabilities as a list of strings containing unary keys
        (["capability1"], {"capability1": None}, False),
        # Test with mixed capabilities
        (
            [{"name": "capability1", "value": "value1"}, "capability2=value2", "capability3"],
            {"capability1": "value1", "capability2": "value2", "capability3": None}, False
        ),
        # Test with capabilities as a list of dictionaries
        ([{"name": "capability1", "value": "value1"}, {"name": "capability2", "value": "value2"}], {"capability1": "value1", "capability2": "value2"}, False),
        # Test with capabilities as a list of strings with "="
        (["capability1=value1", "capability2=value2"], {"capability1": "value1", "capability2": "value2"}, False),
        # Test with capabilities as a list of strings without "="
        (["capability1", "capability2"], {"capability1": None, "capability2": None}, False),
        # Test with capabilities as a list of strings with multiple "="
        (["capability1=value1=value2"], {"capability1": "value1=value2"}, False),
        # Invalid test case, list of dicts with name, value pairs but name is missing, or misspelled
        ([{"value": "value1"}, {"name": "capability2", "value": "value2"}, {"name": "capability"}, {"name"}, {"name": "capability4", "values": "value"}], {}, True),
        # Invalid case, set
        ([{"capability1"}], {}, True),
        # Invalid case, dict with no value
        ([{"name": "capability1"}], {}, True),
        # Valid case, integer value
        ([{"name": "capability1", "value": 123}], {"capability1": '123'}, False),
        # Invalid case, tuples
        ([("name", "value"), ("name2", 4)], {}, True),
        # Add unary capability with None as dict value
        ([{"name": "capability1", "value": None}, {"capability2": None}], {"capability1": None, "capability2": None}, False),
    ],
    ids=[
        "empty",
        "dict containing name, value pairs",
        "dict containing key:value pairs",
        "str containing unary key",
        "str_no_value",
        "mixed",
        "list of dicts with name, value pairs",
        "list of str with =",
        "list of str without =",
        "str with multiple =",
        "list of dicts with name, value pairs missing name or misspelled",
        "set",
        "dict with no value",
        "int value",
        "tuples",
        "unary capability with None as dict value",
    ],
)
def test_convert_capabilities(capabilities, expected, error_expected):
    if error_expected:
        with pytest.raises(ValueError):
            CapabilityConverter.convert_capabilities(capabilities)
    else:
        assert CapabilityConverter.convert_capabilities(capabilities) == expected

