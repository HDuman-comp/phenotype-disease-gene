import json

# Load the JSON data
with open('remove_ref.json', 'r') as f:
    data = json.load(f)

# Iterate through each entry in the data
output_data = []
for entry in data:
    gene_name = entry.get('gene')  # Get the gene name
    diseases = entry.get('diseases', [])  # Get the diseases associated with the gene
    gene_entry = {gene_name: []}  # Create a dictionary entry for the gene

    # Iterate through diseases
    for disease in diseases:
        # Check if the "gene" key exists before attempting to delete it
        if 'gene' in disease:
            del disease['gene']
        gene_entry[gene_name].append(disease)  # Add the modified disease entry to the gene entry

    output_data.append(gene_entry)

with open("lastVersion.json", "w") as f:
    json.dump(output_data, f, indent=2)
