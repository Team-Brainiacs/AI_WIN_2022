# Reading the data
data <- read.table(file.choose(), header = TRUE, col.names = c("EC100", "EC160", "IT101","IT161","MA101","PH100","PH160","HS101", "QP"))

# We need to convert character variables to factor variables

data[sapply(data, is.character)] <- lapply(data[sapply(data, is.character)], as.factor)

# The following data need to be converted to Bayesian network

bn <- hc(data[, -9], score = 'k2')

# Fitting the data to the bayesian network

fitted_bn <- bn.fit(bn, data[,-9])

# Need to predict the grade obtained in PH100

# Predict the grade in PH100 based on evidence provided
prediction.PH100 <- data.frame(cpdist(fitted_bn, nodes = c("PH100"), evidence = (EC100 == "DD" & IT101 == "CC" & MA101 == "CD")))

my_table <- table(prediction.PH100)
my_table <- my_table/(sum(my_table))
print(my_table)

