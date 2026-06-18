# pathlib gives Python a clean way to point at files and folders.
from pathlib import Path

# pandas helps us transform event rows into numeric feature columns.
import pandas as pd


# This path points to the IAM event table created by the boto3 step.
INPUT_FILE_PATH = Path("data/processed/iam_events.csv")

# This path points to the numeric feature table this script will create.
OUTPUT_FILE_PATH = Path("data/processed/iam_event_features.csv")

# These columns are the numeric features we want to give to machine learning later.
FEATURE_COLUMNS = ["hour_of_day", "action_frequency", "is_new_source_ip_for_user", "has_error"]


# This function loads the IAM events CSV into a pandas DataFrame.
def load_iam_events():
    # read_csv opens the CSV file and turns it into a table-like DataFrame.
    return pd.read_csv(INPUT_FILE_PATH)


# This function adds numeric feature columns to the IAM events table.
def build_features(events_table):
    # copy protects the original table from being changed unexpectedly.
    features_table = events_table.copy()

    # to_datetime turns timestamp text into real datetime values.
    features_table["timestamp"] = pd.to_datetime(features_table["timestamp"], utc=True)

    # sort_values puts events in time order so "first seen" logic makes sense.
    features_table = features_table.sort_values("timestamp")

    # dt.hour extracts the hour number from each timestamp, from 0 through 23.
    features_table["hour_of_day"] = features_table["timestamp"].dt.hour

    # groupby counts how often each event name appears in the full table.
    features_table["action_frequency"] = features_table.groupby("event_name")["event_name"].transform("count")

    # duplicated marks source IPs we have already seen before for the same user.
    seen_user_ip_before = features_table.duplicated(subset=["user", "source_ip"], keep="first")

    # The first event for a user and IP becomes 1, and later repeats become 0.
    features_table["is_new_source_ip_for_user"] = (~seen_user_ip_before).astype(int)

    # notna checks whether error_code has a value, which means the AWS call had an error.
    features_table["has_error"] = features_table["error_code"].notna().astype(int)

    # Return the enriched table with both original columns and new feature columns.
    return features_table


# This function saves only the columns needed for the next machine-learning step.
def save_feature_table(features_table):
    # These context columns help a human understand which event each feature row came from.
    context_columns = ["timestamp", "event_name", "user", "identity_type", "source_ip", "error_code"]

    # This list combines human-readable context and numeric ML-ready features.
    output_columns = context_columns + FEATURE_COLUMNS

    # to_csv writes the selected columns to a CSV file without the pandas index column.
    features_table[output_columns].to_csv(OUTPUT_FILE_PATH, index=False)


# main() is the starting point for this script's work.
def main():
    # Load the IAM event table from the previous step.
    events_table = load_iam_events()

    # If the table has no rows, stop with a friendly message.
    if events_table.empty:
        # This tells the learner to rerun the boto3 fetch step if needed.
        print(f"No events found in {INPUT_FILE_PATH}. Run fetch_iam_events_with_boto3.py first.")

        # return exits main() early because there are no features to build.
        return

    # Build numeric feature columns from the raw event table.
    features_table = build_features(events_table)

    # Save the feature table for the next machine-learning step.
    save_feature_table(features_table)

    # Print the number of rows so the learner knows what happened.
    print(f"Built numeric features for {len(features_table)} IAM events.")

    # Print the save location so the learner can find the table.
    print(f"Saved feature table to: {OUTPUT_FILE_PATH}")

    # Print the first few feature rows so the learner can see the result.
    print(features_table[FEATURE_COLUMNS].head())


# This line makes main() run only when this file is executed directly.
if __name__ == "__main__":
    # Calling main() starts the script.
    main()
