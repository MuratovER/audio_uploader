from functools import cache

AVAILABLE_AUDIO_TYPES: str = (
    "&audio/aac&application/x-cdf&audio/midi&audio/mpeg&audio/ogg&audio/wav&audio/webm"
)


@cache
def get_available_audio_types() -> list[str]:
    return AVAILABLE_AUDIO_TYPES.split("&")
