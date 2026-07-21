import streamlit as st
from openai import OpenAI

ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 선택한 화학 물질 저장
if "chemical" not in st.session_state:
    st.session_state.chemical = "물"

st.title("🧪 AI 화학 물질 설명기")

# 화학 물질 선택
chemical = st.selectbox(
    "화학 물질을 선택하세요.",
    ["물", "에탄올", "아세톤", "포도당", "암모니아"],
    key="chemical"
)

# AI 설명
if st.button("AI 설명 보기"):

    prompt = f"""
    {chemical}에 대해 고등학생이 이해하기 쉽게 설명해줘.

    아래 내용을 포함해줘.
    1. 어떤 물질인지
    2. 분자식
    3. 어디에 사용하는지
    4. 위험성
    """

    response = ai_client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    with st.container(border=True):
        st.subheader(f"🧪 {chemical}")
        st.write(response.choices[0].message.content)

# 추가 질문
with st.expander("AI에게 더 질문하기"):

    question = st.text_input("궁금한 점을 입력하세요.")

    if st.button("질문하기"):

        response = ai_client.chat.completions.create(
            model="gpt-5.4-mini",
            messages=[
                {
                    "role": "system",
                    "content": "너는 친절한 화학 선생님이다."
                },
                {
                    "role": "user",
                    "content": f"{chemical}에 대해 질문: {question}"
                }
            ]
        )

        st.write(response.choices[0].message.content)
if st.button("퀴즈 풀기"):

    prompt = f"""
    {chemical}에 관한 객관식 퀴즈를 하나 만들어줘.

    정답도 마지막에 알려줘.
    """

    response = ai_client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role":"user","content":prompt}
        ]
    )

    st.write(response.choices[0].message.content)
