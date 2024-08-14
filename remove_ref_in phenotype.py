import json

# Load the JSON data
with open('addedlitevlist.json', 'r') as f:
    data = json.load(f)

# Iterate through the diseases
for gene_data in data:
    diseases = gene_data.get('diseases', [])
    for disease in diseases:
        for phenotype in disease.get('phenotypes', []):
            # Remove the 'reference' field if it exists
            if 'reference' in phenotype:
                del phenotype['reference']

# Write the modified data to the output file
with open("remove_ref.json", "w") as f:
    json.dump(data, f, indent=2)
