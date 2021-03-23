from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import os
import traceback


# finds a pdf from search engine results for a given part number
def search_part(driver, part):
	driver.get("https://duckduckgo.com/")

	# wait for page to load
	try:
		WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".search-wrap--home")))
	except:
		print("Timed out while loading search engine - closing program")
		driver.quit()
		os._exit(0)
	
	searchbar = driver.find_element_by_xpath("//input[@type='text']")			# web element to type into
	search_button = driver.find_element_by_xpath("//input[@type='submit']")		# submit button

	if (part.lower() == "exit"):	# close the program if the user submits 'exit'
		print("Exiting")
		driver.quit()
		os._exit(0)

	searchbar.send_keys(part_num)
	search_button.click()

	# wait until page loads
	WebDriverWait(driver, 10).until(expected_conditions.visibility_of(driver.find_element_by_xpath("//div[@class='result__body links_main links_deep']")))
	print("Searching web results")

	# search through results to find PDF links
	try:
		search_results = driver.find_elements_by_xpath('.//a')
		for result in search_results:
			link = str(result.get_attribute('href'))
			if ".pdf" in link:
				print("Found PDF datasheet at: " + link)
				return link

	except:
		print(str(part) + " couldn't be found")
		pass		# move to next part


# PROGRAM START
if(os.name == 'nt'):
	geckodriver_path = '.\\geckodriver.exe'
else:
	geckodriver_path = './geckodriver'

print("\nDatasheet finder")
print("\nType 'exit' at any time to close the program")
part_list = input("\nEnter a part number or list of part numbers: ").split(",")

# driver for running web search
options = Options()
options.headless = False	# visible window
driver = webdriver.Firefox(executable_path = geckodriver_path, options = options)

current_tab = "tab-"	# keeps track of open tab
count = 0				# used to increment current tab

try:
	while(True):
		for part_num in part_list:
			pdf_link = search_part(driver, part_num)
			driver.get(pdf_link)	# open pdf in current tab

			# open a new tab for next part in list
			if part_list.index(part_num) != len(part_list) - 1:	
				current_tab = current_tab + str(count)
				execute_string = "window.open('about:blank', '" + current_tab + "');"	# arguments for execute_script
				driver.execute_script(execute_string)
				driver.switch_to.window(current_tab)
				count += 1

		quit = input("Find another part? Y/N\n")
		if quit.lower() == "n" or quit.lower() == "exit":
			break

		part_list = input("\nEnter another part or list of parts: ").split(",")
	
except:
	logfile = open("exception.log", "w")
	traceback.print_exc(file = logfile)
	driver.quit()
	os._exit(0)

print("Finished - closing program")

