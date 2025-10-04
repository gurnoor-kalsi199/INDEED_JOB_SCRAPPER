from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from bs4 import BeautifulSoup
import random


#Define our stealthy driver
driver = Driver(uc=True)

#Necessary Stuff
URL = "https://in.indeed.com/jobs?q=software+developer&l=India"
MAX_PAGES = 5
wait = WebDriverWait(driver, 10)

#Now make the terminal header
terminal_width = os.get_terminal_size().columns
text = "Indeed Job Scrapper"
header = text.center(terminal_width, '-')
print(header)

#Now comes the actual scrapping
print(f"Getting url - {URL}")
driver.get(URL)

#Make a Data folder
os.makedirs("data", exist_ok=True)

try:
    page = 1
    while driver.find_element(By.CSS_SELECTOR, 'a[data-testid="pagination-page-next"]'):
        wait.until(
            EC.visibility_of_element_located((By.ID, "mosaic-zone-ssrSerpModals"))
        )
        print(f"Moved to {driver.current_url}")

        #Get The list of jobs
        elems = driver.find_elements(By.CSS_SELECTOR, ".cardOutline.tapItem.dd-privacy-allow.result")
        n_jobs = len(elems)
        print(f"Retreived {n_jobs} jobs")

        #Create sub_folder
        os.makedirs(f"data/page-{page}", exist_ok=True)

        job_index = 1
        #Get html's of each job
        for elem in elems:
            time.sleep(random.uniform(0.1, 0.5))
            print(f"->Retreiving job{job_index}")
            d = elem.get_attribute("outerHTML")

            #Prettify the HTML
            soup = BeautifulSoup(d, "html.parser")
            pretty_html = soup.prettify(formatter="html")

            #Now save into a file
            with open(f"data/page-{page}/job-{job_index}.html", "w", encoding="utf-8") as f:
                f.write(pretty_html)

            time.sleep(random.uniform(0.1, 0.5))
                
            #Move to next job
            job_index += 1

        next_button = driver.find_element(By.CSS_SELECTOR, 'a[data-testid="pagination-page-next"]')
        #slowly move to this element
        driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            next_button
        )
        #Click the button
        wait.until(EC.element_to_be_clickable(next_button)).click()

        #Move to next page
        page += 1

except Exception as e:
    print(f":Failure, Error: {e}")

finally:
    print("Scrapping done, please check Data/")
    print(header)
    time.sleep(10)
    driver.quit()