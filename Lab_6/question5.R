# Reading the data
data <- read.table(file.choose(), header = TRUE, col.names = c("EC100", "EC160", "IT101","IT161","MA101","PH100","PH160","HS101", "QP"))

# We need to convert character variables to factor variables

data[sapply(data, is.character)] <- lapply(data[sapply(data, is.character)], as.factor)

# The following data need to be converted to Bayesian network

bn <- hc(data[, -9], score = 'k2')

# Fitting the data to the bayesian network

fitted_bn <- bn.fit(bn, data[,-9])

# Setting the seed values

set.seed(101)

# Initializing an empty vector to store accuracy results

accuracy_results <- c()

# Looping 20 times

for (i in 1 : 20){
  #Build the TAN classifier on the training data using the tan_cl function from the bnlearn package.
  tn <- tan_cl("QP", data.train)
  #Fit the TAN classifier to the training data using the lp function
  tn <- lp(tn, data.train, smooth = 1)
  
  
  #Use the predict function to predict the grades of the test data.
  p <- predict(tn, data.test)
  
  #Compute the confusion matrix using the table function
  cm1<-table(predicted=p, true=data.test$QP)
  cm1
  
  #Compute the accuracy of the prediction using the accuracy function from the bnclassify package
  accuracy <- bnclassify:::accuracy(p, data.test$QP)
  
  # Store the accuracy in the vector
  accuracy_results <- c(accuracy_results, accuracy)
  
}

# Getting mean of accuracy results

print(mean(accuracy_results))

