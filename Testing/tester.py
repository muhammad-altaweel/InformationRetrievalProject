# from searchengine import matcher, loader
import json
import math

from QueryHandling.QueryProcess import processQuery
from indexing.indexer import load_index
from matching.Matching_functions import build_vectors, query_vector, getmatches


def loadQueries():
    file = open('../Documents/queries.txt','r')
    queries = file.read()
    file.close()
    return [q for q in queries.split('\n') if q]

def loadRelevance():
    file = open('../Documents/relevance.txt', 'r')
    text = file.read()
    file.close()
    relevances = [r for r in text.split('\n') if r]
    final_relevance = [relevance.split() for relevance in relevances ]
    return final_relevance

def getNGCD(items):
    doc  , rel1 = items[0]
    index = 0
    sum = 0.0
    idcg = 0.0
    for d , r in items: 
        idcg = idcg + r
        if index > 1:
            sum = sum + (r / math.log(index,10))
        index = index + 1
    # print("sum")
    # print(sum)        
    dcg = rel1 + sum
    ndcg = dcg / idcg
    return ndcg


# def getEvaluaton():
#     queries = loadQueries()
#     sumNdcg = 0.0
#     for query in queries :
#         itemsResults = matcher.match(query.lower())
#         sumNdcg = sumNdcg + getNGCD(list(itemsResults.items()))
#
#     Ndcg = sumNdcg / 83
#     # print("nnnnn")
#     # print(Ndcg)
#     return Ndcg

def save_json(path, data):
    try:
        file = open(path, "w")
        file.write(json.dumps(data))
        file.close()
        return True

    except:
        print("EXCEPTION: while save JSON file: " + path)
        return False


def load_json(path):
    try:
        file = open(path, "r")
        data = json.loads(file.read())
        file.close()
        return data
    except:
        print("EXCEPTION: while load JSON file: " + path)
        return False

def test(Vectors,index):
    queries = loadQueries()
    relevances = loadRelevance()
    test_cases = {}
    for query, relevance in zip(queries, relevances):
        query = processQuery(query)
        query_terms = query.split()
        queryVector = query_vector(query_terms, index)
        results = getmatches(queryVector, Vectors)
        results = [x[1] for x in results]
        results = [r.replace(".txt", "") for r in results]
        shared_res = set(relevance) & set(results)
        test_cases[query] = [(doc, results.index(doc) + 1 if doc in results else -1)
                             for doc in shared_res]
        test_cases[query].append(len(results))
    return test_cases

if __name__ == '__main__':
    index = load_index('../indexfiles/index.json')
    Vectors = load_json('../indexfiles/Vectors.json')
    results = test(Vectors, index)
    save_json('../indexfiles/test_cases.json', results)


