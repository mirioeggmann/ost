import pytest
from leap_year import is_leap_year


def test_is_leap_year_for_default_argument():
    # default argument is 2024, which is a leap year
    assert is_leap_year() == True


def test_is_leap_year_for_negative_year_raises_value_error():
    with pytest.raises(ValueError):
        is_leap_year(-1584)


def test_is_leap_year_for_selected_years():
    years = [2010, 2008, 1700, 1701, 1702, 1703, 1704, 1600, 1584]
    expected_answers = [False, True, False, False, False, False, True, True, True]
    for year, expected in zip(years, expected_answers):
        assert is_leap_year(year) == expected
