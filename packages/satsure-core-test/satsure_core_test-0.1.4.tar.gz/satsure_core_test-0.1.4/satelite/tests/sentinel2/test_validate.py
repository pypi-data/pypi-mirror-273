from pathlib import Path

import pytest

from satelite.core.downloader import Downloader


class TestDownloader:

    def test_validate_fields(self):
        """Testcase to validate input params
        """
        params = {"tile_code": "34dse",
                  "from_date": "2023-05-04",
                  "download_path": Path("satelite.tests/sentinels"),
                  "bands": ("B01",)}

        errors = {"tile_code": (
            f"tile_codes expected a non empty str, got {type([])}",
            [], TypeError),
            "from_date": (
                f"from_date expected a string of form: YYYY-MM-DD, got {type(12)}",
                12, TypeError),
            "download_path": (
                f"download_path expected a PosixPath, got {type('str')}",
                "path", TypeError),

            "bands": (
                f"bands expected a tuple / list, got {type('str')}",
                "path", TypeError),

        }

        for error in errors:
            current = params.copy()
            assert_val, value, err_type = errors[error]
            current[error] = value
            with pytest.raises(err_type) as exc_info:
                Downloader.validate_fields(**current)

            assert str(exc_info.value) == assert_val

    def test_retry_request(self):
        """
         Testcase for retry request
        """
        result =Downloader.retry_request(5)

        assert result.adapters["http://"].max_retries.total == 5
        assert result.adapters["https://"].max_retries.total == 5

