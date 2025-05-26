def calculate_experience_per_minute(experience_gained, elapsed_time):
    """Calculate experience gained per minute."""
    if elapsed_time == 0:
        return 0
    minutes = elapsed_time / 60
    return experience_gained / minutes if minutes > 0 else 0

def get_current_time():
    """
    Get the current time in seconds since the epoch.

    Returns:
    float: Current time in seconds.
    """
    import time
    return time.time()