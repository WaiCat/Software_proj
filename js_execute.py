import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# Chrome 브라우저를 실행
driver = webdriver.Chrome()

# 웹페이지 열기
driver.get("https://young.busan.go.kr/policySupport/list.nm?menuCd=12")

# 시작 페이지
current_page = 0

for _ in range(10):
    # 실행할 자바스크립트 함수 호출
    javascript_code = f"fn_page({current_page});"

    # 자바스크립트 코드 실행
    driver.execute_script(javascript_code)

    # 브라우저 창을 열어둘 시간을 주기 위해 대기 (여기서는 5초로 설정)
    driver.implicitly_wait(5)

    # 현재 페이지 소스 가져오기
    page_source = driver.page_source
    print(page_source)

    current_page += 1
    

# 웹 드라이버 종료
driver.quit()
