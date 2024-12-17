from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time

url = 'https://www.indeed.com/'
driver = webdriver.Chrome()
driver.get(url)
driver.maximize_window()
time.sleep(25)
box = driver.find_element(By.XPATH, '//*[@id="text-input-what"]')
time.sleep(15)
location = driver.find_element(By.XPATH, '//*[@id="text-input-where"]')
for _ in range(25):
    location.send_keys(Keys.BACK_SPACE)
time.sleep(25)
driver.find_element(By.XPATH, '//*[@id="jobsearch"]/button').click()
df = pd.DataFrame(columns=['Link', 'Job Title', 'Company', 'Location', 'Salary', 'Date'])
while True:
    soup = BeautifulSoup(driver.page_source, 'lxml')
    postings = soup.find_all('div', class_='slider_container css-g7s71f eu4oa1w0')
    job_list = []
    for post in postings:
        link = post.find('a', class_='jcs-JobTitle css-jspxzf eu4oa1w0').get('href')
        full_link = 'https://www.indeed.com' + link
        title = post.find('h2', class_='jobTitle').text
        try:
            company = post.find('span', class_='companyName').text
        except:
            company = 'n/a'

        date = post.find('span', class_='date').text
        date = date.replace('Posted', '').replace('EmployerActive', '').strip()
        if date == 'Just posted':
            date = 'Today'
        location = post.find('div', class_='companyLocation').text.split('+', 1)[0]

        try:
            salary = post.find('div', class_='metadata salary-snippet-container').text
        except:
            salary = 'n/a'

        
        job_list.append({'Link': full_link, 'Job Title': title, 'Company': company, 'Location': location, 'Salary': salary, 'Date': date})

        df = pd.concat([df, pd.DataFrame(job_list)], ignore_index=True)
    try:
        next_button = soup.find('a', {'aria-label': 'Next Page'}).get('href')
        driver.get('https://www.indeed.com' + next_button)
        time.sleep(25)
    except:
        break

