### Scrape Doctor Profile Data from State's Board of Medicine Websites

an example of using **selenium + lxml** libs to extract table data from web pages.

### Background

I'll use the Washington DC board of medicine website as an example: https://app.hpla.doh.dc.gov/Weblookup/

![](.//img/dc.png)

My goal is to scrape all the search results (multiple pages) from the .asp website and then save the data into a csv file.
![](.//img/table.png)

First let's set up our environment:

```
$ pip install selenium
$ pip install lxml
```
Then we add the following libs in our script
```
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from lxml import html
import csv
```

#### Loading the search page
```
driver = webdriver.Firefox()
driver.get("https://app.hpla.doh.dc.gov/Weblookup/")
```
#### Selecting from the "License Type" dropdown menu
If you look at the HTML associated with this dropdown menu, you will see the ```name``` that attributes to it is ```t_web_lookup__license_type_name```
Next, select "Medicine and Surgery" from the dropdown and click the "Inspect Element", you will find the value associated with it is ```"MEDICINE AND SURGERY"```.

Let's add these attributions in our script:
```
dropdown = Select(driver.find_element_by_name("t_web_lookup__license_type_name"))
dropdown.select_by_value("MEDICINE AND SURGERY")
```
#### Click the Search button
Like the dropdown, we need to find the HTML of the search button on the search page, here it is in the web inspector:
![](.//img/id.png)

We can select this button and add a .click function in our script:
```
search_button = driver.find_element_by_id("sch_button")
search_button.click()
```
Now when you run our script, a Firefox broswer will pop out and submit the form to the server.:musical_note:

#### Extracting the search results
Let's create a function called ```get_data()``` and use the ```html``` function from ```lxml``` to extract the table data (ps: you can also use beautifulsoup if you like, I like lxml better because it is more straight forward.)
```
def get_data(source):
    texts = []
    content = html.fromstring(source)
    rows - content.xpath(".//table[id@='datagrid_results']//tr")
    for row in rows:
        columns = row.xpath(".//td")
        text = [col.text_content() for col in columns]
        texts.append(text)
    return texts
```
This function will extract all the table dat on the current page, and put it in the list ```texts```.

#### Pagination
When you scoll down to the bottom of the page, you will notice that it only shows 40 pages at a time:
![](.//img/page.png)
And when you click the "..." next to page 40, it will take to page 41 - 80, and so on so forth.
In order to get all the reuslts, we need to find the ```xpath``` of each page  number link, starting with page2:
```
def go_to_next_page():
    next_page_link = driver.find_element_by_xpath("//table[@id='datagrid_results']//tr//td//span/following-sibling::a")
    next_page_link.click()
```
This function allows the script to go through all the ```<a>```tags that contain the page number link.
Now we have all the stuff we need to extract data from this database, all we need to do write the data into a csv file:
```
With open("dc.csv", "wb") as output:
    writer = csv.writer(output, delimiter=",")
    While True:
        data_from_page = get_data(driver.page_source)
        writer.writerows(data_from_page)
        try:
            go_to_next_page()
        except:
            break
driver.close()
```
####Conclusion
That's all! Run the script on your computer and go get yourself a cup of coffee:coffee:By the time you come back, the data will be ready for you in a csv file!:octocat:

####Contact
If you have questions regarding the script or scraping in general, feel free to shoot me an email at wongsiutan@gmail.com
