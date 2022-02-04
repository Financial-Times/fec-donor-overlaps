# This script specifically checks for overlap between Biden 2020 donors and 2022 cycle GOP candidates
# and between Trump 2020 donors and 2022 cycle Dem candidates. It doesn't go through the song-and-dance
# of generating the donor list files itself or checking whether the cache should be refreshed, so it's
# somewhat dependent on the "find_campaign_donor_overlap.py" script running first, since that will check
# for same party overlap and generate or refresh the donor list files that this uses.

import time
import json
import csv


OVERLAP_DIRECTORY = "../data/processed_data/overlap/"
OVERLAP_OUTFILE_DESTINATION = "../data/processed_data/overlap/cross_party_donor_overlap.csv"
TOTALS_OUTFILE_DESTINATION = "../data/processed_data/overlap/cross_party_donor_totals.csv"


def process_comparison(main_id, compare_id, main_list, compare_list):
    overlap_rows = []

    compare_donors = set(compare_list)
    overlap = list(main_list & compare_donors)

    # If there's any overlap, add an entry to return
    # (probably worth adding a threshold on overlap count down the line, but we'll keep everything for now)
    if (len(overlap) > 0):
        overlap_rows.append({
            "campaign_1": main_id,
            "campaign_2": compare_id,
            "overlap_count": len(overlap)
        })

    return overlap_rows


def main():
    trump_2020_campaign_id = "P80001571~2020"
    biden_2020_campaign_id = "P80000722~2020"

    for committee in ["winred", "actblue"]:
        with open((OVERLAP_DIRECTORY + f"{committee}_donor_lists.json"), 'r') as f:
            donor_list = json.load(f)

            if committee == "winred":
                trump_donor_list = set(donor_list[trump_2020_campaign_id])
                gop_donor_lists = donor_list
            elif committee == "actblue":
                biden_donor_list = set(donor_list[biden_2020_campaign_id])
                dem_donor_lists = donor_list

    out_data = []
    start = time.time()

    for i, campaign in enumerate(list(gop_donor_lists.items())):
        campaign_id = campaign[0]
        compare_campaign_donors = campaign[1]

        out_data += process_comparison(biden_2020_campaign_id,
                                       campaign_id, biden_donor_list, compare_campaign_donors)

        if ((i + 1) % 25 == 0):
            print(f"{i+1} records done! Total time: {time.time() - start}")

    for i, campaign in enumerate(list(dem_donor_lists.items())):
        campaign_id = campaign[0]
        compare_campaign_donors = campaign[1]

        out_data += process_comparison(trump_2020_campaign_id,
                                       campaign_id, trump_donor_list, compare_campaign_donors)

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
        for k, v in {**gop_donor_lists, **dem_donor_lists}.items():
            out_csv.writerow({
                'campaign_id': k,
                'total_unique_donors': len(v)
            })


if __name__ == "__main__":
    main()
