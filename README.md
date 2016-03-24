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
Now when you run it, a Firefox broswer will open. It will select the license Type we chose, and submit the form to the server.:musical_note:
