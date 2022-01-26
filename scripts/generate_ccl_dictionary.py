import os
import json


def process_rows(rows, committee_type_dict):
    output_data = {}
    for row in rows:
        split_row = row.split("|")
        campaign = split_row[0]
        committee = split_row[3]

        # For our purposes, we want to find links between committees and individual campaigns,
        # ...so we'll filter out any joint-fundraising committees (J) and leadership PACs (D)
        if (committee not in committee_type_dict.keys() or (committee_type_dict[committee] != "D" and committee_type_dict[committee] != "J")):
            output_data[committee] = campaign
    return output_data


def get_committee_types():
    committee_type_dict = {}

    committee_data_prefix = '../data/fec_bulk_data/committees'
    committee_files = [x for x in os.listdir(
        committee_data_prefix) if x != ".DS_Store"]
    for file in committee_files:
        with open(committee_data_prefix + "/" + file, 'r') as f:
            rows = [x for x in f.readlines()]
            for row in rows:
                row_data = row.split("|")
                committee_id = row_data[0]
                committee_type = row_data[8]

                committee_type_dict[committee_id] = committee_type

    return committee_type_dict


def main():
    committee_type_dict = get_committee_types()

    out_data = {}
    output_location = "../data/processed_data/ccl_mapping.json"

    ccl_prefix = '../data/fec_bulk_data/candidate_committee_linkages'
    ccl_files = [x for x in os.listdir(ccl_prefix) if x != ".DS_Store"]
    for file in ccl_files:
        with open(ccl_prefix + "/" + file, 'r') as f:
            rows = [x for x in f.readlines()]
            mapping = process_rows(rows, committee_type_dict)

            out_data.update(mapping)

    with open(output_location, "w") as f:
        json.dump(out_data, f)


if __name__ == "__main__":
    main()
