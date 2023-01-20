import logging  # for logging
import os  # for environment variables
from dotenv import load_dotenv  # for loading environment variables
import json  # for JSON
import pymongo  # for MongoDB
from bson import json_util  # for converting BSON to JSON
import boto3  # for AWS S3
import click  # for CLI
from datetime import datetime  # for timestamps

# ==============================================================================
# LOGGING
# ==============================================================================

# ---- TODO: eventually log to cloudtrail
logging.basicConfig(level=logging.DEBUG,
                    format="[TS: %(asctime)s]\t[NAME: %(name)s]\t[LEVEL: %(levelname)s]\t[MODULES: %(module)s]\t[FUNCTION: %(funcName)s]\t[MSG: %(message)s]")
logger = logging.getLogger("contextlab-data-warehouse-exporter")

# ==============================================================================
# CONSTANTS
# ==============================================================================

# ---- Load environment variables
load_dotenv()
logger.info("Loaded .env file")

# ---- DEBUGGING ----------------------------------------------------------------
DEBUG_FLAG = False

# ---- APP CONFIG ----------------------------------------------------------------
APP_NAME = os.getenv("APP_NAME")
APP_VERSION = os.getenv("APP_VERSION")
APP_DEPLOYMENT = os.getenv("APP_DEPLOYMENT")

# ---- SPECIFY COLLECTIONS/TABLES
COLLECTION_DATA = os.getenv("COLLECTION_DATA")

# DB CONFIG --------------------------------------------------------

# ---- deployment: dev
DEV_DB_USERNAME = os.getenv("DEV_DB_USERNAME")
DEV_DB_PASSWORD = os.getenv("DEV_DB_PASSWORD")
DEV_DB_CLUSTERID = os.getenv("DEV_DB_CLUSTERID")
DEV_DB_RETRYWRITES = os.getenv("DEV_DB_RETRYWRITES")

# ---- deployment: production
PROD_DB_USERNAME = os.getenv("PROD_DB_USERNAME")
PROD_DB_PASSWORD = os.getenv("PROD_DB_PASSWORD")
PROD_DB_CLUSTERID = os.getenv("PROD_DB_CLUSTERID")
PROD_DB_RETRYWRITES = os.getenv("PROD_DB_RETRYWRITES")

# specify database name
DATA_DB = os.getenv("DATA_DB")

# ---- AWS CONFIG
AWS_REGION = os.getenv("AWS_REGION")

# DEPLOYMENT PROFILES ----------------------------------------------------------------

# ---- set AWS deployment profile based on deployment
AWS_REGION = os.getenv("AWS_REGION")

# TODO: def get_deployment_profile("dev"):
if APP_DEPLOYMENT == "dev":
    AWS_UPLOAD_BUCKET = os.getenv("DEV_AWS_UPLOAD_BUCKET")
    AWS_SERVER_PUBLIC_KEY = os.getenv("DEV_AWS_SERVER_PUBLIC_KEY")
    AWS_SERVER_SECRET_KEY = os.getenv("DEV_AWS_SERVER_SECRET_KEY")
    MONGODB_ENDPOINT_URL = f"mongodb+srv://{DEV_DB_USERNAME}:{DEV_DB_PASSWORD}@{DEV_DB_CLUSTERID}/?retryWrites=true&w=majority"
elif APP_DEPLOYMENT == "production":
    AWS_UPLOAD_BUCKET = os.getenv("PROD_AWS_UPLOAD_BUCKET")
    AWS_SERVER_PUBLIC_KEY = os.getenv("PROD_AWS_SERVER_PUBLIC_KEY")
    AWS_SERVER_SECRET_KEY = os.getenv("PROD_AWS_SERVER_SECRET_KEY")
    DOCDB_RETRYWRITES = os.getenv("PROD_DOCDB_RETRYWRITES")
    MONGODB_ENDPOINT_URL = f"mongodb://{PROD_DB_USERNAME}:{PROD_DB_PASSWORD}@{PROD_DB_CLUSTERID}:27017/?tls=true&tlsCAFile=rds-combined-ca-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites={DOCDB_RETRYWRITES}"

logger.info("All constants read")
logger.info("App deployment: " + APP_DEPLOYMENT)

# ==============================================================================
# FUNCTIONS
# ==============================================================================
# ---- Get the current timestamp in filename-friendly format
def get_fn_ts():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return timestamp
