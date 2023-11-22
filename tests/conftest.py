"""
    Dummy conftest.py for kanban_python.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import pytest

from kanban_python import config


@pytest.fixture
def start_time_str():
    return "2023-11-01 10:00:00"


@pytest.fixture
def end_time_str():
    return "2023-11-01 10:02:30"


@pytest.fixture
def test_task():
    return {
        "Title": "Welcome Task",
        "Description": "Welcome to kanban-python, I hope this helps your productivity",
        "Tag": "HI",
        "Status": "Ready",
        "Begin_Time": "",
        "Complete_Time": "",
        "Duration": "0",
        "Creation_Date": "",
    }


@pytest.fixture
def test_config_path(tmp_path):
    return tmp_path / ".kanban-python"


@pytest.fixture
def test_config_filepath(test_config_path):
    return test_config_path / "pykanban.ini"


@pytest.fixture
def test_config(test_config_path, test_config_filepath):
    config.create_init_config(test_config_path)

    cfg = config.KanbanConfig(path=test_config_filepath)
    return cfg


@pytest.fixture
def mock_confirm(monkeypatch):
    confirm_responses = []

    def mock_confirm_ask(message):
        response = confirm_responses.pop(0)
        return response

    monkeypatch.setattr("rich.prompt.Confirm.ask", mock_confirm_ask)

    return confirm_responses


@pytest.fixture
def mock_ask(monkeypatch):
    prompt_responses = []

    def mock_prompt_ask(message):
        response = prompt_responses.pop(0)
        return response

    monkeypatch.setattr("rich.prompt.Prompt.ask", mock_prompt_ask)

    return prompt_responses


@pytest.fixture
def mock_int_ask(monkeypatch):
    confirm_responses = []

    def mock_intprompt_ask(message, choices, show_choices):
        response = confirm_responses.pop(0)
        return response

    monkeypatch.setattr("rich.prompt.Intprompt.ask", mock_intprompt_ask)

    return confirm_responses
