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
  # Splitting the data into training set and testing set
  sample <- sample.int(n = nrow(data), size = floor(0.7*nrow(data)), replace = F)
  data.train <- data[sample,]
  data.test <- data[-sample,]
  # Building the classifier
  nb.grades <- nb(class = "QP", dataset = data.train)
  # Fitting the naive bayes classifier
  nb.grades <- lp(nb.grades, data.train, smooth = 0)
  #nb.grades$.params
  
  p <- predict(nb.grades, data.test)
  cm <- table(prediction=p, true = data.test$QP)
  cm
  
  accuracy <- bnclassify::accuracy(p, data.test$QP)
  
  accuracy_results <- c(accuracy_results, accuracy)
  
}

# Getting mean of accuracy results

print(mean(accuracy_results))

