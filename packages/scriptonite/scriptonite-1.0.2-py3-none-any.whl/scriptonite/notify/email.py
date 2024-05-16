from base import baseNotification
from ..email import EmailMessage, EmailSender


class EmailNotification(baseNotification):
    def __init__(self, settings: dict, message: str) -> None:
        super().__init__(settings, message)
        self.message = EmailMessage(sender=settings['from'],
                                    recipients=settings['recipients'],
                                    subject=settings['subject'],
                                    body=settings['body'])

        self.sender = EmailSender(server=settings['server'],
                                  username=settings['username'],
                                  password=settings['password'],
                                  starttls=settings['starttls'])

    def attach_file(self, filename: str):
        self.message.attach_file(filename)

    def attach_data(self, stream: bytes, filename: str):
        self.message.attach_data(stream, filename=filename)

    def send(self):
        self.sender.send(self.message)
