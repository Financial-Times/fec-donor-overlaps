import os
import csv
import json

DATAFILE_DIRECTORY = "../data/winred"
OUTFILE_DESTINATION = "../data/processed_data/contributions/consolidated_winred.csv"
# saving some file size by removing "employer", "occupation" for now, but
# ...some version of this processed data may eventually need to include these
RETAINED_FIELDS = ["first_name", "last_name", "zip", "date", "amount"]


def process_row(row, ccl_mappings):
    # On WinRed/ActBlue filings, contributions towards committees contain the destination committee in the memo text
    # (e.g. "Earmarked for NRCC (C00075820)"). Here, we'll want to filter out any refunds, etc (non-contributions)
    # and any rows where row is a contribution, but the committee isn't specified in parentheses (very rare)
    if "Earmarked for " not in row["memo_text"] or "(" not in row["memo_text"]:
        return None

    donor_id = row["first_name"].lower() + "~" + \
        row["last_name"].lower() + "~" + row["zip"]
    destination_committee = row["memo_text"].split("(")[1].strip(")")

    out_data = {k: v for k, v in row.items() if k in RETAINED_FIELDS}
    out_data["donor_id"] = donor_id
    out_data["destination_committee"] = destination_committee

    # For now, if the destination committee isn't associated with any particular campaign in
    # ...our mapping, we'll just ignore the row, since we won't be able to assign it to a candidate
    # ...for overlap analysis anyway. We'll definitely want to include these rows in other projects
    affiliated_campaign = ccl_mappings.get(destination_committee)
    if affiliated_campaign == None:
        return None
    out_data["destination_campaign"] = affiliated_campaign

    return out_data


def process_file(file, ccl_mappings):
    out_data = []
    row_count = 0

    reader = csv.DictReader(file)
    rows_remaining = True
    while rows_remaining:
        try:
            current_row = next(reader)
            processed_row_data = process_row(current_row, ccl_mappings)
            if processed_row_data:
                out_data.append(processed_row_data)
        except StopIteration:
            rows_remaining = False

        if (row_count % 100000 == 0):
            print(f"Finished processing {row_count:,} rows")
        row_count += 1

    return out_data


def main():
    processed_rows = []

    with open("../data/processed_data/ccl_mapping.json", "r") as f:
        ccl_mappings = json.load(f)

    winred_files = [x for x in os.listdir(DATAFILE_DIRECTORY) if ".csv" in x]
    for file in winred_files:
        with open(DATAFILE_DIRECTORY + "/" + file, 'r') as f:
            processed_rows += process_file(f, ccl_mappings)

    with open(OUTFILE_DESTINATION, 'w') as f:
        out_csv = csv.DictWriter(f, fieldnames=list(processed_rows[0].keys()))
        out_csv.writeheader()
        for row in processed_rows:
            out_csv.writerow(row)


if __name__ == "__main__":
    main()
