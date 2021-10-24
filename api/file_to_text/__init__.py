__all__ = [
    'ConverterClient',
    'AsyncConverterClient',
    'ConverterError'
]

__version__ = '0.0.1'


import io
from pathlib import Path

import aiofiles
from httpx import AsyncClient, Client, BasicAuth, Response


class ConverterError(Exception):
    pass


class BaseConverterClient:
    _base_url = None
    _convert_service = "/convert"

    def __init__(self, service_base_url, username, password, timeout=60.0):
        self._base_url = service_base_url
        self.auth = BasicAuth(username, password)
        self.timeout = timeout

    @property
    def url(self):
        return self._base_url + self._convert_service

    @staticmethod
    def _process_result(res: Response) -> str:
        if res.status_code == 200:
            data = res.json()
            if data['result'] != 'error':
                return data['text']
            else:
                raise ConverterError(data['messages'])

        elif res.status_code == 401:
            raise ConverterError('Not authorized')
        else:
            raise ConverterError('Unexpected Response')


class ConverterClient(BaseConverterClient):

    def convert(self, filepath: str) -> str:
        with io.open(filepath, "rb") as file:
            file_data = file.read()

        files = {'file': (Path(filepath).name, file_data)}

        with Client(timeout=self.timeout) as http_client:
            res = http_client.post(self.url,
                                   files=files,
                                   auth=self.auth)

        return ConverterClient._process_result(res)


class AsyncConverterClient(BaseConverterClient):

    async def convert(self, filepath: str) -> str:
        async with aiofiles.open(filepath, "rb") as file:
            file_data = await file.read()

        files = {'file': (Path(filepath).name, file_data)}

        async with AsyncClient(timeout=self.timeout) as http_client:
            res = await http_client.post(self.url,
                                         files=files,
                                         auth=self.auth)

        return AsyncConverterClient._process_result(res)
