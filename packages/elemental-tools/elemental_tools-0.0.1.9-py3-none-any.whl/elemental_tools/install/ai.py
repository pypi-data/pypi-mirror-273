class InstallAI:
    from elemental_tools.settings import SettingController

    _settings = SettingController()

    developer = "Elemental Company"

    @staticmethod
    def install():
        import nltk

        nltk.download('wordnet')
