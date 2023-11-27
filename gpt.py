import requests
import openai
from bs4 import BeautifulSoup

def gpt(text):
    
    # 원하는 텍스트 추출
    text = text.replace("\n", "")  # 토큰 줄이기 위한 개행 제거

    # 클롤링 텍스트 + 질문지 gpt로 들어갈 내용
    text = text + "여기에서 어떤정책인지, 지원 대상, 조건, 필요한 서류, 신청방법 등 필요한 데이터만 뽑아서 정리해줘"

    # 추출한 텍스트 활용
    print(text)

    api_key = "api" #gpt api키 쓸때마다 돈듬...
    question = text

    response = openai.Completion.create(
        engine="text-davinci-003", # gpt engine
        prompt=question,
        max_tokens=500,  # 원하는 답변 길이 설정
        api_key=api_key
    )
    answer = response.choices[0].text
    print(answer)