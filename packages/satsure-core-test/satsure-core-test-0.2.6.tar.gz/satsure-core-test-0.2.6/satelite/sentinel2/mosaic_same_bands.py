from pathlib import Path, PosixPath
from typing import List

from satelite.raster.raster import merge


class MosaicSameBands:
    """
    Stack similar bands on same date
    """
    BANDS = ("B02", "B03", "B04", "B05", "B08", "B12",)

    def __init__(self, input_folder: PosixPath,
                 output_folder: PosixPath,
                 bands: List[str] = None,
                 tile_identifier_position: int = 1):

        self.input_folder = input_folder
        self.output_folder = output_folder
        self.bands = bands or self.BANDS
        self.tile_identifier_position = tile_identifier_position

    def mosaic_same_bands(self, file_name_delimiter: str = "_",
                          date_identifier_position: int = 0,
                          input_file_format: str = "jp2") -> None:
        """
            mosaic same bands on same date

        :param file_name_delimiter:
        :param date_identifier_position:
        :param input_file_format:
        :return:
        """
        input_folder = Path(self.input_folder)
        files = input_folder.glob(f"*.{input_file_format}")
        unique_tiles = set()
        for file in files:
            unique_tiles.add(
                file.stem.split(file_name_delimiter)[
                    self.tile_identifier_position])
        for band in self.bands:
            for unique_tile in unique_tiles:
                files = list(input_folder.glob(
                    f"*{unique_tile}*{band}.{input_file_format}"))
                if len(files) < 1:
                    continue
                files.sort()
                date = files[0].stem.split(file_name_delimiter)[
                           date_identifier_position][:8]
                creation_option = None
                if input_file_format == "tif":
                    creation_option = "COMPRESS=LZW"
                merge(
                    files,
                    output_folder=str(self.output_folder),
                    output_name=f"{date}_{unique_tile}_{band}.{input_file_format}",
                    output_nodata_value=0,
                    keep_separate=False,
                    output_format=None,
                    output_datatype=None,
                    output_crs=None,
                    output_pixel_size=(10, 10),
                    creation_option=creation_option
                )

                for file in files:
                    print(file.name, f"{date}_{unique_tile}_{band}.{input_file_format}","pacakes")
                    print(file.name == f"{date}_{unique_tile}_{band}.{input_file_format}", "this assert")
                    if file.name == f"{date}_{unique_tile}_{band}.{input_file_format}":
                        continue
                    print("file unlink",file)
                    file.unlink()
