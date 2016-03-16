import requests
from lxml import html
import csv
import time
# -*- coding: utf-8 -*-

#create an empty list to store data
texts = []
#range of pages to loop through
pages = range(1000, 1500)

#create a for loop to iterate all the pages.
for page in pages:

	result = requests.post("http://www.vahealthprovider.com/search_results.asp", data = {'whichpage': page, 'last_Name':'', 'county': 'Any', 'specialty': 'Any'})
	# print result

	#convert the raw HTML into something we can search through
	content = html.fromstring(result.content)
	#pull out every table row ()
	rows = content.xpath(".//tr")

	for row in rows:
		#grab every table cell that's inside of that row
		columns = row.xpath(".//td")
		
		#get the text out of each of those columns using .text_content()
		text = [col.text_content() for col in columns]

		# print text
		
		#append all the data in the empty list
		texts.append(text)

	time.sleep(1)
	print "Page added"

# Write the data into a csv file
with open('virginia2.csv', "wb") as output:
	writer = csv.writer(output, delimiter=',')
	writer.writerows(texts)