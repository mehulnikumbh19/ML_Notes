# json gives us the JSONDecodeError name for broken JSON files.
import json

# is_console_login_without_mfa checks one event for missing MFA on ConsoleLogin.
from detect_console_login_without_mfa import is_console_login_without_mfa

# is_iam_change_event checks one event for permission-changing IAM activity.
from detect_iam_changes_and_unexpected_ips import is_iam_change_event

# is_unexpected_ip_event checks one event against our known-good source IP list.
from detect_iam_changes_and_unexpected_ips import is_unexpected_ip_event

# is_root_user_event checks one event for AWS root account activity.
from detect_root_usage import is_root_user_event

# load_cloudtrail_file opens one CloudTrail file and turns JSON into Python data.
from load_one_cloudtrail_file import load_cloudtrail_file

# find_cloudtrail_files finds every .json and .json.gz file in data/raw.
from print_cloudtrail_table import find_cloudtrail_files

# get_user_name chooses a readable user label from a CloudTrail event.
from print_cloudtrail_table import get_user_name

# RAW_LOG_FOLDER is the folder where our raw CloudTrail files live.
from print_cloudtrail_table import RAW_LOG_FOLDER


# This function turns one rule match into a structured finding dictionary.
def build_finding(rule_id, title, event):
    # A dictionary stores related values under clear names called keys.
    return {
        # rule_id is a stable short name future code can use.
        "rule_id": rule_id,
        # title is the human-readable explanation of what matched.
        "title": title,
        # eventTime tells us when the AWS action happened.
        "timestamp": event.get("eventTime", "UNKNOWN_TIME"),
        # get_user_name handles the nested userIdentity dictionary for us.
        "user": get_user_name(event),
        # eventName tells us which AWS action happened.
        "action": event.get("eventName", "UNKNOWN_ACTION"),
        # sourceIPAddress tells us where the request came from.
        "source_ip": event.get("sourceIPAddress", "UNKNOWN_IP"),
    }


# This function checks one CloudTrail event against every rule we have so far.
def collect_findings_from_event(event):
    # findings starts as an empty list because this one event may match zero rules.
    findings = []

    # If the event used the root account, add a root-user finding dictionary.
    if is_root_user_event(event):
        # append adds one new item to the end of the findings list.
        findings.append(build_finding("ROOT_USER_ACTIVITY", "Root user activity detected", event))

    # If the event was a console login without MFA, add an MFA finding dictionary.
    if is_console_login_without_mfa(event):
        # This keeps detection separate from printing.
        findings.append(build_finding("CONSOLE_LOGIN_WITHOUT_MFA", "Console login without MFA", event))

    # If the event changed IAM permissions, add an IAM-change finding dictionary.
    if is_iam_change_event(event):
        # One event can match more than one rule, so this is a separate if.
        findings.append(build_finding("IAM_CHANGE", "IAM policy or access change detected", event))

    # If the event came from an unexpected IP, add an IP finding dictionary.
    if is_unexpected_ip_event(event):
        # This finding uses the same event details but a different rule_id and title.
        findings.append(build_finding("UNEXPECTED_SOURCE_IP", "Unexpected source IP detected", event))

    # Return the list of findings for this one event.
    return findings


# This function loads every raw log file and collects every finding.
def collect_all_findings():
    # all_findings starts empty and grows as matching events are discovered.
    all_findings = []

    # Loop over each CloudTrail file path in the raw log folder.
    for cloudtrail_file in find_cloudtrail_files(RAW_LOG_FOLDER):
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
            # extend adds every finding from this event into the full list.
            all_findings.extend(collect_findings_from_event(event))

    # Return the complete structured list to the caller.
    return all_findings


# This function prints structured finding dictionaries in a readable way.
def print_findings(findings):
    # If the list is empty, there are no findings to print.
    if not findings:
        # This message confirms the collector ran successfully.
        print("No findings found in the current CloudTrail files.")

        # return exits the function early because there is no report to print.
        return

    # Loop over each finding dictionary in the findings list.
    for finding in findings:
        # Print the dictionary directly so the learner can see the structure.
        print(finding)


# main() is the starting point for this script's work.
def main():
    # Collect findings first so detection happens before reporting.
    findings = collect_all_findings()

    # Print the findings after they have been collected.
    print_findings(findings)


# This line makes main() run only when this file is executed directly.
if __name__ == "__main__":
    # Calling main() starts the script.
    main()
