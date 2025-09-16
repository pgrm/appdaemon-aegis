def test_get_safe_brightness():
    from appdaemon_aegis.utils import get_safe_brightness

    assert get_safe_brightness(0) == 0
    assert get_safe_brightness(255) == 255
    assert get_safe_brightness(300) == 255
    assert get_safe_brightness(-10) == 0

    assert get_safe_brightness("0") == 0
    assert get_safe_brightness("255") == 255
    assert get_safe_brightness("300") == 255
    assert get_safe_brightness("-10") == 0

    assert get_safe_brightness(0.3) == 0
    assert get_safe_brightness(255.9) == 255
    assert get_safe_brightness(300.0) == 255
    assert get_safe_brightness(-10.5) == 0

    assert get_safe_brightness("0.3") == 0
    assert get_safe_brightness("255.9") == 255
    assert get_safe_brightness("300.0") == 255
    assert get_safe_brightness("-10.5") == 0
