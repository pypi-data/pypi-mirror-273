from enum import Enum


class BaseBands(Enum):
    """ sentinel2 l1a and l1c base bands
    """
    L1C = ("B02", "B03", "B04", "B05", "B06", "B07", "B08", "B11", "B12")
    L2A = ("B02", "B03", "B04", "B05", "B06", "B07", "B08", "B11", "B12", "SCL")


class ProcessingLevel(Enum):
    """
        sentinel2 image processing levels
    """
    L1C = "L1C"
    L2A = "L2A"
