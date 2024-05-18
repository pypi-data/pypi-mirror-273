import datetime
from pathlib import Path

from satelite.sentinel2 import S2L2AUrls


class TestS2L2AUrls:

    def test_get_urls(self, monkeypatch):
        """
            Testcase to check get_urls data
        :param monkeypatch:
        :return:
        """
        params = {"tile_code": "43QDB",
                  "from_date": "2023-05-04",
                  "download_path": Path("sample/temp")}

        obj = S2L2AUrls()
        result = obj.get_urls(**params)

        assert len(result) > 0

    def test_query_sentinel_2_using_s3(self):
        params = {"tile_code": "43QDB",
                  "from_date": datetime.datetime.strptime("2023-05-04",
                                                          "%Y-%m-%d").date()}

        obj = S2L2AUrls()
        s2_data = obj._query_sentinel_2_using_s3(**params)

        assert "43QDB" in s2_data[0]
        assert "L2A" in s2_data[0]
