import streamlit as st
import requests
from openai import OpenAI

ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "chemical" not in st.session_state:
    st.session_state.chemical = None

# 화학물질 검색
def page_search():

    st.header("🧪 화학 물질 검색")
    name = st.text_input("영어로 물질 이름을 입력하세요")
    if st.button("검색"):
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/property/MolecularFormula,MolecularWeight,IUPACName/JSON"
        response = requests.get(url)

        if response.status_code == 200:

            data = response.json()

            st.session_state.chemical = data["PropertyTable"]["Properties"][0]

            st.success("검색 완료!")

        else:
            st.error("검색 결과가 없습니다.")

# 검색 결과
def page_info():

    st.header("📖 화학 물질 정보")

    if st.session_state.chemical == None:
        st.write("먼저 검색을 해주세요.")
    else:

        c = st.session_state.chemical

        st.write("**분자식** :", c["MolecularFormula"])
        st.write("**분자량** :", c["MolecularWeight"])
        st.write("**IUPAC 이름** :", c["IUPACName"])

# AI 설명
def page_ai():

    st.header("🤖 AI 설명")

    if st.session_state.chemical == None:
        st.write("먼저 검색을 해주세요.")
    else:

        if st.button("설명 듣기"):

            c = st.session_state.chemical

            prompt = f"""
            {c["IUPACName"]}을(를)
            고등학생이 이해하기 쉽게 설명해줘.
            어떤 물질인지, 어디에 쓰는지,
            위험성도 알려줘.
            """

            response = ai_client.chat.completions.create(
                model="gpt-5.4-mini",
                messages=[
                    {"role":"user","content":prompt}])
           
            st.write(response.choices[0].message.content)
            
# AI 질문
def page_chat():

    st.header("💬 AI에게 질문")

    question = st.chat_input("질문을 입력하세요.")

    if question:

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):

            response = ai_client.chat.completions.create(
                model="gpt-5.4-mini",
                messages=[{"role":"system","content":"너는 친절한 화학 선생님이다."}, {"role":"user","content":question}])
            st.write(response.choices[0].message.content)

pg = st.navigation([
    st.Page(page_search, title="검색", icon="🧪"),
    st.Page(page_info, title="정보", icon="📖"),
    st.Page(page_ai, title="AI 설명", icon="🤖"),
    st.Page(page_chat, title="질문", icon="💬")
], position="top")

st.title("🧪 화학 물질 정보 검색기")

pg.run()
