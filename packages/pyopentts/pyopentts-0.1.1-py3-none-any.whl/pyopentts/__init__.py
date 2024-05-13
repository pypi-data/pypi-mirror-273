import requests
import os

# The line `from /cache import OpenTTSCache` in the code snippet is attempting to import the
# `OpenTTSCache` class from a module named `cache`. However, the usage of `/` in the import statement
# is not valid in Python.
from .cache import OpenTTSCache


class OpenTTSClient:

    def __init__(self, base_url="http://kbytes.lat:5500"):
        self.base_url = base_url
        self.cache = OpenTTSCache(self)

    def speak_text(self, voice, text, vocoder=None, denoiser_strength=None, cache=None):
        """Generate speech from text."""
        if not self.cache.validate_voice(voice):
            raise ValueError(f"Invalid voice: {voice}")
        params = {
            "voice": voice,
            "text": text,
            # "vocoder": vocoder,
            # "denoiserStrength": denoiser_strength,
            # "cache": cache,
        }
        # Filter out None values to avoid sending them in the request
        params = {k: v for k, v in params.items() if v is not None}
        response = requests.get(f"{self.base_url}/api/tts", params=params)
        response.raise_for_status()
        return response.content  # Returns the binary content of the WAV file

    def get_voices(self, language=None, locale=None, gender=None, tts_name=None):
        """Retrieve available voices."""
        params = {
            "language": language,
            "locale": locale,
            "gender": gender,
            "tts_name": tts_name,
        }
        params = {k: v for k, v in params.items() if v is not None}
        response = requests.get(f"{self.base_url}/api/voices", params=params)
        response.raise_for_status()
        return response.json()  # Returns a JSON object with the voices

    def get_languages(self, tts_name=None):
        """Retrieve available languages."""
        params = {"tts_name": tts_name} if tts_name else {}
        response = requests.get(f"{self.base_url}/api/languages", params=params)
        response.raise_for_status()
        return response.json()  # Returns a list of languages

    def refresh_cache(self):
        self.cache.refresh_cache()
