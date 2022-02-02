import csv

committee_for_analysis = "winred"

DATAFILE_SOURCE = f"../data/processed_data/contributions/consolidated_{committee_for_analysis}.csv"
OUTFILE_DESTINATION = f"../data/processed_data/contributions/{committee_for_analysis}_candidate_donor_mappings.csv"


def process_row(row):
    # By eventually piling these unique hashes (donor_id + "/~/" + campaign_id) into a set
    # ...we can quickly eliminate any duplicates without holding the whole, very large datafile
    # ...in memory and then re-parse the individual fields into rows using the unique separator ("/~/")
    set_entry = row["donor_id"] + "/~/" + row["destination_campaign"]
    return set_entry


def process_file(file):
    all_mappings = set()
    row_count = 0

    reader = csv.DictReader(file)
    rows_remaining = True
    while rows_remaining:
        try:
            current_row = next(reader)
            processed_row_data = process_row(current_row)
            all_mappings.add(processed_row_data)
        except StopIteration:
            rows_remaining = False

        if (row_count % 100000 == 0):
            print(f"Finished processing {row_count:,} rows")
        row_count += 1

    out_data = []
    for entry in all_mappings:
        entry_data = entry.split("/~/")
        out_data.append({
            "donor_id": entry_data[0],
            "campaign_id": entry_data[1]
        })

    return out_data


def main():
    with open(DATAFILE_SOURCE, 'r') as f:
        processed_rows = process_file(f)

    with open(OUTFILE_DESTINATION, 'w') as f:
        out_csv = csv.DictWriter(f, fieldnames=list(processed_rows[0].keys()))
        out_csv.writeheader()
        for row in processed_rows:
            out_csv.writerow(row)


if __name__ == "__main__":
    main()
