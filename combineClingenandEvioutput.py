import json

def combine_data(omim_orphanet_file, gene_disease_file):
    # Load data from the JSON files
    with open(omim_orphanet_file, 'r') as f:
        omim_orphanet_data = json.load(f)
    with open(gene_disease_file, 'r') as f:
        gene_disease_data = json.load(f)

    # Combine the data
    combined_data = []
    for gene_disease_entry in gene_disease_data:
        gene_symbol = gene_disease_entry["gene_symbol"]
        disease_id = gene_disease_entry["disease_id"]
        mode_of_inheritance = gene_disease_entry["mode_of_inheritance"]
        classification = gene_disease_entry["classification"]

        # Find matching entry in omim_orphanet_data
        for entry in omim_orphanet_data:
            if entry["id"] == disease_id:
                omim_ids = entry["omim_ids"]
                orphanet_ids = entry["orphanet_ids"]

                # Add combined entries
                for omim_id in omim_ids:
                    combined_data.append({
                        "gene_symbol": gene_symbol,
                        "omim_id": omim_id,
                        "mode_of_inheritance": mode_of_inheritance,
                        "classification": classification
                    })
                for orphanet_id in orphanet_ids:
                    combined_data.append({
                        "gene_symbol": gene_symbol,
                        "orphanet_id": orphanet_id,
                        "mode_of_inheritance": mode_of_inheritance,
                        "classification": classification
                    })
                break

    return combined_data

def main(omim_orphanet_file, gene_disease_file, output_file):
    combined_data = combine_data(omim_orphanet_file, gene_disease_file)
    with open(output_file, 'w') as f:
        json.dump(combined_data, f, indent=4)

if __name__ == "__main__":
    omim_orphanet_file = "evioutput.json"
    gene_disease_file = "clingenSumm.json"
    output_file = "combined_dataCE.json"
    main(omim_orphanet_file, gene_disease_file, output_file)
