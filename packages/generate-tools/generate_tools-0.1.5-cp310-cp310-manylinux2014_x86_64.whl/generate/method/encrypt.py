
from requests import post

import generate


class Encrypt:
    def decodeString(
        self: 'generate.Generate',
        key: str,
        string: str
    ) -> str:
        results = post(
            f'{self._apiUrlEncrypt}/decode',
            json={
                'type': 'ayiin',
                'text': f'{string}',
                'key': key
            },
            headers={
                'Content-Type': 'application/json'
            }
        )
        if results.ok:
            res = results.json()
            return res['data']


    def encodeString(
        self: 'generate.Generate',
        key: str,
        string: str
    ) -> str:
        results = post(
            f'{self._apiUrlEncrypt}/encode',
            json={
                'type': 'ayiin',
                'text': f'{string}',
                'key': key
            },
            headers={
                'Content-Type': 'application/json'
            }
        )
        if results.ok:
            res = results.json()
            return res['data']
