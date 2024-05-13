from .helpers import Helpers

class HsCloud:

    def __init__(self, username=None, password=None):
        super().__init__()
        self.username = username
        self.password = password
        self.endpoint = None
        self.access_token = None

    def login(self) -> bool:
        response = Helpers.login(self.username, self.password)
        if response[0] == 0:
            self.endpoint = response[1].get("endpoint")
            self.access_token = response[1].get("access_token")
            return True
        else:
            return False

    def get_devices(self) -> tuple:
        return Helpers.devices(self.endpoint, self.access_token)

    def get_status(self, devicesn) -> tuple:
        return Helpers.status(self.endpoint, self.access_token, devicesn)

    def update_status(self, devicesn, **kwargs) -> tuple:
        return Helpers.update(self.endpoint, self.access_token, devicesn, **kwargs)
