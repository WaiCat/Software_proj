import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


base_url = 'https://young.busan.go.kr/policySupport/list.nm?menuCd=12&page={}'

# ChromeOptions를 사용하여 실행 경로 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')  # 특정 환경에서 필요한 경우

# Chrome 드라이버 경로 설정 (본인의 환경에 맞게 수정)
chrome_driver_path = '/path/to/chromedriver'

# 웹 드라이버 생성
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# 페이지 로드 대기 시간 (초)
wait_time = 10
wait = WebDriverWait(driver, wait_time)

# 페이지를 열고 JavaScript 함수 실행
page_number = 2
url = "https://young.busan.go.kr/policySupport/list.nm?menuCd=12"
driver.get(url)

# JavaScript 함수 실행
javascript_function = f"fn_page({page_number})"
driver.execute_script(javascript_function)

# 페이지가 로드될 때까지 대기
try:
    element_present = EC.presence_of_element_located((By.ID, '여러분이 기다리는 요소의 ID'))
    wait.until(element_present)
except TimeoutException:
    print("타임아웃: 페이지가 로드되지 않았습니다.")


        
# def get_page_url(page_number):
#     return base_url.format(page_number)

# # 시작 페이지
# current_page = 1

# while True:
#     # 현재 페이지에 해당하는 URL 생성
#     url = get_page_url(current_page)

#     # 웹 페이지의 내용을 가져오기
#     response = requests.get(url)

#     # HTTP 요청이 성공한 경우
#     if response.status_code == 200:
#         # BeautifulSoup를 사용하여 HTML 파싱
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # 페이지 처리 코드

#         # <div> 요소 중 class가 "photo_type2"인 것을 찾기
#         specific_div = soup.find('div', class_='photo_type2')

#         if specific_div:
#             # <li> 요소 내부의 <ul> 요소 찾기
#             ul_element = specific_div.find('ul')
#             ur = 'https://young.busan.go.kr/'

#             if ul_element:
#                 # <li> 요소들을 모두 찾기
#                 li_elements = ul_element.find_all('li')

#                 for li in li_elements:
#                     div = li.find('div', class_='photo2_tit')
#                     link = div.find('a')
#                     href = link.get('href')

#                     href = href[1:]
#                     href = ur + href
#                     print(href)

#                     response1 = requests.get(href)  # URL 요청

#                     # 2. 웹 페이지 내용 파싱
#                     soup1 = BeautifulSoup(response1.text, "html.parser")

#                     # 3. 원하는 텍스트 추출
#                     element = soup1.find("div", class_="detail_page ct")
#                     if element:
#                         text = element.text.replace("\n", "")  # 토큰 줄이기 위한 개행 제거
#                         # print(text)
#                     else:
#                         print("No 'sub_content' found on the page")

#         # 다음 페이지로 이동
#         current_page += 1

#     else:
#         print(f'HTTP 요청에 실패했습니다. 상태 코드: {response.status_code}')
#         break
