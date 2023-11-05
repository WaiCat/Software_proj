import openai

api_key = "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"
question = 

response = openai.Completion.create(
    engine="davinci",
    prompt=question,
    max_tokens=500,  # 원하는 답변 길이 설정
    api_key=api_key
)

answer = response.choices[0].text
print(answer)