import math
from os import listdir
from os.path import isfile, join
from scipy import spatial

from QueryHandling.QueryProcess import processQuery
from indexing.indexer import load_index, corpusDir


def build_vectors(index):
    DocumentsVectors = {}
    Terms = index.keys()
    Terms = list(Terms)
    corpusfiles = [f for f in listdir(corpusDir) if isfile(join(corpusDir, f))]
    for file in corpusfiles:
        DocumentsVectors[file] = [0] * len(Terms)
    for i in range(len(Terms)):
        term = str(Terms[i])
        for record in index[term]:
            DocumentsVectors[record[0]][i] = len(index[term]) / record[1]
    return DocumentsVectors


def getTermsId(index):
    dic = {}
    Terms = index.keys()
    Terms = list(Terms)
    for i in range(len(Terms)):
        dic[Terms[i]] = i
    return dic


def query_vector(query_terms, index):
    TermsId = getTermsId(index)
    queryVector = [0] * len(TermsId)
    temp_dict = {}
    for term in query_terms:
        if (temp_dict.__contains__(term)):
            temp_dict[term] += 1
        else:
            temp_dict[term] = 1
    for term in temp_dict.keys():
        if (TermsId.__contains__(term)):
            queryVector[TermsId[term]] = temp_dict[term] * len(index[term])
    return queryVector


def cosine_similarity(v1, v2):
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]
        y = v2[i]
        sumxx += x * x
        sumyy += y * y
        sumxy += x * y
    try:
        ret = sumxy / math.sqrt(sumxx * sumyy)
    except:
        return 0
    return ret


def getmatches(queryVector, DocumentVectors):
    answers = []
    for vector in DocumentVectors.keys():
        value = 1 - spatial.distance.cosine(queryVector, DocumentVectors.get(vector))
        # value2 = cosine_similarity(queryVector, DocumentVectors.get(vector))
        if (value > 0.0):
            answers.append([value, vector])
    return sorted(answers, reverse=True)


if __name__ == '__main__':
    query = """ U.N . CONSIDERATION OF THE CONFLICT BETWEEN ISRAEL AND ITS
ARAB NEIGHBORS ."""
    query = processQuery(query)
    print(query)
    index = load_index('../indexfiles/index.json')
    Vectors = build_vectors(index)
    query_terms = query.split()
    queryVector = query_vector(query_terms, index)
    val = getmatches(queryVector, Vectors)
    print(val.__len__())
    for some in val:
        print(str(some[1]) + "       " + str(some[0]))
