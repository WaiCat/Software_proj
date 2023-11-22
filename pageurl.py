import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# Chrome 브라우저를 실행
driver = webdriver.Chrome()

# 웹페이지 열기
driver.get("https://young.busan.go.kr/policySupport/list.nm?menuCd=12")

# 시작 페이지4
current_page = 0

while True:
    # 실행할 자바스크립트 함수 호출
    javascript_code = f"fn_page({current_page});"

    # 자바스크립트 코드 실행
    driver.execute_script(javascript_code)

    # 브라우저 창을 열어둘 시간을 주기 위해 대기 (여기서는 5초로 설정)
    driver.implicitly_wait(5)

    # 현재 페이지 소스 가져오기
    page_source = driver.page_source

    # BeautifulSoup를 사용하여 HTML 파싱
    soup = BeautifulSoup(page_source, 'html.parser')

    # 페이지 처리 코드
    specific_div = soup.find('div', class_='photo_type2')

    if specific_div:
        ul_element = specific_div.find('ul')
        base_url = 'https://young.busan.go.kr/'

        if ul_element:
            li_elements = ul_element.find_all('li')

            for li in li_elements:
                # 웹 페이지 내용 파싱
                # 모집 완료 게시글 필터링
                spt_state_element = li.find('div', class_='spt_state end')

                if spt_state_element is None:
                    div = li.find('div', class_='photo2_tit')
                    link = div.find('a')
                    href = link.get('href')

                    # 정규표현식을 사용하여 href에서 숫자 추출
                    page_number_match = re.search(r'\((\d+)\)', href)
                    if page_number_match:
                        page_number = int(page_number_match.group(1))

                        # current_page와 추출한 페이지 번호 비교
                        if current_page == page_number:
                            print(f"현재 페이지: {current_page}, href의 페이지 번호: {page_number}")
                        elif current_page > page_number:
                            print(f"현재 페이지({current_page})가 href의 페이지 번호({page_number})보다 큽니다. 종료합니다.")
                            driver.quit()
                            exit()

                    href = base_url + href[1:]

                    print(href)

                    response2 = requests.get(href)  # URL 요청

                    # 웹 페이지 내용 파싱
                    soup2 = BeautifulSoup(response2.text, "html.parser")

                    # 원하는 텍스트 추출
                    # element = soup2.find("div", class_="detail_page ct")
                    element = soup2.find("div", class_="dt_list")
                    if element:
                        text = element.text.replace("\n", "")  # 토큰 줄이기 위한 개행 제거
                        print(text)
                    else:
                        print("페이지에서 'sub_content'를 찾을 수 없음")

    # 다음 페이지가 있는지 확인

    # span 태그의 class="p next"의 하위인 a태그의 href 값 가져오기
    next_page_element = soup.find('span', class_='p next')
    if next_page_element:
        next_page_link = next_page_element.find('a')
        if next_page_link:
            next_page_href = next_page_link.get('href')

            # 정규표현식을 사용하여 href에서 숫자 추출
            next_page_number_match = re.search(r'\((\d+)\)', next_page_href)
            if next_page_number_match:
                next_page_number = int(next_page_number_match.group(1))
                # print(f"다음 페이지 링크의 페이지 번호: {next_page_number}")

                # current_page가 더 크면 종료
                if current_page > next_page_number:
                    print(f"현재 페이지({current_page})가 다음 페이지 번호({next_page_number})보다 큽니다. 종료합니다.")
                    driver.quit()
                    exit()
                    break
            else:
                print("다음 페이지 링크의 페이지 번호를 찾을 수 없음")

        else:
            print("다음 페이지 링크를 찾을 수 없음")

    current_page += 1

# 웹 드라이버 종료
driver.quit()
