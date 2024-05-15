from satelite.sentinel2 import FetchUniqueTileDatePystac


class TestFetchUniqueTileDatePystac:

    def test_test_get_unique_tile_date(self, polygon_list):
        """Testcase for fetching features using polygons"""

        obj = FetchUniqueTileDatePystac("2023-05-01", "2023-05-30",
                                        "l2a", "0,100")
        result = obj.get_unique_tile_date(polygon_list)

        assert len(result) > 0
