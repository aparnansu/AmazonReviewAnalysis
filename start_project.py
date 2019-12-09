from amazon_review_scanner import ProductReader

# Begin the tests
# List of all datasets (Takes longer duration)
#dirPath = "Datasets"
# Small dataset to realize the result
dirPath = "Small_dataset"
# Option to plot a chart
plotGraph = True
# Option to aggregate the top rated info on all the categories mentioned in dirPath
printReport = True
# Limits for holding the number of products in memory
maxProducts = 1000000

# This is for printing the global reports after reading all the files under the directory.
productReader = ProductReader(dirPath, plotGraph, printReport, maxProducts)
productReader.printReportMethod()
