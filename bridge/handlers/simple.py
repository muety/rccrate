from .handler import Handler

class SimpleCachingHandler(Handler):
    def __init__(self, initial_value=None, preprocess=lambda m: m):
        self.preprocess = preprocess
        self.value = self.preprocess(initial_value)

    def handle(self, payload):
        self.value = self.preprocess(payload)

    def get_latest(self):
        return self.value