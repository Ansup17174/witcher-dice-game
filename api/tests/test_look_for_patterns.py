from ..utils import look_for_patterns


# look_for_patterns tests

def test_poker():
    assert look_for_patterns([1, 1, 1, 1, 1]) == 8
    assert look_for_patterns([2, 2, 2, 2, 2]) == 8
    assert look_for_patterns([3, 3, 3, 3, 3]) == 8
    assert look_for_patterns([4, 4, 4, 4, 4]) == 8
    assert look_for_patterns([5, 5, 5, 5, 5]) == 8
    assert look_for_patterns([6, 6, 6, 6, 6]) == 8


def test_kareta():
    assert look_for_patterns([1, 4, 4, 4, 4]) == 7
    assert look_for_patterns([2, 2, 2, 2, 5]) == 7
    assert look_for_patterns([1, 1, 1, 2, 3]) != 7


def test_st():
    assert look_for_patterns([1, 2, 3, 4, 5]) == 4
    assert look_for_patterns([2, 3, 4, 5, 6]) == 5
    assert look_for_patterns([1, 2, 3, 4, 6]) != 5


def test_trojka():
    assert look_for_patterns([1, 1, 1, 2, 3]) == 3
    assert look_for_patterns([3, 4, 1, 3, 3]) == 3
    assert look_for_patterns([1, 2, 3, 4, 5]) != 3


def test_dwie_pary():
    assert look_for_patterns([1, 1, 2, 2, 3]) == 2
    assert look_for_patterns([2, 2, 4, 4, 6]) == 2
    assert look_for_patterns([6, 5, 6, 5, 1]) == 2
    assert look_for_patterns([1, 1, 1, 1, 1]) != 2


def test_para():
    assert look_for_patterns([1, 1, 2, 3, 4]) == 1
    assert look_for_patterns([2, 2, 3, 4, 5]) == 1
    assert look_for_patterns([5, 1, 2, 3, 5]) == 1


def test_no_pattern():
    assert look_for_patterns([1, 2, 4, 5, 6]) == 0
    assert look_for_patterns([2, 1, 3, 4, 6]) == 0
