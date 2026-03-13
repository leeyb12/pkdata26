# 구글 제미나이 AI
from google import genai
from dotenv import load_dotenv
import os

load_dotenv() # .env 파일로드
gen_key = os.getenv("GEMINI_API_KEY")

def gai(que):
    client = genai.Client(api_key = gen_key) 
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite", contents = que + '너는 200자 이내로 답하고 교수님 말투로 하라. 나는 학생이야')
    print(response.text)

if __name__ == "__main__":
    for n in range(5):
        gai(input("질문하세요: >> "))