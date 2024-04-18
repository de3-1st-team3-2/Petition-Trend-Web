import os
import subprocess
from visualize.models import Epeople, Congress, Ideaseoul 
subprocess.run(['python', 'crawling\\crawling_idea.py'])
subprocess.run(['python', 'crawling\\epeople_scrapping.py'])
subprocess.run(['python', 'crawling\\petition_crwaling.py'])

def upload_json_to_database(json_file, model):
    with open(json_file, 'r') as f:
        data = json.load(f)
        for item in data:
            obj = model(**item)
            obj.save()

# JSON 파일 경로
idea_json_file = 'crawling/idea.json'
epeople_json_file = 'crawling/epeople.json'
petition_json_file = 'crawling/petition.json'

# 모델과 JSON 파일 매핑
model_json_mapping = {
    Epeople: idea_json_file,
    Congress: epeople_json_file,
    Ideaseoul: petition_json_file
}

# 데이터베이스에 업로드
for model, json_file in model_json_mapping.items():
    upload_json_to_database(json_file, model)
