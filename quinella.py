import os.path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import date
import time
import pandas as pd

# Step 1: Set up the WebDriver (for Chrome)

driver = webdriver.Chrome()


def linkrequest(type, date, racing_state, nthrace):
    return f'https://bet.hkjc.com/en/racing/{type}/{date}/{racing_state}/{nthrace}'

def WinPlace (date_, racing_venue, path=None):
    # Xpath ="//*[@id="rcOddsTable"]/section/div[2]/div[1]"
    if path != None:
        if not os.path.exists(path):
            os.makedirs(path)
    url = linkrequest('wpq', date_, racing_venue, 1)
    print(f'visiting ->{url}')
    driver.get(url)
    #if racing_venue == 'ST':
    #    racing_venue = "Sha Tin"
    div_element = driver.find_element(By.XPATH, f'//*[@id="venue_{racing_venue}"]')
    div_element.click()
    time.sleep(5)
    for race in range(1, 12):
        # Step 3: Optionally wait for the page to fully load and JavaScript to execute
          # Adjust this based on the page loading time
        print(f'Race{race} Win &Place info:')
        try:
            if race != 1:
                div_element = driver.find_element(By.XPATH, f'//div[@aria-label="Race {str(race)}"]')
                div_element.click()
            print('clicked button')
            time.sleep(3)

            print(f'refresh odds ....Start')
            div_element = driver.find_element(By.XPATH, f'//*[@id="refreshButton"]')
            div_element.click()
            print(f'refresh odds ....Done')
            time.sleep(2)
            # Step 4: Find elements dynamically rendered by JavaScript
            # Replace 'your-id-name' with the actual id of the element you're targeting #iwn-odds-table
            # table name = "iwn-odds-table"
            # //*[@id="rcOddsTable"]/section/div[3]/div/div[2]/div/div/div[1]/div
            #//*[@id="rcOddsTable"]/section/div[2]/div[1]

            winplace_table = [["no.", "Win", "place"]]
            for horse in range(1,30):

                print (f'round {horse}:f"//*[@id=\"odds_WIN_{str(race)}_{str(horse)}\"]/a')
                try:

                    div_win_content = driver.find_element(By.XPATH,  f"//*[@id=\"odds_WIN_{race}_{horse}\"]/a")  # //*[@id="odds_PLA_2_6"]

                    div_pla_content = driver.find_element(By.XPATH,f"//*[@id=\"odds_PLA_{str(race)}_{str(horse)}\"]/a") #//*[@id="odds_PLA_2_6"]

                    print(f'{horse} =\nwin=\"{div_win_content.text}\",pla=\"{div_pla_content.text}\"')
                    temp_odds =[horse,div_win_content.text,div_pla_content.text]
                    winplace_table.append(temp_odds)
                    #div_content = driver.find_element(By.XPATH, f"//*[@id=\"root\"]")
                    #print(div_content.text)
                except:

                    print("An exception occurred")

            df = pd.DataFrame(winplace_table)
            print(f'df =\n {df}')
            if path == None:
                csv_loca = f'{date.today()}_{racing_venue}_WinPlace_race_{race}.csv'
            else:
                csv_loca = f'{os.path.join(os.path.dirname(__file__), path, f'{date.today()}_{racing_venue}_WinPlace_race_{race}.csv')}'

            df.to_csv(csv_loca, header=None, index=None)
            time.sleep(5)  # Adjust this based on the page loading time
        except:

            print("An exception occurred")

#//*[@id="odds_WIN_6_11"]
    driver.quit()


# date.today()
def Qtable(type, date_, racing_venue, path=None):
    if path != None:
        if not os.path.exists(path):
            os.makedirs(path)
    url = linkrequest(type, date_, racing_venue, 1)
    print(f'visiting ->{url}')
    driver.get(url)

    # div_element = driver.find_element(By.XPATH, '//div[@aria-label="Sha Tin"]')
    if racing_venue == 'ST':
        racing_venue = "Sha Tin"
    div_element = driver.find_element(By.XPATH, f'//div[@aria-label="{racing_venue}"]')
    div_element.click()

    for race in range(1, 12):
        # Step 3: Optionally wait for the page to fully load and JavaScript to execute
        time.sleep(5)  # Adjust this based on the page loading time
        print(f'Race{race} {type} info:')
        try:
            div_element = driver.find_element(By.XPATH, f'//div[@aria-label="Race {str(race)}"]')
            div_element.click()
            print('clicked button')
            # Step 4: Find elements dynamically rendered by JavaScript
            # Replace 'your-id-name' with the actual id of the element you're targeting
            div_content = driver.find_element(By.CLASS_NAME, 'qin-table ')
            # Step 5: Print or work with the element's text
            time.sleep(5)
            Qin = div_content.text.split('\n')[1:]
            list_Qin = []
            for (idx, odds) in enumerate(Qin):
                print(odds)
                temp_odds = odds.split(' ')
                if idx == 0:
                    temp_odds.insert(0, ' ')
                    temp_odds.insert(0, ' ')
                if idx == 1:
                    temp_odds.insert(0, ' ')
                if idx >= 2:
                    indices_of_table = [index for index, value in enumerate(temp_odds) if value == str(7 + idx)]
                    print(indices_of_table)
                    for k in range(idx - indices_of_table[1]):
                        temp_odds.insert(indices_of_table[1], ' ')
                        indices_of_table[1] += 1
                list_Qin.append(temp_odds if idx == 0 else temp_odds[:-1])
            print(list_Qin)
            df = pd.DataFrame(list_Qin)
            if path == None:
                csv_loca = f'{date.today()}_{racing_venue}_wq_race_{race}.csv'
            else:
                csv_loca = f'{os.path.join(os.path.dirname(__file__), path, f'{date.today()}_{racing_venue}_wq_race_{race}.csv')}'

            df.to_csv(csv_loca, header=None, index=None)
            time.sleep(5)  # Adjust this based on the page loading time
        except:
            print("An exception occurred")
    # Close the browser
    driver.quit()


def Double ( date_, racing_venue, path=None):
    if path != None:
        if not os.path.exists(path):
            os.makedirs(path)
    url = linkrequest('dbl', date_, racing_venue, 1)
    print(f'visiting ->{url}')
    driver.get(url)
    if racing_venue == 'ST':
        racing_venue = "Sha Tin"
    div_element = driver.find_element(By.XPATH, f'//div[@aria-label="{racing_venue}"]')
    div_element.click()


    for race in range(1, 12):
        # Step 3: Optionally wait for the page to fully load and JavaScript to execute
        time.sleep(5)  # Adjust this based on the page loading time
        print(f'Race{race} Double info:')
        #try:
        div_element = driver.find_element(By.XPATH, f'//div[@aria-label="Race {str(race)}"]')
        div_element.click()
        print('clicked button')
        # Step 4: Find elements dynamically rendered by JavaScript
        # Replace 'your-id-name' with the actual id of the element you're targeting #iwn-odds-table
        # table name = "iwn-odds-table"
        #//*[@id="rcOddsTable"]/section/div[3]/div/div[2]/div/div/div[1]/div
        #//*[@id="refreshButton"]


        time.sleep(5)
        div_content = driver.find_element(By.XPATH, '//*[@id="rcOddsTable"]/section/div[3]/div/div[2]/div/div/div[1]/div')
        time.sleep(5)
        Dblin = div_content.text.split('\n')[2:]
        #print(f'Double table :\n {Dblin}')
        dbl_odds_table =[]
        for idx ,item  in enumerate(Dblin):
            temp_odds =item.split(' ')
            if idx ==0 :
                temp_odds.insert(0,' ')
            else:
                for i in range(15-len(temp_odds)):
                    temp_odds.append(' ')
            dbl_odds_table.append(temp_odds)

        print(f'Double table :\n {dbl_odds_table}')

        df = pd.DataFrame(dbl_odds_table)
        if path == None:
            csv_loca = f'{date.today()}_{racing_venue}_dbl_race_{race}.csv'
        else:
            csv_loca = f'{os.path.join(os.path.dirname(__file__), path, f'{date.today()}_{racing_venue}_dbl_race_{race}.csv')}'

        df.to_csv(csv_loca, header=None, index=None)
        time.sleep(5)  # Adjust this based on the page loading time


        #except:
        #    print("An exception occurred")
    # Close the browser
    driver.quit()






# 'wpq',str(date.today()),'ST',1

if __name__ == "__main__":
    print("Welcome download hkjc info!")
    # racing_venue input 'ST' or 'S1'
    #Qtable('wpq', str(date.today()), 'ST')
    # print(f'path -> {os.path.join(os.path.abspath('quinella.py'),'csv')}')
    #Double(str(date.today()), 'ST')
    WinPlace(str(date.today()), 'S1',path='WinPlace')
"""


import requests
from bs4 import BeautifulSoup
from datetime import date
# Step 1: Make a request to the website
# sample :https://bet.hkjc.com/en/racing/wpq/2024-09-15/ST/1

def linkrequest (type,date,racing_state,nthrace):
    return f'https://bet.hkjc.com/en/racing/{type}/{date}/{racing_state}/{nthrace}'

#date.today()
url = linkrequest('wp',str(date.today()),'ST',1)

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
div_content = soup.find_all()
if div_content:
    print(div_content)
else:
    print("Div with specified class not found")
"""

""""
url = linkrequest()
response = requests.get(url)

# Step 2: Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Step 3: Find the div with the specific class name
# Replace 'your-class-name' with the actual class name you're targeting
div_content = soup.find('div', class_='your-class-name')

# Step 4: Extract and print the text within the div
if div_content:
    print(div_content.text)
else:
    print("Div with specified class not found")

"""
