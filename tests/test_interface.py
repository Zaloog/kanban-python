from kanban_python import interface


def test_input_ask_for_action():
    pass


def test_input_confirm_delete_board(mock_confirm):
    mock_confirm.append(True)
    result = interface.input_confirm_delete_board("TestBoard")
    assert result is True

    mock_confirm.append(False)
    result = interface.input_confirm_delete_board("TestBoard")
    assert result is False
