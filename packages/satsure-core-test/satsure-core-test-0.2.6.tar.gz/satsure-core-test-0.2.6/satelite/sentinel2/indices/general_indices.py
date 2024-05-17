from pathlib import Path, PosixPath
from typing import Tuple

from satelite.raster.raster import create_normalised_difference_index, \
    mask_cloud


class GeneralIndices:
    """
     Create indices based on bands
    """

    def __init__(self, input_folder: PosixPath,
                 output_folder: PosixPath,
                 level: str = "L1C"):

        self.input_folder = input_folder
        self.output_folder = output_folder
        self.level = level

    def create_s2_normalised_index(self,
                                   band_A_identifier: str,
                                   band_B_identifier: str,
                                   tile_identifier_position: int = 1,
                                   file_name_delimiter: str = "_",
                                   date_identifier_position: int = 0,
                                   band_combination_id: str = "8",
                                   input_file_format: str = "jp2",
                                   create_cloud_mask: bool = True,
                                   cloud_mask_bands: Tuple[str] = (
                                           "B02", "B03"),
                                   cloud_mask_threshold: Tuple[int] = (
                                           3200, 3000),
                                   cloud_mask_output_folder: PosixPath = None,
                                   file_version: str = "0"
                                   ):
        """
            Create indices based on bands

        :param band_A_identifier:
        :param band_B_identifier:
        :param file_name_delimiter:
        :param date_identifier_position:
        :param band_combination_id:
        :param create_cloud_mask:
        :param cloud_mask_bands:
        :param cloud_mask_threshold:
        :param cloud_mask_output_folder:
        :param input_file_format:
        :param file_version:
        :return:
        """
        input_folder = Path(self.input_folder)
        files = input_folder.glob(f"*.{input_file_format}")
        unique_tiles = set()
        for file in files:
            unique_tiles.add(
                file.stem.split(file_name_delimiter)[
                    tile_identifier_position])

        for unique_tile in unique_tiles:
            filename_band_A = list(input_folder.glob(
                f"*{unique_tile}*{band_A_identifier}*.{input_file_format}"))
            filename_band_B = list(input_folder.glob(
                f"*{unique_tile}*{band_B_identifier}*.{input_file_format}"))

            if not filename_band_A or not filename_band_B:
                continue

            output_folder = Path(f"{self.output_folder}/{unique_tile}")
            if cloud_mask_output_folder:
                cloud_mask_output_folder = Path(
                    f"{cloud_mask_output_folder}/{unique_tile}")

            date = filename_band_A[0].stem.split(file_name_delimiter)[
                       date_identifier_position][:8]
            index_path = create_normalised_difference_index(
                filename_band_A[0],
                filename_band_B[0],
                output_folder,
                output_name=f"{date}_{unique_tile}_IS1{band_combination_id}01{file_version}.tif")
            if not create_cloud_mask or not index_path:
                continue

            cloud_mask_bands_path = []
            for cloud_mask_band in cloud_mask_bands:
                cloud_mask_bands_path += list(input_folder.glob(
                    f"*{unique_tile}*{cloud_mask_band}.{input_file_format}"))
            if not cloud_mask_bands_path:
                continue

            mask_cloud(
                index_path,
                cloud_mask_output_folder,
                output_name=f"{date}_{unique_tile}_IS1{band_combination_id}02{file_version}.tif",
                cloud_mask_bands=cloud_mask_bands_path,
                cloud_mask_threshold=cloud_mask_threshold,
                level=self.level
            )
