from __future__ import annotations

_TRACK_MAP: dict[str, str] = {
    "vietnam_letter":       "ambient_vietnam.mp3",
    "counterculture":       "ambient_counter.mp3",
    "dylan_era_reflection": "ambient_dylan.mp3",
}
_DEFAULT = "ambient_default.mp3"


def select_ambient_track(source_type: str) -> str:
    return _TRACK_MAP.get(source_type, _DEFAULT)
