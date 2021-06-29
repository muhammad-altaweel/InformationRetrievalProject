import re
import string

from nltk import PorterStemmer

from indexing.indexer import get_irregular_verbs, get_Days_names, get_Months_names, get_stop_words, getCurrencies

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


def processQuery(query):
    global irregularVerbsDict
    global DaysOfTheWeek
    global MonthsNames
    global Currencies
    global StopWords
    irregularVerbsDict = get_irregular_verbs()
    DaysOfTheWeek = get_Days_names()
    MonthsNames = get_Months_names()
    StopWords = get_stop_words()
    Currencies = getCurrencies()
    StopWords = get_stop_words()
    # Remove Unicode
    document_test = re.sub(r'[^\x00-\x7F]+', ' ', query)
    # Remove Mentions
    document_test = re.sub(r'@\w+', '', document_test)
    # Lowercase the document
    document_test = document_test.lower()
    # # Remove punctuations
    document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test)
    # Remove the doubled space
    document_test = re.sub(r'\s{2,}', ' ', document_test)
    # Remove stop words
    document_test = " ".join([word for word in document_test.split(' ') if word not in StopWords])
    document_test = stemSentence(document_test)
    return document_test


if __name__ == '__main__':
    query= "gone to africa and learned alot "
    print(processQuery(query))
