# pathlib gives Python a clean way to point at files and folders.
from pathlib import Path

# json gives us the JSONDecodeError name for broken JSON files.
import json

# load_cloudtrail_file is the helper we wrote in the previous step.
from load_one_cloudtrail_file import load_cloudtrail_file


# This path points to the folder where we save raw CloudTrail files.
RAW_LOG_FOLDER = Path("data/raw")


# This function finds CloudTrail files inside the raw data folder.
def find_cloudtrail_files(folder_path):
    # glob("*.json") finds regular JSON files directly inside the folder.
    json_files = list(folder_path.glob("*.json"))

    # glob("*.json.gz") finds compressed JSON files directly inside the folder.
    gzip_files = list(folder_path.glob("*.json.gz"))

    # Combining both lists lets the rest of the script treat them the same way.
    return json_files + gzip_files


# This function chooses the best human-readable username from one CloudTrail event.
def get_user_name(event):
    # userIdentity is a nested dictionary that describes who made the AWS request.
    user_identity = event.get("userIdentity", {})

    # userName is present for normal IAM users, like our nimbus-student user.
    user_name = user_identity.get("userName")

    # If userName exists, return it because it is the easiest value to read.
    if user_name:
        # Return stops the function and sends this value back to the caller.
        return user_name

    # arn is a longer identity string that can help when userName is missing.
    arn = user_identity.get("arn")

    # If arn exists, return it as a fallback identity label.
    if arn:
        # This fallback keeps the table useful for roles, root, or unusual identities.
        return arn

    # This final fallback makes missing identity data obvious in the output.
    return "UNKNOWN_USER"


# main() is the starting point for this script's work.
def main():
    # Find every CloudTrail file we know how to read in the raw log folder.
    cloudtrail_files = find_cloudtrail_files(RAW_LOG_FOLDER)

    # If there are no files, tell the learner what folder the script checked.
    if not cloudtrail_files:
        # This message is friendlier than printing an empty table with no context.
        print(f"No CloudTrail files found in {RAW_LOG_FOLDER}")

        # return exits main() early because there is nothing else to print.
        return

    # Print a header row so each column has a clear label.
    print(f"{'Timestamp':<22} {'User':<24} {'Action':<28} {'Source IP'}")

    # Print a separator row so the table is easier to scan.
    print("-" * 90)

    # Loop over each file path found in the raw log folder.
    for cloudtrail_file in cloudtrail_files:
        # try starts a block where Python will watch for errors.
        try:
            # Load this CloudTrail file into Python dictionaries and lists.
            cloudtrail_data = load_cloudtrail_file(cloudtrail_file)

        # except runs only if the matching error happens inside the try block.
        except json.JSONDecodeError:
            # This warning helps us skip broken JSON without crashing the whole script.
            print(f"Could not read JSON from {cloudtrail_file}")

            # continue skips to the next file in the loop.
            continue

        # Records is the top-level list where CloudTrail stores individual events.
        records = cloudtrail_data.get("Records", [])

        # Loop over each event dictionary inside the Records list.
        for event in records:
            # eventTime tells us when the AWS action happened.
            timestamp = event.get("eventTime", "UNKNOWN_TIME")

            # get_user_name handles the nested userIdentity dictionary for us.
            user = get_user_name(event)

            # eventName tells us which AWS action happened, like CreateBucket.
            action = event.get("eventName", "UNKNOWN_ACTION")

            # sourceIPAddress tells us where the request came from.
            source_ip = event.get("sourceIPAddress", "UNKNOWN_IP")

            # Print one clean row with fixed-width columns for readability.
            print(f"{timestamp:<22} {user:<24} {action:<28} {source_ip}")


# This line makes main() run only when this file is executed directly.
if __name__ == "__main__":
    # Calling main() starts the script.
    main()
