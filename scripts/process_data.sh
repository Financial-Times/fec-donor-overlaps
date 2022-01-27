# ====== Prep committee/campaign data ======
# This generates a JSON file that can be loaded in as a dictionary mapping
python generate_ccl_dictionary.py
# This ingests the FEC bulk data file, trims it down and outputs a JSON with rich candidate data
python generate_candidate_data.py

# ====== Parse and simplify contribution data ======
# This ingests all filing files in a target directory, trims them down and consolidates them
python process_contributions.py
# This ingests the consolidated file and aggregates/trims it down more to generate a file of just donor-campaign mappings
python create_campaign_donor_mappings.py

# ====== Generate overlap data ======
# This ingests the donor-campaign mappings, generates donor lists for each candidate and creates simple overlap file
python find_campaign_donor_overlap.py
# This attaches the rich campaign data to the overlap file to create a readable/helpful overlap CSV
python create_readable_overlap_data.py