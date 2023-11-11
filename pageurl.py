import requests
from bs4 import BeautifulSoup

# 웹 페이지의 URL 설정
url = 'https://young.busan.go.kr/policySupport/list.nm?menuCd=12'

# 웹 페이지의 내용을 가져오기
response = requests.get(url)

# HTTP 요청이 성공한 경우
if response.status_code == 200:
    # BeautifulSoup를 사용하여 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # <div> 요소 중 class가 "photo_type2"인 것을 찾기
    specific_div = soup.find('div', class_='photo_type2')

    if specific_div:
        # <li> 요소 내부의 <ul> 요소 찾기
        ul_element = specific_div.find('ul')
        ur = 'https://young.busan.go.kr/'

        if ul_element:
            # <li> 요소들을 모두 찾기
            li_elements = ul_element.find_all('li')

            for li in li_elements:
                div = li.find('div', class_='photo2_tit')
                link = div.find('a')
                href = link.get('href')
                
                href = href[1:]
                href = ur + href
                print(href)

                response1 = requests.get(href)  # URL 요청

                # 2. 웹 페이지 내용 파싱
                soup1 = BeautifulSoup(response1.text, "html.parser")

                # 3. 원하는 텍스트 추출
                element = soup1.find("div", class_="detail_page ct")
                if element:
                    text = element.text.replace("\n", "")  # 토큰 줄이기 위한 개행 제거
                    print(text)
                else:
                    print("No 'sub_content' found on the page")
else:
    print(f'HTTP 요청에 실패했습니다. 상태 코드: {response.status_code}')
