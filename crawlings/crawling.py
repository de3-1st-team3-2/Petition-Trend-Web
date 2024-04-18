import subprocess
import models
import os



subprocess.run(['python', 'crawlings\\crawling_idea.py'])
subprocess.run(['python', 'crawlings\\epeople_scrapping.py'])
subprocess.run(['python', 'crawlings\\petition_crwaling.py'])
subprocess.run(['python', 'crawlings\\crawling_cw24.py'])

def load_data(json_file):

    # loaddata 명령 실행
    subprocess.run(['python', 'manage.py', 'loaddata', json_file])



# 데이터 로드 함수 호출
load_data('crawling_ideaseoul.json')
load_data('crawling_epeople.json')
load_data('crawling_petition.json')
load_data('crawling_cw24.json')