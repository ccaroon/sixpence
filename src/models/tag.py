import re
from tinydb import where

from models.base import Base

class Tag(Base):
    def __init__(self, id=None, **kwargs):
        self.__name = None

        super().__init__(id=id, **kwargs)


    @property
    def name(self):
        return self.__name


    @name.setter
    def name(self, new_name):
        self.__name = self.normalize(new_name)


    def update(self, data):
        self.name = data.get('name', self.name)


    @classmethod
    def normalize(cls, name):
        norm_name = name.strip()
        norm_name = name.lower()

        # Start/End with non-word char => strip
        norm_name = re.sub(r"^\W+|\W+$", "", norm_name)
        # Strip Misc Char that don't want as space
        norm_name = re.sub(r"[']", "", norm_name)
        # Non-var chars => space
        norm_name = re.sub(r"[^a-zA-Z0-9_\-.]", " ", norm_name)
        # Spaces => '-'
        norm_name = re.sub(r"\s+", "-", norm_name)

        return norm_name


    @classmethod
    def exists(cls, name):
        return cls._database().contains(where('name') == cls.normalize(name))


    def _serialize(self):
        return {
            'name': self.name
        }


    def __lt__(self, other_tag):
        return self.name < other_tag.name


    def __gt__(self, other_tag):
        return self.name > other_tag.name


    def __eq__(self, other_tag):
        return self.name == other_tag.name


    def __str__(self):
        return self.name


    def __repr__(self):
        return self.name


    def __hash__(self):
        return hash(self.name)
