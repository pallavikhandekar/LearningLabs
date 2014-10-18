
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from learning_labs.models import Quiz,Answers

def getChartData():
    pi = robjects.r['pi']
    base = importr('base')
    tm = importr('tm')
    r = robjects.r
    docs = base.c("")
    #p=""
    #queryset = StudentAnswers.objects.all();
    for obj in Answers.objects.all().filter(questionId =23156645):
        answer = obj.Answer;
        print(answer)
        docs = base.cbind(answer, docs)
    #p ="first Docuent"
    #p = base.cbind("nimmi", p)
    #docs = base.c("Three musketers", "The three musketers", "musketer", "musketers")
    ans = tm.VCorpus(tm.VectorSource(docs))
    ans = tm.tm_map(ans, tm.stripWhitespace)
    ans = tm.tm_map(ans, tm.content_transformer(base.tolower))
    ans = tm.tm_map(ans, tm.removeWords, tm.stopwords("english"))
    dtm= tm.DocumentTermMatrix(ans)
    words= base.dimnames(dtm)[1]
    print(" word sis " + str(words))
    freqVec = r.colSums(r.matrix(dtm,r.length(docs)))
    ind = 0
    wordDict = {}
    for w in words:
        wordDict[w] = freqVec[ind]
        ind = ind+ 1
    #displayDict = {"C#":5, "Python": 6 , "Scala":7, "R":2}
    print str(wordDict)
    return wordDict;