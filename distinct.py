from lib import *

# ==============================================================================
# CREATE CLI
# ==============================================================================
@click.command()
@click.option('--db', prompt='db')
@click.option('--collection', prompt='collection')
@click.option('--field', prompt='field')
@click.option('--count', is_flag=True)
def query_mongodb_collection_names(db, collection, field, count):
    logger.info(f"Querying MongoDB | {db}")

    # ---- attempt to initialize collection
    logger.info("Connecting to MongoDB")
    client = pymongo.MongoClient(MONGODB_ENDPOINT_URL)
    db_ = client[db]
    collection_ = db_[collection]

    # get distinct values for field
    cursor = collection_.distinct(key=field)
    print(cursor)

    # print count of distinct values if requested
    if count:
        print(f"Total distinct values: {len(cursor)}")

# ---- make this script executable
if __name__ == '__main__':
    query_mongodb_collection_names()