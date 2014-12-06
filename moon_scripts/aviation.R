aviation.data <- read.csv("../data/AviationData.CSV", sep = "|", row.names = NULL)
aviation.data <- subset(aviation.data, Country==" United States ")
useful.labels <- c("Event.Date", "Location", "Injury.Severity")
aviation.data.useful <- aviation.data[useful.labels]
aviation.data.useful$Event.Date <- as.Date(aviation.data.useful$Event.Date, " %m/%d/%Y ")

# trim
s <- as.character(aviation.data.useful$Location)
aviation.data.useful$Location <- substr(s, 2, nchar(s) - 1)

endsWith <- function(S, l) { s <- as.character(S); substr(s, nchar(s) - 1, nchar(s)) %in% l }
pst <- c("WA", "OR", "NV", "CA")
mst <- c("MT", "ID", "WY", "UT", "CO", "AZ", "NM")
cst <- c("ND", "SD", "MN", "IA", "WI", "IL", "NE", "KS", "MO", "AR", "TN", "OK", "TX", "AR", "LA", "MS", "AL")
# est <- others
write.csv(subset(aviation.data.useful, endsWith(Location, pst)), file="../data/AviationPst.csv")
write.csv(subset(aviation.data.useful, endsWith(Location, mst)), file="../data/AviationMst.csv")
write.csv(subset(aviation.data.useful, endsWith(Location, cst)), file="../data/AviationCst.csv")
write.csv(subset(aviation.data.useful, !endsWith(Location, c(pst, mst, cst))), file="../data/AviationEst.csv")
