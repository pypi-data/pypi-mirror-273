from os import environ

import fiona
from fiona.session import AWSSession
from sqlalchemy import text

from satelite.config import DBSession


class GetTiles:
    """To get tiles from different resources"""

    def __init__(self):
        self.db = DBSession.create()

    def fetch_tile_from_db(self, sql_query, geom_):
        """
            Fetch tile from database
        :param sql_query:
        :param geom_:
        :return:
        """

        result = self.db.execute(sql_query,
                                 {"geojson_geometry": str(geom_)})
        return result.fetchall()

    def get_tile_from_geom(self, geom_list: list) -> list:
        """generate tile from in geom
        :rtype: list
        """
        tile_list = set()
        sql_query = text(
            f"""SELECT tile FROM tileids WHERE ST_Intersects( geometry,
                                            ST_GeomFromGeoJSON(:geojson_geometry)) """
        )

        for geom_ in geom_list:
            rows = self.fetch_tile_from_db(sql_query, geom_)
            for row in rows:
                tile_list.add(row[0])

        tile_list = list(tile_list)
        self.db.close()

        return tile_list

    def get_tile_from_rids(self, rids: list, shape_path: str):
        """To get tiles from rids
        :param rids:
        :param shape_path:
        :return: list
        """
        master_tile_list = []

        for region_ in rids:
            with fiona.Env(
                    session=AWSSession(
                        aws_access_key_id=environ.get(
                            "AWS_ACCESS_KEY_ID", None
                        ),
                        aws_secret_access_key=environ.get(
                            "AWS_SECRET_ACCESS_KEY", None
                        ),
                        requester_pays=True,
                        region_name=environ.get(
                            "AWS_DEFAULT_REGION", None
                        ),
                    )
            ) as env:
                with fiona.open(
                        f"s3://satsure-immutables/{shape_path}/{region_}.shp"
                ) as src:
                    bbox = src.bounds

                sql_query = text(
                    """SELECT tile FROM tileids
                                    WHERE ST_Intersects(
                                        geometry,
                                        ST_MakeEnvelope(:minx, :miny, :maxx, :maxy, 4326) -- 4326 is the SRID, adjust if needed
                                    )
                                    """
                )
                result = self.db.execute(
                    sql_query,
                    {
                        "minx": bbox[0],
                        "miny": bbox[1],
                        "maxx": bbox[2],
                        "maxy": bbox[3],
                    },
                )
                rows = result.fetchall()
                tile_list = []
                for row in rows:
                    tile_list.append(row[0])
                master_tile_list.extend(tile_list)

        self.db.close()
        master_tile_list = list(set(master_tile_list))

        return master_tile_list
