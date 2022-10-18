import enchant
import spacy
from date_extractor import extract_dates
from itertools import permutations
from os import listdir
from os.path import isfile, join

from indexing.indexer import corpusDir

global EnglishDict


def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


def editDistDP(str1, str2):
    m = len(str1)
    n = len(str2)
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i][j - 1],  # Insert
                                   dp[i - 1][j],  # Remove
                                   dp[i - 1][j - 1])  # Replace
    return dp[m][n]


def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union


def CorrectWord(word):
    global EnglishDict
    suggetList = EnglishDict.suggest(word)
    l = list()
    for k in suggetList:
        jaccardVar = jaccard_similarity(k, word)
        editDisVar = levenshteinDistance(k, word)
        isPermutated = k in (''.join(j) for j in permutations(word))
        newList = list()
        newList.append(jaccardVar / (editDisVar - (1 if isPermutated else 0)))
        newList.append(k)
        l.append(newList)
    return sorted(l, reverse=True)[0]


def CorrectQuery(query):
    query = query.split(' ')
    EnglishDict = enchant.Dict("en_US")
    newQuery = list()
    for word in query:
        if (not EnglishDict.check(word)):
            newQuery.append((CorrectWord(word))[1])
        else:
            newQuery.append(word)
    return " ".join(newQuery)


def extractDates():
    corpusfiles = [f for f in listdir(corpusDir) if isfile(join(corpusDir, f))]
    matches = []
    for file in corpusfiles:
        temp_file = open(join(corpusDir, file), 'r')
        string = temp_file.read()
        match = extract_dates(string)
        match = list(match)
        if (len(match) > 0):
            matches.append([match, file])
    return matches


def get_noun(sentence):
    sp = spacy.load('en_core_web_sm')
    sentence = sp(sentence)
    for m in sentence.noun_chunks:
        print(m.text)


if __name__ == '__main__':
    # print(CorrectQuery('mohter helcopter speak ris'))
    # print(extractDates())
    get_noun('sami wins football game,karam plays with fadi')
