"""
Base class for notifications.

- setup connection
- create message
- attachments
- send message

"""


class baseNotification:

    def __init__(self, settings: dict, message: str) -> None:
        self.message = message
        self.settings = settings

    def attach_file(self, filename: str):
        raise NotImplementedError()

    def attach_data(self, stream: bytes, filename: str):
        raise NotImplementedError()

    def send(self, destination):
        raise NotImplementedError()
