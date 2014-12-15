class FeedKeyError(KeyError):

    def __init__(self, key):
        self.key = key

    def __str__(self):
        return str(self.key)
