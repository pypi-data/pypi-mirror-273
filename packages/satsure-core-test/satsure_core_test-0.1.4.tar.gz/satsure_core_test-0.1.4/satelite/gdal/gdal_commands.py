import re
import subprocess
from pathlib import PosixPath
from typing import Optional, Tuple


def create_jpeg_image(
        input_file: PosixPath,
        output_file: Optional[str] = None,
        bands_position: Tuple[int, int, int] = (3, 2, 1),
        quality: int = 10,
        target_resolution: int = 100,
):
    """Generates JPG image for a given tif

    Args:
        input_file (PosixPath): Path of the input file
        output_file (Optional[PosixPath], optional): Output path for the file. If not proivded, defaults to input file by changing extension. Defaults to None.
        quality (int): Compression ratio. (how much you want to compress)
        bands_position (Iterable[int, int, int], optional): List of rgb bands to use. Defaults to (3, 2, 1).
        target_resolution (int, optional): Target resolution. Defaults to 100.
    """
    if output_file is None:
        output_file = f"{str(input_file)[:-4]}.jpg"

    command = ("gdal_translate", "-of", "JPEG", "-scale", "-ot", "Byte")
    for band in bands_position:
        command += ("-b", f"{band}")
    command += (
        "-tr",
        f"{target_resolution}",
        f"{target_resolution}",
        "-co",
        f"QUALITY={int(quality)}",
        f"{input_file}",
        f"{output_file}",
    )
    subprocess.run(command, shell=False, capture_output=True)


def reproject(
        input_file: PosixPath,
        output_file: PosixPath,
        target_crs: str) -> None:
    """
     reproject the given polygon file
    :param input_file:
    :param output_file:
    :param target_crs:
    :return:
    """
    command = (
        "gdalwarp", "-t_srs", f"{target_crs}", f"{input_file}",
        f"{output_file}")
    subprocess.run(command, shell=False, capture_output=True)


def get_projection(file_path: str) -> str:
    """
    Function to get projection of file (Vector / Raster)
    Currently supports only EPSG based projections
    :param file_path:
    :return:
    """
    command = f"gdalsrsinfo {file_path} -e"
    projection_str = subprocess.check_output(
        command, stderr=subprocess.STDOUT, shell=True)

    if "error" in projection_str.decode("utf-8")[:20].lower():
        raise Exception(projection_str.decode("utf-8"))

    projection_code = re.findall(rb"\nEPSG:(.+?)\n", projection_str)
    if not projection_code:
        raise Exception(
            "Cannot find projection, currently supports only " "EPSG based projections"
        )

    return f"EPSG:{projection_code[0].decode('utf-8')}"
