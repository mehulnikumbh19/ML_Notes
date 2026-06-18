# json lets Python read the detailed CloudTrail event string returned by boto3.
import json

# datetime gives us timezone-aware start and end times for the CloudTrail search.
from datetime import datetime, timedelta, timezone

# pathlib gives Python a clean way to point at files and folders.
from pathlib import Path

# boto3 is the AWS SDK that lets Python call AWS APIs.
import boto3

# pandas helps turn many CloudTrail events into a table.
import pandas as pd


# This is the AWS CLI profile we configured earlier with aws configure.
AWS_PROFILE_NAME = "nimbus"

# This project only uses us-east-1 to keep the learning environment simple.
AWS_REGION_NAME = "us-east-1"

# This path points to the folder where processed tables should be saved.
PROCESSED_DATA_FOLDER = Path("data/processed")

# This path points to the CSV file this script will create.
OUTPUT_FILE_PATH = PROCESSED_DATA_FOLDER / "iam_events.csv"

# This keeps the first boto3 step useful while staying safely inside the 90-day event history.
LOOKBACK_DAYS = 7

# These identity types represent AWS access performed by users, roles, or root.
IAM_IDENTITY_TYPES = {"IAMUser", "AssumedRole", "Root"}

# These are the table columns we want even when CloudTrail returns zero events.
TABLE_COLUMNS = ["timestamp", "event_name", "user", "identity_type", "source_ip", "error_code"]


# This function chooses the best human-readable username from one CloudTrail event.
def get_user_name(event_detail):
    # userIdentity is a nested dictionary that describes who made the AWS request.
    user_identity = event_detail.get("userIdentity", {})

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
        # This keeps the table useful for roles, root, or unusual identities.
        return arn

    # This final fallback makes missing identity data obvious.
    return "UNKNOWN_USER"


# This function creates a CloudTrail client using our named AWS CLI profile.
def create_cloudtrail_client():
    # A boto3 Session loads credentials and settings from the selected profile.
    session = boto3.Session(profile_name=AWS_PROFILE_NAME, region_name=AWS_REGION_NAME)

    # The CloudTrail client is the object that can call CloudTrail APIs.
    return session.client("cloudtrail")


# This function asks CloudTrail Event history for recent management events.
def lookup_recent_management_events(cloudtrail_client):
    # EndTime is now, using UTC because AWS event timestamps are in UTC.
    end_time = datetime.now(timezone.utc)

    # StartTime is a small lookback window before now.
    start_time = end_time - timedelta(days=LOOKBACK_DAYS)

    # A paginator lets boto3 fetch multiple result pages if AWS has many events.
    paginator = cloudtrail_client.get_paginator("lookup_events")

    # This list will hold every event returned by CloudTrail.
    events = []

    # paginate calls LookupEvents with our time window.
    pages = paginator.paginate(
        # StartTime tells CloudTrail the oldest event time we want.
        StartTime=start_time,
        # EndTime tells CloudTrail the newest event time we want.
        EndTime=end_time,
    )

    # Loop over each result page returned by the paginator.
    for page in pages:
        # Events is the list of CloudTrail matches inside this page.
        events.extend(page.get("Events", []))

    # Return the complete list of management events.
    return events


# This function answers one question: was this event made by an IAM-style identity?
def is_iam_access_event(event_detail):
    # userIdentity is a nested dictionary that describes who made the AWS request.
    user_identity = event_detail.get("userIdentity", {})

    # type tells us whether the caller was an IAM user, assumed role, root user, and so on.
    identity_type = user_identity.get("type")

    # Return True only when the identity type is one we want for this first ML table.
    return identity_type in IAM_IDENTITY_TYPES


# This function turns one detailed CloudTrail event into one simple table row.
def build_row(event_detail):
    # Return a dictionary because pandas can easily turn dictionaries into rows.
    return {
        # eventTime is the timestamp from the detailed CloudTrail event.
        "timestamp": event_detail.get("eventTime"),
        # eventName tells us which IAM action happened.
        "event_name": event_detail.get("eventName", "UNKNOWN_ACTION"),
        # get_user_name handles nested userIdentity data.
        "user": get_user_name(event_detail),
        # identity_type helps us separate IAM users, roles, and root later.
        "identity_type": event_detail.get("userIdentity", {}).get("type", "UNKNOWN_TYPE"),
        # sourceIPAddress tells us where the request came from.
        "source_ip": event_detail.get("sourceIPAddress", "UNKNOWN_IP"),
        # errorCode tells us if AWS denied or failed the request.
        "error_code": event_detail.get("errorCode", ""),
    }


# main() is the starting point for this script's work.
def main():
    # Create a CloudTrail client using the nimbus AWS CLI profile.
    cloudtrail_client = create_cloudtrail_client()

    # Look up recent management events from CloudTrail Event history.
    events = lookup_recent_management_events(cloudtrail_client)

    # Start with an empty list because not every management event is an IAM access event.
    rows = []

    # Loop over each event returned by boto3.
    for event in events:
        # CloudTrailEvent is a JSON string with detailed event fields inside it.
        event_detail = json.loads(event["CloudTrailEvent"])

        # Keep only events made by IAM-style identities.
        if is_iam_access_event(event_detail):
            # Add one simple table row for this event.
            rows.append(build_row(event_detail))

    # Create a pandas DataFrame from the list of row dictionaries.
    iam_events_table = pd.DataFrame(rows, columns=TABLE_COLUMNS)

    # Create the processed data folder if it does not already exist.
    PROCESSED_DATA_FOLDER.mkdir(exist_ok=True)

    # Save the table as CSV so we can inspect or reuse it later.
    iam_events_table.to_csv(OUTPUT_FILE_PATH, index=False)

    # Print the number of events so the learner knows what happened.
    print(f"Fetched {len(iam_events_table)} IAM events from CloudTrail Event history.")

    # Print the save location so the learner can find the table.
    print(f"Saved table to: {OUTPUT_FILE_PATH}")

    # Print the first few rows so the learner can see the table shape.
    print(iam_events_table.head())


# This line makes main() run only when this file is executed directly.
if __name__ == "__main__":
    # Calling main() starts the script.
    main()
