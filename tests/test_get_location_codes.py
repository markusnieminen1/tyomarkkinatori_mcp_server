from unittest.mock import patch
from mcp_server.main import get_location_codes
import pytest 

mock_data = [
    {"classificationName": "Helsinki", "code": 1},
    {"classificationName": "Tampere", "code": 2},
    {"classificationName": "Turku", "code": 3},
    {"classificationName": "Äänekoski", "code": 4},
]

def test_get_location_codes_basic():
    with patch("mcp_server.main.read_file_contents_tojson", return_value=mock_data):
        result = get_location_codes("Ää")
        assert result == [{"classificationName": "Äänekoski", "code": 4}]

def test_get_location_codes_case_insensitive():
    with patch("mcp_server.main.read_file_contents_tojson", return_value=mock_data):
        result = get_location_codes("hEls")
        assert result == [{"classificationName": "Helsinki", "code": 1}]

def test_get_location_codes_no_match():
    with patch("mcp_server.main.read_file_contents_tojson", return_value=mock_data):
        result = get_location_codes("X")
        assert result == []

def test_get_location_codes_empty_input():
    with patch("mcp_server.main.read_file_contents_tojson", return_value=mock_data):
        result = get_location_codes("")
        assert result == []
    
def test_get_location_codes_str_int_input():
    with patch("mcp_server.main.read_file_contents_tojson", return_value=mock_data):
        result = get_location_codes("1")
        assert result == []

def test_get_location_codes_int_input():
    with patch("mcp_server.main.read_file_contents_tojson", return_value=mock_data):
        result = get_location_codes(1)
        assert result["isError"] == True
        
def test_get_location_codes_bool_input():
    with patch("mcp_server.main.read_file_contents_tojson", return_value=mock_data):
        result = get_location_codes(True)
        assert result["isError"] == True
