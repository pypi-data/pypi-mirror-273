from db import db
from models.root.root_model import RootModel


class HeadersModel:
    def __init__(self, locale: str = None, client_os: str = None, client_os_version: str = None, client_timezone: str = None, client_model: str = None, app_version: str = None):
        self.locale = locale
        self.client_os = client_os
        self.client_os_version = client_os_version
        self.client_timezone = client_timezone
        self.client_model = client_model
        self.app_version = app_version
