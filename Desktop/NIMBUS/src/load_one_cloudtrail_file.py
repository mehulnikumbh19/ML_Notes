# pathlib gives Python a clean way to point at files and folders.
from pathlib import Path

# gzip lets Python open compressed files that end in .gz.
import gzip

# json lets Python turn JSON text into Python dictionaries and lists.
import json


# This path points to the one CloudTrail file we downloaded by hand.
LOG_FILE_PATH = Path("data/raw/sample-cloudtrail.json")


# This function hides the file-opening detail so main() stays easy to read.
def load_cloudtrail_file(file_path):
    # This check gives a friendly error if the file is missing.
    if not file_path.exists():
        # FileNotFoundError is Python's standard error for a missing file.
        raise FileNotFoundError(f"Could not find the file: {file_path}")

    # CloudTrail files often end in .json.gz because AWS compresses them.
    if file_path.suffix == ".gz":
        # gzip.open reads compressed text when we pass mode="rt".
        with gzip.open(file_path, mode="rt", encoding="utf-8") as log_file:
            # json.load reads JSON from an open file object.
            return json.load(log_file)

    # This branch handles regular .json files like our current sample file.
    with file_path.open(mode="r", encoding="utf-8") as log_file:
        # json.load turns the JSON text into Python data.
        return json.load(log_file)


# main() is the starting point for this script's work.
def main():
    # Load the CloudTrail file into a Python dictionary.
    cloudtrail_data = load_cloudtrail_file(LOG_FILE_PATH)

    # json.dumps turns Python data back into nicely formatted JSON text.
    pretty_json = json.dumps(cloudtrail_data, indent=2)

    # print sends the formatted JSON to the terminal so we can inspect it.
    print(pretty_json)


# This line makes main() run only when this file is executed directly.
if __name__ == "__main__":
    # Calling main() starts the script.
    main()
