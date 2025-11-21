import json
import pytest
from mcp_server.main import read_file_contents_tojson

def test_read_file_basic(tmp_path):
    data = [
    {
        "code": "20",
        "classificationName": "Akaa"
    },
    {
        "code": "9",
        "classificationName": "Alavieska"
    }
    ]
    
    file_path = tmp_path / "cities.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    result = read_file_contents_tojson(file_path)

    assert result == data


def test_read_file_empty_list(tmp_path):
    file_path = tmp_path / "empty.json"
    file_path.write_text(json.dumps([]), encoding="utf-8")

    result = read_file_contents_tojson(file_path)

    assert result == []


def test_read_file_invalid_json(tmp_path):
    file_path = tmp_path / "invalid.json"
    file_path.write_text("not a json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        read_file_contents_tojson(file_path)


def test_read_file_not_exist(tmp_path):
    file_path = tmp_path / "does_not_exist.json"

    with pytest.raises(FileNotFoundError):
        read_file_contents_tojson(file_path)
