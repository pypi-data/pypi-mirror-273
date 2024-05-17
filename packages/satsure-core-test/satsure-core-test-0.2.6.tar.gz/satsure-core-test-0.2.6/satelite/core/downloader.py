import re
from datetime import datetime, timedelta
from pathlib import PosixPath
from subprocess import Popen, PIPE
from typing import Tuple, List

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

    @staticmethod
    def _get_dates_between(start_date, end_date) -> List[datetime.date]:
        """
            Generating dates for given start and end date
        :param start_date:
        :param end_date:
        :return:
        """
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        num_days = (end_date - start_date).days + 1
        return [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in
                range(num_days)]

    @staticmethod
    def _list_objects_from_s3(bucket_name: str, prefix: str = "",
                              include: List[str] = ["*"],
                              exclude: List[str] = ["*"]) -> List[str]:
        """
            fetching data from AWS
        :param bucket_name:
        :param prefix:
        :param include:
        :param exclude:
        :return:
        """

        command = f"""aws s3 cp "s3://{bucket_name}/{prefix}" "." --recursive --request-payer --dryrun"""
        command += f""" {' '.join([f'--exclude "{exclude_}"' for exclude_ in exclude])}"""
        command += f""" {' '.join([f'--include "{include_}"' for include_ in include])}"""

        process = Popen(command, shell=True, stdout=PIPE)
        stdout, _ = process.communicate()
        pattern = r"(?<=download: ).+?(?= to)"

        return re.findall(pattern, stdout.decode("utf-8"))

    def list_filenames_with_date(self, bucket_name: str, prefix: str,
                                 start_date: str, end_date: str,
                                 include: List[str] = [""],
                                 exclude: List[str] = ["*"],
                                 ) -> List[str]:
        """
            generating dates for start and end date, fetching data from AWS
        :param bucket_name:
        :param prefix:
        :param start_date:
        :param end_date:
        :param include:
        :param exclude:
        :return:
        """

        includes = [f"*{date.replace('-', '')}*" for date in
                    self._get_dates_between(start_date, end_date)]
        if include:
            includes = include + includes

        return self._list_objects_from_s3(bucket_name, prefix, includes,
                                          exclude)
