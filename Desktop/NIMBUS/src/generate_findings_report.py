# pathlib gives Python a clean way to point at files and folders.
from pathlib import Path

# get_cis_mapping looks up CIS control details for one NIMBUS rule ID.
from cis_mapping import get_cis_mapping

# collect_all_findings gathers every finding from the raw CloudTrail files.
from collect_findings import collect_all_findings


# This path points to the folder where generated reports should be saved.
REPORT_FOLDER = Path("reports")

# This path points to the specific report file this script creates.
REPORT_FILE_PATH = REPORT_FOLDER / "findings_report.txt"


# This function turns one finding dictionary into readable report lines.
def format_finding(finding):
    # Look up CIS details by using the finding's rule_id value.
    mapping = get_cis_mapping(finding["rule_id"])

    # If no CIS mapping exists, use safe fallback values.
    if mapping is None:
        # This fallback keeps the report from crashing on a new unknown rule.
        mapping = {
            # UNKNOWN makes missing compliance mapping obvious.
            "cis_control_id": "UNKNOWN",
            # UNKNOWN makes missing requirement mapping obvious.
            "cis_requirement": "UNKNOWN",
            # This title explains that the lookup failed.
            "cis_control_title": "No CIS mapping found for this rule",
            # UNKNOWN avoids pretending we know the severity.
            "severity": "UNKNOWN",
            # unmapped tells the reader this is not tied to CIS yet.
            "mapping_type": "unmapped",
        }

    # Return a list because each finding should become several report lines.
    return [
        # Print the finding title first so the reader knows what happened.
        f"Finding: {finding['title']}",
        # Print the NIMBUS rule ID so the result connects back to our code.
        f"NIMBUS rule ID: {finding['rule_id']}",
        # Print the CIS control and requirement in one place.
        f"CIS control: {mapping['cis_control_id']} / requirement {mapping['cis_requirement']}",
        # Print the CIS title so the compliance meaning is readable.
        f"CIS title: {mapping['cis_control_title']}",
        # Print severity and mapping type together because both explain priority.
        f"Severity: {mapping['severity']} | Mapping: {mapping['mapping_type']}",
        # Print the event details from the original finding dictionary.
        f"Event: {finding['timestamp']} | {finding['user']} | {finding['action']} | {finding['source_ip']}",
        # Add a blank line after each finding.
        "",
    ]


# This function builds the full report text from all findings.
def build_report_text(findings):
    # Start the report with a simple title.
    report_lines = ["NIMBUS CloudTrail Findings Report", ""]

    # If there are no findings, say that clearly in the report.
    if not findings:
        # Append a clean result message.
        report_lines.append("No findings found in the current CloudTrail files.")

        # Join the lines into one text block.
        return "\n".join(report_lines)

    # Loop over each finding dictionary in the findings list.
    for finding in findings:
        # Add the formatted lines for this one finding to the report.
        report_lines.extend(format_finding(finding))

    # Join the lines into one text block.
    return "\n".join(report_lines)


# main() is the starting point for this script's work.
def main():
    # Collect findings first so detection happens before reporting.
    findings = collect_all_findings()

    # Build one readable text report from the structured findings.
    report_text = build_report_text(findings)

    # Create the reports folder if it does not already exist.
    REPORT_FOLDER.mkdir(exist_ok=True)

    # Write the report text to disk using UTF-8 text encoding.
    REPORT_FILE_PATH.write_text(report_text, encoding="utf-8")

    # Print the report so the learner can see it in the terminal too.
    print(report_text)

    # Print the output path so the learner knows where the file was saved.
    print(f"\nReport saved to: {REPORT_FILE_PATH}")


# This line makes main() run only when this file is executed directly.
if __name__ == "__main__":
    # Calling main() starts the script.
    main()
