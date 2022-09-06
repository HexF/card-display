from typing import Generator, Type


def subclass_recursive(cls: object) -> Generator[Type[object], None, None]:
    for sklass in cls.__subclasses__():
        yield sklass
        for klass in subclass_recursive(sklass):
            yield klass