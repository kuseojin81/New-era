import streamlit as st
import requests
from openai import OpenAI

ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 저장공간
if "chemical" not in st.session_state:
    st.session_state.chemical = None

####################################################
# PubChem 검색
####################################################

def search_chemical(name):

    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/property/MolecularFormula,MolecularWeight,IUPACName/JSON"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        return data["PropertyTable"]["Properties"][0]

    else:
        return None

####################################################
# 검색 페이지
####################################################

def page_search():

    st.header("🧪 화학 물질 검색")

    chemical = st.text_input("물질 이름을 입력하세요")

    if st.button("검색"):

        result = search_chemical(chemical)

        if result:
            st.session_state.chemical = result
            st.success("검색 완료!")
        else:
            st.error("검색 결과가 없습니다.")

####################################################
# 정보 페이지
####################################################

def page_info():

    st.header("📖 화학 물질 정보")

    if st.session_state.chemical is None:
        st.info("먼저 물질을 검색하세요.")
        return

    c = st.session_state.chemical

    st.metric("분자식", c["MolecularFormula"])
    st.metric("분자량", c["MolecularWeight"])
    st.write("### IUPAC 이름")
    st.write(c["IUPACName"])

####################################################
# AI 설명
####################################################

def page_ai():

    st.header("🤖 AI 화학 선생님")

    if st.session_state.chemical is None:
        st.info("먼저 검색을 해주세요.")
        return

    c = st.session_state.chemical

    if st.button("AI 설명 듣기"):

        prompt = f"""
        다음 화학물질을 고등학생 수준으로 설명해줘.

        이름 : {c["IUPACName"]}

        분자식 : {c["MolecularFormula"]}

        분자량 : {c["MolecularWeight"]}

        아래 내용을 포함해줘.

        1. 어떤 물질인지
        2. 어디에 사용되는지
        3. 위험성
        4. 재미있는 사실
        """

        with st.spinner("AI가 설명 중..."):

            response = ai_client.chat.completions.create(
                model="gpt-5.4-mini",
                messages=[
                    {
                        "role":"user",
                        "content":prompt
                    }
                ]
            )

        st.write(response.choices[0].message.content)

####################################################
# 자유 질문
####################################################

def page_chat():

    st.header("💬 AI에게 질문하기")

    if "messages" not in st.session_state:

        st.session_state.messages = [
            {
                "role":"system",
                "content":"너는 친절한 화학 선생님이다."
            }
        ]

    for msg in st.session_state.messages:

        if msg["role"] != "system":

            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    question = st.chat_input("질문하세요.")

    if question:

        st.session_state.messages.append(
            {
                "role":"user",
                "content":question
            }
        )

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):

            response = ai_client.chat.completions.create(
                model="gpt-5.4-mini",
                messages=st.session_state.messages
            )

            answer = response.choices[0].message.content

            st.write(answer)

        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":answer
            }
        )

####################################################
# Navigation
####################################################

pg = st.navigation([

    st.Page(page_search, title="검색", icon="🧪"),

    st.Page(page_info, title="정보", icon="📖"),

    st.Page(page_ai, title="AI 설명", icon="🤖"),

    st.Page(page_chat, title="질문", icon="💬")

], position="top")

st.title("🧪 화학 물질 정보 검색기")

pg.run()
