import re
import json

def extract_ids(xrefs):
    omim_ids = []
    orphanet_ids = []
    for xref in xrefs:
        match = re.search(r'(OMIM|Orphanet):(\d+)', xref)
        if match:
            if match.group(1) == 'OMIM':
                omim_ids.append(match.group(0))
            elif match.group(1) == 'Orphanet':
                orphanet_ids.append(match.group(0))
    return omim_ids, orphanet_ids

def process_data(data):
    entries = data.strip().split('\n\n')
    output = []

    for entry in entries:
        entry_lines = entry.strip().split('\n')
        term_id = ''
        xrefs = []
        for line in entry_lines:
            if line.startswith('id:'):
                term_id = line.split(': ')[1]
            elif line.startswith('xref:'):
                xrefs.append(line.split(': ')[1].split(' ')[0])

        omim_ids, orphanet_ids = extract_ids(xrefs)
        if omim_ids or orphanet_ids:
            entry_data = {
                "id": term_id,
                "omim_ids": omim_ids,
                "orphanet_ids": orphanet_ids
            }
            output.append(entry_data)

    return output

def main(input_file, output_file):
    with open(input_file, 'r') as f:
        data = f.read()

    processed_data = process_data(data)

    with open(output_file, 'w') as f:
        json.dump(processed_data, f, indent=4)

if __name__ == "__main__":
    input_file = "mondo.obo"
    output_file = "evioutput.json"
    main(input_file, output_file)
