args = commandArgs(trailingOnly=TRUE)

ds1<-read.table(args[1], sep=";", header=F)
ds2<-read.table(args[2], sep=";", header=F)


print(mean(as.numeric(ds1$V1)))
print(mean(as.numeric(ds2$V1)))
print(sd(as.numeric(ds1$V1)))
print(sd(as.numeric(ds2$V1)))
png(args[3])
par(mfrow=c(2,1))
hist(as.numeric(ds1$V1), main="Running time: Asssigning blocks to main contour (ms)", col="dark red", breaks=10, xlab="Time, ms")
hist(as.numeric(ds2$V1), main="Running time: Asssigning blocks to subcontours (ms)", col="dark blue", breaks=10, xlab="Time, ms")
dev.off()

