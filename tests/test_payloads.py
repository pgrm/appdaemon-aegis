from __future__ import annotations

import pytest

from appdaemon_aegis.payloads import LightCommandPayload


@pytest.mark.parametrize(
    "raw_payload, expected_state, expected_brightness",
    [
        # --- Valid Payloads ---
        ('{"state": "ON", "brightness": 128}', "on", 128),
        ('{"state": " on "}', "on", None),
        ('{"brightness": "150"}', None, 150),
        ('{"brightness": 255.0}', None, 255),
        ('{"state": "OFF"}', "off", None),
        ("{}", None, None),
        # --- Malformed or Invalid Payloads ---
        ("invalid-json", None, None),
        ("[]", None, None),
        ('{"state": 123}', None, None),
        ('{"brightness": "invalid"}', None, None),
        ('{"state": null, "brightness": null}', None, None),
        ('{"brightness": []}', None, None),
    ],
)
def test_from_json(
    raw_payload: str, expected_state: str | None, expected_brightness: int | None
) -> None:
    """Test various scenarios for LightCommandPayload.from_json."""
    payload = LightCommandPayload.from_json(raw_payload)
    assert payload.state == expected_state
    assert payload.brightness == expected_brightness
