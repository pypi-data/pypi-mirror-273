import os

import requests

from praetorian_cli.sdk.keychain import verify_credentials, Keychain


class Chariot:

    def __init__(self, keychain: Keychain):
        self.keychain = keychain

    @verify_credentials
    def my(self, params: dict) -> {}:
        resp = requests.get(f"{self.keychain.api}/my", params=params, headers=self.keychain.headers)
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')
        return resp.json()

    @verify_credentials
    def count(self, params: dict) -> {}:
        resp = requests.get(f"{self.keychain.api}/my/count", params=params, headers=self.keychain.headers)
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')
        return resp.json()

    @verify_credentials
    def add(self, type, payload: dict) -> {}:
        resp = requests.post(f"{self.keychain.api}/{type}", json=payload, headers=self.keychain.headers)
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')
        return resp.json()

    @verify_credentials
    def delete_seed(self, key: str) -> {}:
        resp = requests.delete(f"{self.keychain.api}/seed", json={'key': key}, headers=self.keychain.headers)
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')
        return resp.json()

    @verify_credentials
    def update(self, resource: str, data: dict) -> {}:
        resp = requests.put(f"{self.keychain.api}/{resource}", json=data, headers=self.keychain.headers)
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')
        return resp.json()

    @verify_credentials
    def link_account(self, username: str, config: dict):
        resp = requests.post(f"{self.keychain.api}/account/{username}", json={'config': config},
                             headers=self.keychain.headers)
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')
        return resp.json()

    @verify_credentials
    def unlink_account(self, username: str):
        resp = requests.delete(f"{self.keychain.api}/account/{username}", headers=self.keychain.headers)
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')
        return resp.json()

    @verify_credentials
    def upload(self, name: str):
        with open(name, 'rb') as file:
            resp = requests.put(f"{self.keychain.api}/file", params={"name": name}, data=file, allow_redirects=True,
                                headers=self.keychain.headers)
            if not resp.ok:
                raise Exception(f'[{resp.status_code}] Request failed')

    @verify_credentials
    def download(self, name: str, download_path: str) -> bool:
        directory = os.path.dirname(download_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        resp = requests.get(f"{self.keychain.api}/file", params={"name": name}, allow_redirects=True,
                            headers=self.keychain.headers)
        if not resp.ok:
            raise Exception(f'[{resp.status_code}] Request failed')
        with open(download_path, 'wb') as file:
            file.write(resp.content)
