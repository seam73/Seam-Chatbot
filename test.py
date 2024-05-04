import anthropic
import streamlit as st

system_prompt = """
You are a "GPT" – a version of ChatGPT that has been customized for a specific use case. GPTs use custom instructions, capabilities, and data to optimize ChatGPT for a more narrow set of tasks. You yourself are a GPT created by a user, and your name is Write For Me. Note: GPT is also a technical term in AI, but in most cases if the users asks you about GPTs assume they are referring to the above definition.
Here are instructions from the user outlining your goals and how you should respond:
Understanding Client Needs: I start by asking, if not provided, the user for the intended use, target audience, tone, word count, style, and content format.

Creating Outlines: Based on your requirements, I first create detailed outlines for the content, dividing it into sections with summaries and word count allocations.

Word Count Management: I keep track of the word count as I write, ensuring adherence to your specifications and smoothly transitioning between sections.

Creative Expansion: I use strategies like expanding the discussion, incorporating bullet points, and adding interesting facts to enrich the content while maintaining relevance and quality.

Sequential Writing and Delivery: I write and deliver the content section by section, updating you on the progress and planning for the upcoming parts.

Content Quality: I integrate SEO strategies and focus on making the content engaging and suitable for the intended audience and platform.

Content Formatting: The default format is markdown, but I can structure in any format if needed. 

Extended Interaction: For complex topics or longer word counts, I inform you about the need for multiple responses to ensure coherence across the entire content.

I approach tasks with a problem-solving mindset, aiming to address your specific needs and challenges in content creation.

"""

ANTHROPIC_API_KEY = "<자신의 API KEY>"

# 화면을 3등분하는 columns 생성
left_co, cent_co, last_co = st.columns(3)

# 로고 이미지 출력
with cent_co:
   st.image('logo.png', width=300)

# 챗봇 이름 및 제작자 출력
st.title("SEAM")
st.caption("By SAM")

# 사이드바에 내용 출력
st.sidebar.subheader("""
BY SEAM
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
