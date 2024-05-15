import os
from os import environ

import fiona
import pyproj
import rasterio
from fiona.session import AWSSession as FAWSSession
from rasterstats import zonal_stats
from shapely.geometry import shape
from shapely.ops import transform


class CheckShapeOfRID:
    """
        To check tile in particular area
    """

    @staticmethod
    def main(rid, file_path, s3_folder_shapefile):
        """
            This method used to check shape of RID
        :param file_path:
        :param s3_folder_shapefile:
        :return:
        """
        # Set your AWS credentials and region

        fio_aws_session = FAWSSession(
            aws_access_key_id=environ.get('AWS_ACCESS_KEY_ID', "None"),
            aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY', "None"),
            requester_pays=True,
            region_name=environ.get('AWS_DEFAULT_REGION', "None")
        )
        # Configure the AWS session

        shp = f's3://satsure-immutables/{s3_folder_shapefile}/{rid}.shp'
        # S3 object URL
        FioSession = fiona.Env(session=fio_aws_session)
        os.environ['AWS_REQUEST_PAYER'] = 'requester'
        # Open the raster dataset using rasterio with the AWS session and requester payer set
        with rasterio.open(file_path, 'r') as src:
            affine = src.transform
            array = src.read(1)
            image_crs = str(src.crs)
            resolution_x = src.transform[0]
            resolution_y = src.transform[4]
            with FioSession:
                with fiona.open(shp) as geom:
                    wgs84 = pyproj.CRS(geom.crs)
                    utm = pyproj.CRS(image_crs)
                    project = pyproj.Transformer.from_crs(wgs84, utm,
                                                          always_xy=True).transform
                    geometry = shape(geom[0]['geometry'])
                    utm_geom = transform(project, geometry)
            stats = zonal_stats(utm_geom, array, affine=affine, nodata=0,
                                all_touched=True)
            total_count = stats[0]['count']
            area = abs(
                (resolution_x * resolution_y * total_count) / 1000000)
            vector_area = utm_geom.area / 1000000
            raster_area = area
            if abs(vector_area - raster_area) < 20:
                return rid
            else:
                return None
