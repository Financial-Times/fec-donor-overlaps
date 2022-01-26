import json
import csv


OVERLAP_SOURCE = "../data/processed_data/overlap/donor_overlap.csv"
TOTALS_SOURCE = "../data/processed_data/overlap/donor_totals.csv"
CAMPAIGN_DATA_SOURCE = "../data/processed_data/campaign_data.json"


def process_row():
    pass


def append_rich_data(overlap_counts, donor_totals, campaign_details_data):
    pass


def main():
    with open(CAMPAIGN_DATA_SOURCE, 'r') as f:
        campaign_details_data = json.load(f)

    with open(TOTALS_SOURCE, 'r') as f:
        donor_totals = [x for x in csv.DictReader(f)]

    with open(OVERLAP_SOURCE, 'r') as f:
        overlap_counts = [x for x in csv.DictReader(f)]

    processed_data = append_rich_data(
        overlap_counts, donor_totals, campaign_details_data)

    # with open(OUTFILE_DESTINATION, 'w') as f:
    #     out_csv = csv.DictWriter(f, fieldnames=list(out_data[0].keys()))
    #     out_csv.writeheader()
    #     for row in out_data:
    #         out_csv.writerow(row)


if __name__ == "__main__":
    main()
