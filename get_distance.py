import geopy.distance
import csv

lattitude = []
longitude = []
with open('shopping_mall.csv', 'rb') as shopping_mall:
	readerSM = csv.reader(shopping_mall)
	for row in readerSM:
		lattitude.append(row[1])
		longitude.append(row[2])

lattitude = lattitude[1:-1]
longitude = longitude[1:-1]

la = []
lon = []
inputrows = []
with open('properties_0419.csv', 'rb') as csvinput:
	reader = csv.reader(csvinput)
	for row in reader:
		# la.append(row[1])
		# lon.append(row[2])
		inputrows.append(row)

# la = la[1:]
# lon = lon[1:]
inputrows = inputrows[1:]

print len(lattitude)
print lattitude

with open('output.csv', 'wb') as csvoutput:
	writer = csv.writer(csvoutput)
	for row in inputrows:
		temp = row
		for i in range(len(lattitude)):
			coor1 = (lattitude[i], longitude[i])
			coor2 = (row[1], row[2])
			dis = geopy.distance.vincenty(coor1, coor2).km
			temp.append(dis)

		writer.writerow(temp)



# with open('properties_0419.csv', 'r') as csvinput:
# 	with open('output.csv', 'w') as csvoutput:
# 		writer = csv.writer(csvoutput, lineterminator='\n')
# 		reader = csv.reader(csvinput)

# 		all = []
# 		row = next(reader)
# 		for i in 
