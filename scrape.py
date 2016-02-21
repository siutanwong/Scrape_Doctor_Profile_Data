import urllib2
import requests

from bs4 import BeautifulSoup

r = requests.get("http://medboard.nv.gov/Patients/Disciplinary/DisciplinaryActions/")
# html_str = urllib2.urlopen("http://medboard.nv.gov/Patients/Disciplinary/DisciplinaryActions/").read()
# document = BeautifulSoup(html_str)
document = BeautifulSoup(r.text, "html.parser")

doctor_list = []

question_tags = document.find("div", attrs = {"class": "cat-questions"})

for question_tag in question_tags:
	#create empty dictionary to store the doctors' information
	doctor_dict = {}

	#doctor's name and id
	h3_tag = question_tag.find("h3")

	if h3_tag is None:
		continue

	doctor_dict['name'] = h3_tag.string

	#action records
	answer_tag = question_tag.find("div", attrs = {"class": "answer"})
	
	li_tag = answer_tag.find("li")
	a_tag = li_tag.find("a")
	if a_tag is None:
		doctor_dict['case_date'] = None
	else:
		doctor_dict['case_date'] = a_tag.string

	#action description
	ul_tag = answer_tag.find("ul")
	li_tag = ul_tag.find("li")
	ul_tag2 = li_tag.find("ul")
	li_tag2 = ul_tag2.find_all("li")
	doctor_dict['description'] = li_tag2

	#append to list
	doctor_list.append(doctor_dict)

print doctor_list




