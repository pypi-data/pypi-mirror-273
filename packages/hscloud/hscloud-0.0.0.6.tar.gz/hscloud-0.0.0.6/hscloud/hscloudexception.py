
class HsCloudException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class HsCloudAccessDenied(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)