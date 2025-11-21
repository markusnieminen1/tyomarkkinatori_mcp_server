from mcp_server.main import get_all_high_level_occupation_codes
from unittest.mock import patch

occupation_codes = [
    {
        "code": "0",
        "preferredLabel": "Sotilaat"
    },
    {
        "code": "1",
        "preferredLabel": "Upseerit"
    },
    {
        "code": "2",
        "preferredLabel": "Aliupseerit"
    }
]

def test_basic_out():
    with patch("mcp_server.main.read_file_contents_tojson", return_value=occupation_codes):
        result = get_all_high_level_occupation_codes()
        assert type(result) == list

def test_basic():
    with patch("mcp_server.main.read_file_contents_tojson", return_value=occupation_codes):
        result = get_all_high_level_occupation_codes()
        assert type(result[0]) == dict
        
