import pandas as pd
import json
import string
from tqdm import tqdm
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


lemmatizer = WordNetLemmatizer()

# list of substrings to remove. stopwords, punctuation, etc.
remove = stopwords.words('english')
remove.extend(list(string.punctuation))


def clean_abstract(abstract):
    """ Takes raw abstract string, lemmatizes the words, strips punctuation, etc."""
    tokens = word_tokenize(abstract.lower())
    lemmatized_abstract = [
        lemmatizer.lemmatize(t) for t in tokens if t not in remove
    ]
    cleaned_abstract = ' '.join(lemmatized_abstract)
    return cleaned_abstract


def clean_doi(doi):
    """ removes website url from some dois """
    if "https" in doi or "http" in doi:
        return doi.split('.org')[1]
    return doi


def paperdf_from_json(filename = "COVIDScholar_snapshot.json"):
    """ Loads json paper data into a dataframe """

    print('Loading data.')

    abstracts = []
    titles = []
    authors = []
    dois = []
    oids = []

    raw_data = open(filename, 'r', encoding = "utf8")
    for line in tqdm(raw_data, leave=True):
        obj = json.loads(line)
        try:
            doi = obj['doi']
            oid = obj['_id']['$oid']
            title = obj['title']
            author = obj['authors']
            abstract = obj['abstract']
            doctype = obj['document_type']
            if abstract and doctype == 'paper':  # only papers with abstract are needed
                abstracts.append(clean_abstract(abstract))
                titles.append(title)
                authors.append(author)
                dois.append(clean_doi(doi))
                oids.append(oid)
        except KeyError:
            # might be a NaN row or badly formatted data
            continue

    print('Creating paper dataframe.')
    return pd.DataFrame({
        'doi'     : dois,
        'oid'     : oids,
        'authors' : authors,
        'title'   : titles,
        'abstract': abstracts
    })


def authordf_from_paperdf(paperdf):
    """ Given a dataframe of paper data, returns a dataframe of author names and the papers they have
    contributed to """

    # TODO: once we have author database change index from name to id

    print('Constructing author dataframe.')
    print('Gathering author names.')

    # authordf: dataframe of all authors and the dois of the papers they wrote
    # first, populate the unique authors
    authors_list = {'first_name': [], 'last_name': [], 'name': []}
    for i in tqdm(range(len(paperdf)), position=0, leave=True):
        author_list = paperdf['authors'][i]
        # doi_column.extend([doi]*len(author_list))
        for author in author_list:
            # error checking because some authors have no first/last name field
            try:
                first = author['first_name']
                last = author['last_name']
                name = author['name']
            except:
                continue
            authors_list['first_name'].append(first)
            authors_list['last_name'].append(last)
            authors_list['name'].append(name)

    print('Cleaning dataframe.')

    authordf = pd.DataFrame(authors_list)
    authordf.drop_duplicates('name', inplace = True)
    authordf.set_index('name', inplace = True)
    authordf['dois'] = [[] for _ in range(len(authordf))]

    print('Gathering paper DOIs.')

    # second, populate paper dois for each author
    for i in tqdm(range(len(paperdf)), position=0, leave=True):
        author_list = paperdf['authors'][i]
        doi = paperdf['doi'][i]
        for author in author_list:
            # error checking because some authors have no first/last name field
            try:
                first = author['first_name']
                last = author['last_name']
                name = author['name']
            except:
                continue
            authordf.loc[name]['dois'].append(doi)

    return authordf


def load_data():
    """ Main function """

    paperdf = paperdf_from_json()

    return paperdf


if __name__ == '__main__':
    load_data()
