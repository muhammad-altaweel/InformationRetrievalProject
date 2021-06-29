import json

from QueryHandling.QueryProcess import processQuery
from indexing.indexer import load_index
from matching.Matching_functions import build_vectors, query_vector, getmatches


def loadQueries():
    file = open('../Documents/queries.txt', 'r')
    queries = file.read()
    file.close()
    return [q for q in queries.split('\n') if q]


def loadRelevance():
    file = open('../Documents/relevance.txt', 'r')
    text = file.read()
    file.close()
    relevances = [r for r in text.split('\n') if r]
    final_relevance = [relevance.split() for relevance in relevances]
    return final_relevance


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


def test(Vectors, index):
    queries = loadQueries()
    relevances = loadRelevance()
    test_cases = {}
    final = 0
    for query, relevance in zip(queries, relevances):
        query = processQuery(query)
        query_terms = query.split()
        queryVector = query_vector(query_terms, index)
        results = getmatches(queryVector, Vectors)
        results = [x[1] for x in results]
        results = [r.replace(".txt", "") for r in results]
        shared_res = set(relevance) & set(results)
        total = len(shared_res)
        res = total / len(relevance)
        dif1 = len(results) - len(shared_res)
        dif1 /= 423
        res -= dif1
        test_cases[query] = res
        final += res

    final /= len(queries)
    return final


if __name__ == '__main__':
    index = load_index('../indexfiles/index.json')
    Vectors = build_vectors(index)
    save_json('../indexfiles/Vectors.json', Vectors)
    results = test(Vectors, index)
    print(results)
