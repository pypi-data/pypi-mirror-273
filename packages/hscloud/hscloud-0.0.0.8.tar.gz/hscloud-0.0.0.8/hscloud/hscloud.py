from .helpers import Helpers

class HsCloud:

    def __init__(self, username=None, password=None):
        super().__init__()
        self.username = username
        self.password = password
        self.endpoint = None
        self.access_token = None

    def login(self):
        response = Helpers.login(self.username, self.password)
        if response is not None:
            self.endpoint = response.get("endpoint")
            self.access_token = response.get("access_token")
            return True
        else:
            return False

    def get_devices(self):
        if not self.endpoint or not self.access_token:
            return None

        return Helpers.devices(self.endpoint, self.access_token)

    def get_status(self, devicesn):
        if not self.endpoint or not self.access_token:
            return None

        return Helpers.status(self.endpoint, self.access_token, devicesn)

    def update_status(self, devicesn, **kwargs):
        if not self.endpoint or not self.access_token:
            return None

        response = Helpers.update(self.endpoint, self.access_token, devicesn, **kwargs)
        if response is not None:
            return True
        else:
            return False