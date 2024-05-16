from pathlib import Path

from satelite.sentinel2.indices.general_indices import GeneralIndices

import pytest


@pytest.skip("need to rewrite")
class TestGeneralIndices:

    def test_general_indices(self):
        base_path = "/home/ubuntu/"
        date = "2024-03-29"
        level = "L2A"
        input_folder = Path(base_path, level, date.replace("-", ""))
        product_code = "IS18021"
        params = {'band_A_identifier': 'B04', 'band_B_identifier': 'B08',
                  'tile_identifier_position': 1, 'file_name_delimiter': '_',
                  'date_identifier_position': 0, 'band_combination_id': '8',
                  'input_file_format': 'tif',
                  'cloud_mask_bands': ('B02', 'B03'),
                  'cloud_mask_threshold': (3600, 3800),
                  'cloud_mask_output_folder': 'IS18021', 'file_version': '1'}

        obj = GeneralIndices(input_folder, f"{base_path} / {product_code}",
                             "L2a")
        obj.create_s2_normalised_index(**params)
