import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from konlpy.tag import Hannanum
import json
import re
hannanum = Hannanum()
##### 데이터 파일의 경로를 여기서 지정해주세요 ########

# df_24[1]['date']#title
# df_T[1]['periods']#title
# df_E[2]#[0]
# df_C['날짜']#['제목']
# df_I['date']#['title]

site_name='상상대로 서울'
file_path='graph_png/'
df_I=pd.read_json('Ideaseoul.json')

data_date_I=[str(x) for x in df_I['date']]
data_word_I=[x for x in df_I['title']]

      
site_name='국민 신문고'
file_path='graph_png/'
df_E=pd.read_json('Epeople.json').values
df2_E=pd.read_json('Epeople2.json').values

data_date_E=np.append(df_E[2],df2_E[2])
data_word_E=np.append(df_E[0],df2_E[0])


site_name='국민동의 청원'
file_path='graph_png/'
df_C=pd.read_json('Congress.json')

data_date_C=df_C['날짜']
data_word_C=df_C['제목']
sort_C=sorted(zip(data_date_C,data_word_C))
data_date_C,data_word_C=zip(*sort_C)

site_name='청원 24'
file_path='graph_png/'
df_24=pd.read_json('CW24.json')
df_24=df_24['fields']

data_date_24=[(df_24[x]['date']) for x in range(len(df_24))]
data_word_24=[df_24[x]['title'] for x in range(len(df_24))]



site_name='국민 생각함'
file_path='graph_png/'
df_T=pd.read_json('Think.json').values#2차원 리스트[[데이터들],[데이터들]]
data_date_T=[]
data_word_T=[]
df2_T=df_T[0]
for x in range(1,len(df_T)):
    df2_T=np.append(df2_T,df_T[x])
df_T=df2_T#[데이터들]

for x in range(0,len(df_T)):
    data_date_T.append(df_T[x]['periods'].split(' ~ ')[0])
    data_word_T.append(df_T[x]['title'])

data_date_T2=[]
for x in range(len(data_date_T)):
    data_date_T2.append(float(data_date_T[x].split('.')[1]+'.'+data_date_T[x].split('.')[2]))

sort_T=sorted(zip(data_date_T2,data_date_T,data_word_T))
data_date_T2,data_date_T,data_word_T=zip(*sort_T)
    



########### 워드 data를 만들기 #########
def split_month(data_date,split_char):
    # try:
    period=[[]]
    y=data_date[0].split(split_char)[0]
    m=data_date[0].split(split_char)[1]
    period[0].append((f'{m}월')) 

    ycount=0
    
    for x in data_date:
        data_m = x.split(split_char)[1]
        data_y = x.split(split_char)[0]
        if data_m != m:
            m=data_m
            if data_y != y:
                period.append(f'{y}년')
                period.append([])
                
                y=data_y
                ycount+=2
            
            period[ycount].append(f'{data_m}월') 
  
    period.append(f'{data_y}년') 
    

            
            
# except:print(period)


    return period if period!=None else print('엥?')

#날짜 쪼개줌
month=[['months'],'year']

month_I=split_month(data_date_I,'-')
month_E=split_month(data_date_E,'-')
month_C=split_month(data_date_C,'-')
month_24=split_month(data_date_24,'-')
month_T=split_month(data_date_T,'.')
#달 기준으로 제목들 합쳐줌


def data_word(data_date,data_word,split_text):
    text=[]
    data={}
    data['title']=[]
    m=data_date[0].split(split_text)[1]
    for x in range(len(data_date)):
        # print(data_date[x])
        if data_date[x].split(split_text)[1] == m :
            text.append(data_word[x])
        else : #지금 나 이동했네?
            data['title'].append(' '.join(text))#이전 텍스트 합쳐서 넣어줌
            m=data_date[x].split(split_text)[1]#지금 날짜도 바꿔주고
            text=[]#다시 비워주고
            text.append(data_word[x])
    if text != []:        #다 돌았을떄 쌓인거 push해주고
        data['title'].append(' '.join(text))
        m=data_date[x].split(split_text)[1]
        text=[]
        text.append(data_word[x])
    
    return data['title']

text_24=data_word(data_date_24,data_word_24,'-')
text_E=data_word(data_date_E,data_word_E,'-')
text_C=data_word(data_date_C,data_word_C,'-')
text_I=data_word(data_date_I,data_word_I,'-')
text_T=data_word(data_date_T,data_word_T,'.')


def Count_word(text):
    counter=[]
    for i in range(len(text)):
        words=[]

        nouns=hannanum.nouns(text[i])
        words+=nouns
        
        counter.append(Counter(words))
    return counter
#단어 카운트 해줌
count_24=Count_word(text_24)
count_T=Count_word(text_T)
count_E=Count_word(text_E)
count_I=Count_word(text_I)
count_C=Count_word(text_C)
def data(count_):
    data={'word':[],'count':[]}
    for count in count_ :
        data['count'].append(list(count.values()))
        data['word'].append(list(count.keys()))

    return data
#데이터 형식에 맞춰 넣어줌
# data={'word':[],'count':[]}

data_24=data(count_24)
data_T=data(count_T)
data_C=data(count_C)
data_E=data(count_E)
data_I=data(count_I)
word_site_monthly_data=[]
len(data_T['word'][0])
#개별로 세서 dict에 추가
def add_word_dict(site_name,data_,month_):
    
    num=0
    next=0
    for x in range(0,len(month_)//2):#연
        num+=1
        month=x*2
        year=x*2+1
        for m in month_[month]:#월
            num+=1
            for temp in range(len(data_['word'][next])):
                data={}
                data['word']=data_['word'][next][temp]
                data['cnt']=data_['count'][next][temp]
                data['source']=site_name
                data['date']=f'{month_[year][0:4]}-{m[0:2]}-01'
                data_form={'model':'visualization_data_store.MonthlySitewiseWordCount',
                        'fields':data}
                word_site_monthly_data.append(data_form)
            next+=1
# #리스트로 dict에 추가
# def add_word_dict(site_name,data_,month_):
    
#     num=0
#     next=0#
    
#     for x in range(0,len(month_)//2):#연
#         num+=1
#         month=x*2
#         year=x*2+1
#         for m in month_[month]:#월
#             num+=1
            
#             data={}
#             data['word']=data_['word'][next]
#             data['cnt']=data_['count'][next]
#             data['source']=site_name
#             data['date']=f'{month_[year][0:4]}-{m[0:2]}-01'
#             data_form={'model':'visualization_data_store.MonthlySitewiseWordCount',
#                        'fields':data}
#             word_site_monthly_data.append(data_form)
##dict에 추가 

word_site_monthly_data=[]
add_word_dict('sub-think',data_T,month_T)
add_word_dict('congress',data_C,month_C)
add_word_dict('epeople',data_E,month_E)
add_word_dict('ideaseoul',data_I,month_I)
add_word_dict('cw24',data_24,month_24)
### save
with open("./data/MonthlyWordcount_data.json", "w", encoding='utf-8') as f:
    json.dump(word_site_monthly_data, f, ensure_ascii=False, indent=4)
# ####### 월 청원 수 # ########
def monthly_num_count(data_date,splittype):
    monthly_num=[]
    for month in range(1,13):
        data=[x for x in data_date if (x.split(splittype)[0] == '2022')&( int(x.split(splittype)[1])== month)]
        num = len(data)
        monthly_num.append(num)

    for month in range(1,13):
        data=[x for x in data_date if (x.split(splittype)[0] == '2023')&( int(x.split(splittype)[1])== month)]
        num = len(data)
        monthly_num.append(num)

    for month in range(1,5):
        data=[x for x in data_date if (x.split(splittype)[0] == '2024')&( int(x.split(splittype)[1])== month)]
        num = len(data)
        monthly_num.append(num)

    return monthly_num

monthly_num_E=monthly_num_count(data_date_E,'-')
monthly_num_24=monthly_num_count(data_date_24,'-')
monthly_num_I=monthly_num_count(data_date_I,'-')
monthly_num_C=monthly_num_count(data_date_C,'-')
monthly_num_T=monthly_num_count(data_date_T,'.')
MonthlyNum_data=[]
year=2022
month=1
month_=['00','01','02','03','04','05','06','07','08','09','10','11','12']
for x in range(len(monthly_num_24)):
    data={'date':f'{year}-{month_[month]}-01',
          'epeople':monthly_num_I[x],
          'congress':monthly_num_C[x],
          'cw24':monthly_num_24[x],
          'ideaseoul':monthly_num_I[x],
          'subthink':monthly_num_T[x]}
    data_form={
        'model':'visualization_data_store.MonthlySitewiseWrites',
        'fields':data
    }
    MonthlyNum_data.append(data_form)
    month+=1
    if month>12:
        month=1
        year+=1
    
with open("./data/MonthlyNum_data.json", "w", encoding='utf-8') as f:
    json.dump(MonthlyNum_data, f, ensure_ascii=False, indent=4)