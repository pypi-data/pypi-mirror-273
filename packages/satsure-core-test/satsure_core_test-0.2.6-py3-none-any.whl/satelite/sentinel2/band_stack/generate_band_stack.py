from pathlib import Path, PosixPath
from typing import Tuple

from satelite.gdal.gdal_commands import create_jpeg_image
from satelite.raster.raster import merge


class GenerateBandStack:
    """
    Stack bands based band input
    """
    BANDS = ("B02", "B03", "B04", "B08", "B12")

    def __init__(self, input_folder: PosixPath,
                 output_folder: PosixPath,
                 bands: Tuple[str] = None,
                 tile_identifier_position: int = 1, ):

        self.input_folder = input_folder
        self.output_folder = output_folder
        self.bands = bands or self.BANDS
        self.tile_identifier_position = tile_identifier_position

    def create_fcc(self, file_name_delimiter: str = "_",
                   date_identifier_position: int = 0,
                   band_combination_id: int = 1,
                   create_jpeg: bool = False,
                   rgb_bands_position: Tuple[int, int, int] = (3, 2, 1),
                   input_file_format: str = "jp2",
                   file_version: str = "0"
                   ):
        """
            Stack bands based band input
        :param file_name_delimiter:
        :param date_identifier_position:
        :param band_combination_id:
        :param create_jpeg:
        :param rgb_bands_position:
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
                    self.tile_identifier_position])

        for unique_tile in unique_tiles:
            files = []
            for band in self.bands:
                files += list(input_folder.glob(
                    f"*{unique_tile}*{band}*.{input_file_format}"))
            if files:
                date = files[0].stem.split(file_name_delimiter)[
                           date_identifier_position][:8]
                output_folder = Path(f"{self.output_folder}/{unique_tile}")
                fcc_path = merge(
                    files,
                    output_folder=output_folder,
                    output_name=f"{date}_{unique_tile}_IS{len(files)}{band_combination_id}01{file_version}.tif",
                    output_nodata_value=0,
                    keep_separate=True,
                    output_format="COG",
                    output_datatype="unit16",
                    output_crs=None,
                    output_pixel_size=(10, 10),
                    creation_option="COMPRESS=LZW",
                )
                if create_jpeg and fcc_path:
                    create_jpeg_image(fcc_path,
                                      bands_position=rgb_bands_position)
