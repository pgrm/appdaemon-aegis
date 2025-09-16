def get_safe_brightness(brightness: int | float | str):
    return max(0, min(255, int(float(brightness))))
