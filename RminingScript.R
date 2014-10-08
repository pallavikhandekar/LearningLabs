library(tm)
library(SnowballC)
docs <- c("Three musketers", "The three musketers", "musketers", "musketer")

ans <-VCorpus(VectorSource(docs))
 ans<-tm_map(ans, stripWhitespace)
ans <- tm_map(ans, content_transformer(tolower))
ans <- tm_map(ans, removeWords, stopwords("english"))
#tm_map(ans, stemDocument)
dtm <- DocumentTermMatrix(ans)
freq<-colSums(as.matrix(dtm))
indFreq<-order(freq)

