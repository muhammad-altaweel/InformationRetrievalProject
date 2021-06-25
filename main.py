

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import enchant
import spacy
from os import listdir
from os.path import isfile, join
from itertools import permutations


def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


def editDistDP(str1, str2):
    # Create a table to store results of subproblems
    m = len(str1)
    n = len(str2)
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]

    # Fill dp[][] in bottom up manner
    for i in range(m + 1):
        for j in range(n + 1):

            # If first string is empty, only option is to
            # insert all characters of second string
            if i == 0:
                dp[i][j] = j  # Min. operations = j

            # If second string is empty, only option is to
            # remove all characters of second string
            elif j == 0:
                dp[i][j] = i  # Min. operations = i

            # If last characters are same, ignore last char
            # and recur for remaining string
            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]

            # If last character are different, consider all
            # possibilities and find minimum
            else:
                dp[i][j] = 1 + min(dp[i][j - 1],  # Insert
                                   dp[i - 1][j],  # Remove
                                   dp[i - 1][j - 1])  # Replace
    return dp[m][n]


def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union


def compare(l1, l2):
    if abs(l1[0] - l2[0]) < 0.001:
        pass
    if l1[0] > l2[0]:
        return True
    else:
        return False

if __name__ == '__main__':
    onlyfiles = [f for f in listdir('./test') if isfile(join('./test', f))]
    print(onlyfiles)
    # sp = spacy.load('en_core_web_sm')
    # sentence = sp(u'Latest Rumours: Manchester United is looking to sign Harry Kane for $90 million')
    # for word in sentence:
    #     print(word.text,word.pos_)
    # for entity in sentence.ents:
        # print(entity.text + ' - ' + entity.label_ + ' - ' + str(spacy.explain(entity.label_)))
    # for m in sentence.noun_chunks:
    #     print(m.text)


    # d = enchant.Dict("en_US")
    # wrong = 'mohter'
    # suggetList = d.suggest(wrong)
    # print(suggetList)
    # l = list()
    # for k in suggetList:
    #     jaccardVar = jaccard_similarity(k,wrong)
    #     editDisVar = levenshteinDistance(k,wrong)
    #     isPermutated = k in (''.join(j) for j in permutations(wrong))
    #     newList = list()
    #     newList.append(jaccardVar)
    #     newList.append(editDisVar-(1 if isPermutated else 0))
    #     newList.append(k)
    #     l.append(newList)
    # print(l.sort(key => compare))


