import os
import csv
import json

committee_for_analysis = "actblue"

DATAFILE_DIRECTORY = f"../data/{committee_for_analysis}"
OUTFILE_DESTINATION = f"../data/processed_data/contributions/consolidated_{committee_for_analysis}.csv"
# saving some file size by removing "employer", "occupation" for now, but
# ...some version of this processed data may eventually need to include these
RETAINED_FIELDS = ["first_name", "last_name", "zip", "date", "amount", "cycle"]

direct_file_field_mapping = {
    "contributor_first_name": "first_name",
    "contributor_last_name": "last_name",
    "contribution_date": "date",
    "contribution_amount": "amount",
    "contributor_zip_code": "zip",
    "contribution_purpose_descrip": "memo_text"
}


def process_row(row, ccl_mappings, campaign_data, direct=False):
    if direct:
        for field in direct_file_field_mapping.keys():
            row[direct_file_field_mapping[field]] = row[field]

        row["zip"] = row["zip"][:5]
        row["cycle"] = "2022"
    # On WinRed/ActBlue filings, contributions towards committees contain the destination committee in the memo text
    # (e.g. "Earmarked for NRCC (C00075820)"). Here, we'll want to filter out any refunds, etc (non-contributions)
    # and any rows where row is a contribution, but the committee isn't specified in parentheses (very rare)
    if "Earmarked for " not in row["memo_text"] or "(" not in row["memo_text"]:
        return None

    donor_id = row["first_name"].lower() + "~" + \
        row["last_name"].lower() + "~" + row["zip"]
    destination_committee = row["memo_text"].split("(")[1].strip(")")

    out_data = {k: v for k, v in row.items(
    ) if k in RETAINED_FIELDS and k in row.keys()}
    out_data["donor_id"] = donor_id
    out_data["destination_committee"] = destination_committee

    # For now, if the destination committee isn't associated with any particular campaign in
    # ...our mapping, we'll just ignore the row, since we won't be able to assign it to a candidate
    # ...for overlap analysis anyway. We'll definitely want to include these rows in other projects
    affiliated_campaign = ccl_mappings.get(destination_committee)
    if affiliated_campaign == None:
        return None
    else:
        out_data["destination_campaign"] = affiliated_campaign

    if campaign_data.get(affiliated_campaign) == None:
        return None

    affiliated_campaign_cycles = str(campaign_data.get(
        affiliated_campaign)["all_cycles"])

    # This ensures that our consolidated dataset only includes "in-cycle" contributions
    # (e.g. we won't consider contributions to 2022 senate candidates during the 2020 cycle)
    # Including these contributions skews overlap data in a way that's misleading
    if str(row["cycle"]) not in affiliated_campaign_cycles:
        return None
    else:
        out_data["cycle"] = str(row["cycle"])
        return out_data


def process_file(file, ccl_mappings, campaign_data, out_csv, direct=False):
    row_count = 0

    reader = csv.DictReader(file)
    rows_remaining = True
    while rows_remaining:
        try:
            current_row = next(reader)
            processed_row_data = process_row(
                current_row, ccl_mappings, campaign_data, direct)
            if processed_row_data:
                out_csv.writerow(processed_row_data)
        except StopIteration:
            rows_remaining = False

        if (row_count % 1000000 == 0):
            print(f"Finished processing {row_count:,} rows")
        row_count += 1


def main():
    with open("../data/processed_data/ccl_mapping.json", "r") as f:
        ccl_mappings = json.load(f)

    with open("../data/processed_data/campaign_data.json", "r") as f:
        campaign_data = json.load(f)

    with open(OUTFILE_DESTINATION, 'w') as out_file:
        all_fields = ["first_name", "last_name", "zip", "date", "amount",
                      "cycle"] + ["donor_id", "destination_committee", "destination_campaign"]
        out_csv = csv.DictWriter(out_file, fieldnames=all_fields)
        out_csv.writeheader()

        winred_files = [x for x in os.listdir(
            DATAFILE_DIRECTORY) if ".csv" in x]
        for file in sorted(winred_files):
            with open(DATAFILE_DIRECTORY + "/" + file, 'r') as f:
                print(f"===== FILE: {file} =====")

                direct = "direct" in file
                process_file(f, ccl_mappings, campaign_data, out_csv, direct)


if __name__ == "__main__":
    main()
