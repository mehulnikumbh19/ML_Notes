# json gives us the JSONDecodeError name for broken JSON files.
import json

# find_cloudtrail_files finds every .json and .json.gz file in data/raw.
from print_cloudtrail_table import find_cloudtrail_files

# get_user_name chooses a readable user label from a CloudTrail event.
from print_cloudtrail_table import get_user_name

# RAW_LOG_FOLDER is the folder where our raw CloudTrail files live.
from print_cloudtrail_table import RAW_LOG_FOLDER

# load_cloudtrail_file opens one CloudTrail file and turns JSON into Python data.
from load_one_cloudtrail_file import load_cloudtrail_file


# These IAM actions can change permissions or identity settings.
IAM_CHANGE_ACTIONS = {
    "AttachGroupPolicy",
    "AttachRolePolicy",
    "AttachUserPolicy",
    "CreateAccessKey",
    "CreatePolicy",
    "CreatePolicyVersion",
    "DeletePolicy",
    "DeletePolicyVersion",
    "DetachGroupPolicy",
    "DetachRolePolicy",
    "DetachUserPolicy",
    "PutGroupPolicy",
    "PutRolePolicy",
    "PutUserPolicy",
}

# These source IPs are expected for this learning project right now.
KNOWN_GOOD_SOURCE_IPS = {
    "47.147.128.120",
}


# This function answers one question: did this event change IAM permissions?
def is_iam_change_event(event):
    # eventSource tells us which AWS service received the request.
    event_source = event.get("eventSource")

    # eventName tells us which AWS action happened.
    event_name = event.get("eventName")

    # IAM events come from iam.amazonaws.com.
    is_iam_service = event_source == "iam.amazonaws.com"

    # Permission-changing IAM actions should be in our set above.
    is_change_action = event_name in IAM_CHANGE_ACTIONS

    # Both conditions must be true for this rule to match.
    return is_iam_service and is_change_action


# This function answers one question: did this event come from an unexpected IP?
def is_unexpected_ip_event(event):
    # sourceIPAddress tells us where the request came from.
    source_ip = event.get("sourceIPAddress")

    # Missing IP data is worth noticing, so we treat it as unexpected.
    if not source_ip:
        # Returning True means the event should become a finding.
        return True

    # If the IP is not in our known-good set, the event is unexpected.
    return source_ip not in KNOWN_GOOD_SOURCE_IPS


# This function prints a finding in a simple human-readable format.
def print_finding(rule_name, event):
    # eventTime tells us when the AWS action happened.
    timestamp = event.get("eventTime", "UNKNOWN_TIME")

    # get_user_name handles the nested userIdentity dictionary for us.
    user = get_user_name(event)

    # eventName tells us which AWS action happened.
    action = event.get("eventName", "UNKNOWN_ACTION")

    # sourceIPAddress tells us where the request came from.
    source_ip = event.get("sourceIPAddress", "UNKNOWN_IP")

    # This message explains which rule matched.
    print(rule_name)

    # This line prints the key event details in one compact sentence.
    print(f"User: {user} | Time: {timestamp} | Action: {action} | Source IP: {source_ip}")

    # This blank line keeps multiple findings visually separated.
    print()


# main() is the starting point for this script's work.
def main():
    # Find every CloudTrail file we know how to read in the raw log folder.
    cloudtrail_files = find_cloudtrail_files(RAW_LOG_FOLDER)

    # Start a counter so we know whether any findings were found.
    finding_count = 0

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
            # If this event changed IAM permissions, print a finding.
            if is_iam_change_event(event):
                # Print the finding so the learner can see what was flagged.
                print_finding("IAM POLICY OR ACCESS CHANGE DETECTED", event)

                # Add one to the finding counter.
                finding_count = finding_count + 1

            # If this event came from a new IP, print a finding.
            if is_unexpected_ip_event(event):
                # Print the finding so the learner can see what was flagged.
                print_finding("UNEXPECTED SOURCE IP DETECTED", event)

                # Add one to the finding counter.
                finding_count = finding_count + 1

    # If no findings were found, print a clear success message.
    if finding_count == 0:
        # This tells the learner the detector ran but found nothing suspicious.
        print("No IAM changes or unexpected source IPs found in the current CloudTrail files.")


# This line makes main() run only when this file is executed directly.
if __name__ == "__main__":
    # Calling main() starts the script.
    main()
