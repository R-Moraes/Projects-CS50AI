import nltk
import sys
import os
import string
from math import log
from operator import itemgetter
import collections

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    filenames = dict()
    paths = [path for path in os.listdir(directory)]
    
    for p in paths:
        with open(os.path.join(directory,p), 'r') as file:
            words = file.read()
        filenames[p] = words
    
    return filenames


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    
    words = document.lower()
    words = nltk.word_tokenize(words)
    x = []
    for w in words:
        for i in string.punctuation:
            if i in w:
                w = w.replace(i, "")
        x.append(w)
    words = x
    words = [w for w in words if w != ""]
    words = [w for w in words if not w in nltk.corpus.stopwords.words("english")]
    words = sorted(words, reverse=True)

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    NUM_DOC = len(documents)
    c_idfs = dict()
    for k,v in documents.items():
        for word in v:
            if word in documents[k]:
                if word in c_idfs:
                    c_idfs[word] += 1
                else:
                    c_idfs[word] = 1
    
    for word in c_idfs.keys():
        c_idfs[word] = abs(log((NUM_DOC/c_idfs[word])))
    
    return c_idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    ranked = dict()
    for k in files.keys():
        summ = 0
        tf = 0
        for word in query:
            if word in files[k]:
                tf = files[k].count(word)
                summ += (tf * idfs[word])
        ranked[k] = summ           
    
    ranked = [k for k,v in sorted(ranked.items(),key=itemgetter(1), reverse=True)]
    
    return ranked


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    wcm = dict()
    ctd = dict()
    
    for key in sentences.keys():
        summ = 0
        count = 0
        counter=collections.Counter(sentences[key])

        for word in query:
            if word in sentences[key]:
                summ += idfs[word]
                count += counter[word]

        wcm[key] = summ
        ctd[key] = count/len(sentences[key])
    
    wcm2 = [ k for k,v in sorted(wcm.items(), key=itemgetter(1), reverse=True)]
    
    for i,sent in enumerate(wcm2):
        for j,sent2 in enumerate(wcm2):
            if sent != sent2:
                if wcm[sent] == wcm[sent2]:
                    if ctd[sent] > ctd[sent2]:
                        wcm2[j] = sent
                        wcm2[i] = sent2
    for i in wcm2[:30]:
        print(i)
    return wcm2[:n]
                


if __name__ == "__main__":
    main()
