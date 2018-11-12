import pandas as pd
house_price = pd.read_csv('data/City_House_Prices.csv')
city_zipcode = pd.read_csv('data/City_Zipcode.csv', dtype={"Zaxis":float})
zipcode_longlat = pd.read_csv('data/Zipcode_LongLat.csv')
merge1 = pd.merge(house_price, city_zipcode, how='inner', left_on = 'RegionName', right_on = 'Region')
house_info = pd.merge(merge1, zipcode_longlat, how='inner', left_on = 'Zipcode', right_on = 'GEOID')
del house_info['LocationType']
del house_info['State_x']
del house_info['State_y']
del house_info['Metro']
del house_info['Lat']
del house_info['Long']
del house_info['Region']
del house_info['TotalWages']
del house_info['Notes']
del house_info['GEOID']
del house_info['City']
del house_info['ZipCodeType']
house_info = house_info.rename(columns = {'INTPTLAT' : 'lat', 'INTPTLONG' : 'long'})
house_info.to_csv('data/House_Zipcode_LL.csv', sep=',')