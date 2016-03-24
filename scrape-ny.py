from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from lxml import html
import csv
import time
# -*- coding: utf-8 -*-

def go_to_next_page():
	next_page_link = driver.find_element_by_xpath('//tr[2]/td/table/tbody/tr/td/a/img[@ src="images/goIN_12.gif"]')
	print "Going to page", next_page_link.text
	next_page_link.click()


def get_data(source):
	texts = []
	#convert the page source into soemthing lxml can parse
	content = html.fromstring(source)
	rows = content.xpath(".//table[2]/tbody/tr/td/table[2]/tbody/tr")

	for row in rows:
		columns = row.xpath(".//td")
		text = [col.text_content().encode("utf-8") for col in columns]
		texts.append(text)

	return texts

#Load the first page:
print "Loading the first page"
driver = webdriver.Firefox()
driver.get("http://www.nydoctorprofile.com/dispatch?action=process_welcome")

#Click Advanced search
print "Clicking the Advancd Search button"
advanced = driver.find_element_by_xpath("//tr[6]/td/input")
advanced.click()
#Enter a last name letter to search
currentletter = "a"
print "Selecting last names that start with '" + currentletter + "'"
textinput = driver.find_element_by_id("LastNameParam")
textinput.send_keys(currentletter)

#Click search button
print "Clicking the search button"
search_button = driver.find_element_by_name("pbSearch")
search_button.click()

#Do the actual scraping and save into a csv file
failed = False
currentcsv = "ny-" + currentletter + ".csv"
with open(currentcsv, "wb") as output:
	writer = csv.writer(output, delimiter=",")

	while not failed:
		print "Trying a new page"
		#Get data on the page
		data_from_page = get_data(driver.page_source)
		#Write them to the csv
		writer.writerows(data_from_page)
		#Go to the next page
		try:
			#loops all the pages
			go_to_next_page()
		except:
			#When it can't find the next page link
			failed = True

driver.close()