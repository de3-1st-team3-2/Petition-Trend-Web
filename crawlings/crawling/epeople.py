import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import time

def extract_epeople_posts(driver):
    """
    driver는 국민 신문고의 공개 제안 페이지가 띄워져 있어야합니다.
    """
    base_view_url = "https://www.epeople.go.kr/nep/prpsl/opnPrpl/opnpblPrpslView.npaid"
    
    total_datas = {}
    columns = ["번호", "제목", "처리 기관", "신청일", "추진상황", "조회"]
    table = driver.find_element(By.CLASS_NAME, "tbl.default.brd1").find_elements(By.TAG_NAME, "tr")
    for row_elem in table:
        elems = row_elem.find_elements(By.TAG_NAME, "td")
        if len(elems) == len(columns):
            a_tags = row_elem.find_elements(By.TAG_NAME, "a")
            onclick_txt = a_tags[0].get_attribute("onclick").split("'")
            prplRqstNo, instRcptSn = onclick_txt[1], onclick_txt[-2]
            elem_url = base_view_url + f"?prplRqstNo={prplRqstNo}&instRcptSn={instRcptSn}"
            col_dict = {}
            for col, elem in zip(columns, elems):
                if col != '번호':
                    col_dict[col] = elem.text
            total_datas[elem_url] = col_dict
    return total_datas

def set_search_period(driver, start_date, end_date):
    """
    특정 검색 구간으로 검색 범위를 설정해줍니다.
    Parameters
        driver: 국민 신문고의 공개 제안 페이지가 띄워져 있어야합니다.
        start_date: datetime.datetime 객체이어야 합니다.
        end_date: datetime.datetime 객체이어야 합니다.
    """
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    print(f"search period: \n\
          start: {start_date_str} \t end: {end_date_str}")
    start_date_input = driver.find_element(By.ID, "rqstStDt")
    end_date_input = driver.find_element(By.ID, "rqstEndDt")

    ActionChains(driver).send_keys_to_element(start_date_input, start_date_str).perform()
    ActionChains(driver).send_keys_to_element(end_date_input, end_date_str).perform()

    date_search_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn.black"))
    )
    ActionChains(driver).click(date_search_btn).perform()
    
def find_last_page_num(driver):
    page_lists = driver.find_element(By.CLASS_NAME, "page_list").find_elements(By.TAG_NAME, "a")
    for elem in page_lists[::-1]:
        if len(elem.text) > 0:
            return int(elem.text)
    return 1

def epeople_list_crawling(start_date, end_date):
    """
    start_date부터 end_date까지의 국민신문고 공개 제안 데이터의 리스팅 되어있는 데이터를 크롤링합니다.
    상세 데이터는 나중에 다른 함수로 처리하게 될 예정입니다.

    parameter
        start_date: datetime.datetime 객체이어야 합니다.
        end_date: datetime.datetime 객체이어야 합니다.

    return
        total_data_dict: 각 게시물 페이지 링크를 key로 하며 
            key: 각 게시물 페이지 링크
            value: {"제목", "처리 기관", "신청일", "추진상황", "조회"}를 key로 하는 dict
    """

    target_url = "https://www.epeople.go.kr/nep/prpsl/opnPrpl/opnpblPrpslList.npaid"
    total_data_dict = {}

    with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
        driver.get(target_url)
        driver.implicitly_wait(10)

        set_search_period(driver, start_date, end_date)
        time.sleep(0.1)

        last_page = find_last_page_num(driver)
        for _ in tqdm(range(0, last_page)):
            new_total_data_dict = extract_epeople_posts(driver)
            for k, v in new_total_data_dict.items():
                total_data_dict[k] = v

            next_page_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "nep_p_next"))
            )
            ActionChains(driver).click(next_page_btn).perform()
            time.sleep(0.1)
        
    return total_data_dict

def clean_text(text):
    """
        개행문자를 제거해주는 함수.
    """
    return text.replace('\t', '').replace('\r', '').replace('\n', '')

def reply_crawling(driver, target_url):
    """
    국민 신문고의 target_url의 댓글 내역을 크롤링하는 함수.

    parameter
        driver: webdriver.Chrome(service=Service(ChromeDriverManager().install()))로
                생성된 크롬 드라이버
        target_url: 국민 신문고의 특정 제안의 url

    return
        total_reply_dict: 해당 글의 모든 댓글의 정보를 크롤링한 dict 객체
                {댓글 수, 댓글}로 구성되며
                각 댓글마다 {내용, 추천, 비추천, 대댓글수, 대댓글}로 구성되며
                대댓글의 경우 {내용, 추천, 비추천}으로 구성됨
    """
    driver.get(target_url)
    driver.implicitly_wait(20)
    time.sleep(0.1)

    total_reply_dict = {}
    try:
        total_reply_dict["댓글 수"] = int(driver.find_element(By.ID, "replyTotalCnt").text)
    except Exception as e:
        print(e)
        time.sleep(0.1)
        
    replies = driver.find_element(By.ID, "replyListUl").find_elements(By.TAG_NAME, "li")
    reply_dict_lst = []
    for reply in replies:
        reply_dict = {}
        reply_dict['내용'] = reply.find_element(By.CLASS_NAME, "reply_conA").text
        reply_dict['추천'] = int(reply.find_element(By.CLASS_NAME, "stBtn.like").text)
        reply_dict['비추천'] = int(reply.find_element(By.CLASS_NAME, "stBtn.like").text)
        reply_dict['대댓글수'] = int(reply.find_element(By.CLASS_NAME, "rereply").text.replace("답글 ", ""))
        reply_dict['대댓글'] = []

        if reply_dict['대댓글수'] > 0:
            button = WebDriverWait(reply, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "rereply"))
            )
            ActionChains(driver).click(button).perform()
            time.sleep(0.1)

            reReplies = reply.find_element(By.CLASS_NAME, f"re_reply").find_elements(By.TAG_NAME, "li")
            for reReply in reReplies:
                reReply_dict = {}
                reReply_dict['내용'] = reReply.find_element(By.CLASS_NAME, "reply_conA").text
                reReply_dict['추천'] = reReply.find_element(By.CLASS_NAME, "stBtn.like").text
                reReply_dict['비추천'] = reReply.find_element(By.CLASS_NAME, "stBtn.hate").text
                
                reply_dict['대댓글'].append(reReply_dict)
        reply_dict_lst.append(reply_dict)
    total_reply_dict["댓글"] = reply_dict_lst
    return total_reply_dict

def epeople_crawling(start_date, end_date):
    """
    국민 신문고를 특정 기간에 대해서 크롤링하는 함수
    parameter
        start_date: datetime.datetime 객체이어야 합니다.
        end_date: datetime.datetime 객체이어야 합니다.

    return:
        crawling_result_dict: 전체 크롤링을 수행 완료한 dict 객체
    """
    # list 정보 수집
    crawling_result_dict = epeople_list_crawling(start_date, end_date)
    print(f"len: {len(crawling_result_dict)}")

    # 각 글의 detail 정보 수집
    for k in tqdm(crawling_result_dict.keys()):
        get_result = requests.get(k)
        soup = bs(get_result.text, "html.parser")

        # 별점
        rating = clean_text(soup.find("span", "starCnt").text)
        if rating != '-':
            rating = rating.strip('()')
        crawling_result_dict[k]['별점'] = rating
        
        # 분야와 추진 상황
        table_datas = soup.find_all("div", "cellBig")
        field = clean_text(table_datas[1].text)
        current_status = clean_text(table_datas[-1].text)
        crawling_result_dict[k]['분야'] = field
        crawling_result_dict[k]['추진 상황'] = current_status

        # 내용
        content = soup.find("div", "b_content")
        cleaned_content = ""
        for item_div in content.find_all('div', class_='b_conItem'):
            title = item_div.find('strong', class_='b_conTit').get_text(strip=True)
            content = item_div.find('div', class_='b_cont').get_text(strip=True)
            content = content.replace('<br>', '\n').replace('</br>', '')
            cleaned_content += f"{title}\n {content}\n\n"

        cleaned_content = cleaned_content.strip()
        crawling_result_dict[k]['내용'] = cleaned_content
        time.sleep(0.5)

    # 각 글의 댓글 정보 수집
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # for target_url in tqdm(crawling_result_dict.keys()):
    #     total_reply_dict = reply_crawling(driver, target_url)
    #     crawling_result_dict[target_url]['댓글정보'] = total_reply_dict

    # driver.quit()
    return crawling_result_dict


if __name__ == "__main__":
    end_date = datetime(2024, 4, 13)
    start_date = datetime(2024, 4, 12)

    crawling_result_dict = epeople_crawling(start_date, end_date)
    
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    

    total_list = []
    for k, v in crawling_result_dict.items():
        new_dict = {"model": "visualize.epeople"}
        new_dict['fields'] = {}
        new_dict['fields']['url'] = k
        new_dict['fields']['title'] = v['제목']
        new_dict['fields']['agency'] = v['처리 기관']
        new_dict['fields']['pub_date'] = v['신청일']
        new_dict['fields']['status'] = v['추진상황']
        new_dict['fields']['views'] = int(v['조회'])
        new_dict['fields']['rating'] = float(v['별점']) if v['별점'] != '-' else 0
        new_dict['fields']['field'] = v['분야']
        new_dict['fields']['content'] = v['내용']
        total_list.append(new_dict)
    import json
    with open(f"./crawling_epeople.json", "w", encoding='utf-8') as f:
        json.dump(total_list, f, ensure_ascii=False, indent=4)