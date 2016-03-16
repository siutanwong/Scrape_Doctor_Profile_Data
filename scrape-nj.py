from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from lxml import html
import csv
# -*- coding: utf-8 -*-

def go_to_next_page():
    next_page_link = driver.find_element_by_xpath('//table[@id="datagrid_results"]//tr//td//span/following-sibling::a')
    print "Going to page", next_page_link.text
    next_page_link.click()

def get_data(source):
    texts = []
    # convert the page source into something lxml can parse
    content = html.fromstring(source)
    # grab all of the rows from the data table
    rows = content.xpath(".//table[@id='datagrid_results']//tr")
    # loop through each of the rows to get the content
    for row in rows:
        columns = row.xpath(".//td")
        text = [col.text_content().encode("utf-8") for col in columns]
        texts.append(text)
    # Remove the first and last columns (header + pagination)
    return texts[1:-1]


# Load the first page
print "Loading the first page"
driver = webdriver.Firefox()
driver.get("https://newjersey.mylicense.com/verification/Search.aspx")

# Select medicine and surgery
print "Selecting the dropdown"
dropdown = Select(driver.find_element_by_name("t_web_lookup__license_type_name"))
dropdown.select_by_value("Medical Doctor")

# Here we'll enter a last name letter and wildcard
currentletter = "a"
print "Selecting last names that start with '" + currentletter + "'"
textinput = driver.find_element_by_name("t_web_lookup__last_name")
textinput.send_keys(currentletter + "*")


# Click the search button
print "Clicking the search button"
search_button = driver.find_element_by_id("sch_button")
search_button.click()

failed = False
currentcsv = "pa-" + currentletter + ".csv"
with open(currentcsv, "wb") as output:
    writer = csv.writer(output, delimiter=',')
    
    while not failed:
        print "Trying a new page"
        # Get the data on the page
        data_from_page = get_data(driver.page_source)
        # Write them to the CSV
        writer.writerows(data_from_page)
        # Go to the next page
        try:
            # And then it just loops back up
            go_to_next_page()
        except:
            # But it goes into here if it can't find the next link
            failed = True

    
driver.close()