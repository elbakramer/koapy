class RateLimitException(Exception):

    def __init__(self, message):
        super(RateLimitException, self).__init__(message)
        