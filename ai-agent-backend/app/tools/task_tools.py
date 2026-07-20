from datetime import datetime

from agents import function_tool


@function_tool
def get_current_datetime() -> str:
    """Return the current server date and time."""

    print("get_current_datetime tool was called")

    current_datetime = datetime.now()

    return current_datetime.strftime("%Y-%m-%d %H:%M:%S")
