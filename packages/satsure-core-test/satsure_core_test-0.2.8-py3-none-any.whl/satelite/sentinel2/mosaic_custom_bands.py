from dataclasses import dataclass
from pathlib import Path, PosixPath
from typing import List

from rasterio.merge import merge as rio_merge


@dataclass
class MosaicCustomBands:
    input_files: List[PosixPath]
    output_folder: PosixPath
    output_name: PosixPath
    output_nodata_value: int = 0
    output_datatype: str = "uint8"

    def mosaic_custom(self):
        """
            mosaic custom bands
        :return:
        """
        output_folder = Path(self.output_folder)
        output_folder.mkdir(exist_ok=True, parents=True)
        output_path = Path(f"{output_folder}/{self.output_name}")
        rio_merge(self.input_files,
                  nodata=self.output_nodata_value,
                  dtype=self.output_datatype,
                  method='max',
                  dst_path=output_path
                  )
