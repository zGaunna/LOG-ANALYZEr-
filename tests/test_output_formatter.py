import json
from src.log_analyzer.output_formatter import format_table_output, format_json_output, format_jsonl_output, format_html_output

def test_format_table_output():
    error_messages = [
        ("test.log", 1, "ERROR: test message"),
        ("app.log", 5, "WARNING: something happened")
    ]
    output = format_table_output(error_messages)
    assert "test.log" in output
    assert "ERROR: test message" in output
    assert "app.log" in output
    assert "WARNING: something happened" in output
    # Test empty
    empty_output = format_table_output([])
    assert "ERROR veya WARNING mesajı bulunamadı." in empty_output

def test_format_json_output():
    error_messages = [
        ("test.log", 1, "ERROR: test message"),
        ("app.log", 5, "WARNING: something happened")
    ]
    output = format_json_output(error_messages)
    data = json.loads(output)
    assert len(data) == 2
    assert data[0]["file"] == "test.log"
    assert data[0]["line"] == 1
    assert data[0]["message"] == "ERROR: test message"
    assert data[1]["file"] == "app.log"
    assert data[1]["line"] == 5
    assert data[1]["message"] == "WARNING: something happened"

def test_format_jsonl_output():
    error_messages = [
        ("test.log", 1, "ERROR: test message"),
        ("app.log", 5, "WARNING: something happened")
    ]
    output = format_jsonl_output(error_messages)
    lines = output.strip().split('\n')
    assert len(lines) == 2
    data1 = json.loads(lines[0])
    data2 = json.loads(lines[1])
    assert data1["file"] == "test.log"
    assert data1["line"] == 1
    assert data1["message"] == "ERROR: test message"
    assert data2["file"] == "app.log"
    assert data2["line"] == 5
    assert data2["message"] == "WARNING: something happened"

def test_format_html_output():
    error_messages = [
        ("test.log", 1, "ERROR: test message"),
        ("app.log", 5, "WARNING: something happened")
    ]
    output = format_html_output(error_messages)
    assert "<table" in output
    assert "test.log" in output
    assert "ERROR: test message" in output
    assert "app.log" in output
    assert "WARNING: something happened" in output
    # Test empty
    empty_output = format_html_output([])
    assert "ERROR veya WARNING mesajı bulunamadı." in empty_output