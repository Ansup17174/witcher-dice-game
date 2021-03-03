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


def test_compare_fulls():
    pattern = 6
    assert compare_dices([6, 6, 6, 5, 5], [5, 5, 5, 6, 6], pattern) == 0
    assert compare_dices([6, 6, 6, 5, 5], [6, 6, 6, 4, 4], pattern) == 0
    assert compare_dices([6, 6, 6, 1, 1], [1, 1, 1, 2, 2], pattern) == 0
    assert compare_dices([4, 4, 4, 3, 3], [6, 6, 6, 1, 1], pattern) == 1


def test_compare_trojki():
    pattern = 3
    assert compare_dices([1, 1, 1, 3, 2], [2, 3, 2, 1, 2], pattern) == 1
    assert compare_dices([4, 6, 5, 4, 4], [4, 4, 4, 3, 2], pattern) == 0
    assert compare_dices([4, 2, 3, 4, 4], [4, 3, 2, 4, 4], pattern) == -1
    assert compare_dices([4, 4, 4, 2, 1], [4, 2, 1, 4, 4], pattern) == -1


def test_compare_dwie_pary():
    pattern = 2
    assert compare_dices([6, 6, 1, 1, 3], [5, 5, 4, 4, 2], pattern) == 1
    assert compare_dices([6, 6, 1, 1, 3], [6, 6, 1, 1, 2], pattern) == 0
    assert compare_dices([1, 1, 2, 2, 3], [2, 1, 2, 1, 3], pattern) == -1


def test_compare_pary():
    pattern = 1
    assert compare_dices([1, 1, 2, 3, 4], [2, 2, 3, 4, 5], pattern) == 1
    assert compare_dices([4, 4, 5, 6, 1], [4, 4, 1, 2, 3], pattern) == 0
    assert compare_dices([1, 1, 2, 3, 4], [4, 3, 2, 1, 1], pattern) == -1
