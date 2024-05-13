from satelite.sentinel2 import FetchUniqueTileDate


class TestFetchUniqueTileDate:

    def test_get_unique_tile_date(self):
        """Testcase for fetching features using tile list"""
        obj = FetchUniqueTileDate("0,100", "2024-03-01",
                                  "2024-04-02", "l1c")
        result = obj.get_unique_tile_date(["43QCU"])

        assert len(result) > 0
