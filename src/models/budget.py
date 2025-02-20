from .base import Base
from .taggable import Taggable

# TODO: update to correct schema

class Budget(Taggable, Base):
    def __init__(self, id=None, **kwargs):
        self.category = None

        super().__init__(id=id, **kwargs)


    def _serialize(self):
        data =  {
            'category': self.category
        }

        # Tags
        data.update(super()._serialize())

        return data


    def update(self, data):
        self.category = data.get('category', self.category)
        self.tags = data.get('tags', self.tags)
