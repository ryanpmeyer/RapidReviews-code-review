from Bio import Entrez
import json, time

def search(query):
    Entrez.email = 'isaacmerritt@berkeley.edu'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='1000',
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    return results

def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'isaacmerritt@berkeley.edu'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results

search_words = ["COVID-19", "Biological Sciences", "Chemical Sciences", "Biochemistry", "Chemistry", "Ecology", "Evolution", "Biodiversity", "Genetics", "Genomics", "Epigenetics", "Immunology", "Integrative Biology", "Molecular and Cell Biology", "Plant Biology", "Structural Biology", "Toxicology", "Vaccinology", "Virology", "Zoonotic Diseases", "Public Health", "Physical Sciences", "Engineering", "Biomedical Engineering", "Biotechnology", "Biophysics", "Botany", "Chemical Engineering", "Climate Science", "Computational Sciences", "Data Science", "Information Science", "Earth Sciences", "Geosciences", "Materials Science", "Mathematics", "Physics", "Statistics", "Zoology", "Humanities", "Social Sciences", "Medical Sciences"]

if __name__ == '__main__':
    for word in search_words:
        results = search(word)
        id_list = results['IdList']
        papers = fetch_details(id_list)
        with open("data/" + word.replace(' ', '_').lower() + ".json", 'w') as f:
            f.write(json.dumps(papers))
        print("Data collection for", word, "done")
        time.sleep(5)
