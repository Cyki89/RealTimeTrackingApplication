import json


setting_file = 'files\Settings\settings.json'


class Settings:
    def __init__(self, settings_file=setting_file):
        self.settings_file = settings_file
        self.settings = self.read_settings()
        self.initialize_settings()

    def read_settings(self):
        with open(self.settings_file, 'r') as json_file:
            settings = json.load(json_file)
        return settings

    def save_settings(self):
        self.save_settings_to_json()
        self.save_settings_to_csv()

    def change_settings(self, key, value):
        if not key in self.settings:
            raise KeyError("Setting dosn't exist")

        self.settings[key] = value
        self.save_settings()
        self.initialize_settings()

    def save_settings_to_json(self):
        with open(self.settings_file, 'w') as json_file:
            json.dump(self.settings, json_file, indent=4)

    def save_settings_to_csv(self):
        with open(SETTINGS_FILE, 'r') as json_file:
            settings = json.load(json_file)

        with open(BASE_SETTINGS_FILE, 'w') as settings_file, \
                open(PATCHS_FILE, 'w') as patchs_file:

            for key, value in settings.items():
                if 'DIR' in key or 'FILE' in key:
                    patchs_file.write(f'{key};{value};\n')
                else:
                    settings_file.write(f'{key};{value};\n')

    def initialize_settings(self):
        for key, value in self.settings.items():
            source = f'{key}={value}' if isinstance(value, int)\
                     else f'{key}="{value}"'
            exec(source, globals())


SETTINGS_INSTANCE = Settings()
