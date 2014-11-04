
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from learning_labs.models import Quiz,Answers
import nltk
from nltk.corpus import stopwords


def getChartData():
    pi = robjects.r['pi']
    base = importr('base')
    tm = importr('tm')
    r = robjects.r
    docs = base.c("")
    #p=""
    #queryset = StudentAnswers.objects.all();
    wordDict = {}
    for obj in Answers.objects.all().filter(Question_Id =23156645):
        answer = obj.Answer;
        if answer == None or answer == "":
            continue
        print(" Before Preprocess : " + answer)
        #NLTK pre-process
        anstokens = nltk.word_tokenize(answer)
        looper = 0
        for token in anstokens:
            anstokens[looper] = token.lower()
            looper += 1
        anstokens2 = [token for token in anstokens if (not token in stopwords.words('english'))]
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
