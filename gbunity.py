'''
Daniel Marcos -- 2016
UniT2 scrapes TSquare to generate a combined gradebook of
all your current classes 

'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


# Replace with your own
USERNAME = ""
PASSWORD = ""
CHROME_PATH = "./chromedriver"
browser = webdriver.Chrome(executable_path = CHROME_PATH)

def loginToT2(username, password):
	# Navigate to the main page and click on login button
	url = "https://t-square.gatech.edu/portal"
	browser.get(url)
	browser.find_element_by_id('loginLink1').click()

	# Wait for page to load
	try:
		element = WebDriverWait(browser, 5).until(
			EC.presence_of_element_located((By.NAME, "username"))
		)
	except TimeoutException:
		print("Loading took too long")

	# Make sure username and password are empty
	browser.find_element_by_name("username").clear()
	browser.find_element_by_name("password").clear()
	# Enter my username and password, log in 
	browser.find_element_by_name("username").send_keys(username)
	browser.find_element_by_name("password").send_keys(password)
	browser.find_element_by_name('submit').click()


'''
You must be logged into T2 to get current classes
Returns a list of links to each class site for the current term.
'''
def getCurrentClasses():
	# Find list of active sites
	try:
		element = WebDriverWait(browser, 5).until(
			EC.presence_of_element_located((By.ID, "siteLinkList"))
			)
	except TimeoutException:
		print("Loading took too long")

	# Clicks on "Active Sites"
	browser.execute_script("return dhtml_more_tabs();")
	# Selects the current term
	terms = []
	terms = browser.find_elements_by_class_name('termContainer')
	currentTerm = terms[0]
	# Finds all the lnks under the current term
	classes = currentTerm.find_elements_by_tag_name('a')
	classLinks = []
	for c in classes:
		classLinks.append(c.get_attribute("href"))

	return classLinks

def processGradebooks(classLinks):
	
	for link in classLinks:
		browser.get(link)
		classTitle = browser.find_elements_by_css_selector(".selectedTab")[0].find_element_by_tag_name("a").find_element_by_tag_name("span").text

		print(" \n -----------------------------------------")
		print(classTitle + "\n")

		toolMenu = browser.find_element_by_id("toolMenu")
		for elem in toolMenu.find_elements_by_tag_name("a"):
			if elem.get_attribute("class") == "icon-sakai-gradebook-tool ":
				browser.get(elem.get_attribute("href"))
				# Here we are looking at one Gradebook
				processTable()
				break

def processTable():
	# First we have to find the table. It has a class="listHier wideTable lines"
	iframe = browser.find_elements_by_tag_name('iframe')[0]
	browser.switch_to_frame(iframe)
	gbTable = None
	time.sleep(1)
	for t in browser.find_elements_by_tag_name("table"):
		if t.get_attribute("class") == "listHier wideTable lines":
			gbTable = t
	time.sleep(1)
	if gbTable:
		# Classes have different things on the gradebook so we need to know
		# what position contains title and what position contains grade
		head = gbTable.find_element_by_tag_name("thead")
		headRow = head.find_elements_by_tag_name("th")
		pos = 0
		titlePos = None
		gradePos = None
		for pos in range(len(headRow)):
			header = headRow[pos].find_elements_by_tag_name("a")
			if len(header) > 0:
				headerText = header[0].text
				if headerText == "Title":
					titlePos = pos
				elif headerText == "Grade*" or headerText == "Grade":
					gradePos = pos
			pos = pos + 1
		body = gbTable.find_element_by_tag_name("tbody")
		rows = body.find_elements_by_tag_name("tr")
		
		# Print title and grade
		for row in rows:
			rowData = row.find_elements_by_tag_name("td")
			print(rowData[gradePos].text + " --- " + rowData[titlePos].text)
			
		browser.switch_to_default_content()

def createCombinedGradebook():
	loginToT2(USERNAME, PASSWORD)
	processGradebooks(getCurrentClasses())

if __name__ == '__main__':
	if USERNAME == "" and PASSWORD == "":
		import getpass
		USERNAME = raw_input("Enter your GT Username: ") 
		PASSWORD = getpass.getpass("Enter your password: ")
	createCombinedGradebook()