from pathlib import Path

from satelite.sentinel2 import S2L1CUrls


class TestS2L1CUrls:

    def test_get_urls(self, monkeypatch):
        """
            Testcase to check get_urls data
        :param monkeypatch:
        :return:
        """
        params = {"tile_code": "43QDB",
                  "from_date": "2023-05-04",
                  "download_path": Path("sample/temp")}

        obj = S2L1CUrls()
        result = obj.get_urls(**params)

        assert len(result) > 0

    def test_query_sentinel2_using_gcs(self):
        """
        Testcase to check query_sentinel2_using_gcs method
        :return:
        """
        params = {"tile_code": "43QDB",
                  "from_date": "2023-05-04"}

        obj = S2L1CUrls()
        result = obj._query_sentinel2_using_gcs(**params)

        assert len(result) > 0
        assert "43QDB" in result[0]
