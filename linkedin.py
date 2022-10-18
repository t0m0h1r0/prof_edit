import pandas as pd
import time
from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

yourName = 'hogehoge'
csv_file = 'gp-search-20221016-125053.csv'

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=options)
url = "https://www.linkedin.com/in/tomohiro-kawaguchi-055567124/edit/forms/patent/new/?profileFormEntryPoint=PROFILE_COMPLETION_HUB"

inputItems = {
	"title":"single-line-text-form-component-profileEditFormElement-PATENT-profilePatent-ACoAAB6x0YEB0RnQyX4Ja2B4-pWzaC54ZP1o8DQ-1-title",
	"number":"single-line-text-form-component-profileEditFormElement-PATENT-profilePatent-ACoAAB6x0YEB0RnQyX4Ja2B4-pWzaC54ZP1o8DQ-1-externalReference",
	"issueDate":"-profileEditFormElement-PATENT-profilePatent-ACoAAB6x0YEB0RnQyX4Ja2B4-pWzaC54ZP1o8DQ-1-issueDate-date-picker",
	"ref":"single-line-text-form-component-profileEditFormElement-PATENT-profilePatent-ACoAAB6x0YEB0RnQyX4Ja2B4-pWzaC54ZP1o8DQ-1-url",
}
button = "form-component__typeahead-cta-ember79-button"
inv = "form-component__typeahead-cta-ember79"
save = "ember88"


df = pd.read_csv(csv_file,skiprows=1)
for l,x  in df.sort_values(by="priority date").iterrows():
	x_inventors = str(x['inventor/author']).replace(', ',',').split(',')
	x_inventors.remove(yourName)
	title = str(x['title'])[:255]
	number = str(x['id'])
	issueDate = str(x["priority date"]).replace('-','/')
	ref = str(x['result link'])
	val = {
		"title":title,
		"number":number,
		"issueDate":issueDate,
		"ref":ref,
	}

	while True:
		try:
			driver.get(url)
			time.sleep(2)
			for i,s in inputItems.items():
				#print(i,val[i],s)
				g = driver.find_element(By.ID, s)
				#print(g.text)
				g.send_keys(val[i])
			for j in x_inventors:
				g = driver.find_element(By.ID, button).click()
				time.sleep(2)
				g = driver.find_element(By.ID, inv).find_element(By.TAG_NAME, "input")
				g.send_keys(j)
				g.send_keys(Keys.ENTER)
			g = driver.find_element(By.ID, save).find_element(By.TAG_NAME,"button").click()	
		except:
			pass
		else:
			break
