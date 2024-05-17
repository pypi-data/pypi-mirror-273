import datetime
import re
from pathlib import PosixPath
from typing import List, Tuple

from google.cloud import storage
from google.oauth2 import service_account

from satelite.config import GCP_BASE_URL, key_json, S3_L1C_BUCKET
from satelite.core.downloader import Downloader
from satelite.models.s2_enum import ProcessingLevel, BaseBands


class S2L1CUrls:
    """
        This class used to fetch L1C urls from given tile code and from date
    """

    @staticmethod
    def _query_sentinel2_using_gcs(tile_code: str,
                                   from_date: datetime.date) -> List[str]:
        """
         Query Sentinel-2 data using Google Cloud Storage (GCS).

        This method retrieves manifest files for Sentinel-2 tiles within the specified
        tile codes and available dates from the GCS bucket "gcp-public-data-sentinel-2."
        The manifest files provide metadata for Sentinel-2 scenes.

        :param tile_code:
        :param from_date:
        :return:
        """
        credentials = service_account.Credentials.from_service_account_file(
            key_json)
        gcs = storage.Client(credentials=credentials)
        gcs_bucket = gcs.get_bucket(S3_L1C_BUCKET)
        prefix = f"tiles/{tile_code[:2]}/{tile_code[2]}/{tile_code[-2:]}/"
        blobs = gcs_bucket.list_blobs(
            max_results=10000, prefix=prefix, delimiter="/")
        next(blobs, ...)
        date = str(from_date).replace("-", "")
        manifest_files = [
            f"{ GCP_BASE_URL}{S3_L1C_BUCKET}/{blob}manifest.safe"
            for blob in blobs.prefixes if date in blob
        ]

        return manifest_files

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

        manifest_files = self._query_sentinel2_using_gcs(tile_code, from_date)

        to_download = []
        for manifest_file in manifest_files:
            fetch_request = Downloader.retry_request(10)
            manifest = fetch_request.get(manifest_file).text
            to_download_bands = []
            for band in bands:
                to_download_bands += re.findall(
                    f"GRANULE/L1C.{{32}}IMG_DATA.{{24}}{band}\.jp2",
                    manifest
                )
            to_download_bands = [
                f"{manifest_file.replace('manifest.safe', '')}{band_path}"
                for band_path in to_download_bands
            ]
            to_download += to_download_bands

        return to_download
