class System(object):
    def __init__(self, message_handlers):
        self.messages = []
        self.message_handlers = message_handlers

    def send_message(self, message):
        self.messages.append(message)

    def update(self, delta):
        return

    def handle_messages(self):
        supported_message_handlers = self.message_handlers.keys()
        for message in self.messages:
            message_type = message['message_type']
            if message_type not in supported_message_handlers:
                continue
            self.message_handlers[message_type](message)

        self.messages = []