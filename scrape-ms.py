from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml import html
import csv
import time
# -*- coding: utf-8 -*-

# def go_to_next_page():
# 	next_page_link = driver.find_elecment_by_id("view:_id1:viewPanel1:pager1__Next__lnk")
# 	print "Going to page", next_page_link.text
# 	next_page_link.click()


def get_data(source):
	texts = []
	#convert the page source into something lxml can parse
	content = html.fromstring(source)
	rows = content.xpath(".//tr/td/table/tbody/tr")

	for row in rows:
		columns = row.xpath(".//td")
		text = [col.text_content().encode("utf-8") for col in columns]
		texts.append(text)

	return texts[1:]

#Load the first page
print "Loading the first page"
driver = webdriver.Firefox()
driver.get("http://www.msbml.ms.gov/msbml/medical.nsf")

#Do the actual scraping and save into a csv find_elecment_by_id
with open("ms.csv", "wb") as output:
	writer = csv.writer(output, delimiter=",")

	wait = WebDriverWait(driver, 10)
	# wait.until(EC.element_to_be_clickable((By.ID, 'view:_id1:viewPanel1:pager1__Next__lnk')))
	while True:
		print "Trying a new page"
		#Get the data on the page
		data_from_page = get_data(driver.page_source)
		#Write them to the csv
		writer.writerows(data_from_page)
		#Go to the next page

		try:
			element = wait.until(EC.element_to_be_clickable((By.ID, 'view:_id1:viewPanel1:pager1__Next__lnk')))
			element.click()
		except TimeoutException:
			break

		time.sleep(0.5)

driver.close()