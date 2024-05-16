import pytest
from unittest.mock import patch
from src.db.database_instance import SessionManager
from src.runner import UpdateRunner

@patch('src.db.database_instance.DatabaseInstance')
@patch('src.runner.update_runner.UpdateRunner._load_yaml')
@patch('src.runner.update_runner.UpdateRunner._check_table_exists')
def test_process_yaml(mock_check_table_exists, mock_load_yaml, mock_database_instance):
    mock_check_table_exists.return_value = True
    mock_load_yaml.return_value = {
        "deploy": [
            {
                "table": "test_table",
                "action": "insert",
                "columns": ["id"],
                "data": [
                    {
                        "id": 1
                    }
                ]
            }
        ]
    }

    update_runner = UpdateRunner(mock_database_instance)
    update_runner.process_yaml("test_file.yaml")

    assert mock_check_table_exists.called
    assert mock_load_yaml.called
    assert update_runner.yaml_data == {
        "deploy": [
            {
                "table": "test_table",
                "action": "insert",
                "columns": ["id"],
                "data": [
                    {
                        "id": 1
                    }
                ]
            }
        ]
    }
    assert update_runner.was_table_updated == True

@patch('src.runner.update_runner.UpdateRunner._load_yaml')
@patch('src.runner.update_runner.UpdateRunner._check_table_exists')
def test_process_yaml_invalid_table_name(mock_check_table_exists, mock_load_yaml):
    mock_check_table_exists.return_value = False
    mock_load_yaml.return_value = {
        "deploy": [
            {
                "table": "test_table",
                "columns": ["id"]
            }
        ]
    }

    update_runner = UpdateRunner(None)
    update_runner.process_yaml("test_file.yaml")

    assert mock_check_table_exists.called
    assert mock_load_yaml.called
    assert update_runner.yaml_data == {
        "deploy": [
            {
                "table": "test_table",
                "columns": ["id"]
            }
        ]
    }
    assert update_runner.was_table_updated == False