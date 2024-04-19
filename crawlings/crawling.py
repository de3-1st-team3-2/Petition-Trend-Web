
import os

os.system('python crawlings//crawling//ideaseoul.py')
os.system('python crawlings//crawling//cw24.py')
os.system('python crawlings//crawling//epeople.py')
os.system('python crawlings//crawling//petition.py')


def load_data(json_file):

    # loaddata 명령 실행
    os.system('python manage.py loaddata '+ json_file)



# 데이터 로드 함수 호출
load_data('crawling_ideaseoul.json')
load_data('crawling_epeople.json')
load_data('crawling_petition.json')
<<<<<<< HEAD
load_data('crawling_cw24.json')
=======
load_data('crawling_cw24.json')
>>>>>>> e89249657016e6edd1c9fa4db2bf0d45ffe8db37
