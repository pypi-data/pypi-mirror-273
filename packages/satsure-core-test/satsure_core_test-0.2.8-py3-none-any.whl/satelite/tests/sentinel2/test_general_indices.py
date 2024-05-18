import glob
import os
from pathlib import Path

import pytest

from satelite.sentinel2.indices.general_indices import GeneralIndices


@pytest.mark.skip("need to add tiff files")
class TestGeneralIndices:
    """Testcase for General Indices """

    def test_general_indices(self):
        """ test

        :return:
        """
        base_path = "/Users/meenakshisundaram/Documents/airflow-dags-file/L2A/20240329"
        input_folder = Path(base_path)
        product_code = "IS18021"
        params = {'band_A_identifier': 'B04', 'band_B_identifier': 'B08',
                  'tile_identifier_position': 1, 'file_name_delimiter': '_',
                  'date_identifier_position': 0, 'band_combination_id': '8',
                  'input_file_format': 'tif',
                  'cloud_mask_bands': ('B02', 'B03'),
                  'cloud_mask_threshold': (3600, 3800),
                  'cloud_mask_output_folder': 'IS18021', 'file_version': '1'}

        obj = GeneralIndices(input_folder, f"{base_path}/{product_code}",
                             "L2A")
        obj.create_s2_normalised_index(**params)

        pattern = os.path.join(
            '/Users/meenakshisundaram/Documents/airflow-dags-file/IS18021/T43PCT/',
            "*.tif")
        result = glob.glob(pattern)

        assert len(result) == 1
