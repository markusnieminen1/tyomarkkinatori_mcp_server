from mcp_server.main import get_all_high_level_occupation_codes, OCCUPATIONS_HIGH_LEVEL_FILE
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
        


def test_reads_high_level_file():
    with patch("mcp_server.main.read_file_contents_tojson", return_value=occupation_codes) as mock_read:
        get_all_high_level_occupation_codes()
        mock_read.assert_called_once_with(OCCUPATIONS_HIGH_LEVEL_FILE)


def test_real_file_returns_single_digit_codes():
    # No mock: reads the real data file. High-level (major group) codes have one digit.
    result = get_all_high_level_occupation_codes()
    assert len(result) > 0
    assert all(len(item["code"]) == 1 for item in result)
