from pathlib import PosixPath
from typing import Tuple

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class Downloader:
    """
       Common downloader for all request methods
    """

    @staticmethod
    def retry_request(retries: int = 3) -> requests.Session:
        """
            This method used to create separate session with retry
        :param retries:
        :return:
        """
        session = requests.Session()
        retry_strategy = Retry(
            total=retries,
            backoff_factor=1,
            status_forcelist=[status_code for status_code in range(400, 600) if
                              status_code not in range(200, 300)])
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def download_and_write(self, source: str, destination: str,
                           retries: int = 10) -> bool:
        """
            THis method will use GET method to fetch data and write in given destination

        :param source:
        :param destination:
        :param retries:
        :return:
        """
        request = self.retry_request(retries)
        response = request.get(source)
        if response.status_code == 200:
            with open(destination, 'wb') as f:
                f.write(response.content)
            return True

        return False

    @staticmethod
    def validate_fields(tile_code: str, from_date: str,
                        download_path: PosixPath,
                        bands: Tuple[str] = None):
        if not isinstance(tile_code, str) or len(tile_code) == 0:
            raise TypeError(
                f"tile_codes expected a non empty str, got {type(tile_code)}"
            )
        if not isinstance(download_path, PosixPath):
            raise TypeError(
                f"download_path expected a PosixPath, got {type(download_path)}"
            )
        if not isinstance(from_date, str):
            raise TypeError(
                f"from_date expected a string of form: YYYY-MM-DD, got {type(from_date)}"
            )
        if bands is not None:
            if not isinstance(bands, tuple):
                raise TypeError(
                    f"bands expected a tuple / list, got {type(bands)}")
            if len(bands) == 0:
                raise ValueError("bands expected a non empty tuple / list")
