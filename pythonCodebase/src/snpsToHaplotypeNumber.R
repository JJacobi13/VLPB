args<-commandArgs(TRUE)
#Read the file
file <- args[1]
data <- read.table(file, header=T,row.names=1)

#Give each string in a row a unique number
allelesAsNumeric <- t(apply(data,1,function(x){
  return(factor(x, labels=c(1:length(table(x)))))
}))
class(allelesAsNumeric) <- "numeric"

#Give the numbers with the lowest number of occurences 1 and increase for each following number
rankedNumeric <- t(apply(allelesAsNumeric,1,function(x){
  x.order <- sort(table(x), TRUE)
  x <- unlist(lapply(x,function(val){which(as.numeric(names(x.order)) == val)})) #Give the most occurences the lowest number
  as.numeric(factor(x,levels=unique(x)))
}))
colnames(rankedNumeric) <- colnames(data)

write.csv(rankedNumeric, args[2])
