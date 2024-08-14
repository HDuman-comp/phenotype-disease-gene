import csv
import json

def parse_hpo_obo(file_path):
    hpo_dict = {}
    with open(file_path, 'r') as hpo_file:
        for line in hpo_file:
            line = line.strip()
            if line.startswith("id:"):
                hpo_id = line.split(': ')[1]
                hpo_dict[hpo_id] = {'name': None, 'definition': None}
            elif line.startswith("name:"):
                hpo_dict[hpo_id]['name'] = line.split(': ')[1]
            elif line.startswith("def:"):
                hpo_dict[hpo_id]['definition'] = line.split('"')[1]
    return hpo_dict

def load_hpo_annotations(file_path):
    hpo_data = {}
    with open(file_path, 'r') as hpo_file:
        # Find and skip comment lines until the header is reached
        header_found = False
        while not header_found:
            line = hpo_file.readline()
            if line.startswith("database_id"):
                header_found = True
        # Read the header line
        header = line.strip().split('\t')
        # Find the index of the 'database_id' field
        database_id_index = header.index('database_id')
        reader = csv.DictReader(hpo_file, delimiter='\t', fieldnames=header)
        for row in reader:
            disease_id = row[header[database_id_index]].split(':')[1]  # Extract OMIM or ORPHA ID
            disease_name = row['disease_name']
            hpo_id = row['hpo_id']
            frequency = row['frequency']
            reference = row.get('reference', None)  # Handle potential missing reference

            hpo_data.setdefault(disease_id, []).append({
                'disease_name': disease_name,
                'hpo_id': hpo_id,
                'reference': reference,
                "frequency": frequency
            })
    return hpo_data

def update_frequency(frequency):
    if frequency.startswith("HP:"):
        hp_code = frequency
        if hp_code == "HP:0040281":
            return "Very frequent"
        elif hp_code == "HP:0040280":
            return "Obligate"
        elif hp_code == "HP:0040282":
            return "Frequent"
        elif hp_code == "HP:0040283":
            return "Occasional"
        elif hp_code == "HP:0040284":
            return "Very rare"
        elif hp_code == "HP:0040285":
            return "Excluded"
        else:
            return frequency  # Return unchanged if not matched with known HP codes
    else:
        try:
            value = eval(frequency)  # Evaluate string expression to get the value
            if 0 <= value <= 0.1:
                return "Very rare"
            elif 0.1 < value <= 0.3:
                return "Occasional"
            elif 0.31 <= value <= 0.74:
                return "Frequent"
            elif 0.75 <= value <= 1:
                return "Very frequent"
            else:
                return frequency  # Return unchanged if value is out of expected range
        except:
            return frequency  # Return unchanged if evaluation fails

# Load HPO term details
hpo_definitions = parse_hpo_obo("hp.obo")

# Load HPO annotations
hpo_data = load_hpo_annotations("phenotype.hpoa")

# Process gene-disease information (adjust based on 'all-gene-disease.txt' structure)
output_data = []
with open("all-gene-disease.txt", 'r') as gene_file:
    for line in gene_file:
        parts = line.strip().split()
        gene = parts[0]
        diseases = []

        for part in parts[1:]:
            disease_info = {}
            if part.startswith('OMIM:'):
                omim_id = part.split(':')[1]
                disease_info['omim_id'] = omim_id
                # Get OMIM name from HPO data
                omim_name = hpo_data.get(omim_id, [{}])[0].get('disease_name', '')
                disease_info['omim_name'] = omim_name
            elif part.startswith('ORPHA:'):
                orpha_id = part.split(':')[1]
                disease_info['orpha_id'] = orpha_id
                # Get ORPHA name from HPO data
                orpha_name = hpo_data.get(orpha_id, [{}])[0].get('disease_name', '')
                disease_info['orpha_name'] = orpha_name

            disease_id = disease_info.get('omim_id') or disease_info.get('orpha_id')
            if disease_id and disease_id in hpo_data:
                disease_info['phenotypes'] = [
                    {
                        'hpo_id': phenotype['hpo_id'],
                        'hpo_name': hpo_definitions[phenotype['hpo_id']]['name'],
                        'definition': hpo_definitions[phenotype['hpo_id']]['definition'],
                        'frequency': update_frequency(phenotype['frequency']),  # Update frequency here
                        'reference': phenotype['reference']
                    } for phenotype in hpo_data[disease_id]
                ]
                diseases.append(disease_info)

        if diseases:
            output_data.append({"gene": gene, "diseases": diseases})

with open("newout.json", 'w') as output_file:
    json.dump(output_data, output_file, indent=4)
