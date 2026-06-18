# json gives us the JSONDecodeError name for broken JSON files.
import json

# find_cloudtrail_files finds every .json and .json.gz file in data/raw.
from print_cloudtrail_table import find_cloudtrail_files

# RAW_LOG_FOLDER is the folder where our raw CloudTrail files live.
from print_cloudtrail_table import RAW_LOG_FOLDER

# load_cloudtrail_file opens one CloudTrail file and turns JSON into Python data.
from load_one_cloudtrail_file import load_cloudtrail_file


# This function answers one question: did this event use the AWS root user?
def is_root_user_event(event):
    # userIdentity is a nested dictionary that describes who made the AWS request.
    user_identity = event.get("userIdentity", {})

    # type tells us what kind of AWS identity made the request.
    identity_type = user_identity.get("type")

    # CloudTrail marks root account activity with the identity type "Root".
    return identity_type == "Root"


# This function prints one finding in a simple human-readable format.
def print_root_finding(event):
    # eventTime tells us when the AWS action happened.
    timestamp = event.get("eventTime", "UNKNOWN_TIME")

    # eventName tells us which AWS action happened.
    action = event.get("eventName", "UNKNOWN_ACTION")

    # sourceIPAddress tells us where the request came from.
    source_ip = event.get("sourceIPAddress", "UNKNOWN_IP")

    # This message explains why the event is suspicious.
    print("ROOT USER ACTIVITY DETECTED")

    # This line prints the time, action, and IP in one compact sentence.
    print(f"Time: {timestamp} | Action: {action} | Source IP: {source_ip}")

    # This blank line keeps multiple findings visually separated.
    print()


# main() is the starting point for this script's work.
def main():
    # Find every CloudTrail file we know how to read in the raw log folder.
    cloudtrail_files = find_cloudtrail_files(RAW_LOG_FOLDER)

    # Start a counter so we know whether any root findings were found.
    root_finding_count = 0

    # Loop over each CloudTrail file path.
    for cloudtrail_file in cloudtrail_files:
        # try starts a block where Python will watch for JSON parsing errors.
        try:
            # Load this CloudTrail file into Python dictionaries and lists.
            cloudtrail_data = load_cloudtrail_file(cloudtrail_file)

        # except runs only if the file is not valid JSON.
        except json.JSONDecodeError:
            # Print a warning and keep going to the next file.
            print(f"Could not read JSON from {cloudtrail_file}")

            # continue skips the rest of this loop and moves to the next file.
            continue

        # Records is the top-level list where CloudTrail stores individual events.
        records = cloudtrail_data.get("Records", [])

        # Loop over each event dictionary inside the Records list.
        for event in records:
            # If the event was made by root, it should become a finding.
            if is_root_user_event(event):
                # Print the finding so the learner can see what was flagged.
                print_root_finding(event)

                # Add one to the finding counter.
                root_finding_count = root_finding_count + 1

    # If no root findings were found, print a clear success message.
    if root_finding_count == 0:
        # This tells the learner the detector ran but found nothing suspicious.
        print("No root user activity found in the current CloudTrail files.")


# This line makes main() run only when this file is executed directly.
if __name__ == "__main__":
    # Calling main() starts the script.
    main()
