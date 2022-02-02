import os
import time
import json
import csv
import pandas as pd

committee_for_analysis = "winred"

DATAFILE_SOURCE = f"../data/processed_data/contributions/{committee_for_analysis}_candidate_donor_mappings.csv"
DONOR_LIST_SOURCE = f"../data/processed_data/overlap/{committee_for_analysis}_donor_lists.json"

OVERLAP_OUTFILE_DESTINATION = f"../data/processed_data/overlap/{committee_for_analysis}_donor_overlap.csv"
TOTALS_OUTFILE_DESTINATION = f"../data/processed_data/overlap/{committee_for_analysis}_donor_totals.csv"


def get_campaign_donors_list(campaign_id, df):
    return df.loc[df['campaign_id'] == campaign_id]['donor_id'].to_list()


def get_donor_lists(all_campaigns, mappings_df):
    cached_file = True

    # I'm caching these donor lists in a JSON file because they take a few mintues to generate
    # we can referesh the cached file based on last modified time (or if there's no file found)
    try:
        last_modified_time = os.path.getmtime(DONOR_LIST_SOURCE)
        # Checks if cached file has been updated in the last 15 days (1,296,000 seconds)
        if time.time() - last_modified_time > 1296000:
            cached_file = False
    except FileNotFoundError:
        cached_file = False

    # If there's a cached file, just load that, then return
    if cached_file:
        print("Pulling donor lists from cached file!")
        with open(DONOR_LIST_SOURCE, "r") as f:
            donor_lists = json.load(f)
    # Otherwise, generate donor lists, store in cached file, then return
    else:
        print("Cached donor list file is missing or more than a month old, generating new donor lists (this may take a few minutes...)")
        donor_lists = {}
        for i, campaign_id in enumerate(all_campaigns):
            donor_list = get_campaign_donors_list(campaign_id, mappings_df)
            donor_lists[campaign_id] = donor_list

        with open(DONOR_LIST_SOURCE, 'w') as f:
            json.dump(donor_lists, f)

    return donor_lists


def process_campaign(current_id, all_ids, donor_lists, current_index):
    current_donors = set(donor_lists[current_id])
    overlap_rows = []

    # We'll compare to all campaigns after the in-focus campaign's index so we avoid looking at every overlap twice
    comparison_campaigns = all_ids[current_index:]
    for campaign_comparison_id in comparison_campaigns:
        compare_donors = set(donor_lists[campaign_comparison_id])
        overlap = list(current_donors & compare_donors)

        # If there's any overlap, add an entry to return
        # (probably worth adding a threshold on overlap count down the line, but we'll keep everything for now)
        if (len(overlap) > 0):
            overlap_rows.append({
                "campaign_1": current_id,
                "campaign_2": campaign_comparison_id,
                "overlap_count": len(overlap)
            })

        # print(f"{current_id} ({len(current_donors)}) to {campaign_comparison_id} ({len(compare_donors)}): {len(overlap)}")

    return overlap_rows


def main():
    mappings_df = pd.read_csv(DATAFILE_SOURCE)

    all_campaigns = mappings_df.campaign_id.unique()
    donor_lists = get_donor_lists(all_campaigns, mappings_df)

    out_data = []
    start = time.time()
    for i, campaign in enumerate(all_campaigns):
        out_data += process_campaign(campaign, all_campaigns, donor_lists, i)

        if ((i + 1) % 25 == 0):
            print(f"{i+1} records done! Total time: {time.time() - start}")

    with open(OVERLAP_OUTFILE_DESTINATION, 'w') as f:
        out_csv = csv.DictWriter(f, fieldnames=list(out_data[0].keys()))
        out_csv.writeheader()
        for row in out_data:
            out_csv.writerow(row)

    with open(TOTALS_OUTFILE_DESTINATION, 'w') as f:
        out_csv = csv.DictWriter(
            f, fieldnames=['campaign_id', 'total_unique_donors'])
        out_csv.writeheader()
        for k, v in donor_lists.items():
            out_csv.writerow({
                'campaign_id': k,
                'total_unique_donors': len(v)
            })


if __name__ == "__main__":
    main()
