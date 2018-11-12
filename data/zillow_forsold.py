from lxml import html
import requests
import unicodecsv as csv
import argparse

def parse(zipcode,filter=None):

	if filter=="newest":
		url = "https://www.zillow.com/homes/recently_sold/{0}/0_singlestory/days_sort".format(zipcode)
	elif filter == "cheapest":
		url = "https://www.zillow.com/homes/recently_sold/{0}/0_singlestory/pricea_sort/".format(zipcode)
	else:
		url = "https://www.zillow.com/homes/recently_sold/{0}_rb/?fromHomePage=true&shouldFireSellPageImplicitClaimGA=false&fromHomePageTab=buy".format(zipcode)

	for i in range(5):
		# try:
		headers= {
					'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
					'accept-encoding':'gzip, deflate, sdch, br',
					'accept-language':'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
					'cache-control':'max-age=0',
					'upgrade-insecure-requests':'1',
					'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
		}
		response = requests.get(url,headers=headers)
		print(response.status_code)
		parser = html.fromstring(response.text)
		search_results = parser.xpath("//div[@id='search-results']//article")
		p = parser.xpath("//div[@id='search-pagination-wrapper']//ol//li[@class='zsg-pagination-next']//a/@href")
		print(len(p))
		page = "http://www.zillow.com%s"%p[0]
		pages = parser.xpath("//div[@id='search-pagination-wrapper']//ol//li//a/@href")
		end_page = pages[len(pages)-2]
		end_page_url = "http://www.zillow.com" + end_page
		print(end_page)
		i = 0
		while True:
			i+=1
			p = '/homes/recently_sold/{0}'.format(zipcode) + '/0_singlestory/days_sort/{0}_p/'.format(i)
			if (p == end_page):
				break
		print(i)
		properties_list = []

		for properties in search_results:
			raw_address = properties.xpath(".//span[@itemprop='address']//span[@itemprop='streetAddress']//text()")
			raw_city = properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressLocality']//text()")
			raw_state= properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressRegion']//text()")
			raw_postal_code= properties.xpath(".//span[@itemprop='address']//span[@itemprop='postalCode']//text()")
			raw_price = properties.xpath(".//span[@class='zsg-photo-card-price']//text()")
			raw_info = properties.xpath(".//span[@class='zsg-photo-card-info']//text()")
			raw_broker_name = properties.xpath(".//span[@class='zsg-photo-card-broker-name']//text()")
			url = properties.xpath(".//a[contains(@class,'overlay-link')]/@href")
			raw_title = properties.xpath(".//h4//text()")
			raw_lat = properties.xpath(".//span[@itemprop='geo']//meta[@itemprop='latitude']/@content")
			raw_lon = properties.xpath(".//span[@itemprop='geo']//meta[@itemprop='longitude']/@content")
			
			address = ' '.join(' '.join(raw_address).split()) if raw_address else None
			city = ''.join(raw_city).strip() if raw_city else None
			state = ''.join(raw_state).strip() if raw_state else None
			lat = ''.join(raw_lat).strip() if raw_lat else None
			lon = ''.join(raw_lon).strip() if raw_lon else None
			postal_code = ''.join(raw_postal_code).strip() if raw_postal_code else None
			price = ''.join(raw_price).strip() if raw_price else None
			info = ' '.join(' '.join(raw_info).split()).replace(u"\xb7",',')
			broker = ''.join(raw_broker_name).strip() if raw_broker_name else None
			title = ''.join(raw_title) if raw_title else None
			property_url = "https://www.zillow.com"+url[0] if url else None 
			is_recentlysold = properties.xpath('.//span[@class="zsg-icon-recently-sold"]')
			properties = {
							'address':address,
                            'latitude': lat,
                            'longitude': lon,
							'city':city,
							'state':state,
							'postal_code':postal_code,
							'price':price,
							'facts and features':info,
							'real estate provider':broker,
							'url':property_url,
							'title':title
			}
			if is_recentlysold:
				properties_list.append(properties)

		while True:
			re = requests.get(page, headers=headers)
			print(re.status_code)
			parser2 = html.fromstring(re.text)
			search_results2 = parser2.xpath("//div[@id='search-results']//article")

			for properties in search_results2:
				raw_address = properties.xpath(".//span[@itemprop='address']//span[@itemprop='streetAddress']//text()")
				raw_city = properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressLocality']//text()")
				raw_state = properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressRegion']//text()")
				raw_postal_code = properties.xpath(".//span[@itemprop='address']//span[@itemprop='postalCode']//text()")
				raw_price = properties.xpath(".//span[@class='zsg-photo-card-price']//text()")
				raw_info = properties.xpath(".//span[@class='zsg-photo-card-info']//text()")
				raw_broker_name = properties.xpath(".//span[@class='zsg-photo-card-broker-name']//text()")
				url = properties.xpath(".//a[contains(@class,'overlay-link')]/@href")
				raw_title = properties.xpath(".//h4//text()")
				raw_lat = properties.xpath(".//span[@itemprop='geo']//meta[@itemprop='latitude']/@content")
				raw_lon = properties.xpath(".//span[@itemprop='geo']//meta[@itemprop='longitude']/@content")

				address = ' '.join(' '.join(raw_address).split()) if raw_address else None
				city = ''.join(raw_city).strip() if raw_city else None
				state = ''.join(raw_state).strip() if raw_state else None
				lat = ''.join(raw_lat).strip() if raw_lat else None
				lon = ''.join(raw_lon).strip() if raw_lon else None
				postal_code = ''.join(raw_postal_code).strip() if raw_postal_code else None
				price = ''.join(raw_price).strip() if raw_price else None
				info = ' '.join(' '.join(raw_info).split()).replace(u"\xb7", ',')
				broker = ''.join(raw_broker_name).strip() if raw_broker_name else None
				title = ''.join(raw_title) if raw_title else None
				property_url = "https://www.zillow.com" + url[0] if url else None
				is_recentlysold = properties.xpath('.//span[@class="zsg-icon-recently-sold"]')
				properties = {
					'address': address,
					'latitude': lat,
					'longitude': lon,
					'city': city,
					'state': state,
					'postal_code': postal_code,
					'price': price,
					'facts and features': info,
					'real estate provider': broker,
					'url': property_url,
					'title': title
				}
				if is_recentlysold:
					properties_list.append(properties)

			if (page == end_page_url):
				break
			else:
				p = parser2.xpath("//div[@id='search-pagination-wrapper']//ol//li[@class='zsg-pagination-next']//a/@href")
				page = "http://www.zillow.com%s"%p[0]
				print(page)
				continue

		return properties_list

		# except:
		# 	print ("Failed to process the page",url)

if __name__=="__main__":
	argparser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
	argparser.add_argument('zipcode',help = '')
	sortorder_help = """
    available sort orders are :
    newest : Latest property details,
    cheapest : Properties with cheapest price
    """
	argparser.add_argument('sort',nargs='?',help = sortorder_help,default ='Homes For You')
	args = argparser.parse_args()
	zipcode = args.zipcode
	sort = args.sort
	for zipciode in range(30002,30010):
		print ("Fetching data for")
		scraped_data = parse(zipcode,sort)
		print ("Writing data to output file")
		with open("properties-%s.csv"%(zipcode),'wb')as csvfile:
			for zipciode in range(30002,30010):
				print ("Fetching data for %s"%(zipcode))
				scraped_data = parse(zipcode,sort)
				print ("Writing data to output file")
				fieldnames = ['title','zipcode','address','latitude','longitude','city','state','postal_code','price','facts and features','real estate provider','url']
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
				writer.writeheader()
				for row in  scraped_data:
					writer.writerow(row)

