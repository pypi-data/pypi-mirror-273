from apex_dojo.time_calculator.time_calculator import add_time


def test_same_period():
    assert add_time("3:30 PM", "2:12") == "5:42 PM"


def test_different_period():
    assert add_time("11:55 AM", "3:12") == "3:07 PM"


def test_next_day():
    assert add_time("9:15 PM", "5:30") == "2:45 AM (next day)"


def test_period_change_at_twelve():
    assert add_time("11:40 AM", "0:25") == "12:05 PM"


def test_twenty_four():
    assert add_time("2:59 AM", "24:00") == "2:59 AM (next day)"


def test_two_days_later():
    assert add_time("11:59 PM", "24:05") == "12:04 AM (2 days later)"


def test_high_duration():
    assert add_time("8:16 PM", "466:02") == "6:18 AM (20 days later)"


def test_no_change():
    assert add_time("5:01 AM", "0:00") == "5:01 AM"


def test_same_period_with_day():
    assert add_time("3:30 PM", "2:12", "Monday") == "5:42 PM, Monday"


def test_twenty_four_with_day():
    assert add_time("2:59 AM", "24:00", "saturDay") == "2:59 AM, Sunday (next day)"


def test_two_days_later_with_day():
    assert (
        add_time("11:59 PM", "24:05", "Wednesday") == "12:04 AM, Friday (2 days later)"
    )


def test_high_duration_with_day():
    assert add_time("8:16 PM", "466:02", "tuesday") == "6:18 AM, Monday (20 days later)"
