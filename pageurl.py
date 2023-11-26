import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

# Chrome 브라우저 실행
driver = webdriver.Chrome()
driver.get("https://young.busan.go.kr/policySupport/list.nm?menuCd=12")  # 웹페이지 열기

current_page = 0  # 시작 페이지
data_list = []  # 빈 리스트 생성

while True:
    # 실행할 자바스크립트 함수 호출
    javascript_code = f"fn_page({current_page});"
    driver.execute_script(javascript_code)  # 자바스크립트 코드 실행
    driver.implicitly_wait(5)  # 브라우저 창 열어둘 시간 대기 (5초)

    # 현재 페이지 소스 가져오기
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')  # BeautifulSoup를 사용하여 HTML 파싱

    policy_div = soup.find('div', class_='photo_type2')  # 게시글 URL div 불러오기

    
    if policy_div:
        ul_element = policy_div.find('ul')
        base_url = 'https://young.busan.go.kr/'

        if ul_element:
            li_elements = ul_element.find_all('li') # 현 페이지 게시글 가져오기

            for li in li_elements:
                spt_state_element = li.find('div', class_='spt_state end')  # 모집 완료 게시글 필터링

                if not spt_state_element:
                    div = li.find('div', class_='photo2_tit')
                    link = div.find('a')
                    href = base_url + link.get('href')[1:]  # 게시글 URL
                    print(href)
                    
                    response2 = requests.get(href)  # 게시글 URL 요청
                    soup2 = BeautifulSoup(response2.text, "html.parser")  # 게시글 내용 파싱
                    
                    # 현 게시글에 사용할 디렉토리
                    row_data = {'정책이름': None, '신청기간': None, '진행일정': None, '지원대상': None, '담당기관': None,
                                        '문의': None, '홈페이지': None, '상세정보': None}

                    policy_name_div = soup2.find('div', class_='dt_tit')  # 게시글 제목 div 불러오기
                    row_data['정책이름'] =  policy_name_div.get_text(strip=True) if policy_name_div else None # 제목 추출
                    
                    summary_div = soup2.find("div", class_="dt_list") # 간략 설명 div 불러오기

                    #간략 설명에 있는 데이터 불러오기
                    if summary_div:
                        dl_element = summary_div.find('dl')

                        if dl_element:
                            dt_elements = dl_element.find_all('dt') # 설명 key값
                            dd_elements = dl_element.find_all('dd') # 설명 value값

                            # 디렉토리 값 설정
                            for dt, dd in zip(dt_elements, dd_elements):
                                key = dt.get_text(strip=True)
                                if key == '조회수' :
                                    pass
                                value = dd.get_text(strip=True)

                                if key in row_data:
                                    row_data[key] = value
                    
                    explain_div = soup2.find('div', class_='text')  # 게시글 상세살명 div 불러오기
                    row_data['상세정보'] = explain_div.get_text(strip=True) if explain_div else None # 상세설명 추출
                        
                    # 완성된 디렉토리 추가
                    data_list.append(row_data)
                    
    # 다음페이지 있는지 확인후 종료 코드
    next_page_element = soup.find('span', class_='p next')  # 다음 페이지가 있는지 확인
    if next_page_element:
        next_page_link = next_page_element.find('a')
        if next_page_link:
            next_page_href = next_page_link.get('href')

            next_page_number_match = re.search(r'\((\d+)\)', next_page_href)
            if next_page_number_match:
                next_page_number = int(next_page_number_match.group(1))

                if current_page > next_page_number:
                    print(f"현재 페이지({current_page})가 다음 페이지 번호({next_page_number})보다 큽니다. 종료합니다.")
                    driver.quit()
                    break
            else:
                print("다음 페이지 링크의 페이지 번호를 찾을 수 없음")

        else:
            print("다음 페이지 링크를 찾을 수 없음")

    current_page += 1

df = pd.DataFrame(data_list)
df.to_excel('C:\\Users\\Administrator\\Downloads\\software_study\\Software_proj\\output.xlsx', index=False)

driver.quit()  # 웹 드라이버 종료
