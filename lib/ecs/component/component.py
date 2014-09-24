class Component(object):
    def __init__(self, message_handlers=None):
        self._messages = []
        if message_handlers:
            self._message_handlers = message_handlers

    def get_message_subscriptions(self):
        return []

    def handle_messages(self):
        pass

    def send_message(self, message):
        self._messages.append(message)

    def handle_messages(self):
        supported_message_handlers = self._message_handlers.keys()
        for message in self._messages:
            message_type = message['message_type']
            if message_type not in supported_message_handlers:
                continue
            self._message_handlers[message_type](message)

        self._messages = []
