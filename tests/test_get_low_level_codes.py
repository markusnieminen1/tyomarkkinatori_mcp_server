from unittest.mock import patch
from mcp_server.main import get_low_level_occupation_codes
import pytest 

mock_data = [
    {
        "code": "111",
        "preferredLabel": "Upseerit"
    },
    {
        "code": "211",
        "preferredLabel": "Aliupseerit"
    },
    {
        "code": "311",
        "preferredLabel": "Sotilasammattihenkilöstö"
    }
]

def test_get_low_level_occupation_str():
    with patch("mcp_server.main.read_file_contents_tojson", return_value=mock_data):
        with pytest.raises(ValueError):
            get_low_level_occupation_codes("abc")

def test_get_lowlevel_occupation_int_str():
    with patch("mcp_server.main.read_file_contents_tojson", return_value=mock_data):
        result = get_low_level_occupation_codes("21")
        assert result == [{"code": "211", "preferredLabel": "Aliupseerit"}]

def test_get_low_level_occupation_int():
    with patch("mcp_server.main.read_file_contents_tojson", return_value=mock_data):
        result = get_low_level_occupation_codes(11)
        assert result == [{"code": "111", "preferredLabel": "Upseerit"}]
        
def test_get_low_level_occupation_value_not_found():
    with patch("mcp_server.main.read_file_contents_tojson", return_value=mock_data):
        result = get_low_level_occupation_codes(22)
        assert result == []
        
def test_get_low_level_occupation_large_input():
    with patch("mcp_server.main.read_file_contents_tojson", return_value=mock_data):
        with pytest.raises(ValueError):
            get_low_level_occupation_codes(120)