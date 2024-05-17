from pathlib import Path

from osgeo import ogr


class PathRowFromSHP:

    @staticmethod
    def process(shp_path, sentinel_wrs2_path=None):
        """
        Get PATH and ROW by reading SHP file
        :param shp_path: path to the SHP file
        :param sentinel_wrs2_path: WRS2_descending file path
        :return: path and row
        """
        shp_path = Path(shp_path)
        if not sentinel_wrs2_path:
            sentinel_wrs2_path = Path(
                Path(
                    __file__).parent / "Sentinel2_tiles" / "wrs_Sentinel2_tiles.shp"
            )
        else:
            sentinel_wrs2_path = Path(sentinel_wrs2_path)

        if not sentinel_wrs2_path.exists():
            raise FileNotFoundError(
                f"sentinel WRS2 Descending Path Row file not found at {sentinel_wrs2_path}"
            )

        tileid = []
        l8_grid = ogr.Open(str(sentinel_wrs2_path))
        shp = ogr.Open(str(shp_path))
        l8_grid_layer = l8_grid.GetLayer(0)
        shp_layer = shp.GetLayer(0)

        # perform intersection of shp and sentinel_wrs2_path to get path row
        for feature1 in l8_grid_layer:
            geom1 = feature1.GetGeometryRef()
            for feature2 in shp_layer:
                geom2 = feature2.GetGeometryRef()
                attribute2 = feature1.GetField("Name")
                # select only the intersections
                if geom2.Intersects(geom1):
                    tileid.append(str(attribute2))

        return tileid
