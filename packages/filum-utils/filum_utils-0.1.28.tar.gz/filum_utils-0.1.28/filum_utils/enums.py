from typing import TypedDict


class BaseEnum:
    @classmethod
    def get_list(cls):
        return [getattr(cls, attr) for attr in dir(cls) if attr.isupper()]


class ParentType(BaseEnum):
    AUTOMATED_ACTION = "automated_action"
    CAMPAIGN = "campaign"


class ObjectType(BaseEnum):
    INSTALLED_SOURCE = "installed_source"
    INSTALLED_MINI_APP = "installed_mini_app"
    ACTION = "action"


class Organization(TypedDict):
    id: str
    slug: str


class Object(BaseEnum):
    CAMPAIGN = "campaign"
    SEGMENT = "segment"


class BaseStatus(BaseEnum):
    COMPLETED = "completed"


class FileCSVDelimiter(BaseEnum):
    COMMA = ","
    SEMICOLON = ";"
    TAB = "\t"


class Codec:
    UTF8 = "utf-8"
    UTF16 = "utf-16"

    @classmethod
    def get_list(cls):
        return [cls.UTF8, cls.UTF16]
