import anthropic
import streamlit as st

system_prompt = """
<GPTs의 Instruction>
"""

ANTHROPIC_API_KEY = "<자신의 API KEY>"

# 화면을 3등분하는 columns 생성
left_co, cent_co, last_co = st.columns(3)

# 로고 이미지 출력
with cent_co:
   st.image('logo.png', width=300)

# 챗봇 이름 및 제작자 출력
st.title("<챗봇 이름>")
st.caption("By 이름")

# 사이드바에 내용 출력
st.sidebar.subheader("""
<왼쪽 사이드바에 넣고 싶은 내용 아무거나>
""")

# 세션 상태에 messages가 있는 경우에만 이전 대화 내용 출력
if "messages" in st.session_state:
   for msg in st.session_state.messages:
       st.chat_message(msg["role"]).write(msg["content"])

# 사용자 입력 받기
if prompt := st.chat_input():
   client = anthropic.Anthropic(
       api_key=ANTHROPIC_API_KEY,
   )
   
   # 사용자 입력 메시지를 세션 상태에 추가
   if "messages" not in st.session_state:
       st.session_state["messages"] = []
   st.session_state.messages.append({"role": "user", "content": prompt})
   
   # 사용자 입력 메시지 출력
   st.chat_message("user").write(prompt)
   
   # 어시스턴트의 응답을 출력할 빈 메시지 생성
   assistant_chat_message = st.chat_message("assistant")
   response_placeholder = assistant_chat_message.empty()
   
   response_text = ""
   
   # 어시스턴트의 응답을 실시간으로 스트리밍 받아 출력
   with client.messages.stream(model="claude-3-opus-20240229", max_tokens=4000, temperature=0.8, system=system_prompt, messages=st.session_state.messages) as stream:
       for text in stream.text_stream:
           response_text += text
           response_placeholder.markdown(response_text)
   
   # 어시스턴트의 응답을 세션 상태에 추가
   st.session_state.messages.append({"role": "assistant", "content": response_text})