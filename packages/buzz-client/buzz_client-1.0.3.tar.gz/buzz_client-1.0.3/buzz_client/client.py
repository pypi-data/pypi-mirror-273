from email.policy import HTTP
from functools import cached_property
import re
from httpx import HTTPError
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
        self.headers = {'x-auth-token': self.settings.token}

    def get(self, endpoint: str):
        response = requests.get(f"{self.api}{endpoint}",
                                headers=self.headers)
        return response

    def check(self):
        try:
            api_info = self.get('/')
        except requests.exceptions.ConnectionError:
            return dict(api_ok=False, token_ok=False)
        if api_info.ok:
            api_path = api_info.json().get('api_path')
            token_check = self.get(f"{api_path}/check")

            if token_check.ok:
                return dict(api_ok=True, token_ok=True)
            else:
                return dict(api_ok=True, token_ok=False)

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
        response = self.get(f'{self.api_path}/notifiers')
        if response.ok:
            return self.get(f'{self.api_path}/notifiers').json().get('notifiers')
        else:
            return []

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
            headers=self.headers)

        response.raise_for_status()
        return response


if __name__ == "__main__":
    c = Configuration()
    c.from_file(filename='settings.yaml', load=yaml_load)  # type: ignore
    c.from_environ(prefix="BC")
    bc = BuzzClient(c)
