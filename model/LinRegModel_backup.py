
import numpy as np
import csv

class BaseModel()

	def __init__(self, config):
		lat = []
		lon = []
		out = []

		train_Xlat = np.array([])
		train_Xlong = np.array([])
		train_X = np.array([0, 0])
		train_Y = np.array([0])

		with open('house_price_test.csv', 'r') as csvfile:
		    csvReader = csv.reader(csvfile)
		    legend = next(csvReader)
		    for row in csvReader:
		        temp = []
		        temp.append(float(row[legend.index("Lat")]))
		        temp.append(float(row[legend.index("Long")]))
		        # print temp
		        train_X = np.vstack((train_X, temp))
		        train_Y = np.vstack((train_Y,float(row[legend.index("2017-09")])))

		newdataX = np.ones([train_X.shape[0], train_X.shape[1] + 1])
		newdataX[:, 0:train_X.shape[1]] = train_X

		print train_Y[1:]

		# train the lin reg model
		model_coefs, residuals, rank, s = np.linalg.lstsq(newdataX[1:], train_Y[1:])
		print model_coefs


	def query(postcode)
		# query the model
		points = np.array([[33.79], [-84.32]])
		res = (model_coefs[:-1] * points).sum(axis=0) + model_coefs[-1]
		print res


