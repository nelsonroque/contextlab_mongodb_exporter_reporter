# Create a virtual environment and install the required packages
python3 -m venv venv
source venv/bin/activate
pip install python-dotenv pymongo pymongo[srv] click boto3
source venv/bin/activate

# To encrypt data in transit when working with DocumentDB, download the public key for Amazon DocumentDB
# https://docs.aws.amazon.com/documentdb/latest/developerguide/connect_programmatically.html
wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem