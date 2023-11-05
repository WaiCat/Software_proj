import requests
import openai
from bs4 import BeautifulSoup


# 1. 웹 페이지에 연결
url = "https://young.busan.go.kr/index.nm?menuCd=0"
response = requests.get(url)

# 2. 웹 페이지 내용 파싱
soup = BeautifulSoup(response.text, "html.parser")

# 3. 원하는 텍스트 추출
element = soup.find("div", class_="sub_content")
text = element.text.replace("\n", "")
# text = text.replace(" ", "")
text = text + "여기에서 어떤정책인지, 지원 대상, 조건, 필요한 서류, 신청방법 등 필요한 데이터만 뽑아서 정리해줘"


# 4. 추출한 텍스트 활용
print(text)


api_key = "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"
question = text

response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=question,
    max_tokens=500,  # 원하는 답변 길이 설정
    api_key=api_key
)

answer = response.choices[0].text
print(answer)