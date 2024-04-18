import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}
# 동의 진행중인 청원들에 대해서는 pageIndex 1~4까지
# https://petitions.assembly.go.kr/api/petits?pageIndex=1&recordCountPerPage=8&sort=AGRE_CO-&searchCondition=&searchKeyword=&petitRealmCode=&sttusCode=AGRE_PROGRS,CMIT_FRWRD,PETIT_FORMATN&proceedAt=proceed&beginDate=&endDate=&ageCd=
# 동의 완료 url pageIndex 1~120
# 아래 url 마지막의 beginDate와 endDate를 조절하면 원하는 기간내의 게시물들을 검색가능, 기본상태는 2년
# https://petitions.assembly.go.kr/api/petits?pageIndex=1&recordCountPerPage=8&sort=AGRE_END_DE-&searchCondition=sj&searchKeyword=&petitRealmCode=&sttusCode=PETIT_FORMATN,CMIT_FRWRD,PETIT_END&resultCode=BFE_OTHBC_WTHDRAW,PROGRS_WTHDRAW,PETIT_UNACPT,APPRVL_END_DSUSE,ETC_TRNSF&notInColumn=RESULT_CODE&beginDate=20220416&endDate=20240416&ageCd=


all_data = []

# 동의진행 청원 가져오기
for i in range(1, 5):
  url = f"https://petitions.assembly.go.kr/api/petits?pageIndex={i}&recordCountPerPage=8&sort=AGRE_CO-&searchCondition=&searchKeyword=&petitRealmCode=&sttusCode=AGRE_PROGRS,CMIT_FRWRD,PETIT_FORMATN&proceedAt=proceed&beginDate=&endDate=&ageCd="
  res = requests.get(url, headers=headers)
  data = res.json()
  all_data += data


# 동의종료 청원 가져오기
for i in range(1, 121):
  url = f"https://petitions.assembly.go.kr/api/petits?pageIndex={i}&recordCountPerPage=8&sort=AGRE_END_DE-&searchCondition=sj&searchKeyword=&petitRealmCode=&sttusCode=PETIT_FORMATN,CMIT_FRWRD,PETIT_END&resultCode=BFE_OTHBC_WTHDRAW,PROGRS_WTHDRAW,PETIT_UNACPT,APPRVL_END_DSUSE,ETC_TRNSF&notInColumn=RESULT_CODE&beginDate=20220416&endDate=20240416&ageCd="
  res = requests.get(url, headers=headers)
  data = res.json()
  all_data += data

# 가져온 json 데이터에서 필요한 항목만 뽑기
DB = []

for da in all_data:
  temp = {
      'title' : da['petitSj'],
      'pub_date' : da['agreBeginDe'][:10],
      'category' : da['petitRealmNm'],
      'rating' : da['agreCo'],
      'status' : da['resultCodeNm'],
      'url' : 'https://petitions.assembly.go.kr/proceed/onGoingAll/' + da['petitId'],
      'agency' : da['jrsdCmitNm']
  }
  DB.append(temp)

# json 파일로 저장
import json

new_list = []

for data in DB:
  new_data = {"model": "visualize.congress"}
  new_data["fields"] = {}
  new_data["fields"] = data
  new_list.append(new_data)

with open("./crawling_petition.json", "w", encoding='utf-8') as f:
    json.dump(new_list, f, ensure_ascii=False, indent=2)