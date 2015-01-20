#! /usr/bin/env Rscript

library(e1071)
library(lattice)
library(latticeExtra)


df <- read.csv('eastern.csv', na.string='-')
df <- na.exclude(df)

df.tw <- subset(df, select=c(love, joy, sadness, anger, other, surprise, fear))
df.m <- subset(df, select=c(radio_flux, phase, moon_day, sunspot_number, sunspot_area, new_regions))
df.tw$all <- df$X.

for (tw in names(df.tw)) {
    for (m in c("radio_flux", "moon_day", "sunspot_number", "sunspot_area", "new_regions")) {
        print(cor(df.tw[[tw]], df.m[[m]]))
    }
}

df.aggr <- aggregate(df.tw, by=list(df.m$moon_day), FUN="median")
xyplot(all ~ Group.1, data=df.aggr, type="b")
xyplot(df.tw$all ~ df.m$moon_day) + as.layer(xyplot(all ~ Group.1, data=df.aggr, type="b"))

df$all <- df$X.
df$X. <- NULL
xyplot(all ~ date, data=df)
xyplot(all ~ date, data=head(tail(df, n=-28)))
df.fix <- tail(df, n=-28)

df.fix.m <- subset(df.fix, select=c(radio_flux, phase, moon_day, sunspot_number, sunspot_area, new_regions))
df.fix.tw <- subset(df.fix, select=c(all, love, joy, sadness, anger, other, surprise, fear))
df.fix.aggr <- aggregate(df.fix.tw, by=list(df.fix.m$moon_day), FUN="median")
xyplot(df.fix.tw$all ~ df.fix.m$moon_day) + as.layer(xyplot(all ~ Group.1, data=df.fix.aggr, type="b"))

densityplot(~ all, df.fix.tw)
df.fix <- subset(df.fix, all >= 1.5e6 & all <= 3.5e6)
df.fix.tw <- subset(df.fix, select=c(love, joy, sadness, anger, other, surprise, fear, all))
df.fix.m <- subset(df.fix, select=c(radio_flux, phase, moon_day, sunspot_number, sunspot_area, new_regions))

for (tw in names(df.fix.tw)) {
    for (m in c("radio_flux", "moon_day", "sunspot_number", "sunspot_area", "new_regions")) {
        print(cor(df.fix.tw[[tw]], df.fix.m[[m]]))
    }
}

xyplot(df.fix.tw$all ~ df.fix.m$moon_day) +
    as.layer(xyplot(all ~ Group.1, data=aggregate(df.fix.tw, by=list(df.fix.m$moon_day), FUN="median"), type="b"))
xyplot(df.fix.tw$all ~ df.fix.m$moon_day) +
    as.layer(xyplot(all ~ Group.1, data=aggregate(df.fix.tw, by=list(df.fix.m$moon_day), FUN="median"), type="b")) +
    as.layer(xyplot(all ~ Group.1, data=aggregate(df.fix.tw, by=list(df.fix.m$moon_day), FUN="max"), type="b")) +
    as.layer(xyplot(all ~ Group.1, data=aggregate(df.fix.tw, by=list(df.fix.m$moon_day), FUN="min"), type="b"))

xyplot(df.tw$all ~ df.m$moon_day) +
    as.layer(xyplot(all ~ Group.1, data=df.aggr, type="b")) +
    as.layer(xyplot(all ~ Group.1, data=aggregate(df.tw, by=list(df.m$moon_day), FUN="max"), type="b")) +
    as.layer(xyplot(all ~ Group.1, data=aggregate(df.tw, by=list(df.m$moon_day), FUN="min"), type="b"))

for (tw in names(df.fix.tw)) {
    print(xyplot(df.fix.tw[[tw]] ~ df.fix$date, ylab=tw, xlab="date"))
}
for (tw in names(df.fix.tw)) {
    for (m in names(df.fix.m)) {
        print(xyplot(df.fix.tw[[tw]] ~ df.fix.m[[m]], ylab=tw, xlab=m))
    }
}

df.svm <- subset(df.fix, select=c(all, radio_flux, phase, moon_day, sunspot_number, sunspot_area, new_regions))
tn.sv <- tune(svm, all ~ ., data=df.svm, kernel="radial", ranges=list(epsilon=seq(0, 1, 0.01), cost=2^(1:10)))
print(tn.sv)
plot(tn.sv)
