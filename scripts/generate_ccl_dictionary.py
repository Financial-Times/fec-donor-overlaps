import os
import json


def process_rows(rows):
    output_data = {}
    for row in rows:
        split_row = row.split("|")
        campaign = split_row[0]
        committee = split_row[3]
        output_data[committee] = campaign
    return output_data


def main():
    out_data = {}
    output_location = "../data/processed_data/ccl_mapping.json"

    ccl_prefix = '../data/fec_bulk_data/candidate_committee_linkages'
    ccl_files = [x for x in os.listdir(ccl_prefix) if x != ".DS_Store"]
    for file in ccl_files:
        with open(ccl_prefix + "/" + file, 'r') as f:
            rows = [x for x in f.readlines()]
            mapping = process_rows(rows)

            out_data.update(mapping)

    with open(output_location, "w") as f:
        json.dump(out_data, f)


if __name__ == "__main__":
    main()
