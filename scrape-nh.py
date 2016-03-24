import requests
import csv
from lxml import html
# -*- coding: utf-8 -*-


root_url1 = 'https://www.nh.gov/medicine/aboutus/actions/'
page_ids = ['1986', '1988', '1989', '1990', '1991', '1992', '1993','1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008']
root_url2 = '.html'

texts = []

# def scrape_page(page_id):
for page_id in page_ids:
	url = root_url1 + page_id + root_url2
	result = requests.get(url)
	content = html.fromstring(result.content)
	#pull out every table row()
	rows = content.xpath(".//p")

	text = [row.text_content().encode("utf-8") for row in rows]
	texts.append(text)
	# for row in rows:
	# 	#grab every table cell that's inside of that row
	# 	# columns = row.xpath(".//span")

	# 	#get the text out of each of those columns
	# 	text = [col.text_content().encode("utf-8") for col in columns]

	# 	# print text
	# 	#append all the data empty list
	# 	texts.append(text)

#Write the data into a csv file
with open("nh-dicipline2.csv", "wb") as output:
	writer = csv.writer(output, delimiter=",")
	writer.writerows(texts)

# 	return content

# if __name__ == '__main__':
# 	for page_id in page_ids:
# 		print content