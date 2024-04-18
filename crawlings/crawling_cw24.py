# 청원 24
from bs4 import BeautifulSoup as bs
import requests
import re
from datetime import datetime,timedelta
import json

"""
class CW24(models.Model):
    title = models.CharField(max_length=50, verbose_name="제목")
    url = models.CharField(max_length=200, verbose_name="URL")
    agency = models.CharField(max_length=10, verbose_name="처리기관")
    pub_date = models.DateTimeField(verbose_name="작성일")
    start_date = models.DateTimeField(verbose_name="시작일")
    end_date = models.DateTimeField(verbose_name="종료일")
    status = models.CharField(null = True, max_length=20, verbose_name="추진상황")
    views = models.IntegerField(null = True, verbose_name="조회수")
    content = models.CharField(null = True, max_length=300, verbose_name="내용")
    comment_num = models.IntegerField(null = True, verbose_name="댓글수")
    result = models.CharField(max_length=300, null = True, verbose_name="처리결과")
"""
# 순회
### requests
header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}


res=requests.get("https://cheongwon.go.kr/portal/petition/open/view",headers=header)
soup=bs(res.text,"html.parser")

petition_dict={"title":[],
               "url":[],
               "content":[],#detail=>content
               "pub_date":[],#pub_date
              #  "period":[],#start/end
              "start_date":[],
              "end_date":[],
               "status":[],#status
               "views":[],
               "comment_num":[],
               "result":[],
               "agency":[],
            #    "agency_detail":[],
              }
#끝페이지 읽어오기
final_index=soup.find('a','cs-paging__last').get('href')
final_index=int(final_index.split("=")[-1])

#스크래핑
#page_index번쨰 페이지  post_count번째 글
#page_index*9+post_count-1번째 글
#page_index*9+post_count-2 가 dict 위치
for page_index in range(1, 3):
#     print (page_index,'페이지')
    res=requests.get(f"https://cheongwon.go.kr/portal/petition/open/view?pageIndex={page_index}&searchType=1&searchKeyword=&type=list",headers=header)
    soup=bs(res.text,"html.parser")
    post_count=0

    #게시판에서 얻을 수 있는 정보들
    #url
    #period
    #pub_date
    #title
    #agency


    ###각 게시글들 url구하기(url)
    #https://cheongwon.go.kr/portal/petition/open/viewdetail/{추출한 속성}
    thispage_posturl=[]#해당 페이지 게시글 탐색시 사용할 url리스트
    a_tag=soup.find_all("a", onclick=True)
    for post in a_tag : #a_tag중 게시글 태그만
        if post.get("style") == "cursor: pointer;":
            post=post.get("onclick").split('\'')[1]
            url="https://cheongwon.go.kr/portal/petition/open/viewdetail/"+post
            # petition_dict["post"].append(post)
            petition_dict["url"].append(url)
            thispage_posturl.append(url)




    ###청원 의견 수렴(동의)기간 구하기(period)
    ###청원 신청 날짜 구하기 == 의견수렴 날짜 -15(pub_date)
    period_tags=soup.find_all("span","date")
    for period in period_tags:
        #날짜만 구함
        period=period.get_text()
        period=period.split(':')[1].strip()
        #[시작 날짜, 종료 날짜]
        period = period.split('~')
        #형식 바꿔서 넣을 period_delta
        period_delta=[]
        #datetime형식으로 바꾸기 
        period_delta.append(datetime.strptime(period[0],'%Y.%m.%d'))
        period_delta.append(datetime.strptime(period[1],'%Y.%m.%d'))
        #datetime형식으로 넣기 싫으면 period넣으면됨
        # petition_dict["period"].append(period_delta)
        petition_dict["start_date"].append(period_delta[0].isoformat())
        petition_dict["end_date"].append(period_delta[1].isoformat())

        pub_date=period_delta[0]-timedelta(days=15)
        #datetime형식으로 넣기 싫으면 아래 코드 주석 처리 해제
        #date=date.strftime("%Y.%m.%d")
        petition_dict["pub_date"].append(pub_date.isoformat())

    ###청원 제목 구하기(title)
    title_tags=soup.find_all("span","subject")
    for title in title_tags:
        petition_dict["title"].append( title.get("title"))

    ###담당부서 구하기(agency)
    agency_tags=soup.find_all("span","category")
    for agency in agency_tags:
        petition_dict["agency"].append(agency.text)

    #게시글에서 추가로 얻을 수 있는 정보들
    #content
    #result
    #status
    #view
    #agency_detail
    #comment_num     근데 이거 반대는 없지만 댓글로 반대의견 표현하는 경우도 있어서 고민중... 일단 comment num만 받음
#     time.sleep(2)
    
    for url in thispage_posturl: #해당 페이지의 게시글 url이 들어있음
            post_count+=1
#             print(post_count)
            res_=requests.get(url,headers=header)
            soup_=bs(res_.text,"html.parser")
            exist=(soup_.find("div").get("class")==['wrap'])
            if exist : ##삭제되지 않았을떄
                ###청원 내용 구하기(content)
                content=soup_.find("div","pet-doc__cont")
                content=content.text   
                #\n이랑 쓸데없는 공백 &nbsp처리
                content=cleaned_text = re.sub(r'\s+', ' ', content)

                petition_dict["content"].append(content)

                ### 처리 결과 구하기  (result)
                result=soup_.find("div","pet-doc__result")
                if result : #답변이 존재할 때
                    result=result.text
                    #\n이랑 쓸데없는 공백 &nbsp처리
                    result = re.sub(r'\s+', ' ', result)
                    petition_dict["result"].append(result)
                else : #답변이 없을 때>None삽입
                    petition_dict["result"].append(None)

                ### 상태 구하기(status)
                status=soup_.find("ul","process").find('li','on')
                status=status.text
                petition_dict["status"].append(status)

                ### 댓글 숫자 구하기(comment_num)
                comment_num=soup_.find("div","total").find('span','blue')
                comment_num=comment_num.text
                petition_dict["comment_num"].append(comment_num)

                ###조회수 구하기 (views)
                views = soup_.find("div","link").find("div")
                views=views.text.replace('조회 수 ','').strip()
                petition_dict['views'].append(views)

                # ### 세부담당 부서 구하기(agency_detail)
                # agency_detail=soup_.find("div","category").find("span")
                # agency_detail=agency_detail.text.replace("처리기관: ","").strip()
                # petition_dict['agency_detail'].append(agency_detail)
    #             time.sleep(2)
            else:
                petition_dict["content"].append(None)
                # petition_dict['agency_detail'].append(None)
                petition_dict['views'].append(None)
                petition_dict["result"].append(None)
                petition_dict["status"].append(None)
                petition_dict["comment_num"].append(None)
                pass


# # 전체 데이터 개수 확인
# data_num = {key: len(value) for key, value in petition_dict.items()}
# data_num
##dict 형식 변환,모델 등록
data_num = len(petition_dict['title'])
keys=list(petition_dict.keys())
CW24=[]

for data_num_ in range(data_num):
    data={"model":"visualize.CW24",
          "fields":{}}
    
    for key in keys :
        if key=='start_date' or key=='end_date':

            temp=petition_dict[key][data_num_].split('T')[0]
            data["fields"][key]=temp
            
        else:
            data["fields"][key]=petition_dict[key][data_num_]
    CW24.append(data)
#json파일로 dict 저장

with open("./CW24_scrapping.json", "w", encoding='utf-8') as f:
    json.dump(CW24, f, ensure_ascii=False, indent=4)
# with open("./CW24_scrapping.json", "w", encoding='utf-8') as f:
#     json.dump(CW24, f, ensure_ascii=False, indent=4)