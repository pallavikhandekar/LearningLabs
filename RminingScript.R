library(tm)
library(SnowballC)
docs <- c(
  "Alibaba", "The three musketer","musketer","Three alibaba", "Three the alibaba",
  "musketer", "musketer","three alibaba", "four three alibaba")
docs<-as.character(livedata2)
docs<- c("River hawks", "Iver", "Ivar Jacobson", "Ivar jackobson", "UML", "Three Amigos", "Three Amigos", 
         "three amigos ",  "Ivar ",  "the three amigos ",  "3 Amigoes ",  "Three Amigos ",  "UML ",  
         "the three aimgos ",  "Three Amigos ",  "Amigos ",  "Three amigos ",  "3 Amigos ",  "three amigos ",  
         "ivar jacobson ",  "Three Musketeers ",  "the three amigos ",  "3 Amigos ",  "the three amigos ",  
         "Three Amigos ",  "The Three Amigos ",  "Three Amigos ",  "Ivar ",  "3 Amgoes ",  "Amigos ",  
         "The Three Amigos ",  "three amigos ",  "Ivar Jacobson    Amigos ",   "three amigos ",  "the three amigos ",
         "3 amigos ",  "the three amigos ",  "three amigos ",  "the Three Amigos ",  "River Hawks ",  "3 AMIGOS ",  
         "The Three Amigos ",  "Three Amigos ",  "Have no idea ",  "Booch ",  "Three Amigos ",  "The 3 amigos ", 
         "Three Amigos ",  "The Three Amigos ",  " Grady Booch, Ivar Jacobson, James Rumbaugh ",  
         "The Three Amigos ",  "3 amigos ",  "The three Amigos ",  "three amigos ",  "Ivor Jacobson ",  "Ivar ", 
         "The Three Amigos ",  "three amigos ",  "Ivy ",  "the three Amigos ",  "The Three Amigos ", 
         "three Amigos ",  "Three Amigos ",   "river hawks ",  "three amigos ",  "Grady booch ",  
         "The three amigos ",  "amigos ",  "Three Amigos ",  "3 Amigos ",  "The three amigos ",  "No Idea ",  
         "No idea ",  "River Hawks ",  "The Three Amigos ",  "The Three Amigos ",  "3 amigos ",  "3 amigos ",  
         "The 3 Amigos ",  "don't know ",  "Three Amigos ",  "don't know ",  "3 amigos ",  "The Three Amigos ", 
         "jacob ",  "Three Amigos ",  "Jacobson ",  "Three Amigos ",  "THE THREE AMIGOS ",  "three amigos ", 
         "ivar jacobson ",  "3 musketeers ",  "Grady Booch ",  "Ivar ",  "Don't know ",  "UML ",  "Three Amigos ",  
         "Three Ambigos ",   "UML ",  "three amigos ",  "3 musketeers ",  "Don't Know ",  "Jacobson ",  "gunja ",
         "3 amigos ",  "3 musketeers ",  "three amigos ",  "Ivar ",  "three amigos ", 
         "Three Amigos of software engineering ",  "The three amigos ",  "Ivar Jacobson ",  "3 amigos ",  
         "river hawks ",  "river hawks ",  "Jacobson ",  "No idea! ",  "James ",  "Three amigos ",  
         "The Three Amigos ",  "Ivar Jacobson ",  "Anurag ",  "3 Amigos ",  "Three amigos ",  "3 musketeers ", 
         "Ivar Jacobson ",  "Gang of 4 ",  "three amigos ",  "donald  ",  "three amigos ",  "Ivar Jacobson ", 
         "Three Amigos ",  "the three amigos ",  "Don't know ",  "Three Amigos ",  "three Amigos ",  "Three Amigos")
numClusters <-4
numWords <- 1
ans <-VCorpus(VectorSource(docs))
ans<-tm_map(ans, stripWhitespace)
ans <- tm_map(ans, content_transformer(tolower))
ans <- tm_map(ans, removeWords, stopwords("english"))
tm_map(ans, stemDocument)
dtm <- DocumentTermMatrix(ans)
##freq<-colSums(as.matrix(dtm))
##indFreq<-order(freq)
dtm_tfxidf <- weightTfIdf(dtm)

m <- as.matrix(dtm_tfxidf)
rownames(m) <- 1:nrow(m)
norm_eucl <- function(m) m/apply(m, MARGIN=1, FUN=function(x) sum(x^2)^.5)
m_norm <- norm_eucl(m)
cl <- kmeans(m_norm,numClusters,50)
clusters <- 1:numClusters
#for (i in clusters){
#cat("Cluster ",i, ":", findFreqTerms(dtm[cl$cluster ==i,],nrow(dtm[cl$cluster==i,])/2)," \n \n")}

for (i in clusters){
  cat("Cluster ",i, ":", head(names(sort(colSums(as.matrix(dtm[cl$cluster ==i,])),decreasing=TRUE)),numWords)," Count = ", sum(cl$cluster==i) ," \n \n")}