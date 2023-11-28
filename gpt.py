import requests
import openai
from bs4 import BeautifulSoup
import json

def gpt(text):
    text = str(text)
    # 클롤링 텍스트 + 질문지 gpt로 들어갈 내용
    text = text + "상세 정보를 토대로 ~로 되어있는 부분 채워서 상세 정보는 뺴고 진행일정은 기간으로 채워주고 데이터가 None일경우 ~로 대체해서 딕셔너리 형태만 반환해줘"

    # 추출한 텍스트 활용
    print(text)

    api_key = "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" #gpt api키 쓸때마다 돈듬...
    question = text

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=question,
            max_tokens=2000,
            api_key=api_key
        )
    except Exception as e:
        print(f"Error occurred: {e}")
        # 에러가 발생하면 question의 반을 새로운 prompt로 설정하여 재시도
        question = question[:len(question)//2]
        question = question + "상세 정보를 토대로 ~로 되어있는 부분 채워서 상세 정보는 뺴고 진행일정은 기간으로 채워주고 데이터가 None일경우 ~로 대체해서 딕셔너리 형태만 반환해줘"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=question,
            max_tokens=2000,
            api_key=api_key
        )
            
            
    answer = response.choices[0].text
    
    index_of_open_brace = answer.find('{')

    # '{' 이후의 문자열만 남기기
    result_str = answer[index_of_open_brace:]
    
    print(answer)
    
    result_str = result_str.replace("'", "\"")
    result_str = result_str.replace("None", "\"~\"")

    print(result_str)

    # 문자열을 딕셔너리로 변환
    try:
        program_info = json.loads(result_str)
    except json.decoder.JSONDecodeError as e:
        print(f"JSON 디코딩 오류: {e}")
        program_info = None  # 또는 다른 기본값을 설정할 수 있음

    # 딕셔너리 출력
    print(program_info)
    return program_info