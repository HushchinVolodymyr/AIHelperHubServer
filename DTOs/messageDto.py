


class MessageDto:
    def __init__(self, id: int, message_type: bool, message: str):
        self.id = id
        self.message_type = message_type
        self.message = message

    def to_dict(self):
        return {
            "id": self.id,
            "messageType": self.message_type,
            "message": self.message
        }

    def __repr__(self):
        return f'MessageDto: id = {self.id}, messageType = {self.message_type}, message = {self.message}'