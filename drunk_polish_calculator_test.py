import pytest

from drunk_polish_calculator import op_plus, op_minus, op_divide, op_multiply, main


# test plus
def test_op_plus():
    # given
    x = 4
    y = 3
    expected_result = 7

    # when
    result = op_plus(x, y)

    # then
    assert result == expected_result


# test minus
def test_op_minus():
    # given
    x = 2
    y = 10
    expected_result = 8

    # when
    result = op_minus(x, y)

    # then
    assert result == expected_result


# test divide
def test_op_divide(): # revised and correct
    # given
    x = 2
    y = 10
    expected_result = 5

    # when
    result = op_divide(x, y)

    # then
    assert result == expected_result


# test op_multiply
def test_op_multiply():
    # given
    x = 7
    y = 5
    expected_result = 35

    # when
    result = op_multiply(x, y)

    # then
    assert result == expected_result


# test main

# revised and correct

@pytest.mark.parametrize("input_string, expected_output", [
    ("2 4 + 3", "6.0\n"),
    ("2 7 + 3 -", "6.0\n"),
    ("2 4 + 3 - 5 *", "15.0\n"),
    ("2 4 + 3 - 5 * 3 /", "3.0\n")
])

def test_main(monkeypatch, capsys, input_string, expected_output):
    # given
    monkeypatch.setattr("builtins.input", lambda _: input_string)
    # when
    main()
    # then
    captured = capsys.readouterr().out
    assert captured == expected_output