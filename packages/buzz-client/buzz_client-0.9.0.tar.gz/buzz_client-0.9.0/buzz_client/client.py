from functools import cached_property
import re
import requests
import logging
from scriptonite.configuration import Configuration, yaml_load
from scriptonite.utilities import dictObj
from scriptonite.logging import Logger


log = Logger(level=logging.DEBUG)


class BuzzClient:

    settings: dictObj

    def __init__(self, settings) -> None:

        # Load config
        self.settings = settings
        self.api = settings.api

    def get(self, endpoint: str):
        response = requests.get(f"{self.settings.api}{endpoint}",
                                headers={"x-auth-token":
                                         self.settings.token})
        return response

    @cached_property
    def api_info(self) -> dict:
        return self.get('/').json()

    @cached_property
    def api_path(self) -> str | None:
        return self.api_info.get('api_path')

    @cached_property
    def api_version(self) -> str | None:
        return self.api_info.get('app_version')

    @cached_property
    def notifiers(self):
        return self.get(f'{self.api_path}/notifiers').json().get('notifiers')

    def send(self, notifier: str,
             recipient: str,
             body: str = "The body",
             title: str = "You got a buzz",
             severity: str = "info",
             attach: str = ''):

        data = dict(recipient=recipient,
                    body=body,
                    title=title,
                    severity=severity)
        files = {}
        if attach:
            log.debug(f"attaching {attach}...")
            files = {'attach': open(attach, 'rb')}

        response = requests.post(
            f"{self.settings.api}{self.api_path}/send/{notifier}",
            data=data,
            files=files,
            headers={"x-auth-token": self.settings.token})

        return response


if __name__ == "__main__":
    c = Configuration()
    c.from_file(filename='settings.yaml', load=yaml_load)  # type: ignore
    c.from_environ(prefix="BC")
    bc = BuzzClient(c)
