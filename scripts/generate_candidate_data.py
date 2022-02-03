import os
import json
from posixpath import split


def process_rows(rows):
    output_data = {}
    for row in rows:
        split_row = row.split("|")

        campaign_id = split_row[0]

        name = split_row[1]
        first_middle_name = name.split(",")[1] if len(
            name.split(",")) > 1 else ""
        surname = name.split(",")[0]

        party = split_row[2]
        campaign_cycle = split_row[3]
        state = split_row[4]
        office = split_row[5]
        district = split_row[6]

        output_data[campaign_id] = {
            "id": campaign_id,
            "full_name": name,
            "first_name": first_middle_name.strip(),
            "last_name": surname.strip(),
            "party": party,
            "campaign_cycle": campaign_cycle,
            "state": state,
            "office": office,
            "district": district
        }

    return output_data


def main():
    out_data = {}
    output_location = "../data/processed_data/campaign_data.json"

    campaign_prefix = '../data/fec_bulk_data/campaigns'
    campaign_files = [x for x in os.listdir(
        campaign_prefix) if x != ".DS_Store"]

    for file in sorted(campaign_files):
        with open(campaign_prefix + "/" + file, 'r') as f:
            rows = [x for x in f.readlines()]
            campaign_data = process_rows(rows)

            out_data.update(campaign_data)

    with open(output_location, "w") as f:
        json.dump(out_data, f)


if __name__ == "__main__":
    main()
