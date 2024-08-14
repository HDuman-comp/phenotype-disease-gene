import json


def convert_to_output(json_data):
    output = ""
    for disorder in json_data['JDBOR'][0]['DisorderList'][0]['Disorder']:
        output += f"Orpha Code: {disorder['OrphaCode']}\n"

        disease_name = disorder['Name'][0]['label']
        output += f"Disease Name: {disease_name}\n"

        synonyms = disorder.get('SynonymList', [{}])[0].get('Synonym', [])
        if synonyms:
            synonym_labels = [synonym['label'] for synonym in synonyms]
            output += f"Synonyms: {', '.join(synonym_labels)}\n"
        else:
            output += "Synonyms: No synonyms available\n"

        try:
            definition = \
            disorder['SummaryInformationList'][0]['SummaryInformation'][0]['TextSectionList'][0]['TextSection'][0][
                'Contents']
            output += f"Definition: {definition}\n"
        except KeyError:
            output += "Definition: Not available\n"

        try:
            omim_references = [ref['Reference'] for ref in
                               disorder['ExternalReferenceList'][0].get('ExternalReference', []) if
                               ref['Source'] == 'OMIM']
            if omim_references:
                output += f"OMIM References: {', '.join(omim_references)}\n"
        except KeyError:
            pass

        output += "-----------------\n"

    return output


# Load JSON data from file
with open('en_product1.json', 'r') as file:
    json_data = json.load(file)

# Convert JSON data to desired output format
output_text = convert_to_output(json_data)

# Write output to file
with open('definitonsandSynoyms.txt', 'w') as file:
    file.write(output_text)
