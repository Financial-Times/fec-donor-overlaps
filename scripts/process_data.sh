# Preps committee/campaign data
python generate_ccl_dictionary.py
python generate_candidate_data.py

# Parses and simplifies contribution data
python process_contributions.py
python create_campaign_donor_mappings.py

# Generates overlap data
python find_campaign_donor_overlap.py