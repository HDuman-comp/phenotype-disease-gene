import os
import ssl
import urllib.request
import subprocess
import tarfile
import certifi

# Adımları gerçekleştirecek fonksiyonlar

def download_file(url, file_name):
    with urllib.request.urlopen(url, context=ssl.create_default_context(cafile=certifi.where())) as response:
        data = response.read()
        with open(file_name, 'wb') as f:
            f.write(data)

def extract_tar_gz(file_name):
    with tarfile.open(file_name, 'r:gz') as tar:
        tar.extractall()

def run_python_script(script_path):
    subprocess.run(["/usr/local/bin/python3.12", script_path])

# Adımlar

# 1. Dosyaları indirme
download_file("https://github.com/obophenotype/human-phenotype-ontology/releases/download/v2024-03-06/phenotype.hpoa", "Phenotype.hpoa")
download_file("https://github.com/obophenotype/human-phenotype-ontology/releases/download/v2024-03-06/hp.obo", "hp.obo")
download_file("https://github.com/obophenotype/human-phenotype-ontology/releases/download/v2024-03-06/genes_to_disease.txt", "gene_to_disease.txt")
download_file("https://www.orphadata.com/data/json/en_product1.json.tar.gz", "en_product1.json.tar.gz")

# 2. Tar.gz dosyasını açma
extract_tar_gz("en_product1.json.tar.gz")

# 3. gene_to_disease.txt dosyasını parse etme
run_python_script("/Users/hamzaduman/script1/genes-to-disease-toAll.py")

# 4. gene-disease-hpo.py scriptini çalıştırma
run_python_script("/Users/hamzaduman/script1/gene-disease-hpo.py")

# 5. en_product1.json dosyasını parse etme
run_python_script("/Users/hamzaduman/script1/toDefSynTxt.py")

# 6. definitonsandSynoyms.txt dosyasını parse etme
run_python_script("/Users/hamzaduman/script1/summarizeDefandSyn.py")

# 7. addingDEF+.py scriptini çalıştırma
run_python_script("/Users/hamzaduman/script1/addingDEF+.py")

# 8. clingene_disease_summary.csv indirme
download_file("https://search.clinicalgenome.org/kb/gene-validity/download", "clingene_disease_summary.csv")

# 9. mondo.obo indirme
download_file("http://purl.obolibrary.org/obo/mondo.obo", "mondo.obo")

# 10. mondo.obo file “mondoToOrphaOrOmim.py” kodu ile çalıştırılır
run_python_script("/Users/hamzaduman/script1/mondoToOrphaOrOmim.py")

# 11. clingendiseaseanaliysis.py scripti ile birlikte clingene_disease_summary.csv çalıştırlır
run_python_script("/Users/hamzaduman/script1/clingendiseaseanaliysis.py")

# 12. clingenSumm.json sonuç olarak bu dosya döner
# Gerekirse burada dosya temizleme işlemleri yapılabilir.

# 13. "clingenSumm.json" ve “evioutput.json" dosyaları “combineClingenandEvioutput.py” scripti ile çalıştırlır
run_python_script("/Users/hamzaduman/script1/combineClingenandEvioutput.py")

# 14. ”combined_dataCE.json” ve “newout.json” fileları kullanılarak “addCombinedCEtoALLDATA.py” scripti çalıştırılır
run_python_script("/Users/hamzaduman/script1/addCombinedCEtoALLDATA.py")

# 15. Lit_evidence list oluşturma: “literature evidence list.py” kullanılarak phenotpye referancelar unique bir şekilde farklı bir arraye taşınır
run_python_script("/Users/hamzaduman/script1/literatureEvidencelist.py")

# 16. Sonrasında phenotpye içerisindeki evidenceler kaldırılır gereksiz duruma düştükleri için son outputun ismi “remove_ref.json”
run_python_script("/Users/hamzaduman/script1/remove_ref_in phenotype.py")
# 17. "lastVersion.json" ile file son halini alır
run_python_script("/Users/hamzaduman/script1/fixtheallformat.py")

