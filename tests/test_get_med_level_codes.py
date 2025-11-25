from unittest.mock import patch
from mcp_server.main import get_medium_level_occupation_codes

mock_data = [
    {
        "code": "11",
        "preferredLabel": "Upseerit"
    },
    {
        "code": "21",
        "preferredLabel": "Aliupseerit"
    },
    {
        "code": "31",
        "preferredLabel": "Sotilasammattihenkilöstö"
    }
]

def test_get_medium_level_occupation_str():
    with patch("mcp_server.main.read_file_contents_tojson", return_value=mock_data):
        result = get_medium_level_occupation_codes("sf")
        assert result["isError"] == True

def test_get_medium_level_occupation_int_str():
    with patch("mcp_server.main.read_file_contents_tojson", return_value=mock_data):
        result = get_medium_level_occupation_codes("2")
        assert result == [{"code": "21", "preferredLabel": "Aliupseerit"}]

def test_get_medium_level_occupation_int():
    with patch("mcp_server.main.read_file_contents_tojson", return_value=mock_data):
        result = get_medium_level_occupation_codes(2)
        assert result == [{"code": "21", "preferredLabel": "Aliupseerit"}]
        
def test_get_medium_level_occupation_value_not_found():
    with patch("mcp_server.main.read_file_contents_tojson", return_value=mock_data):
        result = get_medium_level_occupation_codes(4)
        assert result == []
        
def test_get_medium_level_occupation_large_input():
    with patch("mcp_server.main.read_file_contents_tojson", return_value=mock_data):
        result = get_medium_level_occupation_codes(150)
        assert result["isError"] == True