from rich.prompt import Confirm, IntPrompt, Prompt

from kanban_python import interface


def test_input_ask_for_action(monkeypatch):
    monkeypatch.setattr(IntPrompt, "ask", lambda *args, **kwargs: 1)
    result = interface.input_ask_for_action()
    assert result == 1


def test_input_confirm_set_board_active(monkeypatch) -> bool:
    monkeypatch.setattr(Confirm, "ask", lambda *args, **kwargs: False)
    result = interface.input_confirm_set_board_active("Testboard")
    assert result is False


def test_input_ask_for_new_board_name(monkeypatch):
    monkeypatch.setattr(Prompt, "ask", lambda *args, **kwargs: "Test")
    result = interface.input_ask_for_new_board_name()
    assert result == "Test"


def test_input_confirm_delete_board(monkeypatch):
    monkeypatch.setattr(Confirm, "ask", lambda *args, **kwargs: False)
    result = interface.input_confirm_delete_board("Testboard")
    assert result is False

    monkeypatch.setattr(Confirm, "ask", lambda *args, **kwargs: True)
    result = interface.input_confirm_delete_board("Testboard")
    assert result is True


def test_input_confirm_show_all_todos(monkeypatch):
    monkeypatch.setattr(Confirm, "ask", lambda *args, **kwargs: False)
    result = interface.input_confirm_show_all_todos()
    assert result is False
