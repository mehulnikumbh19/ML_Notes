# This dictionary maps our NIMBUS rule IDs to CIS AWS Benchmark-style controls.
CIS_CONTROL_MAPPING = {
    # ROOT_USER_ACTIVITY is our rule ID from collect_findings.py.
    "ROOT_USER_ACTIVITY": {
        # cis_control_id is the AWS Security Hub control ID for this CIS-related check.
        "cis_control_id": "CloudWatch.1",
        # cis_requirement is the older CIS AWS Foundations Benchmark v1.4.0 requirement number.
        "cis_requirement": "4.3",
        # cis_control_title describes the control in plain English.
        "cis_control_title": 'A log metric filter and alarm should exist for usage of the "root" user',
        # severity is the AWS Security Hub severity for this control.
        "severity": "LOW",
        # mapping_type tells us this rule directly matches the CIS monitoring idea.
        "mapping_type": "direct",
    },
    # CONSOLE_LOGIN_WITHOUT_MFA is our rule ID for console sign-ins without MFA.
    "CONSOLE_LOGIN_WITHOUT_MFA": {
        # cis_control_id is the AWS Security Hub control ID for this CIS-related check.
        "cis_control_id": "CloudWatch.3",
        # cis_requirement is the older CIS AWS Foundations Benchmark v1.2.0 requirement number.
        "cis_requirement": "3.2",
        # cis_control_title describes the control in plain English.
        "cis_control_title": "Ensure a log metric filter and alarm exist for Management Console sign-in without MFA",
        # severity is the AWS Security Hub severity for this control.
        "severity": "LOW",
        # mapping_type tells us this rule directly matches the CIS monitoring idea.
        "mapping_type": "direct",
    },
    # IAM_CHANGE is our rule ID for IAM policy or access changes.
    "IAM_CHANGE": {
        # cis_control_id is the AWS Security Hub control ID for this CIS-related check.
        "cis_control_id": "CloudWatch.4",
        # cis_requirement is the older CIS AWS Foundations Benchmark v1.4.0 requirement number.
        "cis_requirement": "4.4",
        # cis_control_title describes the control in plain English.
        "cis_control_title": "Ensure a log metric filter and alarm exist for IAM policy changes",
        # severity is the AWS Security Hub severity for this control.
        "severity": "LOW",
        # mapping_type tells us this rule directly matches the CIS monitoring idea.
        "mapping_type": "direct",
    },
    # UNEXPECTED_SOURCE_IP is our NIMBUS-specific baseline rule.
    "UNEXPECTED_SOURCE_IP": {
        # cis_control_id is the closest CIS-related monitoring control for suspicious API behavior.
        "cis_control_id": "CloudWatch.2",
        # cis_requirement is the older CIS AWS Foundations Benchmark v1.2.0 requirement number.
        "cis_requirement": "3.1",
        # cis_control_title describes the related control in plain English.
        "cis_control_title": "Ensure a log metric filter and alarm exist for unauthorized API calls",
        # severity is the AWS Security Hub severity for this related control.
        "severity": "LOW",
        # mapping_type warns us that unexpected IP is related to, not identical to, this CIS control.
        "mapping_type": "related",
    },
}


# This function looks up CIS control details for one NIMBUS rule ID.
def get_cis_mapping(rule_id):
    # get returns the matching mapping or None if the rule ID is unknown.
    return CIS_CONTROL_MAPPING.get(rule_id)


# main() is the starting point for this script's work.
def main():
    # Loop over every rule ID and CIS mapping in the dictionary.
    for rule_id, mapping in CIS_CONTROL_MAPPING.items():
        # Print the NIMBUS rule ID so we know which detector the row belongs to.
        print(f"NIMBUS rule: {rule_id}")

        # Print the CIS control ID and requirement number together.
        print(f"CIS control: {mapping['cis_control_id']} / requirement {mapping['cis_requirement']}")

        # Print the official-style control title.
        print(f"Title: {mapping['cis_control_title']}")

        # Print the severity and whether the mapping is direct or related.
        print(f"Severity: {mapping['severity']} | Mapping: {mapping['mapping_type']}")

        # Print a blank line so each mapping is easy to read.
        print()


# This line makes main() run only when this file is executed directly.
if __name__ == "__main__":
    # Calling main() starts the script.
    main()
