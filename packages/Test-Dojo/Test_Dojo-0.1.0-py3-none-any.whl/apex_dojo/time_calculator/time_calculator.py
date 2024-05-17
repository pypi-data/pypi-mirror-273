from dataclasses import dataclass

WEEK_DAYS = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}


@dataclass
class ConvertTimes:
    start: str
    duration: str

    def split_start_time(self) -> tuple[int, int]:
        hours, minutes = map(int, self.start[:5].split(":"))
        if "PM" in self.start:
            hours += 12
        return hours, minutes

    def split_duration(self) -> list[int]:
        return list(map(int, self.duration.split(":")))


def add_time(start: str, duration: str, day: str = "") -> str:
    start_hour, start_minute = ConvertTimes(start, duration).split_start_time()
    duration_hour, duration_minute = ConvertTimes(start, duration).split_duration()

    total_minutes = (
        start_hour * 60 + start_minute + duration_hour * 60 + duration_minute
    )
    actual_hour, actual_minute = divmod(total_minutes, 60)
    day_counter = actual_hour // 24
    actual_hour %= 24

    time_of_the_day = " PM" if actual_hour >= 12 else " AM"

    actual_hour %= 12
    if actual_hour == 0:
        actual_hour += 12

    calculated_time = f"{actual_hour}:{'%02d' % actual_minute}{time_of_the_day}"

    if day:
        week_index = (
            list(WEEK_DAYS.keys())[list(WEEK_DAYS.values()).index(day.capitalize())]
            + day_counter
        ) % 7
        week_day = f", {WEEK_DAYS[week_index]}"
        calculated_time += week_day

    if day_counter == 1:
        calculated_time += " (next day)"
    elif day_counter > 1:
        calculated_time += f" ({day_counter} days later)"

    return calculated_time
