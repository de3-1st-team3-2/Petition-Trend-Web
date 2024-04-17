import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import csv
import json

overall_data = []
for i in range(5):
    url = f"https://idea.eseoul.go.kr/front/allSuggest/list.do?searchCondition2=&searchCondition3=recent&searchCondition4=&sSuggest_divi=&sKeyword=&pageIndex={i}"
    result = requests.get(url)
    soup = bs(result.text, 'html.parser')
    data =soup.find_all('li', class_='overout')
    overall_data += data
print(len(overall_data))
for i in range(5):
    url = f"https://idea.eseoul.go.kr/front/resultSuggest/list.do?searchCondition2=&searchCondition3=&searchCondition4=&sSuggest_divi=&sKeyword=&pageIndex={i}"
    result = requests.get(url)
    soup = bs(result.text, 'html.parser')
    data =soup.find_all('li', class_='overout')
    overall_data += data
print(len(overall_data))
data_list = []

for data in overall_data:
    temp = {
        "model": "visualize.ideaseoul",
        'fields' : {
            'title': [],
            'url': "https://idea.eseoul.go.kr" + data.find('a')['href'],
            'agency' : [],
            'pub_date': [],
            'field': [],
            'period': [],
            'status': [],
            'views': data.find('p', class_='user-txt').find('em').text,
            'content':[]
        }

    }

    url = temp['fields']['url']
    result = requests.get(url)
    soup = bs(result.text, 'html.parser')
    temp['fields']['title'] = soup.find('h4').text.strip()
    temp['fields']['pub_date'] = datetime.strptime(soup.find('span', class_='date').text.strip('.'), '%Y.%m.%d')
    temp['fields']['department'] = soup.find('span', string='정책분류').find_next_sibling('span').text
    temp['fields']['period'] = soup.find('p', class_='txt-term').text.strip().replace('\r', '').replace('\n', '').replace('\t', '')
    temp['fields']['state'] = soup.find('li', class_="on").text

    data_list.append(temp)

# JSON 파일로 저장
with open('idea_data.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(data_list, jsonfile, ensure_ascii=False, indent=4)