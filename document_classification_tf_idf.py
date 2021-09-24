from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from nltk import stem
from nltk.corpus import stopwords
import re


def depunctuate(list_of_strings):
    """
    Remove punctuations (except ‘)
    :param list_of_strings:
    :return: list of strings
    """
    depunctuated_list = [re.sub('[!@#$%&’()*+,\\\'-./:;”“<=>?\"[\]^_—`{|}~\d…]', ' ', title) for title in
                         list_of_strings]
    return depunctuated_list


def stemming(list_of_documents):
    """
    Stems words from the documents
    :param list_of_documents: list of strings
    :return: list of strings, stemmed documents
    """
    stemmer = stem.PorterStemmer()
    stemmed_documents = []

    for text in list_of_documents:
        temp = []
        for word in text.split():
            temp.append(stemmer.stem(word))
        stemmed_documents.append(temp)
    return stemmed_documents


def stop_words_removal(list_of_documents):
    """
    Removes stop words from the list of documents
    :param list_of_documents: list of strings, that are text documents
    :return: list of documents: list of strings
    """
    stop_words = set(stopwords.words('english'))
    sp_titles = []
    for document in list_of_documents:
        temp = []
        for word in document:
            if word not in stop_words:
                temp.append(word)
        sp_titles.append(temp)
    # Convert back to list of text documents
    list_of_documents = [' '.join(doc) for doc in sp_titles]
    return list_of_documents


def cosine_similarity(doc1, doc2):
    """
    Calculates cosine similarity for 2 documents
    :param doc1: string, document_1
    :param doc2: string, document_2
    :return: cosine
    """
    dot_product = np.dot(doc1, doc2)
    normalized_doc1 = np.linalg.norm(doc1)
    normalized_doc2 = np.linalg.norm(doc2)
    cos = dot_product / (normalized_doc1 * normalized_doc2)
    return cos

# Load dataset
collection_E = fetch_20newsgroups(categories=['alt.atheism'])
collection_A = fetch_20newsgroups(categories=['soc.religion.christian'])

# Pre-processing
collection_E = collection_E['data']
collection_E = depunctuate(collection_E)
collection_E = stemming(collection_E)
collection_E = stop_words_removal(collection_E)

collection_A = collection_A['data']
collection_A = depunctuate(collection_A)
collection_A = stemming(collection_A)
collection_A = stop_words_removal(collection_A)


def tf_idf(doc, top_N):
    """
    Calculates tf_idf for all docs and returns stems with top N tf_idf values
    :param doc: list of strings, documents
    :param top_N: integer, N is number of top tf_idf results
    :return: a list of strings, contains top N stems
    """
    # vectorizer returns normalized tf_idf
    vectorizer = TfidfVectorizer(smooth_idf=True, min_df=2, use_idf=True)

    doc = vectorizer.fit_transform(doc)
    # feature names (to get stems)
    feature_array = np.array(vectorizer.get_feature_names())
    # argsort sorts ascending so we reverse the list
    # flatten to make all values into 1st dimension
    # get indexes of sorted tf_idf values for each stem
    index = np.argsort(np.asarray(doc.sum(axis=0)).flatten())[::-1]
    list_of_top_n = feature_array[index[:top_N]]
    return list_of_top_n


doc1_S = tf_idf(collection_E, 4000)
doc2_S = tf_idf(collection_A, 4000)


print(doc1_S, doc2_S)
#x= cosine_similarity(doc2_S, test_doc)
'''
can use these lines to validate tf_idf order
scores = zip(vectorizer.get_feature_names(), np.asarray(doc2.sum(axis=0)).flatten())
sort by 2nd value which is the tf_idf value
sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
for item in sorted_scores:
    print(f"{item[0]:20} Score: {item[1]}")
'''


#x=cosine_similarity(doc1,doc2)

