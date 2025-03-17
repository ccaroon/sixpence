import copy
import os
import yaml

# Singleton class
class Config:
    """Class that represents configuration"""

    DEFAULTS = {
        "backup:path": None,
        "backup:keep": 5,
        "app:mode": "system",
        "app:timezone": 'US/Eastern'
    }

    __instance = None

    def __init__(self, filename=None, transient=None):
        if not Config.__instance:
            if filename == None:
                raise TypeError("Must Specify a Filename")
            Config.__instance = Config.__Instance(filename, transient)


    def force_reload(self):
        Config.__instance.reload()


    def __getattr__(self, name):
        return getattr(Config.__instance, name)


    @classmethod
    def initialize(cls, conf, transient=None):
        """
        Create the config file and init to defaults if not exist.
        Then return a Config instance.
        """
        cfg = None
        if not os.path.exists(conf):
            # Create empty config file
            with open(conf, "w") as fptr:
                yaml.safe_dump({}, fptr)

            # Config instance for empty file
            cfg = Config(conf, transient)

            # Set default key/values
            for key_path, value in cls.DEFAULTS.items():
                cfg.set(key_path, value)

            # Save with defaults
            cfg.save()
        else:
            cfg = Config(conf, transient)

        return cfg

    # --------------------------------------------------------------------------
    class __Instance:
        def __init__(self, filename, transient=None):
            self.__filename = filename
            self.__transient = transient
            self.__read_file()


        def __read_file(self):
            with open(self.__filename, 'r') as fptr:
                try:
                    self.settings = yaml.safe_load(fptr)
                except Exception as exc:
                    raise Exception(F"Error reading config file {exc.message}")


        def reload(self):
            self.__read_file()


        def get(self, name, default=None):
            value = self.settings

            parts = name.split(':')
            for part_name in parts:
                value = value.get(part_name, default)
                if value == default:
                    break

            return value


        def get_all(self):
            return self.settings


        def set(self, name, value):
            settings = self.settings

            parts = name.split(':')
            key = parts.pop()
            for sub_section in parts:
                sub = settings.get(sub_section)
                if sub:
                    settings = sub
                # Create the sub-section if it does not exist
                else:
                    settings[sub_section] = {}
                    settings = settings[sub_section]

            settings[key] = value


        def save(self):
            # Don't save top-level transient keys
            to_save = copy.deepcopy(self.settings)
            if self.__transient:
                for key in self.__transient:
                    del to_save[key]

            with open(self.__filename, 'w') as fptr:
                yaml.safe_dump(to_save, fptr)











#
