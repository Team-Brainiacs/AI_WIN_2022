# Reading the data
data <- read.table(file.choose(), header = TRUE, col.names = c("EC100", "EC160", "IT101","IT161","MA101","PH100","PH160","HS101", "QP"))

# We need to convert character variables to factor variables

data[sapply(data, is.character)] <- lapply(data[sapply(data, is.character)], as.factor)

# The following data need to be converted to Bayesian network

bn <- hc(data[, -9], score = 'k2')

# Fitting the data to the bayesian network

fitted_bn <- bn.fit(bn, data[,-9])

print(fitted_bn)

# Plot the conditional probability 
bn.fit.dotplot(fitted_bn$MA101)

