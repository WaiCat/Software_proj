import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

# Chrome 브라우저 실행
driver = webdriver.Chrome()
driver.get("https://young.busan.go.kr/index.nm")  # 웹페이지 열기

  # 빈 리스트 생성

url = "https://young.busan.go.kr"

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')  # BeautifulSoup를 사용하여 HTML 파싱

menu_li = soup.find('li', id='menu02')  # menu02의 li 읽어오기

i=0
if menu_li:
    li_tags = menu_li.find_all('li')

    # 각 li 태그에서 href 속성 값을 가져옴
    for li_tag in li_tags:
        # li 태그 안에 a 태그가 있는 경우
        a_tag = li_tag.find('a')
        if a_tag:
            href = url + a_tag.get('href')
            print(href)
            data_list = []
            round_box_tit = {}
            response2 = requests.get(href)  # 게시글 URL 요청
            soup2 = BeautifulSoup(response2.text, "html.parser")  # 게시글 내용 파싱
            
            tit_tags = soup2.find('div', class_="round_box_tit")
            if tit_tags:
                key = tit_tags.get_text(strip=True)
            else:
                continue
            txt_tags = soup2.find('div', class_="round_box_txt")
            if txt_tags:
                value = txt_tags.get_text(strip=True)
            else:
                continue

            # 첫 번째 span을 key, 두 번째 span을 value로 사용하여 딕셔너리에 저장
            
            round_box_tit[key] = value
            
            section_tit_divs = soup2.find_all('div', class_="section_tit")
            arrow_list_divs = soup2.find_all('div', class_="arrow_list")
            
            for section_tit_div, arrow_list_div in zip(section_tit_divs, arrow_list_divs):
                key = section_tit_div.get_text(strip=True)
                value = arrow_list_div.get_text(strip=True)
                round_box_tit[key] = value
                
            part_boxs = soup2.find_all('div', class_="part_box")
            part_details = soup2.find_all('div', class_="part_detail")
            
            for part_box, part_detail in zip(part_boxs, part_details):
                key = part_box.get_text(strip=True)
                value = part_detail.get_text(strip=True)
                round_box_tit[key] = value
                
            data_list.append(round_box_tit)
            
            df = pd.DataFrame(data_list)
            file_name = f'C:\\Users\\Administrator\\Downloads\\software_study\\Software_proj\\life\\life_{i}.xlsx'
            i+=1
            # DataFrame을 현재 파일 이름으로 저장
            df.to_excel(file_name, index=False)

driver.quit()  # 웹 드라이버 종료