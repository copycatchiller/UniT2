'''
Daniel Marcos -- 2016
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Replace with your own
USERNAME = ""
PASSWORD = ""
CHROME_PATH = "/home/danielms/Development/UniT2/chromedriver"

def scrape(username, password):
	
	# Starts the webdriver, in this case, Chrome
	path_to_chromedriver = '/home/danielms/Development/UniT2/chromedriver' 
	browser = webdriver.Chrome(executable_path = path_to_chromedriver)

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
		print "Loading took too long fam"

	# Make sure username and password are empty
	browser.find_element_by_name("username").clear()
	browser.find_element_by_name("password").clear()
	# Enter my username and password, log in 
	browser.find_element_by_name("username").send_keys(username)
	browser.find_element_by_name("password").send_keys(password)
	browser.find_element_by_name('submit').click()

	# Find list of active sites
	
	try:
		element = WebDriverWait(browser, 5).until(
			EC.presence_of_element_located((By.ID, "siteLinkList"))
			)
	except TimeoutException:
		print "Loading too hella long fam"

	browser.execute_script("return dhtml_more_tabs();")
	terms = []
	terms = browser.find_elements_by_class_name('termContainer')
	currentTerm = terms[0]

	classes = currentTerm.find_elements_by_tag_name('a')
	classLinks = []

	for c in classes:
		classLinks.append(c.get_attribute("href"))

if __name__ == '__main__':
	if (USERNAME == "" and PASSWORD == ""):
		USERNAME = raw_input("Enter your GT Username: ") 
		PASSWORD = raw_input("Enter your password: ")
	scrape(USERNAME, PASSWORD)

