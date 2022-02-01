import csv

with open('consolidated_sa_indiv.csv', 'r') as f:
    all_rows = [x for x in csv.DictReader(f)]

output_data = {}

for row in all_rows:
    key = row["filer_committee_id_number"] + "~" + row["contributor_first_name"] + \
        "~" + row["contributor_last_name"] + "~" + row["contributor_zip_code"]
    current_data = output_data.get(key, {
        "first_name": row["contributor_first_name"],
        "last_name": row["contributor_last_name"],
        "zipcode": row["contributor_zip_code"],
        "committee_id": row["filer_committee_id_number"],
        "total_amount": 0.0
    })

    current_data["total_amount"] = round(current_data["total_amount"] +
                                         float(row["contribution_amount"]), 2)

    output_data[key] = current_data

out_data = list(output_data.values())
with open("summarized_donors.csv", "w") as f:
    out_csv = csv.DictWriter(f, fieldnames=list(out_data[0].keys()))
    out_csv.writeheader()

    for row in out_data:
        out_csv.writerow(row)
