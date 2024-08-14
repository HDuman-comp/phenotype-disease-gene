import json

# Read the JSON files
with open('newout.json', 'r') as file:
    newout_data = json.load(file)

with open('defSyn.json', 'r') as file:
    defsynnew_data = json.load(file)

# Create a dictionary for faster lookup
synonyms_definitions = {}
for entry in defsynnew_data:
    if 'omim_id' in entry:
        synonyms_definitions[entry['omim_id']] = {
            'Synonyms': entry['Synonyms'].split(', '),
            'disease_definition': entry['Definition']
        }
    elif 'orpha_id' in entry:
        synonyms_definitions[entry['orpha_id']] = {
            'Synonyms': entry['Synonyms'].split(', '),
            'disease_definition': entry['Definition']
        }

# Update the newout_data with Synonyms and disease_definition
for gene_data in newout_data:
    for disease in gene_data['diseases']:
        if 'omim_id' in disease:
            omim_id = disease['omim_id']
            if omim_id in synonyms_definitions:
                disease['Synonyms'] = synonyms_definitions[omim_id]['Synonyms']
                disease['disease_definition'] = synonyms_definitions[omim_id]['disease_definition']
        elif 'orpha_id' in disease:
            orpha_id = disease['orpha_id']
            if orpha_id in synonyms_definitions:
                disease['Synonyms'] = synonyms_definitions[orpha_id]['Synonyms']
                disease['disease_definition'] = synonyms_definitions[orpha_id]['disease_definition']

# Write the updated data to a new JSON file
with open('updated_newout.json', 'w') as file:
    json.dump(newout_data, file, indent=4)
