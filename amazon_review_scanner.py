#Python project
# Amazon reviews analysis

import gzip
from os import listdir
from os.path import isfile, join, basename
from fractions import Fraction

import constants
from printer import Printer
from console_printer import ConsolePrinter
from file_printer import FilePrinter
from graph_plot import GraphPlotter


#Product class
class Product:

    def __init__(self, pId, pName, category):
        self.pId = pId;
        self.pName = pName
        self.category = category;
        self.sumRating=0
        self.nRatings=0        
        self.price=0
        self.rating=0
        self.avgRating = 0
        self.ratingFrequency = {}

            
    def computeAverageRating(self):        
        if(self.nRatings > 0):            
            self.avgRating = self.sumRating/self.nRatings
        return self.avgRating        

    def addRating(self, rating):
        self.sumRating += rating
        frequency = self.ratingFrequency.get(rating, 0) + 1        
        self.ratingFrequency[rating] = frequency
        
    def getDetails(self):
        return "Id: {}; Name: {}; Category: {}; Sum of ratings: {}; No of ratings: {}; Average rating: {}; Price: {}".format(self.pId, self.pName, self.category, self.sumRating, self.nRatings, self.avgRating, self.price)

    def getRatingFrequency(self):
        retStr = "Rating frequency of the product {}".format(self.pId) + "\n" 
        keyList = list(self.ratingFrequency.keys())
        keyList.sort(reverse = True)
        for key in keyList:
            retStr += "{}:{}".format(key, self.ratingFrequency[key]) + "\n"
        return retStr

# Printer class that prints the analytics to console or to a file
class Printer:

    def __init__(self, printer):
        self.printer = printer
    
    def printTopNByAverage(self, products, n):
        printer = self.printer
        printer.print("----------------------")
        printer.print("Top {} products by average ratings, review counts".format(n))
        printer.print("----------------------")
        for product in self.getTopNByAverage(products, n):
            printer.print(product.getDetails())
        printer.print("----------------------")
        printer.print("\n\n")

    def printTopNByReviews(self, products, n):
        printer = self.printer
        printer.print("----------------------")
        printer.print("Top {} by review counts".format(n))
        printer.print("----------------------")
        for product in self.getTopNByReviews(products, n):
            printer.print(product.getDetails())
        printer.print("----------------------")
        printer.print("\n\n") 

    def printRatingFrequency(self, products, n):
        printer = self.printer
        printer.print("----------------------")
        printer.print("Frequency ratings of the first {} items".format(n))
        printer.print("----------------------")
        for productObj in products[:n]:            
            printer.print(productObj.getRatingFrequency())
        printer.print("----------------------")
        printer.print("\n\n")

    def close(self):
        self.printer.close()

    # Common functions    
    def getTopNByAverage(self, productList, n):
        if (n <= 0):
            return []
        sortedList = sorted(productList,key=lambda p:(p.avgRating, p.nRatings),reverse=True)
        return sortedList[:n]
    
    def getTopNByReviews(self, productList, n):
        if (n <= 0):
            return []
        sortedList = sorted(productList,key=lambda p:p.nRatings,reverse=True)
        return sortedList[:n] 

# Product reader class that operates on files and also calls graph plot based on arguments
class ProductReader:

    def __init__(self, dirPath, plotGraph, printReport, maxProducts):
        self.dirPath = dirPath
        self.plotGraph = plotGraph
        self.printReport = printReport
        self.maxProducts = maxProducts

    # Generate entries out of filePath
    def parse(self, filePath):
        f =gzip.open(filePath, 'rt')
        entry = {}
        for l in f:
            l = l.strip()
            colonPos = l.find(':')
            if colonPos == -1:
                yield entry
                entry = {}
                continue
            eName = l[:colonPos]
            rest = l[colonPos+2:]
            entry[eName] = rest
        
    # Load the products out of filePath
    def loadProducts(self, filePath):    
        print("Reading the products from", filePath)
        # Local product map
        localProductMap={}
        # Review count
        rCount = 0
        # Product count
        pCount = 0
        
        for e in self.parse(filePath):
            pId=e[constants.PRODUCT_ID]   
            pName=e[constants.PRODUCT_NAME]                            
            pRating=float(e[constants.PRODUCT_RATING])
            priceStr=e[constants.PRODUCT_PRICE]

            if priceStr==constants.UNKNOWN:
                continue
            price = float(priceStr)
            
            #create an object for each new product, add ratings and number of ratings when product already in dictionary
            #producs{pid:productObj}
            productObj = localProductMap.get(pId)
            if(productObj is None):
                productObj = Product(pId, pName, basename(filePath))
                pCount += 1
            productObj.addRating(pRating)
            productObj.nRatings+=1
            localProductMap[pId] = productObj            
            productObj.price=price
            productObj.rating=pRating
            rCount += 1
            if(pCount == self.maxProducts):
                break
       
        print("Read", rCount, "reviews on", pCount, "products from", filePath)

        productList = list(localProductMap.values())
        # Clear the dictionary
        localProductMap.clear()
        
        # Compute the average ratings of the every product that is read
        # Better than computing while adding for every rating of a review
        for product in productList:           
            product.computeAverageRating()
            
        return productList


    # Global assignment of products from the directory
    def readDir(self, storeGlobal = False):
        dirPath = self.dirPath
        # Global product
        globalProducts = []
        for file in listdir(dirPath):        
            filePath = join(dirPath, file);
            if not isfile(filePath):            
                continue
            categoryProducts = self.loadProducts(filePath)
            if self.plotGraph:
                self.plotGraphMethod(categoryProducts, filePath)
            
            if storeGlobal:
                globalProducts.extend(categoryProducts)

        return globalProducts

    # Plot graph method
    def plotGraphMethod(self, productList, filePath):
        print("-----------------------------------")
        graph_plot = GraphPlotter(productList, filePath)
        graph_plot.plotPriceVsRating()
        graph_plot.plotRatingvsNReviews()

        # Read specific data for generating this particular plot
        data = []             
        for e in self.parse(filePath):        
                helpful=e[constants.REVIEW_HELPFULNESS] 
                # Avoid divide by zero error.
                if(helpful == constants.ZEROONZERO):
                        continue        
                helpfulScore = int(float(Fraction(helpful)) * 100)
                # Skip helpful score > 100 in the dataset.
                if(helpfulScore > 100):
                        continue
                data.append(helpfulScore) 
        graph_plot.plotHelpful(data)
        print("-----------------------------------")

    # Base report method
    def printReportMethod(self):

        # Return if none of the options are enabled
        if not self.plotGraph and not self.printReport:
            return
        
        dirPath = self.dirPath
        globalProducts = self.readDir(self.printReport)

        if self.printReport:            
            # Print the messages to console
            consolePrinter = Printer(ConsolePrinter())    
            consolePrinter.printTopNByAverage(globalProducts, 3)
            consolePrinter.printTopNByReviews(globalProducts, 3)
            consolePrinter.printRatingFrequency(globalProducts, 3)
            consolePrinter.close()

            # Print the messages to file
            filePrinter = Printer(FilePrinter('TestReport.txt'))
            filePrinter.printTopNByAverage(globalProducts, 3)
            filePrinter.printTopNByReviews(globalProducts, 3)
            filePrinter.printRatingFrequency(globalProducts, 3)
            filePrinter.close()

    
