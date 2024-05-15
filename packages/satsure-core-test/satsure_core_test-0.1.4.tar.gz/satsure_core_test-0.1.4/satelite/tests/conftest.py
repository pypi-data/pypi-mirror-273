from pathlib import Path

import pytest


@pytest.fixture
def polygon_list() -> list:
    """This fixture returns polygon list"""
    polygon = [
        {
            "type": "Polygon",
            "coordinates": [
                [
                    [74.66218437999487, 19.46556170905807],
                    [74.6629598736763, 19.466339343697722],
                    [74.6640371158719, 19.4667885366414],
                    [74.66395296156406, 19.46614872872264],
                    [74.66376889497042, 19.466150941501425],
                    [74.66369077563286, 19.46577508478787],
                    [74.6635865047574, 19.465278788212864],
                    [74.66282073408365, 19.46540270444271],
                    [74.66218437999487, 19.46556170905807],
                ]
            ],
        }
    ]

    return polygon


@pytest.fixture
def datadir(tmp_path):
    """Fixture to provide access to the test data directory."""
    return Path(__file__).parent / "raster" / "testdata"
