import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs
import requests as rq
import time
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
def scrolling(nb_jobs):
    i = 0
    while i <= int(nb_jobs/25)+1:
        i = i + 1
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")   
        try:           
            browser.find_element(By.XPATH,'/html/body/div[1]/div/main/section/button').click()
            time.sleep(3)
            if browser.findElement(By.XPATH("/html/body/div[1]/div/main/section/button")).isEnabled() == False:
                break
        except:
            pass
            time.sleep(4)
nb_jobs = {}
job_titles = []
company_names = []
job_locations = []
jobs_description = []
browser = webdriver.Chrome(executable_path=r'C:/Users/lenovo/Desktop/chromedriver_win32/chromedriver')
url ='https://www.linkedin.com/jobs/search?keywords=Data%20Science&location=R%C3%A9gion%20m%C3%A9tropolitaine%20de%20Columbus%2C%20Ohio&geoId=90000184&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
browser.get(url)
nb_job = int(browser.find_element(By.XPATH,"/html/body/div[1]/div/main/div/h1/span[1]").text.replace("\u202f", ""))
scrolling(nb_job)
jobs_offer = browser.find_elements(By.CLASS_NAME,"jobs-search__results-list")
hrefs = []
for i in range(1,nb_job):
    try :
        job_titles.append(browser.find_element(By.XPATH,"/html/body/div[1]/div/main/section[2]/ul/li["+str(i)+"]/div/div[2]/h3"))
        company_names.append(browser.find_element(By.XPATH,"/html/body/div[1]/div/main/section[2]/ul/li["+str(i)+"]/div/div[2]/h4/a"))
    except :
        pass
    try:
        WebDriverWait(browser, 25).until(EC.presence_of_element_located((By.XPATH ,"/html/body/div[1]/div/main/section[2]/ul/li["+str(i)+"]/div/a")))
        hrefs.append(browser.find_element(By.XPATH,"/html/body/div[1]/div/main/section[2]/ul/li["+str(i)+"]/div/a").get_attribute("href"))
    except:
        pass
for i in hrefs : 
    jobs_des = rq.get(i).content
    jobs_desc = bs(jobs_des,'html.parser')
    try:
        jobs_description.append(jobs_desc.find('div',class_='description__text description__text--rich').text)
    except:
        jobs_description.append("Description introuvable")            
jobs_description = [jobs_description[i].strip().replace("\n","").replace("  ","") for i in range(len(jobs_description))]
dict = {'job title': [i.text for i in job_titles],'company name': [i.text for i in company_names], 'job description': jobs_description} 
df = pd.DataFrame(dict)        