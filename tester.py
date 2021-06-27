from searchengine import matcher, loader
import math

def loadQueries():
    queries = loader.loadFile('./storage/queries.txt')
    return [q for q in queries.split('\n') if q]

def loadRelevance():
    text = loader.loadFile('./storage/relevance.txt')
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


def getEvaluaton():
    queries = loadQueries()
    sumNdcg = 0.0
    for query in queries :
        itemsResults = matcher.match(query.lower())
        sumNdcg = sumNdcg + getNGCD(list(itemsResults.items()))

    Ndcg = sumNdcg / 83
    # print("nnnnn")
    # print(Ndcg)
    return Ndcg

def test(fresh = False):
    queries = loadQueries()
    relevances = loadRelevance()
    
    if(not fresh):
        cached_results = loader.loadJsonFile('./storage/test_cases.json')
        if(cached_results):
            return cached_results

    test_cases = {}
    for query, relevance in zip(queries, relevances):
        results = list(matcher.match(query.lower()).keys())
        results = [r.replace(".txt", "") for r in results]
        shared_res = set(relevance) & set(results)
        test_cases[query] = [(doc, results.index(doc) + 1 if doc in results else -1)
                             for doc in shared_res]

    loader.saveJsonFile('./storage/test_cases.json', test_cases)
    return test_cases