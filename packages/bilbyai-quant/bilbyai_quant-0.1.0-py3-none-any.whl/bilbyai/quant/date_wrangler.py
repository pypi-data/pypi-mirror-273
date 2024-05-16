from datetime import datetime, timedelta
from typing import Literal

DayOfWeek = Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]


def get_week_range(
    date: datetime,
) -> tuple[datetime, datetime]:
    """Get the start and end dates of a week.

    Args:
        date: The date to get the week range for.

    Returns:
        A tuple of the start and end dates of the week.
    """
    return (get_date_of_week_by_date(date, "sunday"), get_date_of_week_by_date(date, "saturday"))


def get_date_of_week_by_date(
    date: datetime,
    day_of_week: DayOfWeek,
    *,
    offset_weeks: int = 0,
) -> datetime:
    """Given a date, return the date of the specific day of the week.
    That is, given a date, we are given a week, from sunday to saturday, and we want to
    return the date of the specific day of the week.

    Args:
        date (datetime.datetime): The date to get the date of the specific day of the week for.
        day_of_week (Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]):
            The day of the week to get the date of. Must be one of sunday, monday, tuesday, wednesday, thursday, friday, or saturday.

    Returns:
        The date of the specific day of the week for the given date.
    """
    return (
        date
        - timedelta(days=int(date.strftime("%w")))  # get the sunday
        + timedelta(days=_get_day_of_week_index(day_of_week))  # add the offset
        + timedelta(weeks=offset_weeks)  # add the offset weeks
    )


def _get_day_of_week_index(
    day_of_week: DayOfWeek,
) -> int:
    if day_of_week == "sunday":
        return 0
    elif day_of_week == "monday":
        return 1
    elif day_of_week == "tuesday":
        return 2
    elif day_of_week == "wednesday":
        return 3
    elif day_of_week == "thursday":
        return 4
    elif day_of_week == "friday":
        return 5
    elif day_of_week == "saturday":
        return 6
    else:
        raise ValueError(f"Invalid day_of_week value: {day_of_week}")
