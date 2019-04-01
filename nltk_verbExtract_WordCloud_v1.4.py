import nltk
from urllib.request import urlopen
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import msvcrt as m
import time
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk import word_tokenize,sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk.probability import FreqDist
from heapq import nlargest
from collections import defaultdict
from nltk.tokenize import PunktSentenceTokenizer

def tokenizeWords(text):
    print("Tokenizing words...")
    words = word_tokenize(text.decode().lower())
    return words

def getTextfromUrl(url,choice):
    print("\nDownloading HTML from the URL...")
    page = urlopen(article)
    pageRead = page.read().decode('utf-8', 'ignore')
    page.close()
    soup = BeautifulSoup(pageRead, 'lxml')

    if choice==1:
        # GCP SLA
        rawText = soup.find_all("div", class_="devsite-article-body clearfix")
        text = ' '.join(map(lambda p: p.text, rawText))

    elif choice==2:
        # AWS Agreement
        rawText = soup.find_all("div", {"class":"lb-col lb-tiny-24 lb-mid-24"})
        text = ' '.join(map(lambda p: p.text, rawText))

    else:
        # GCP SLA
        rawText = soup.find_all("div", class_="devsite-article-body clearfix")
        text = ' '.join(map(lambda p: p.text, rawText))

    return text


def posTagging(tokenized):
    print("\nInitiating POS tagging")
    posTagged = []
    for i in tokenized:
        words = nltk.word_tokenize(i)
        tagged = nltk.pos_tag(words)
        # print(tagged)
        posTagged.append(tagged)
    return posTagged

def extractWords(posTagged, posList):
    # Really need to make this more efficient!!!!!
    print("\nExtracting words based on passed POS tags")
    print("> Passed POS tags : ",posList)
    extractedWords = []
    for eachPOSTag in posList:
        for posTaggedEach in posTagged:
            for word, pos in posTaggedEach:
                if (pos == eachPOSTag):
                    extractedWords.append(word)
    return extractedWords


def generateWordCloud(theWords):
    print("\nGenerating the Word Cloud")
    plt.imshow(theWords)
    plt.axis("off")
    plt.show()

def parseAndChunk(posTagged):
    chunkGram = "CHUNK: {<DT>?<JJ>*<NN>}"
    print("Beginning chunking using grammar : ",chunkGram)
    parser = nltk.RegexpParser(chunkGram)
    parsed = parser.parse(posTagged)
    drawTree(parsed)

def drawTree(parsed):
    parsed.draw()





# **************************************************************************************************************

print ("Select the Cloud Provider to process")
print ("1. GCP")
print ("2. AWS")
choice = input('Enter your choice [1-2] : \n')
choice = int(choice)


# The URL of the article

if choice==1:
    article = "https://cloud.google.com/compute/sla"
elif choice==2:
    article = "https://aws.amazon.com/agreement/#"
else:
    print("InValid Choice. Defaulting to GCP")
    article = "https://cloud.google.com/compute/sla"

print("Processing SLA from : ",article)

# article = "https://www.washingtonpost.com/opinions/global-opinions/jamal-khashoggi-what-the-arab-world-needs-most-is-free-expression/2018/10/17/adfc8c44-d21d-11e8-8c22-fa2ef74bd6d6_story.html?utm_term=.a76b41aefd8b"
# article = "https://www.washingtonpost.com/local/obituaries/george-mendonsa-sailor-whose-times-square-kiss-celebrated-end-of-wwii-dies-at-95/2019/02/18/6450196c-3398-11e9-854a-7a14d7fec96a_story.html"


text = getTextfromUrl(article,choice)
# print("The TEXT : ",text)

# Training the PunktTokenizer with our text
custom_token = PunktSentenceTokenizer(text)
# print("The custom Words : ",custom_token)

# Tokenzing our text with our trained tokenizer
print("\nTokenizing text")
tokenized = custom_token.tokenize(text)
print("> The tokennized sentences: ",tokenized)



# POS Tagging
posTagged = posTagging(tokenized)
print("> The POS tagged : ",posTagged)

print ("\n\nSelect the next step : ")
print ("1. Verb Extraction and WordCloud Generation")
print ("2. Chunking")
moreChoice = input('Enter your choice [1-2] : \n')
moreChoice = int(moreChoice)


if moreChoice==1:
    print("Proceeding with verb extraction and word cloud generation")
    posListVerbs = ["VB", "VBG", "VBD"  "VBN", "VBP", "VBZ"]

    # Extract POS words
    extractedWords = extractWords(posTagged, posListVerbs)
    print("> The Extracted words : ",extractedWords)

    # extractedWordsTest = "This is the word Cloud"

    extractedWordsString = ' '.join(extractedWords)


    # Word Cloud Creation
    theWords = WordCloud(collocations=False,background_color='white',relative_scaling=1.0).generate(extractedWordsString)
    generateWordCloud(theWords)

elif moreChoice==2:
    print("Proceeding with chunking!")
    parseAndChunk(posTagged)




