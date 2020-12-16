debug_print     = False  # Enables printing.
decimal_round   = 2     # Digits to which tf-idf matrix values are rounded.
import os
import gensim
import numpy as np
from pathlib import Path

currentpath = os.getcwd()                                        # Returns current path 
# Path to 
sample_paths_gen = Path(currentpath).rglob('sample-texts/*.txt') # Generates paths to any '*.txt' file in given directory
sample_paths     = [path for path in sample_paths_gen]           # Creates the file path for each path from sample_paths_gen
    
test_paths_gen   = Path(currentpath).rglob('text-to-check/*.txt')
test_paths       = [path for path in test_paths_gen]
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


""" Processing of sample texts """ # Gets corpus in the same manner as for texts to check.
def sample_corpus_from_path(sample_paths = sample_paths):
    clean_tokenized_texts = []

    for sample_path in sample_paths:
        f = open(sample_path, 'r', encoding='utf-8', errors='ignore') # Opens file for reading
        text = f.read()
        f.close()

        lemmatizer = WordNetLemmatizer()
        lemmatized = []
        for sentence in nltk.sent_tokenize(text):
            clean_sentence = re.sub('[^0-9A-Za-z \n]+', '', str([word for word in sentence.lower().split() if word not in stopwords.words('english')]))
            lemmatized.append(lemmatizer.lemmatize(clean_sentence))
        
        clean_tokenized_texts.append( [[w for w in word_tokenize(sentence)] for sentence in  lemmatized] )

        if (debug_print):
            print(clean_tokenized_texts[-1])
        
    return clean_tokenized_texts

def corpus_from_dictionary(tk_dictionary, clean_tokenized_texts):
    sample_documents_corpus = []
    for clean_tokenized_text in clean_tokenized_texts:
        sample_document_corpus = [tk_dictionary.doc2bow(clean_sentence) for clean_sentence in clean_tokenized_text]

        if (debug_print):
            print(sample_document_corpus)

        sample_documents_corpus.append(sample_document_corpus)

    return sample_documents_corpus


# Texts to check for similarity
def getMatches(text, samples_corpus):
    samples_corpus = sample_corpus_from_path(sample_paths)

    lemmatizer = WordNetLemmatizer()
    lemmatized = []
    for sentence in nltk.sent_tokenize(text):
        clean_sentence = re.sub('[^0-9A-Za-z \n]+', '', str([word for word in sentence.lower().split() if word not in stopwords.words('english')]))
        lemmatized.append(lemmatizer.lemmatize(clean_sentence))
    
    clean_test_text = [[w for w in word_tokenize(sentence)] for sentence in lemmatized]

    if (debug_print):
        print(clean_test_text)

    tk_dictionary = gensim.corpora.Dictionary(clean_test_text) # Maps each token to an id   
    if (debug_print):
        print(tk_dictionary.token2id)

    check_corpus = [tk_dictionary.doc2bow(clean_test_sentence) for clean_test_sentence in clean_test_text] # Generates BoW from token's dictionary
    if (debug_print):
        print(check_corpus)


    tf_idf_matrix = gensim.models.TfidfModel(check_corpus)    # Generates
    if (debug_print):
        for sentence_keys in tf_idf_matrix[check_corpus]:
            print([[tk_dictionary[id], np.around(freq, decimals=decimal_round)] for id, freq in sentence_keys])

    # From a given corpus of documents (sentences) a static index is created.
    # Another corpus may be used to query for text similarity. 
    # Computes cosine similarity of a dynamic query against the index.
    index = gensim.similarities.Similarity(currentpath, tf_idf_matrix[check_corpus], num_features=len(tk_dictionary))

    similarity_reports = [] #{'percentage':0,'path':''}

    for sample_corpus, path in zip(corpus_from_dictionary(tk_dictionary, samples_corpus), sample_paths):
        sum_of_sims =(np.sum(index[tf_idf_matrix[sample_corpus]], dtype=np.float32))
        similarity_percentage = round(float((sum_of_sims / len(clean_test_text)) * 100), decimal_round)

        similarity_reports.append([similarity_percentage, path])

    similarity_reports.sort(reverse=True, key=percentage_from_report)
    
    return similarity_reports
    
def percentage_from_report(e):
    return e[0]

"""
similarity_reports.sort(reverse=True, key=percentage_from_report)
for i in range (10):
    percentage = similarity_reports[i][0]
    if percentage > 100 :
        percentage = 'MAX ~ 99.99'
    print(f'For text {similarity_reports[i][1]} text similarity is: {percentage} % .')
print("\n")
"""