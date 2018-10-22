library(h2o)        # Professional grade ML pkg
library(lime) 


dataframe = read.csv("/Users/nuexb14/Desktop/Personal/UNCC/Dataset.csv")
dataframe = dataframe[complete.cases(dataframe),]



dataframe$Gender = as.factor(dataframe$Gender)
dataframe$CreditScore = dataframe$CreditScore
dataframe$Exited = as.factor(dataframe$Exited)
dataframe$RowNumber = NULL
dataframe$CustomerId = NULL
dataframe$Geography = NULL
dataframe$Surname = NULL


train_data = head(dataframe, n = 5000)

library(randomForest)

rf = randomForest(Exited~., data = train_data, ntree = 20, na.action = na.exclude,
                  importance=T, proximity= T)
print(rf)


train_data <- dataframe[complete.cases(dataframe),]

mtry <- tuneRF(train_data[-10], train_data$Exited, ntreeTry=20, 
               stepFactor=1.5, improve=0.01, trace=TRUE, plot=TRUE)

best.m <- mtry[mtry[, 2] == min(mtry[, 2]), 1]

print(mtry)

print(best.m)


rf <-randomForest(Exited~., data=train_data, mtry=4, importance=TRUE, ntree=20)
print(rf)

importance(rf)

varImpPlot(rf)

x1 = dataframe[dataframe$Exited == "Exited"]
summary(x1)


x1 = subset(train_data, Exited == 0, select = c(CreditScore,Age,NumOfProducts,EstimatedSalary,Balance))

summary(x1)
x2 = head(x1, n = 20)

write.csv(x2, file = "/Users/nuexb14/Desktop/Personal/UNCC/x2.csv")

