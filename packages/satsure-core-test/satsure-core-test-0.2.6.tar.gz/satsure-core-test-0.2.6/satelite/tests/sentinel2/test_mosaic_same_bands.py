

from satelite.sentinel2 import MosaicSameBands

class TestMosaicSameBands:


    def test_mosaic_same_bands(self):
        input_path = "satelite/tests/sentinel2/input_path"
        output_path = "satelite/tests/sentinel2/output_path"
        obj =MosaicSameBands(input_path,output_path)
        obj.mosaic_same_bands()
