from urllib.request import urlopen
import json
from matplotlib import pyplot
from sklearn.decomposition import PCA
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import nltk
from nltk import word_tokenize, sent_tokenize
import msvcrt as m
import time
import re
from nltk.corpus import stopwords
from string import punctuation
from nltk import word_tokenize,sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk.probability import FreqDist
from heapq import nlargest
from collections import defaultdict
from nltk.tokenize import PunktSentenceTokenizer
import itertools



def tokenizeWords(text):
    print (text)
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
        #rawText = soup.find_all("div", {"class":"lb-col lb-tiny-24 lb-mid-24"})
        rawText = soup.find_all("div", {"class": "parsys content"})
        text = ' '.join(map(lambda p: p.text, rawText))


    elif choice==3:
        # Azure Agreement
        rawText = soup.find_all("div", {"class": "section"})
        text = ' '.join(map(lambda p: p.text, rawText))



    elif choice==4:
        # vmware Agreement
        rawText = soup.find_all("div", {"class": " lb-page-content"})
        text = ' '.join(map(lambda p: p.text, rawText))







    else:
        # GCP SLA
        rawText = soup.find_all("div", class_="devsite-article-body clearfix")
        text = ' '.join(map(lambda p: p.text, rawText))

    return text

def getFreqDist(tokenized):
    print("\n> Getting Freq Dist of modal verbs in the document")
    print("The list of modal verbs : ",listOfMVs)

    tokens = nltk.word_tokenize(str(tokenized))

    # print("The tokens : ",tokens)

    fDist = FreqDist(tokens)
    # print("The fDist : ", fDist)

    result = dict()
    for word, frequency in fDist.most_common(999999):
        if(word in listOfMVs):
            result[word] = frequency

        #print("The result : ",result)
    return result

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
    print (extractedWords)
    return extractedWords

def sentencounter(text):
    sent=sent_tokenize(text)
    counter=0
    modalcount=0
    modalflag=False
    for s in sent:
        counter+=1




        if any(word in s for word in listOfMVs):
            modalcount+=1
            #print("sentens",s)
            #print("no of sent with modal",modalcount)
    #print("no of sentns",counter)
    return counter

def Permissionwords(text):
    dict={}

    sent = sent_tokenize(text)
    counter = 0
    obligationCount = 0
    modalflag = False
    for s in sent:
        #print(s)
        counter += 1

        if any(word in s for word in permissionwords):
            print(obligationWords)
            obligationCount += 1
            print("sent", s)


            #print("no of sent with obligation", obligationCount)
    #print("no of sentns", counter)
    return counter


def generateWordCloud(theWords):
    print("\nGenerating the Word Cloud")
    plt.imshow(theWords)
    plt.axis("off")
    plt.show()

def parseAndChunk(posTagged):
    # chunkGram = "CHUNK: {<DT>?<JJ>*<NN>}"
    # chunkGram = "CHUNK: {<NN|NNS|PRP>*<will|shall|may|must|can|could|should|shall><balancing|apply|serve|include|provide|states|future|load|arises|showing|becomes|violate|meets|notify|comply|responding|meet|receive|failing|forfeit|exceed|auditing|occur><PRP|NNP|NNR*>*}"
    # chunkGram = "CHUNK: {<NN.?|PRP>*<will|shall|may|must|can|could|should|shall><balancing|apply|serve|include|provide|states|future|load|arises|showing|becomes|violate|meets|notify|comply|responding|meet|receive|failing|forfeit|exceed|auditing|occur><PRP|NNP|NNR*>*}"
    # chunkGram = "Chunk: {<NN.*>+<will|shall|may|must|can|could|should|shall>+<VB.?>}"
    # chunkGram = "Chunk: {<DT|PRP|NN.*>*<will|shall|may|must|can|could|should>*<PRP|NNP|NNR*>*}"

    chunkGram = "Chunk: {<DT|NN.*|PRP>?<MD>+<VB.*>*<NN.*|PRP|JJ>*}"

    print("Beginning chunking using grammar : ",chunkGram)
    parser = nltk.RegexpParser(chunkGram)
    print("The parser : ",parser)
    parsed = parser.parse(posTagged)
    print("The parsed : ",parsed)
    drawTree(parsed)
    print("Finished drawing")

def drawTree(parsed):
    parsed.draw()



print ("Select the Cloud Provider to process")
print ("1. GCP")
print ("2. AWS")
print ("3. Azure")
print ("4. VMware")
print ("5. Oracle")

choice = input('Enter your choice [1-5] : \n')
choice = int(choice)

# https://www.vmware.com/support/vcloud-air/sla
#
if choice==1:

# The URL of the article
    article = "https://cloud.google.com/compute/sla"
elif choice==2:
    #article = "https://aws.amazon.com/compute/sla/"
    article = "http://web.archive.org/web/20181214180059/https://aws.amazon.com/compute/sla/"
    #article="http://web.archive.org/web/20190414180539/https://aws.amazon.com/compute/sla/"


elif choice==3:
    article = "https://azure.microsoft.com/en-us/support/legal/sla/virtual-machines/v1_8/"


elif choice==4:
    article = "https://www.vmware.com/support/vcloud-air/sla.html"


elif choice==5:
    article = "https://cloud.oracle.com/iaas/sla"
else:
    print("InValid Choice. Defaulting to GCP")
    article = "https://cloud.google.com/compute/sla"

#print("Processing SLA from : ",article)


text = getTextfromUrl(article,choice)


print(text)

# print("The TEXT : ",text)

# Training the PunktTokenizer with our text
custom_token = PunktSentenceTokenizer(text)
# print("The custom Words : ",custom_token)

# Tokenzing our text with our trained tokenizer
print("\nTokenizing text")
tokenized = custom_token.tokenize(text)
print("> The tokennized sentences: ",tokenized)

# List of modal verbs
listOfMVs = ['will','shall','may','must','might','can','could','should']
obligationWords = ['must','should','have to']
#dispensationwords = ['might','could','may']
permissionwords = ['can','may','could']


mvFreqDist = getFreqDist(tokenized)
print("The modal verb frequency in this document : ",mvFreqDist)

# POS Tagging
posTagged = posTagging(tokenized)

print("> The POS tagged : ",posTagged)
sentcount=sentencounter(text)
#obligation = obligationwords(text)
Permission=Permissionwords(text)

print ("\n\nSelect the next step : ")

print ("1. Verb Extraction and WordCloud Generation")
print ("2. Chunking")
moreChoice = input('Enter your choice [1-2] : \n')
moreChoice = int(moreChoice)
sentcount= sentencounter(text)
#obligation = obligationwords(text)
Permission=Permissionwords(text)
print("sentence",sentcount)
print("Permission:", Permission)

file1=open("C:\\Users\divya\Desktop\TEXT\\test.txt", 'r' , encoding='utf-8')
tokenized=file1.readlines()
from gensim.models import Word2Vec

# train model
word_tokens=[nltk.word_tokenize(sent) for sent in tokenized]

#print(word_tokens)
for i in range(len(tokenized)):
    word_tokens[i]=[w.lower() for w in word_tokens[i]]
    word_tokens[i]= [w for w in word_tokens[i] if len(w)<15]
    word_tokens[i] = [w for w in word_tokens[i] if len(w) > 2]
    #word_tokens[i] = [w for w in word_tokens[i] if not re.search('^[0-9]+\\.[0-9]+$.', w)]
    word_tokens[i] = [w for w in word_tokens[i] if w not in (stopwords.words('english')+ list(punctuation))]

model = Word2Vec(word_tokens,sg=1,min_count=3, iter=10)
# summarize the loaded model
#print('model:', model)
# summarize vocabulary
words = list(model.wv.vocab)
print('words:',words)
# access vector for one word
v1=model.wv['unavailable']
v2=model.wv['downtime']
sim_words=model.wv.most_similar('unavailable')
sim_words2=model.wv.most_similar('downtime')
# result = model.most_similar(positive=['service', 'credit'], negative=['financial'], topn=1)
print('words_similar_to_Unavailable',sim_words)
print('words_similar_to_downtime',sim_words2)
X = model[model.wv.vocab]
pca = PCA(n_components=2)
result = pca.fit_transform(X)
pyplot.scatter(result[:, 0], result[:, 1])
words = list(model.wv.vocab)
for i, word in enumerate(words):


	pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))

pyplot.show()

#print(sim_words)

# if moreChoice==1:
#     print("Proceeding with verb extraction and word cloud generation")
#     posListVerbs = ["VB", "VBG", "VBD"  "VBN", "VBP", "VBZ"]
#
#     # Extract POS words
#     extractedWords = extractWords(posTagged, posListVerbs)
#     print("> The Extracted words : ",extractedWords)
#
#     noDuplicates = list(set(extractedWords))
#     print("> Removing duplicates for global variable : ",noDuplicates)
#
#     # extractedWordsTest = "This is the word Cloud"
#
#     extractedWordsString = ' '.join(extractedWords)
#
#
#     # Word Cloud Creation
#     #theWords = WordCloud(collocations=False,background_color='white',relative_scaling=1.0).generate(extractedWordsString)
#     #generateWordCloud(theWords)
#
# elif moreChoice==2:
#     print("Proceeding with chunking!")
#
#     fullPosTag = list(itertools.chain.from_iterable(posTagged))
#     parseAndChunk(fullPosTag)
#     # for eachPosTogged in posTagged:
#     #     parseAndChunk(eachPosTogged)

