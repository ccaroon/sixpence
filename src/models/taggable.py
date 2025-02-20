from .tag import Tag

class Taggable:
    def __init__(self, id=None, **kwargs):
        self.__tags = set()
        super().__init__(id=id, **kwargs)


    @property
    def tags(self):
        return self.__tags


    @tags.setter
    def tags(self, new_tags):
        self.__tags = set()
        for tag in new_tags:
            self.tag(tag)


    def tag(self, tag):
        if isinstance(tag, str):
            self.__tags.add(Tag(name=tag))
        elif isinstance(tag, Tag):
            self.__tags.add(tag)
        else:
            raise TypeError("'tag' must be of type `str` or `Tag`")


    def remove_tag(self, tag):
        if isinstance(tag, str):
            self.__tags.remove(Tag(name=tag))
        elif isinstance(tag, Tag):
            self.__tags.remove(tag)
        else:
            raise TypeError("'tag' must be of type `str` or `Tag`")


    def _post_save(self):
        # Add all new tags to Tag DB
        for tag in self.__tags:
            if not Tag.exists(tag.name):
                tag.save()


    def _serialize(self):
        # Store Tags that are part of the Object as strings only
        return {
            "tags": [str(tag) for tag in self.tags]
        }
