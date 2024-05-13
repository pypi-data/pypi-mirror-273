class OpenTTSCache:
    def __init__(self, client):
        self.client = client
        self.voices = {}
        self.languages = []
        self.load_cache()

    def load_cache(self):
        """Load and cache voices and languages from the API."""
        self.voices = self.client.get_voices()
        self.languages = self.client.get_languages()
        print("Cache loaded with languages and voices.")

    def validate_voice(self, voice):
        """Check if the voice is available."""
        return any(voice_info == voice for voice_info in self.voices)

    def validate_language(self, language):
        """Check if the language is supported."""
        return language in self.languages

    def refresh_cache(self):
        """Refresh the cached voices and languages."""
        self.load_cache()
        print("Cache refreshed.")
