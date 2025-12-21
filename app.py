import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 (가장 먼저 와야 함)
st.set_page_config(page_title="AI 로고 프롬프트 생성기", page_icon="🎨")

# [여기 추가됨] 상단 배너(Fork 등), 메뉴, 푸터 숨기기
hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

# 2. 제목 및 설명
st.title("🎨 로고 제작 프롬프트 자동 생성기")
st.markdown("---")
st.write("의뢰 내용만 한글로 입력하세요. 미드저니용 고퀄리티 영어 프롬프트를 자동으로 만들어드립니다.")

# 3. 사이드바 (스타일 선택)
with st.sidebar:
    st.header("⚙️ 스타일 설정")
    style_option = st.selectbox(
        "원하는 스타일을 골라주세요",
        ("심플/미니멀 (Apple, Nike 스타일)", 
         "럭셔리/세리프 (호텔, 명품 스타일)", 
         "키치/레트로 (힙한 카페 스타일)", 
         "3D 캐릭터/마스코트 (귀여운 느낌)", 
         "빈티지 엠블럼 (전통, 신뢰감)")
    )

# 4. 메인 입력창
user_input = st.text_area("의뢰 내용 (예: 따뜻한 느낌의 뜨개질 공방, 실과 바늘 포함)", height=150)

# 5. 생성 버튼 및 로직
if st.button("✨ 프롬프트 생성하기", type="primary"):
    if not user_input:
        st.warning("의뢰 내용을 입력해주세요.")
    else:
        try:
            # Secrets에서 키를 가져옴
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            
            # 모델 설정 (가장 최신)
            model = genai.GenerativeModel('gemini-2.5-flash') 
            
            system_prompt = f"""
            너는 미드저니(Midjourney) 로고 프롬프트 전문 엔지니어다.
            사용자의 요청을 바탕으로 최고의 로고를 뽑을 수 있는 영문 프롬프트를 작성해라.
            
            [선택된 스타일]: {style_option}
            [사용자 요청]: {user_input}
            
            [작성 규칙]
            1. 사용자의 요청을 완벽한 영어로 번역해서 반영해라.
            2. 선택된 스타일에 맞는 전문 디자인 용어(Vector, Flat, Minimalist 등)를 반드시 포함해라.
            3. 배경은 항상 'white background'로 설정해라.
            4. 결과물은 오직 프롬프트 명령어만 출력해라. (설명 금지)
            5. 문장 끝에는 --v 6.0 을 붙여라.
            """
            
            with st.spinner("AI가 프롬프트를 작성 중입니다..."):
                response = model.generate_content(system_prompt)
                final_prompt = response.text
                
            st.success("생성 완료! 아래 내용을 복사해서 미드저니에 붙여넣으세요.")
            st.code(final_prompt, language="bash")
            
        except Exception as e:
            st.error(f"에러가 발생했습니다: {e}")

# 6. 하단 푸터 (수동으로 넣은 제작자 표시는 남겨둠)
st.markdown("---")
st.caption("Created by 프비연")
