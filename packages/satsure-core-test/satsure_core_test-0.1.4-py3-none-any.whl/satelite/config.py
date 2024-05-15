import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


class DBSession:
    @staticmethod
    def create():
        DB_HOST = os.environ["DB_HOST"]
        DB_PORT = os.environ["DB_PORT"]
        DB_USERNAME = os.environ["DB_USERNAME"]
        DB_PASSWORD = os.environ["DB_PASSWORD"]
        DB_DATABASE = os.environ["DB_DATABASE"]

        DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
        engine = create_engine(DATABASE_URL)
        instance = sessionmaker(bind=engine)

        return instance()


STAC_URL = "https://earth-search.aws.element84.com/v0"
GCP_BASE_URL = "https://storage.googleapis.com/"
project_id = "satsure-sip-367805"
key_json = str(Path(__file__).parent.resolve() / "gcp.json")

S3_L2A_BUCKET = 'sentinel-cogs'
S3_L2A_PREFIX = 'sentinel-s2-l2a-cogs'

S3_L1C_BUCKET = "gcp-public-data-sentinel-2"
