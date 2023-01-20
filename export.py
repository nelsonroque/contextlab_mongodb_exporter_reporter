from lib import *

# ==============================================================================
# CREATE CLI
# ==============================================================================
@click.command()
@click.option('--save_s3', help=f'Save to AWS S3 Bucket {AWS_UPLOAD_BUCKET}? (y/n)', is_flag=True)
@click.option('--save_disk', help=f'Save to disk? (y/n)', is_flag=True)
@click.option('--db', prompt='db')
@click.option('--collection', prompt='collection')
def query_mongodb(db, collection, save_s3, save_disk):
    logger.info(
        f"Querying MongoDB | {db} | {collection}")
    click.echo(f"Database: {db}")
    click.echo(f"Collection: {collection}")

    # ---- create filename based on query
    fn = f"{get_fn_ts()}-db-{db}_collection-{collection}.json"

    # ---- attempt to initialize collection
    logger.info("Connecting to MongoDB")
    client = pymongo.MongoClient(MONGODB_ENDPOINT_URL)
    db_ = client[db]
    collection_ = db_[collection]

    # ---- query collection
    logger.info(f"About to query collection {collection}")
    cursor = collection_.find()

    # ---- iterate through cursor and append to list
    all_documents = []
    for document in cursor:
        all_documents.append(document)

    # ---- print results summary
    logger.info(f"Query complete!")
    logger.info(f"Total records returned:  {len(all_documents)}")

    # ---- dump all results to json (default = bson.json_util.default)
    all_documents_json = json.dumps(
        all_documents, default=json_util.default, indent=4)

    # ---- save json to AWS S3 Bucket
    if save_s3:
        logger.info(f"Saving to AWS S3 Bucket {AWS_UPLOAD_BUCKET}")
        s3 = boto3.client('s3',
                          aws_access_key_id=AWS_SERVER_PUBLIC_KEY,
                          aws_secret_access_key=AWS_SERVER_SECRET_KEY,
                          region_name=AWS_REGION)
        s3.put_object(Body=(bytes(all_documents_json.encode('UTF-8'))),
                      Bucket=AWS_UPLOAD_BUCKET, Key=fn)
        logger.info(
            f"Records written to S3 Bucket file: s3://{AWS_UPLOAD_BUCKET}/{fn}")

    # ---- save json to local file store
    if save_disk:
        logger.info(f"Saving to file {fn}")
        with open(f"data/{fn}", 'w') as outfile:
            json.dump(all_documents, outfile,
                      default=json_util.default, indent=4)
        logger.info(f"Records written to file: {fn}")

# ---- make this script executable
if __name__ == '__main__':
    query_mongodb()