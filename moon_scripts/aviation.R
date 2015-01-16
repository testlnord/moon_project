aviation.data <- read.csv("../data/AviationData.CSV", sep = "|", row.names = NULL)
aviation.data <- subset(aviation.data, Country==" United States ")
aviation.data.dates <- aviation.data["Event.Date"]
aviation.data.dates$Event.Date <- as.Date(aviation.data.dates$Event.Date, " %m/%d/%Y ")
frequences <- as.data.frame(table(aviation.data.dates[aviation.data.dates$Event.Date >= as.Date("2004-01-01"),]))
write.table(frequences, file="../data/AviationDates.csv", row.names = FALSE, col.names = FALSE, sep=',')