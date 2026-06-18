# json gives us the JSONDecodeError name for broken JSON files.
import json

# find_cloudtrail_files finds every .json and .json.gz file in data/raw.
from print_cloudtrail_table import find_cloudtrail_files

# RAW_LOG_FOLDER is the folder where our raw CloudTrail files live.
from print_cloudtrail_table import RAW_LOG_FOLDER

# load_cloudtrail_file opens one CloudTrail file and turns JSON into Python data.
from load_one_cloudtrail_file import load_cloudtrail_file


# This function chooses the best human-readable username from one CloudTrail event.
def get_user_name(event):
    # userIdentity is a nested dictionary that describes who made the AWS request.
    user_identity = event.get("userIdentity", {})

    # userName is usually present for IAM users.
    user_name = user_identity.get("userName")

    # If userName exists, return it because it is easy to read.
    if user_name:
        # Return stops the function and sends this value back to the caller.
        return user_name

    # arn is a longer identity string that can help when userName is missing.
    arn = user_identity.get("arn")

    # If arn exists, return it as a fallback identity label.
    if arn:
        # This keeps the finding useful for roles, root, or unusual identities.
        return arn

    # This final fallback makes missing identity data obvious.
    return "UNKNOWN_USER"


# This function answers one question: is this event a console login without MFA?
def is_console_login_without_mfa(event):
    # eventName tells us what AWS action happened.
    event_name = event.get("eventName")

    # ConsoleLogin is the CloudTrail event for signing in to the AWS Console.
    if event_name != "ConsoleLogin":
        # If this was not a console login, it cannot match this detector.
        return False

    # additionalEventData often contains extra sign-in details for ConsoleLogin.
    additional_event_data = event.get("additionalEventData", {})

    # MFAUsed is commonly "Yes" or "No" for console login events.
    mfa_used = additional_event_data.get("MFAUsed")

    # This event is suspicious when AWS says MFA was not used.
    return mfa_used == "No"


# This function prints one finding in a simple human-readable format.
def print_console_login_without_mfa_finding(event):
    # eventTime tells us when the AWS action happened.
    timestamp = event.get("eventTime", "UNKNOWN_TIME")

    # get_user_name handles the nested userIdentity dictionary for us.
    user = get_user_name(event)

    # sourceIPAddress tells us where the request came from.
    source_ip = event.get("sourceIPAddress", "UNKNOWN_IP")

    # This message explains why the event is suspicious.
    print("CONSOLE LOGIN WITHOUT MFA DETECTED")

    # This line prints the user, time, and IP in one compact sentence.
    print(f"User: {user} | Time: {timestamp} | Source IP: {source_ip}")

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
            # If the login did not use MFA, it should become a finding.
            if is_console_login_without_mfa(event):
                # Print the finding so the learner can see what was flagged.
                print_console_login_without_mfa_finding(event)

                # Add one to the finding counter.
                finding_count = finding_count + 1

    # If no findings were found, print a clear success message.
    if finding_count == 0:
        # This tells the learner the detector ran but found nothing suspicious.
        print("No console logins without MFA found in the current CloudTrail files.")


# This line makes main() run only when this file is executed directly.
if __name__ == "__main__":
    # Calling main() starts the script.
    main()
