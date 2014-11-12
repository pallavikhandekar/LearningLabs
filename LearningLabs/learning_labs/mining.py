
# import rpy2.robjects as robjects
# from rpy2.robjects.packages import importr
from learning_labs.models import Quiz,Answers
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob
from textblob import Word

numDict = {1:"one",2:"two",3:"three",4:"four",5:"five",6:"six",7:"seven",8:"eight",9:"nine",10:"ten",11:"eleven",
               12:"twelve",13:"thirteen",14:"fourteen",15:"fifteen",16:"sixteen",17:"seventeen",18:"eighteen",
               19:"ninteen",20:"twenty",30:"thirty",40:"fourty",50:"fifty",60:"sixty",70:"seventy",80:"eighty",
               90:"ninty"}

def getChartData(quizId,questionId):
    # pi = robjects.r['pi']
    # base = importr('base')
    # tm = importr('tm')
    # r = robjects.r
    # docs = base.c("")
    #p=""
    #queryset = StudentAnswers.objects.all();
    print(questionId)
    print(quizId)
    wordDict = {}
    nounSet = set()
    for obj in Answers.objects.all().filter(Question_Id =23156645):
        answer = obj.Answer;
        if answer == None or answer == "":
            continue
        print(" Before Preprocess : " + answer)

        #NLTK pre-process
        anstokens = nltk.word_tokenize(answer)
        nouns = [tup[0] for tup in nltk.pos_tag(anstokens) if tup[1] == 'NN' or tup[1]=='NNS']
        for n in nouns:
            nounSet.add(n)
        b = TextBlob(answer)
        nounList = b.noun_phrases
        for n in nounList:
            for m in n.split():
               nounSet.add(m)
        looper = 0
        for token in anstokens:
            if token.isdigit():
                token = convert(int(token))
            if token not in nounSet:
                w = Word(token)
                token = w.correct()
            else:
                print "skipping noun for auto correct : " + token
            anstokens[looper] = token.lower()
            looper += 1
        stopwordsList = ['the','it','she','he']
        anstokens2 = [token for token in anstokens if (not token in stopwordsList)]
       # porter = nltk.PorterStemmer()
       #  looper = 0
       #  for token in anstokens2:
       #      anstokens2[looper] = porter.stem(token)
       #      looper += 1
        processedAnswer =  ' '.join(anstokens2)
        #nltk.Text(anstokens2)
        if processedAnswer in wordDict:
            wordDict[processedAnswer] +=1
        else:
            wordDict[processedAnswer] = 1
        print("After proess : "+str(processedAnswer))
    print str(wordDict)
    return wordDict
       # docs = base.cbind(answer, docs)
    #p ="first Docuent"
    #p = base.cbind("nimmi", p)
    #docs = base.c("Three musketers", "The three musketers", "musketer", "musketers")
    # ans = tm.VCorpus(tm.VectorSource(docs))
    # ans = tm.tm_map(ans, tm.stripWhitespace)
    # ans = tm.tm_map(ans, tm.content_transformer(base.tolower))
    # ans = tm.tm_map(ans, tm.removeWords, tm.stopwords("english"))
    #
    # dtm= tm.DocumentTermMatrix(ans)
    # words= base.dimnames(dtm)[1]
    # print(" word sis " + str(words))
    # freqVec = r.colSums(r.matrix(dtm,r.length(docs)))
    # ind = 0
   # wordDict = {}

    #displayDict = {"C#":5, "Python": 6 , "Scala":7, "R":2}
#   print str(wordDict)

def convert(number):
    value = ''
    while(number>0):
        if(number>=100000):
            lakhs = number%100000
            number = number/100000
            value= value + findTens(lakhs)+" lakhs"
        if(number>=1000):
            thousands = number%1000
            number = number/1000
            value = value + findTens(thousands)+" thousand"
        if(number >=100):
            hundreds = number%100
            number = number/100
            value = value + findTens(hundreds)+" hundred"
        if(number>0):
            if(value != ''):
                value = value + " and"
            value = value + findTens(number)
            number = 0
    return value


def findTens(num):
    returnVal = '';
    if(num<20):
       returnVal = numDict.get(num)
    else:
        tens = num/10
        unit = num%10
        returnVal = numDict.get(tens)+" "+numDict.get(unit)
    return returnVal