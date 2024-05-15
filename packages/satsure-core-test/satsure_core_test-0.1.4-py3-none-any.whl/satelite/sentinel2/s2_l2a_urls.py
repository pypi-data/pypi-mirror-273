import datetime
from pathlib import PosixPath
from subprocess import PIPE, Popen
from typing import List, Tuple

from satelite.config import S3_L2A_BUCKET, S3_L2A_PREFIX
from satelite.models.s2_enum import ProcessingLevel, BaseBands
from satelite.core.downloader import Downloader


class S2L2AUrls:
    """
        This class used to fetch L2A urls from given tile code and from date
    """

    @staticmethod
    def _query_sentinel_2_using_s3(tile_code: str,
                                  from_date: datetime.date) -> List[str]:
        """
        Query Sentinel-2 data using AWS S3 for specified tile codes and date range.
        This function queries an AWS S3 bucket for Sentinel-2 data based on tile codes
        and a specified date range. It constructs S3 prefixes based on the tile codes
        and retrieves relevant folders matching the date range within the specified
        S3 bucket.

        :param tile_code:
        :param from_date:
        :return:
        """
        s3_prefix = (
            f"{S3_L2A_PREFIX}/{int(tile_code[:2])}/{tile_code[2]}/"
            f"{tile_code[-2:]}/{from_date.year}/{from_date.month}/"
        )

        command = f"aws s3 ls s3://{S3_L2A_BUCKET}/{s3_prefix}"
        process = Popen(command, shell=True, stdout=PIPE)
        stdout, _ = process.communicate()
        if not stdout.decode("utf-8"):
            return []

        folders = [
            name.strip() for name in stdout.decode("utf-8").split("PRE")
            if from_date.strftime('%Y%m%d') in name.strip()
        ]

        s2_data = []
        if folders:
            for folder in folders:
                s2_data.append(f"{s3_prefix}{folder}")

        return s2_data

    def get_urls(self, tile_code: str, from_date: str,
                 download_path: PosixPath,
                 bands: Tuple[str] = None) -> List[str]:
        """
        Download Sentinel-2 data for a specified date.
        This method downloads Sentinel-2 data for the specified date and level (L2A or L1C).
        The downloaded data is organized into folders based on the date and contains the selected
        bands. The download progress is logged.

        :param tile_code:
        :param from_date:
        :param download_path:
        :param bands:
        :return:
        """
        Downloader.validate_fields(tile_code, from_date, download_path, bands)
        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d").date()
        bands = tuple(bands) if bands is not None else BaseBands[
            ProcessingLevel.L2A.value].value

        s2_data = self._query_sentinel_2_using_s3(tile_code, from_date)
        download_urls = []
        for each_required_s2_data in s2_data:
            for band in bands:
                download_urls.append(
                    f"https://{S3_L2A_BUCKET}.s3.amazonaws.com/{each_required_s2_data}{band}.tif")

        return download_urls
