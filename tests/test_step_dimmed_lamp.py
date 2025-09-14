import pytest
from appdaemon_aegis.step_dimmed_lamp import StepDimmedLamp


def test_initialization_default():
    """Test initialization with default parameters."""
    lamp = StepDimmedLamp()
    assert lamp.max_brightness == 255
    assert lamp.brightness_levels == [63, 127, 255]


def test_initialization_custom_floats():
    """Test initialization with custom float steps."""
    lamp = StepDimmedLamp(steps=[0.1, 0.5, 0.9])
    assert lamp.brightness_levels == [25, 127, 229]


def test_initialization_custom_ints():
    """Test initialization with custom integer steps."""
    lamp = StepDimmedLamp(steps=[50, 150, 250])
    assert lamp.brightness_levels == [50, 150, 250]


def test_initialization_mixed_steps():
    """Test initialization with a mix of float and int steps."""
    lamp = StepDimmedLamp(steps=[0.2, 100, 0.8])
    assert lamp.brightness_levels == [51, 100, 204]


def test_initialization_invalid_steps():
    """Test initialization with invalid step values."""
    with pytest.raises(ValueError):
        StepDimmedLamp(steps=[])
    with pytest.raises(ValueError):
        StepDimmedLamp(steps=[1.1])
    with pytest.raises(ValueError):
        StepDimmedLamp(steps=[-0.1])
    with pytest.raises(ValueError):
        StepDimmedLamp(steps=[256])
    with pytest.raises(ValueError):
        StepDimmedLamp(steps=[-1])
    with pytest.raises(TypeError):
        StepDimmedLamp(steps=["a"])


def test_get_level_from_brightness():
    """Test converting brightness to level index."""
    lamp = StepDimmedLamp(steps=[50, 100, 150, 200])
    assert lamp.get_level_from_brightness(0) == -1
    assert lamp.get_level_from_brightness(25) == 0  # Closest to 50
    assert lamp.get_level_from_brightness(50) == 0
    assert lamp.get_level_from_brightness(74) == 0  # Closer to 50
    assert lamp.get_level_from_brightness(76) == 1  # Closer to 100
    assert lamp.get_level_from_brightness(100) == 1
    assert lamp.get_level_from_brightness(180) == 3  # Closest to 200
    assert lamp.get_level_from_brightness(255) == 3  # Closest to 200


def test_get_flicks_from_off():
    """Test calculating flicks when the lamp is off."""
    lamp = StepDimmedLamp()  # 3 levels
    assert lamp.get_flicks(None, 0) == 1
    assert lamp.get_flicks(None, 1) == 2
    assert lamp.get_flicks(None, 2) == 3
    assert lamp.get_flicks(-1, 2) == 3


def test_get_flicks_between_levels():
    """Test calculating flicks between different levels."""
    lamp = StepDimmedLamp(steps=[0.1, 0.2, 0.3, 0.4])  # 4 levels
    assert lamp.get_flicks(0, 0) == 0
    assert lamp.get_flicks(0, 1) == 1
    assert lamp.get_flicks(0, 3) == 3
    assert lamp.get_flicks(1, 0) == 3  # Wraps around
    assert lamp.get_flicks(3, 1) == 2  # Wraps around


def test_get_flicks_invalid_levels():
    """Test calculating flicks with invalid level indices."""
    lamp = StepDimmedLamp()
    with pytest.raises(ValueError):
        lamp.get_flicks(None, 3)
    with pytest.raises(ValueError):
        lamp.get_flicks(3, 0)
    with pytest.raises(ValueError):
        lamp.get_flicks(-2, 0)
