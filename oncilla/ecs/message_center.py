class MessageCenter(object):
    instance = None

    @staticmethod
    def get_instance():
        if MessageCenter.instance is None:
            MessageCenter.instance = MessageCenter()

        return MessageCenter.instance
