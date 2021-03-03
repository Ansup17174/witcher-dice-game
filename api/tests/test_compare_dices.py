from ..utils import compare_dices


def test_compare_pokers():
    pattern = 8
    assert compare_dices([1, 1, 1, 1, 1], [2, 2, 2, 2, 2], pattern) == 1
    assert compare_dices([2, 2, 2, 2, 2], [1, 1, 1, 1, 1], pattern) == 0
    assert compare_dices([1, 1, 1, 1, 1], [1, 1, 1, 1, 1], pattern) == -1


def test_compare_karety():
    pattern = 7
    assert compare_dices([1, 1, 1, 1, 4], [4, 4, 4, 4, 1], pattern) == 1
    assert compare_dices([6, 6, 6, 6, 1], [6, 6, 6, 6, 2], pattern) == 1
    assert compare_dices([5, 5, 5, 5, 4], [5, 5, 4, 5, 5], pattern) == -1
    assert compare_dices([2, 2, 2, 1, 2], [1, 2, 1, 1, 1], pattern) == 0


def test_compare_trojki():
    pattern = 3
    assert compare_dices([1, 1, 1, 3, 2], [2, 3, 2, 1, 2], pattern) == 1
    assert compare_dices([], [], pattern)
