from bs4 import BeautifulSoup
import requests
from csv import writer
import time
import datetime as dt
from datetime import date
from datetime import datetime

url = "https://vidyutpravah.in/state-data/tamil-nadu"
page = requests.get(url)
# print(page)

soup = BeautifulSoup(page.content, 'html.parser')
lists = soup.find_all('div', id_="TamilNadu_map")
head = soup.find_all('div', class_="outer_div")


# print(head)

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


with open('03_06_2023_demand_data.csv', 'w', encoding='utf-16le', newline='') as f:
    thewriter = writer(f)
    header = ['Date', 'Time Block', 'Yesterday', 'Currentday', 'Rec. Time']
    thewriter.writerow(header)

    i = 0
    a = []
    while True:
        try:
            today = date.today()
            print(" Date         : ", today)

            for title in soup.find_all('tr', {'class': 'blue_bg'}):
                s1 = str(title.get_text())
            print(" Time Block   : ", s1[45:58:1])

            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'html.parser')

            for yesterday in soup.find_all('span', {'class': 'value_PrevDemandMET_en value_StateDetails_en'}):
                e = str(yesterday.get_text())
            print(" Yesterday    : ", e)
            for current in soup.find_all('span', {'class': 'value_DemandMET_en value_StateDetails_en'}):
                r = str(current.get_text())
            print(" Currentday   : ", r)

            # datetime object containing current date and time
            now = datetime.now()
            # print("now =", now)
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            print(" Rec. Time    : ", dt_string)

            print("-----------------------------------------------")

            time.sleep(60)

            if i == 5000:
                break
            i = i + 1
            a = [i]
            print(a)

            info = [today, s1[45:58:1], e, r, dt_string]
            thewriter.writerow(info)

        except:
            time.sleep(60)

            if i == 5000:
                break
            i = i + 1
            a = [i]
            print(a)

            info_con = 'No Connection'
            info = [info_con]
            print(info)
            thewriter.writerow(info)
print("-------------------Finished--------------------")
