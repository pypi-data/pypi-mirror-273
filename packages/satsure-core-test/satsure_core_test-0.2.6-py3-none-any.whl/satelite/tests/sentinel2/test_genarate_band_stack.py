import glob
import os
from pathlib import Path

import pytest

from satelite.sentinel2.band_stack.generate_band_stack import GenerateBandStack


@pytest.mark.skip("need to do upload tif files")
class TestGenerateBandStack:

    def test_create_fcc(self):
        """
            Testcase for create fcc method
        :return:
        """

        base_path = "/Users/meenakshisundaram/Documents/airflow-dags-file"
        input_folder = Path(base_path)
        product_code = "IS51011"
        obj = GenerateBandStack(input_folder, f"{base_path}/{product_code}",
                                ("B02", "B03", "B04", "B08", "B12"))
        obj.create_fcc(input_file_format="tif", file_version="1",
                       create_jpeg=True)

        tif_pattern = os.path.join(
            '/Users/meenakshisundaram/Documents/airflow-dags-file/IS51011/T43PCT/',
            "*.tif")
        img_pattern = os.path.join(
            '/Users/meenakshisundaram/Documents/airflow-dags-file/IS51011/T43PCT/',
            "*.jpg")
        tif_file = glob.glob(tif_pattern)
        img_file = glob.glob(img_pattern)

        assert len(tif_file) == 1
        assert len(img_file) == 1
