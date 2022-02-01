import os
import csv


DATAFILE_SOURCE = "../data/processed_data/contributions/consolidated_actblue.csv"
OUTFILE_DESTINATION = "../data/processed_data/contributions/actblue_committee_summaries.csv"


def get_committee_data():
    committee_names = {}

    committee_data_prefix = '../data/fec_bulk_data/committees'
    committee_files = [x for x in os.listdir(
        committee_data_prefix) if x != ".DS_Store"]
    for file in committee_files:
        with open(committee_data_prefix + "/" + file, 'r') as f:
            rows = [x for x in f.readlines()]
            for row in rows:
                row_data = row.split("|")
                committee_id = row_data[0]
                committee_name = row_data[1]

                committee_names[committee_id] = committee_name

    return committee_names


def process_row(row):
    committee = row['destination_committee']
    # If we want to do by day, we can use this date definition
    # date = row['date']
    # If we want to do this by month, we can use this date definition
    date = row['date'][:7]
    amount = round(float(row['amount']), 2)
    return committee, date, amount


def process_file(file):
    all_committee_date_mappings = {}
    row_count = 0

    reader = csv.DictReader(file)
    rows_remaining = True
    while rows_remaining:
        try:
            current_row = next(reader)

            committee, date, amount = process_row(current_row)
            key = committee + '-' + date
            existing_entry = all_committee_date_mappings.get(
                key, {'total_raised': 0, 'total_contributions': 0, 'date': date, 'committee': committee})

            existing_entry['total_raised'] += amount
            existing_entry['total_contributions'] += 1

            all_committee_date_mappings[key] = existing_entry
        except StopIteration:
            rows_remaining = False

        if (row_count % 100000 == 0):
            print(f"Finished processing {row_count:,} rows")
        row_count += 1

    return list(all_committee_date_mappings.values())


def main():
    with open(DATAFILE_SOURCE, 'r') as f:
        processed_rows = process_file(f)

    committees = get_committee_data()

    for row in processed_rows:
        row['committee_name'] = committees[row['committee']]

    with open(OUTFILE_DESTINATION, 'w') as f:
        out_csv = csv.DictWriter(f, fieldnames=list(processed_rows[0].keys()))
        out_csv.writeheader()
        for row in processed_rows:
            out_csv.writerow(row)


if __name__ == "__main__":
    main()
