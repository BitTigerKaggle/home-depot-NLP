#@Author:Victor
#@Date: 4/12/2016

#-----------------------------
set.seed(123)
library(data.table)
library(xgboost)
library(caret)

#---------------------------------functions---------------------------------------------------
RMSE<- function(preds, dtrain) {
  err <- sqrt(mean((y-y_pred)^2))
  return(list(metric = "RMSE", value = err))
}

dropcol <- function(data1){
  data = data1

  
  return data
}
#---------------------------------functions---------------------------------------------------
setwd("/Users/victorzhao/Documents/PycharmProjects/home/final2/") #Set working directory 
train = fread("dataframe_train.csv")
test = fread("dataframe_test.csv")
train$V1 = NULL
train$product_title = NULL
train$search_term = NULL
train$product_description = NULL
train$brand = NULL
train$material = NULL
train$attr_text = NULL
train$bullet = NULL

test$V1 = NULL
test$product_title = NULL
test$search_term = NULL
test$product_description = NULL
test$brand = NULL
test$material = NULL
test$attr_text = NULL
test$bullet = NULL
label = train$relevance
dataset = train[,-3,with = FALSE]
Index <- createDataPartition(train$id, p = .5, list = FALSE)
xtrain1 = dataset[Index,]
ytrain1 = label[Index]
xtest1 = dataset[-Index,]
ytest1 = label[-Index]

dtrain <- xgb.DMatrix(data = data.matrix(xtrain1), label= ytrain1)
dtest <- xgb.DMatrix(data = data.matrix(xtest1), label=ytest1)
watchlist<-list(val=dtest,train=dtrain)
param1 <- list(objective = "reg:linear", #reg:logistic
               booster = "gbtree",
               #gamma = 2.2
               eta = 0.03,      #0.03 0.02
               max_depth = 20,  #20 15 10
               subsample = 0.7, #0.8
               colsample_bytree = 0.7 )

gbtree <- xgb.train(params = param1, 
                    data = dtrain, 
                    verbose = 1,
                    nrounds = 1000,#300,1000
                    early.stop.round = 100,
                    watchlist = watchlist,
                    maximize = FALSE,
                    feval = RMSE)

pred <- predict(gbtree,data.matrix(test))
result <- data.table(Id = test$id, Sales = pred)
sub = fread("sample_submission.csv")
sub$Sales[result$Id] = result$Sales
0 %in% sub$Sales
write.csv(sub, file = "sub_v2.csv")









