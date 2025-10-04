import os
from bs4 import BeautifulSoup
from main import MAX_PAGES
import re
from urllib.parse import urljoin
import pandas as pd
import pyshorteners

JOB_TITLE = []
COMPANY_NAME = []
LOCATION = []
SALARY = []
LINK_TO_JOB = []

#Define a function to get proper salary
def formatted_salary(salary_str):
    number_text = re.findall('\d[\d,]*', salary_str) #"₹21,60,000 - ₹32,40,000" -> ['21,60,000', '32,40,000']

    numbers = [int(num.replace(',', '')) for num in number_text]

    salary = 0
    if not number_text:
        return 0
    if len(numbers) == 1:
        salary = numbers[0]
    else:
        total_num = 0
        for num in numbers:
            total_num += num
        total_num /= len(numbers)
        salary = total_num

    if "month" in salary_str.lower():
        salary *= 12
        return salary
    else:
        return salary

#Loop through the fucking pages man
for page in range(1, MAX_PAGES + 1):

    #Loop through the html's
    for job in os.listdir(f"data/page-{page}"):
        directory_path = f"data/page-{page}"
        file_path = os.path.join(directory_path, job)
        with open(file_path) as f:
            html = f.read()
            soup = BeautifulSoup(html, "html.parser")

            #Retreive stuff one by one

            #Get the JOB_TITLES
            try:
                id_pattern = re.compile('^jobTitle-')
                job_title = soup.find('span', id=id_pattern).text
            except Exception as e:
                job_title = 'N/A'

            #The company Name
            try:
                company_name = soup.find('span', attrs={'class': 'css-1ssrdda eu4oa1w0'}).text
            except Exception as e:
                company_name = 'N/A'

            #The location
            try:
                location = soup.find('div', attrs={'data-testid': 'text-location'}).text
            except Exception as e:
                location = 'N/A'

            #Link Stuff
            link_element = soup.find('a', class_='jcs-JobTitle css-1baag51 eu4oa1w0')

            if link_element:
                partial_link = link_element.get('href')

            base_url = "https://in.indeed.com"
            full_link = urljoin(base_url, partial_link)

            #Get salary because it is different in each
            rupee_pattern = re.compile('₹')
            salary_text_node = soup.find(text=rupee_pattern)

            if salary_text_node:
                salary_text = salary_text_node.strip()
                salary = formatted_salary(salary_str=salary_text)
            else:
                salary = 'N/A'


            #Append everything now
            JOB_TITLE.append(job_title)
            COMPANY_NAME.append(company_name)
            LOCATION.append(location)
            SALARY.append(salary)
            LINK_TO_JOB.append(full_link)


#Create a link shortener object
s = pyshorteners.Shortener()

#Clean the arrays
JOB_TITLE = [job.strip() for job in JOB_TITLE]
LOCATION = [job.strip() for job in LOCATION]
SALARY = SALARY
COMPANY_NAME= [job.strip() for job in COMPANY_NAME]
LINK_TO_JOB = [job.strip() for job in LINK_TO_JOB]
#Shorten the links
try:
    LINK_TO_JOB = [s.tinyurl.short(long_url) for long_url in LINK_TO_JOB]
except Exception:
    pass


data = {
    'JOB_TITLE': JOB_TITLE,
    'LOCATION': LOCATION,
    'SALARY': SALARY,
    'COMPANY_NAME': COMPANY_NAME,
    'LINK_TO_JOB': LINK_TO_JOB
}

dataframe = pd.DataFrame(data=data)

dataframe.to_csv('output.csv')


            



