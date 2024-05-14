from typing import Any, Callable, Type

from cloud.protocols import MessagePublisher, StorageUploader

error_message = "%(class)s does not implement %(protocol)s protocol"


def storage_uploader(
    uploader_class: Type[StorageUploader], *args: Any, **kwargs: Any
) -> Callable[[], StorageUploader]:
    error = error_message % {"class": uploader_class.__name__, "protocol": "StorageUploader"}
    assert issubclass(uploader_class, StorageUploader), error

    def maker() -> StorageUploader:
        return uploader_class(*args, **kwargs)

    return maker


def message_publisher(
    publisher_class: Type[MessagePublisher], *args: Any, **kwargs: Any
) -> Callable[[], MessagePublisher]:
    error = error_message % {"class": publisher_class.__name__, "protocol": "MessagePublisher"}
    assert issubclass(publisher_class, MessagePublisher), error

    def maker() -> MessagePublisher:
        return publisher_class(*args, **kwargs)

    return maker
