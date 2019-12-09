import numpy as np
import matplotlib.pyplot as plt
from os.path import basename, splitext
# Plot graph

class GraphPlotter:
	def __init__(self, productList, filePath):
		self.productList = productList
		self.fileName = splitext(basename(filePath))[0]
		
	# Price vs Rating
	def plotPriceVsRating(self):
		productList = self.productList
		title = 'Product Ratings against Price '+self.fileName
		xVals = []
		yVals = []
		for product in productList:
			# convert the values to integer
			xVals.append(int(round(product.avgRating)))
			yVals.append(int(round(product.price)))        

		print("Plotting ", title)
		plt.bar(xVals, yVals, align='center', alpha=0.5, color='#85ad05')
		plt.xlabel('Rating')
		plt.ylabel('Price')
		plt.title(title)    
		plt.savefig("PricevRating_" + self.fileName + ".png")
		#plt.show()
		

	# Rating vs No of reviews
	def plotRatingvsNReviews(self):
		productList = self.productList
		title = 'Product Ratings against number of reviews '+self.fileName
		xVals = []
		yVals = []
		for product in productList:
			# convert the values to integer
			xVals.append(int(round(product.avgRating)))
			yVals.append(int(round(product.nRatings)))

		print("Plotting ", title)
		plt.bar(xVals, yVals, align='center', alpha=0.5, color='#072351')    
		plt.xlabel('Ratings')
		plt.ylabel('Number of Reviews')
		plt.title(title)    
		plt.savefig("PricevReviews_" + self.fileName + ".png")
		#plt.show()    

	# Number of reviews that were helpful per category file supplied
	def plotHelpful(self, data):		
		title = 'Rating helpfulness chart for ' + self.fileName
		print("Plotting ", title)
		plt.hist(data, bins=np.arange(min(data), max(data)+1), color='#9d5ea0', linewidth=0, width=10)    
		plt.xlabel('Helpfulness')
		plt.ylabel('Number of Reviews')
		plt.title(title)    
		plt.savefig("Helpful_" + self.fileName + ".png")
		#plt.show()
