def extract_data(input_file, output_file):
    gene_disease_mapping = {}

    with open(input_file, 'r') as f_in:
        next(f_in)

        for line in f_in:
            columns = line.strip().split('\t')

            gene_symbol = columns[1]
            disease_id = columns[3]

            if gene_symbol in gene_disease_mapping:
                gene_disease_mapping[gene_symbol].append(disease_id)
            else:
                gene_disease_mapping[gene_symbol] = [disease_id]

    with open(output_file, 'w') as f_out:
        for gene_symbol, disease_ids in gene_disease_mapping.items():
            disease_ids_str = ' '.join(disease_ids)
            f_out.write(f"{gene_symbol}\t{disease_ids_str}\n")


input_file = "/Users/hamzaduman/script1/gene_to_disease.txt"
output_file = "all-gene-disease.txt"

extract_data(input_file, output_file)
