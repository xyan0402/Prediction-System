
# coding: utf-8

# In[1]:
def ml_predict(zipcode, latitude, longitude, city, state, numBed, numBath, sqft):
	from sklearn import preprocessing
	from sklearn.preprocessing import LabelEncoder
	import math
	from collections import defaultdict
	import pandas as pd
	import numpy as np
	from flask import jsonify
	from sklearn.ensemble import RandomForestRegressor
	from sklearn.externals import joblib
	import json
	import geopy.distance
	import csv

	# In[2]:
	le_city = LabelEncoder()
	le_city.classes_ = np.load('model/city.npy')
	le_state = LabelEncoder()
	le_state.classes_ = np.load('model/state.npy')
	#to use saved model to predict
	rf = joblib.load('model/rf_model.pkl')


	#input format: latitude	longitude	city	state	postal_code
	#  #bedrooms	#bathrooms	sqft	d1	d2	d3	d4	d5	d6	d7	d8	d9	d10	d11	d12	d13	d14	d15	d16	d17	d18	d19	d20
	# d1-d20 are the 20 distances
	with open('data/shopping_mall.csv', 'r') as shopping_mall:
		readerSM = csv.reader(shopping_mall)
		malllat = []
		malllong = []
		for row in readerSM:
			malllat.append(row[1])
			malllong.append(row[2])

	malllat = malllat[1:-1]
	malllong = malllong[1:-1]
	temp = []
	for i in range(len(malllat)):
			coor1 = (malllat[i], malllong[i])
			coor2 = (latitude, longitude)
			dis = geopy.distance.vincenty(coor1, coor2).km
			temp.append(dis)

	#x_test = [latitude,longitude,le_city.transform([city])[0],
	#          le_state.transform([state])[0],zipcode,numBed,numBath,8407,17.97815547,
	#          11.61922521,10.73757085,17.91580071,12.36143495,12.84093017,
	#          10.95456711,14.2463137,10.22767987,14.97290478,10.60371232,
	#          19.62657156,10.6664712,12.12805345,17.39411973,11.00101478,
	#          12.74852644,16.87761032,14.76784305,3.831071845]
	x_test = [latitude,longitude,le_city.transform([city])[0],
	          le_state.transform([state])[0],zipcode,numBed,numBath,sqft]
	x_test.extend(temp)
	results = rf.predict([x_test]).tolist()
	results.append(min(temp))
	return json.dumps(results)

