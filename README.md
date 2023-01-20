# contex: A pymongo-based MongoDB exporter tool

## Requirements

- Python 3.7+
- `venv` = [Creation of virtual environments](https://docs.python.org/3/library/venv.html)

## Configuration

1. Run `./create_venv.sh`.
2. Modify `sample.env` as needed.
3. Run any of the python files for a different CLI experience, with any parameters you need for your use case, e.g., `python distinct.py --db data-db --collection data --field uid`
   1. `distinct.py` to get unique values for a field
      1. `python distinct.py --db data-db --collection data --field uid`
   2. `metadata.py` to get collection names in a database
      1. `python metadata.py --db data-db`
   3. `export.py` to export data as JSON to disk and/or AWS S3
      1. `save_disk` to save the JSON output to a `data` folder within this directory.
      2. `save_s3` to save to the S3 bucket specified in the `.env` file.