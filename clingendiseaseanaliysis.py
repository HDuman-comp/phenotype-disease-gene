import csv
import json


def process_data(input_file):
    data = []
    with open(input_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            entry = {
                "gene_symbol": row["GENE SYMBOL"],
                "disease_id": row["DISEASE ID (MONDO)"],
                "mode_of_inheritance": row["MOI"],
                "classification": row["CLASSIFICATION"]
            }
            data.append(entry)
    return data


def main(input_file, output_file):
    # Read the contents of the file and remove unwanted lines
    with open(input_file, "r") as file:
        lines = file.readlines()
    header_index = None
    for i, line in enumerate(lines):
        if "GENE SYMBOL" in line:
            header_index = i
            break
    if header_index is not None:
        lines = lines[header_index:]
    with open(input_file, "w") as file:
        file.writelines(lines)

    # Process the data
    processed_data = process_data(input_file)

    # Write the processed data to JSON file
    with open(output_file, 'w') as f:
        json.dump(processed_data, f, indent=4)


if __name__ == "__main__":
    input_file = "clingene_disease_summary.csv"
    output_file = "clingenSumm.json"
    main(input_file, output_file)
