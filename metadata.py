from lib import *

# ==============================================================================
# CREATE CLI
# ==============================================================================
@click.command()
@click.option('--db', prompt='db')
def query_mongodb_collection_names(db):
    logger.info(
        f"Querying MongoDB | {db}")

    # ---- attempt to initialize collection
    logger.info("Connecting to MongoDB")
    client = pymongo.MongoClient(MONGODB_ENDPOINT_URL)
    db_ = client[db]

    # ---- query database for collection names
    logger.info(f"About to query for collection names.")
    rc = db_.list_collection_names()
    collections = ', '.join(rc)
    logger.info(f"Collections: {collections}")
    print(f"Collections: {collections}")
    return rc, collections

# ---- make this script executable
if __name__ == '__main__':
    query_mongodb_collection_names()