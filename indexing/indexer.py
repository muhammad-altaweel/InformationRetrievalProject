import json
from os import listdir
from os.path import isfile, join
from nltk import PorterStemmer
import re
import string


corpusDir = '../corpus/'
irregularVerbsFile = '../Documents/irregular_verbs.txt'
DaysNamesFile = '../Documents/Days.txt'
MonthNamesFile = '../Documents/Months.txt'
CurrenciesFile = '../Documents/Currencies.txt'
StopWordsFile = '../Documents/stop_words.txt'
global irregularVerbsDict
global DaysOfTheWeek
global MonthsNames
global Currencies
global StopWords


def binary_search(array, element):
    mid = 0
    start = 0
    end = len(array) - 1
    step = 0
    while start <= end:
        step = step + 1
        mid = (start + end) // 2

        if element == array[mid]:
            return mid

        if element < array[mid]:
            end = mid - 1
        else:
            start = mid + 1
    return -1


def openfile(filename):
    try:
        file = open(filename, 'r')
        l = file.read()
        file.close()
        return l
    except:
        return 'something went wrong with open file' + filename


def get_irregular_verbs():
    words = openfile(irregularVerbsFile)
    words = words.lower()
    words = words.split('\n')
    dict = {}
    for line in words:
        wordsList = line.split()
        for word in wordsList:
            dict[word] = wordsList[0]
    return dict


def get_Days_names():
    words = openfile(DaysNamesFile)
    words = words.lower()
    words = words.split('\n')
    dict = {}
    for line in words:
        wordsList = line.split()
        for word in wordsList:
            dict[word] = wordsList[0]
    return dict


def get_Months_names():
    words = openfile(MonthNamesFile)
    words = words.lower()
    words = words.split('\n')
    dict = {}
    for line in words:
        wordsList = line.split()
        for word in wordsList:
            dict[word] = wordsList[0]
    return dict


def get_stop_words():
    words = openfile(StopWordsFile)
    words = words.lower()
    words = words.split('\n')
    arr = []
    for line in words:
        wordsList = line.split()
        for word in wordsList:
            arr.append(word)
    arr = sorted(arr)
    return arr


def getCurrencies():
    words = openfile(CurrenciesFile)
    words = words.lower()
    words = words.split('\n')
    dict = {}
    for line in words:
        wordsList = line.split('-')
        for word in wordsList:
            dict[word] = wordsList[0]
    return dict


def getInfinitive(word):
    global irregularVerbsDict
    if irregularVerbsDict.__contains__(word):
        return irregularVerbsDict[word]
    return word


def getInfinitiveDay(word):
    global DaysOfTheWeek
    if DaysOfTheWeek.__contains__(word):
        return DaysOfTheWeek[word]
    return word


def getInfinitiveMonth(word):
    global MonthsNames
    if MonthsNames.__contains__(word):
        return MonthsNames[word]
    return word


def getInfinitiveCurrency(word):
    global Currencies
    if Currencies.__contains__(word):
        return Currencies[word]
    return word


def checkIfIrRegularOrShortcut(word):
    global irregularVerbsDict
    global DaysOfTheWeek
    global MonthsNames
    global Currencies
    word = getInfinitive(word)
    word = getInfinitiveDay(word)
    word = getInfinitiveMonth(word)
    word = getInfinitiveCurrency(word)
    isRorS = True if irregularVerbsDict.__contains__(word) or DaysOfTheWeek.__contains__(
        word) or MonthsNames.__contains__(word) or Currencies.__contains__(word) else False
    return [isRorS, word]


def stemSentence(sentence):
    token_words = sentence.split(' ')
    stem_sentence = []
    porter = PorterStemmer()
    for word in token_words:
        newList = checkIfIrRegularOrShortcut(word)
        if newList[0]:
            stem_sentence.append(newList[1])
            stem_sentence.append(" ")
        else:
            stem_sentence.append(porter.stem(word))
            stem_sentence.append(" ")
    return "".join(stem_sentence)


def build_index(Documents):
    dict = {}
    for i in range(len(Documents)):
        document = Documents[i][0]
        temp_dict = {}
        for term in document.split():
            if (temp_dict.__contains__(term)):
                temp_dict[term] += 1
            else:
                temp_dict[term] = 1
        for term in temp_dict.keys():
            if (dict.__contains__(term)):
                dict[term].append([Documents[i][1], temp_dict[term]])
            else:
                dict[term] = [[Documents[i][1], temp_dict[term]]]
    return dict


def save_index(path, data):
    try:
        file = open(path, "w")
        file.write(json.dumps(data))
        file.close()
        return True

    except:
        print("EXCEPTION: while save JSON file: " + path)
        return False


def load_index(path):
    try:
        file = open(path, "r")
        data = json.loads(file.read())
        file.close()
        return data
    except:
        print("EXCEPTION: while load JSON file: " + path)
        return False


if __name__ == '__main__':
    porter = PorterStemmer()
    irregularVerbsDict = get_irregular_verbs()
    DaysOfTheWeek = get_Days_names()
    MonthsNames = get_Months_names()
    StopWords = get_stop_words()
    Currencies = getCurrencies()
    listOfFilterdDocuments = []
    corpusfiles = [f for f in listdir(corpusDir) if isfile(join(corpusDir, f))]
    corpusfiles = sorted(corpusfiles, reverse= True)
    print (corpusfiles)
    # date1 = datetime.now()
    for file in corpusfiles:
        fileWords = openfile(corpusDir + file)
        # Remove Unicode
        document_test = re.sub(r'[^\x00-\x7F]+', ' ', fileWords)
        # Remove Mentions
        document_test = re.sub(r'@\w+', '', document_test)
        # Lowercase the document
        document_test = document_test.lower()
        # Remove punctuations
        document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test)
        # Remove the doubled space
        document_test = re.sub(r'\s{2,}', ' ', document_test)
        # Remove stop words
        document_test = " ".join([word for word in document_test.split(' ') if binary_search(StopWords, word) == -1])
        listOfFilterdDocuments.append([document_test,file])
    stemmedSentence = []
    for sentence in listOfFilterdDocuments:
        newSentence = stemSentence(sentence[0])
        # print(newSentence)
        stemmedSentence.append([newSentence,sentence[1]])

    index = build_index(stemmedSentence)
    save_index('../indexfiles/index.json', index)
    # index = load_index('../indexfiles/index.json')
    # print(index)
