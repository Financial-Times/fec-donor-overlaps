import json
import csv

committee_for_analysis = "actblue"

OVERLAP_SOURCE = f"../data/processed_data/overlap/{committee_for_analysis}_donor_overlap.csv"
TOTALS_SOURCE = f"../data/processed_data/overlap/{committee_for_analysis}_donor_totals.csv"
CAMPAIGN_DATA_SOURCE = "../data/processed_data/campaign_data.json"

OUTFILE_DESTINATION = f"../data/processed_data/overlap/{committee_for_analysis}_rich_overlap_data.csv"


def process_row(row, donor_totals, campaign_details_data, reverse_direction=False):
    if reverse_direction == True:
        outgoing_key = row["campaign_2"]
        incoming_key = row["campaign_1"]
    else:
        outgoing_key = row["campaign_1"]
        incoming_key = row["campaign_2"]

    outgoing_candidate_id = outgoing_key.split("~")[0]
    incoming_candidate_id = incoming_key.split("~")[0]

    outgoing_candidate_cycle = outgoing_key.split("~")[1]
    incoming_candidate_cycle = incoming_key.split("~")[1]

    outgoing_candidate_data = campaign_details_data[outgoing_candidate_id]
    incoming_candidate_data = campaign_details_data[incoming_candidate_id]

    row_output_data = {
        "outgoing_candidate_id": outgoing_key,
        "outgoing_candidate_name": outgoing_candidate_data["full_name"],
        "outgoing_candidate_office": outgoing_candidate_data["office"],
        "outgoing_candidate_state": outgoing_candidate_data["state"],
        "outgoing_candidate_district": outgoing_candidate_data["district"],
        "outgoing_candidate_cycle": outgoing_candidate_cycle,
        "outgoing_candidate_total_donors": int(donor_totals[outgoing_key]),
        "incoming_candidate_id": incoming_key,
        "incoming_candidate_name": incoming_candidate_data["full_name"],
        "incoming_candidate_office": incoming_candidate_data["office"],
        "incoming_candidate_state": incoming_candidate_data["state"],
        "incoming_candidate_district": incoming_candidate_data["district"],
        "incoming_candidate_cycle": incoming_candidate_cycle,
        "incoming_candidate_total_donors": int(donor_totals[incoming_key]),
        "overlap_count": int(row["overlap_count"]),
        "overlap_pct_of_outgoing": round(int(row["overlap_count"]) / int(donor_totals[outgoing_key]), 4),
        "overlap_pct_of_incoming": round(int(row["overlap_count"]) / int(donor_totals[incoming_key]), 4)
    }

    return row_output_data


def append_rich_data(overlap_counts, donor_totals, campaign_details_data):
    output_data = []

    for row in overlap_counts:
        # I kept overlap with self in on the raw data for now because I felt like it might make sense in some aggregations? (probably not),
        # ...but we'll exclude those rows here
        if row["campaign_1"] == row["campaign_2"]:
            continue

        if row["campaign_1"].split("~")[0] not in campaign_details_data.keys() or row["campaign_2"].split("~")[0] not in campaign_details_data.keys():
            continue

        # We excluded duplicates to keep the data size down on the last script, but here, for ease of searching/filtering,
        # ...we do probably want to represent each overlap both ways, so there will be twice as much data, but it will be easier
        # ...to locate what we're looking for. Unless/until we put this in a database and normalize a little, this is probably better
        processed_row = process_row(row, donor_totals, campaign_details_data)
        reversed_processed_row = process_row(
            row, donor_totals, campaign_details_data, reverse_direction=True)

        # Adding a threshold of at least 20 overlapping donors before adding to output file
        # This alone basically cuts the file size by more than half
        if processed_row["overlap_count"] >= 50 and processed_row["incoming_candidate_total_donors"] >= 500 and processed_row["outgoing_candidate_total_donors"] >= 500:
            # if processed_row["overlap_count"] >= 25:
            output_data += [processed_row, reversed_processed_row]

    return output_data


def main():
    with open(CAMPAIGN_DATA_SOURCE, 'r') as f:
        campaign_details_data = json.load(f)

    with open(TOTALS_SOURCE, 'r') as f:
        donor_totals = {x["campaign_id"]: x["total_unique_donors"]
                        for x in csv.DictReader(f)}

    with open(OVERLAP_SOURCE, 'r') as f:
        overlap_counts = [x for x in csv.DictReader(f)]

    processed_data = append_rich_data(
        overlap_counts, donor_totals, campaign_details_data)

    processed_data.sort(key=lambda x: x["overlap_count"], reverse=True)
    with open(OUTFILE_DESTINATION, 'w') as f:
        out_csv = csv.DictWriter(f, fieldnames=list(processed_data[0].keys()))
        out_csv.writeheader()
        for row in processed_data:
            out_csv.writerow(row)


if __name__ == "__main__":
    main()
