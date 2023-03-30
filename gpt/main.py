import openai
import konlpy
import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

disable_warnings(InsecureRequestWarning)
# OpenAI API 키를 입력해주세요.
openai.api_key = "lg-4HhhsPe3Y0CBMySHPGspT3BlbkFJUF7vy7iApxu3YcAGXh7R"

# ChatGPT 모델 ID를 입력해주세요.
model_id = "text-davinci-003"

# konlpy 라이브러리에서 사용할 형태소 분석기를 선택해주세요.
morph = konlpy.tag.Okt()

# 대화를 시작합니다.
while True:
    openai.verify_ssl_certs = False
    # 사용자 입력을 받습니다.
    user_input = input("사용자: ")

    # 입력된 문장을 형태소 분석합니다.
    tokens = morph.morphs(user_input)

    # ChatGPT 모델에 입력할 문장을 생성합니다.
    prompt = " ".join(tokens)

    # ChatGPT 모델에 문장을 입력하여 답변을 생성합니다.
    response = openai.Completion.create(
        engine=model_id,
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # 생성된 답변을 출력합니다.
    print("ChatGPT: " + response.choices[0].text.strip())