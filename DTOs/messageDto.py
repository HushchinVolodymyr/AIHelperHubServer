


class MessageDto:
    def __init__(self, id: int, messageType: bool, message: str):
        self.id = id
        self.messageType = messageType
        self.message = message

    def to_dict(self):
        return {
            "id": self.id,
            "messageType": self.messageType,
            "message": self.message
        }

    def __repr__(self):
        return f'MessageDto: id = {self.id}, messageType = {self.messageType}, message = {self.message}'