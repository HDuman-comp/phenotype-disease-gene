import json

def parse_text_file(file_path):
    diseases = []
    with open(file_path, 'r') as file:
        data = file.read().split("-----------------\n")
        for entry in data:
            if entry.strip():  # Skip empty lines
                disease = {}
                lines = entry.strip().split('\n')
                for line in lines:
                    parts = line.split(": ", 1)
                    if len(parts) == 2:
                        key, value = parts
                        if key == 'OMIM References':
                            if 'OMIM Code' not in disease:
                                disease['OMIM Code'] = value
                            else:
                                disease['OMIM Code'] += ", " + value
                        elif key == 'Orpha Code':
                            if 'Orpha Code' not in disease:
                                disease['Orpha Code'] = value
                            else:
                                disease['Orpha Code'] += ", " + value
                        elif key == 'Synonyms':
                            disease[key] = value
                        elif key == 'Definition':
                            disease[key] = value
                diseases.append(disease)
    return diseases

def convert_to_output_format(diseases):
    output = []
    for disease in diseases:
        if 'OMIM Code' in disease:
            output_entry = {'OMIM Code': disease['OMIM Code']}
            output_entry['Synonyms'] = disease.get('Synonyms', '')
            output_entry['Definition'] = disease.get('Definition', '')
            output.append(output_entry)

        if 'Orpha Code' in disease:
            output_entry = {'Orpha Code': disease['Orpha Code']}
            output_entry['Synonyms'] = disease.get('Synonyms', '')
            output_entry['Definition'] = disease.get('Definition', '')
            output.append(output_entry)

    return output

# Parse text file and get the data
diseases = parse_text_file('definitonsandSynoyms.txt')

# Convert data to desired output format
output_data = convert_to_output_format(diseases)

# Write output to file
with open('defSyn.json', 'w') as file:
    json.dump(output_data, file, indent=2)
