from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# 웹 드라이버 시작
driver = webdriver.Chrome()

# 첫 번째 페이지
driver.get('https://young.busan.go.kr/policySupport/list.nm')

# 데이터 저장 리스트 정의
titles = []  # 정책명
urls = []  # URL
application_periods = []  # 신청 기간
organizations = []  # 담당 기관

# 시작 페이지 초기화
current_page = 1  # Starting from page 1

while current_page <= 34:
    # 실행할 자바스크립트 함수 호출
    javascript_code = f"fn_page({current_page});"

    # 자바스크립트 코드 실행
    driver.execute_script(javascript_code)

    # 브라우저 창을 열어둘 시간을 주기 위해 대기 (여기서는 5초로 설정)
    driver.implicitly_wait(5)

    # 현재 페이지 소스 가져오기
    page_source = driver.page_source

    # 'div' 태그 내부의 'photo2_tit' 클래스 이름을 가진 모든 요소 찾기
    title_elements = driver.find_elements(By.CLASS_NAME, 'photo2_tit')

    # 텍스트와 URL 추출
    for title_element in title_elements:
        if 'spt_state' in title_element.get_attribute('class') and 'end' in title_element.get_attribute('class'):
            continue
        title_text = title_element.text.strip()
        post_url = title_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
        titles.append(title_text)
        urls.append(post_url)

    # 'div' 태그 내부의 'info_box2' 클래스 이름을 가진 모든 요소 찾기
    info_boxes = driver.find_elements(By.CLASS_NAME, 'info_box2')

    # 신청 기간과 담당 기관 추출
    for info_box in info_boxes:
        if 'spt_state' in title_element.get_attribute('class') and 'end' in title_element.get_attribute('class'):
            continue
        dds = info_box.find_elements(By.TAG_NAME, 'dd')
        if len(dds) >= 2:
            application_period = dds[0].text.strip()
            organization_in_charge = dds[1].text.strip()
            application_periods.append(application_period)
            organizations.append(organization_in_charge)

    # 다음 페이지로 이동 (타이틀, url)
    try:
        next_page_number = current_page + 1
        next_page_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, str(next_page_number)))
        )
        next_page_element.click()
        current_page = next_page_number
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Reached the last page: {current_page}")
        break

# 모든 데이터를 포함하는 DataFrame
data = {
    '정책이름': titles,
    'URL': urls,
    '신청기간': application_periods,
    '담당기관': organizations
}
df = pd.DataFrame(data)
df.to_excel('청년G대 정책들.xlsx', index=False)
driver.quit()