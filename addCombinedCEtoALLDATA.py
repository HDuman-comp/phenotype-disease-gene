import json
import re

def extract_orphanet_number(orphanet_id):
    return re.search(r'\d+', orphanet_id).group()

def extract_omim_number(omim_id):
    return re.search(r'\d+', omim_id).group()

# 1. Load the JSON files
with open('combined_dataCE.json', 'r') as f1:
    data1 = json.load(f1)

with open('updated_newout.json', 'r') as f2:
    data2 = json.load(f2)

# 2. Iterate through the combined data
for gene_data in data1:
    gene_symbol = gene_data.get('gene_symbol')
    orphanet_id = gene_data.get('orphanet_id')
    omim_id = gene_data.get('omim_id')

    # 3. Match against genes in the updated data
    for updated_gene in data2:
        if gene_symbol == updated_gene.get('gene'):

            # 4. Match the Orphanet IDs
            for updated_disease in updated_gene['diseases']:
                if 'orpha_id' in updated_disease:
                    updated_orphanet_id = extract_orphanet_number(updated_disease['orpha_id'])
                    if orphanet_id and updated_orphanet_id == extract_orphanet_number(orphanet_id):
                        # 5. Add the inheritance data if match found
                        updated_disease['mode_of_inheritance'] = gene_data.get('mode_of_inheritance')
                        updated_disease['classification'] = gene_data.get('classification')

                # 6. Match the OMIM IDs
                if 'omim_id' in updated_disease:
                    updated_omim_id = extract_omim_number(updated_disease['omim_id'])
                    if omim_id and updated_omim_id == extract_omim_number(omim_id):
                        # 7. Add the inheritance data if match found
                        updated_disease['mode_of_inheritance'] = gene_data.get('mode_of_inheritance')
                        updated_disease['classification'] = gene_data.get('classification')

# 8. Write the modified data to the output file
with open("merge_total.json", "w") as f:
    json.dump(data2, f, indent=2)
