import json

# Load the JSON data
with open('merge_total.json', 'r') as f:
    data = json.load(f)

# Iterate through the diseases
for gene_data in data:
    diseases = gene_data.get('diseases', [])
    for disease in diseases:
        references = set()  # Set to store unique references
        for phenotype in disease.get('phenotypes', []):
            reference = phenotype.get('reference')
            if reference:
                # Split multiple references separated by semicolon
                references.update(reference.split(';'))

        # Convert set to list for JSON serialization
        disease['literature_evidence'] = list(references)

# Write the modified data to the output file
with open("addedlitevlist.json", "w") as f:
    json.dump(data, f, indent=2)
