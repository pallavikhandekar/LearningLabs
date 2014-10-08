
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr



def getChartData():
    pi = robjects.r['pi']
    base = importr('base')
    tm = importr('tm')
    r = robjects.r
    #p ="first Docuent"
    #p = base.cbind("nimmi", p)
    docs = base.c("Three musketers", "The three musketers", "musketer", "musketers")
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