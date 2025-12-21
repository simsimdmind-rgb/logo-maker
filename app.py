import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 (중앙 정렬)
st.set_page_config(page_title="AI 로고 프롬프트 생성기", page_icon="🎨", layout="centered")

# [UI 숨기기 CSS]
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

# 3. [STEP 1] 스타일 선택 (메인 화면 버튼식)
st.subheader("1. 원하시는 로고 스타일을 선택하세요")

# 스타일 목록 정의 (대표님이 주신 카테고리대로 정리)
style_options = [
    "심플/미니멀 심볼 (아이콘, 기하학)", 
    "미니멀 라인 (선으로 그린 느낌)", 
    "문구 조합형 (알파벳+그림 결합)", 
    "캐릭터/마스코트 (레트로 라인아트)", 
    "텍스트 형태 (이니셜 강조)",
    "테크/퓨처리스틱 (IT, 네온)"
]

# Pills(알약) 형태의 버튼
style_key = st.pills(
    "스타일 태그",
    style_options,
    selection_mode="single"
)

# 4. [STEP 2] 내용 입력
st.subheader("2. 의뢰 내용을 입력하세요")
placeholder_text = "예시: '프비연'이라는 브랜드야. 책과 연필이 결합된 이미지였으면 좋겠어."
if style_key == "문구 조합형 (알파벳+그림 결합)":
    placeholder_text = "예시: 서점 로고를 만들 거야. 알파벳 'B'가 옆에서 본 책 모양처럼 보였으면 좋겠어."
elif style_key == "텍스트 형태 (이니셜 강조)":
    placeholder_text = "예시: 알파벳 'M'으로 심플하게 만들어줘."

user_input = st.text_area(
    "의뢰 내용만 한글로 입력하세요. 미드저니용 고퀄리티 영어 프롬프트를 자동으로 만들어드립니다.", 
    height=150,
    placeholder=placeholder_text
)

# 5. 생성 버튼 및 로직
st.markdown("###") 
if st.button("✨ 프롬프트 생성하기", type="primary", use_container_width=True):
    if not style_key:
        st.warning("☝️ 위에서 '로고 스타일'을 먼저 선택해주세요!")
    elif not user_input:
        st.warning("✌️ '의뢰 내용'을 입력해주세요!")
    else:
        try:
            genai.configure(api_key="sk-AIzaSyCkb8Yjk-5U8o6QKFulFkY6fNUGBxJQwqw")
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # ---------------------------------------------------------
            # [핵심] 대표님의 프롬프트 공식 (System Prompt 설계)
            # ---------------------------------------------------------
            
            # 공통 필수 키워드 및 네거티브 프롬프트 (기본값)
            base_keywords = "vector graphic, simple, minimal, white background"
            base_negative = "--no realistic, shadow, shading, gradient, text"

            # 스타일별 구체적 지시사항 (Prompt Templates)
            instructions = ""
            
            if style_key == "심플/미니멀 심볼 (아이콘, 기하학)":
                instructions = f"""
                [공식]: flat vector logo, minimalist, pictograph, Paul Rand style, negative space, geometric, less is more, iconic, [Subject described in user input], {base_keywords} {base_negative} --v 6.0
                [미션]: 사용자의 입력을 분석해 [Subject] 부분을 영어로 채워넣어라.
                """
            
            elif style_key == "미니멀 라인 (선으로 그린 느낌)":
                instructions = f"""
                [공식]: minimal line logo of a [Subject], vector, {base_keywords} {base_negative} --v 6.0
                [미션]: 사용자의 입력에서 핵심 대상(Subject)을 추출하여 영어로 번역하고 공식에 대입하라. (예: rose, horse)
                """

            elif style_key == "문구 조합형 (알파벳+그림 결합)":
                instructions = f"""
                [공식]: vector logo for [Industry] where the letter [Letter] is [Description], black and white, minimalist, modern, not cartoonish, white background --no realistic, shading, gradient --v 6.0
                [미션]: 사용자의 입력에서 업종(Industry), 알파벳(Letter), 묘사(Description)를 추출해 영어로 번역하고 공식에 대입하라.
                (예시: logo for bookstore where the letter B is a book viewed from the side)
                """

            elif style_key == "캐릭터/마스코트 (레트로 라인아트)":
                instructions = f"""
                [공식]: Minimal retro mascot logo of a [Subject] [Action], [Props/Details], [Expression]. Simple clean black outlines only, flat line art style, no shading, no halftone, white background, no text or typography --v 6.0
                [미션]: 사용자의 입력에서 대상(Subject), 동작(Action), 소품(Props), 표정(Expression)을 추출해 영어로 번역하고 공식에 대입하라.
                (예시: cartoon cat surfing, wearing a bucket hat, winking)
                """

            elif style_key == "텍스트 형태 (이니셜 강조)":
                instructions = f"""
                [공식]: modern and simple logo design, [Character], letter [Character], one color, vector, white background {base_negative} --v 6.0
                [미션]: 사용자의 입력에서 제작할 문자(Character)를 찾아 영어 대문자로 공식에 대입하라.
                (예시: modern and simple logo design, M, letter M, one color, vector)
                """
            
            elif style_key == "테크/퓨처리스틱 (IT, 네온)":
                instructions = f"""
                [공식]: tech logo, futuristic, gradient, app icon, neon glow, cyber style, connected nodes, data flow, modern, [Subject described in user input], white background --no realistic, text, shadow --v 6.0
                [미션]: 사용자의 입력을 분석해 [Subject]를 영어로 추가하고 공식에 맞춰 완성하라. 테크 느낌을 살려라.
                """

            # 최종 시스템 프롬프트 조합
            system_prompt = f"""
            너는 미드저니(Midjourney) 프롬프트 작성 로봇이다.
            사용자의 [의뢰 내용]을 분석하여, 아래 [스타일 지침]에 따라 빈칸을 채워 완벽한 프롬프트 명령어를 출력하라.
            
            [사용자 의뢰 내용]: {user_input}
            
            [스타일 지침]:
            {instructions}
            
            [출력 규칙]
            1. 결과물은 오직 '/imagine prompt: '로 시작하는 영어 명령어 한 줄만 출력한다.
            2. 설명이나 잡담은 절대 하지 않는다.
            """
            
            with st.spinner("AI가 필승 공식을 적용 중입니다..."):
                response = model.generate_content(system_prompt)
                final_prompt = response.text
                
                # 후처리 (혹시 모를 잡다한 텍스트 제거)
                final_prompt = final_prompt.replace("`", "").strip()
                if not final_prompt.startswith("/imagine prompt:"):
                     final_prompt = "/imagine prompt: " + final_prompt

            # 6. 결과 출력
            st.success("🎉 생성 완료! 아래 코드를 복사해서 사용하세요.")
            st.code(final_prompt, language="bash")
            
        except Exception as e:
            st.error(f"에러가 발생했습니다: {e}")

# 7. 하단 푸터
st.markdown("---")
st.caption("Created by 프비연")
