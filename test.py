import csv
import numpy as np

bed_no = 1
bath_no = 1
inputrows = []
with open('data/properties_0419.csv', 'r') as csvfile:
    csvReader = csv.reader(csvfile)
    i = 0
    for row in csvReader:
        if row[8] == str(bed_no) and row[9] == str(bath_no):
            inputrows.append([i, row[6], row[1], row[2]])
            i = i + 1
        
inputrows = inputrows[1:]
inputstring = ["No", "price", "latitude", "longitude"]

with open('data/bbrange.csv', 'w') as csvfile:
    csvWriter = csv.writer(csvfile)
    csvWriter.writerow(inputstring)
    for row in inputrows:
        temp = row
        csvWriter.writerow(temp)