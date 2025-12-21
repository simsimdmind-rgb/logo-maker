import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 (레이아웃을 중앙 정렬로 변경)
st.set_page_config(page_title="AI 로고 프롬프트 생성기", page_icon="🎨", layout="centered")

# [UI 숨기기 CSS] - 상단 배너, 메뉴, 푸터 숨김
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
st.write("의뢰 내용만 한글로 입력하세요. 미드저니용 고퀄리티 영어 프롬프트를 자동으로 만들어드립니다.")
st.markdown("---")

# 3. [STEP 1] 스타일 선택 (메인 화면 버튼식)
st.subheader("1. 원하시는 로고 스타일을 선택하세요")

# 스타일 목록 정의
style_options = [
    "심플/미니멀 (Apple, Nike 스타일)", 
    "럭셔리/세리프 (호텔, 명품 스타일)", 
    "키치/레트로 (힙한 카페 스타일)", 
    "3D 캐릭터/마스코트 (귀여운 느낌)", 
    "빈티지 엠블럼 (전통, 신뢰감)"
]

# Pills(알약) 형태의 버튼으로 선택 UI 구현
style_key = st.pills(
    "스타일 태그",
    style_options,
    selection_mode="single"
)

# 4. [STEP 2] 내용 입력
st.subheader("2. 의뢰 내용을 입력하세요")
user_input = st.text_area(
    "브랜드명, 업종, 넣고 싶은 이미지 등을 한글로 적어주세요.", 
    height=150,
    placeholder="예시: 'ㅇㅁㄹㅁㄹㅁㄹㅇㅁㄹ"
)

# 5. 생성 버튼 및 로직
st.markdown("###") # 간격 띄우기
if st.button("✨ 프롬프트 생성하기", type="primary", use_container_width=True):
    # 유효성 검사 (스타일 선택 안 했을 경우 방지)
    if not style_key:
        st.warning("☝️ 위에서 '로고 스타일'을 먼저 선택해주세요!")
    elif not user_input:
        st.warning("✌️ '의뢰 내용'을 입력해주세요!")
    else:
        try:
            # Secrets에서 키를 가져옴
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            
            # 모델 설정 (Gemini 2.5 Flash)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # 시스템 프롬프트 (기존 로직 유지)
            system_prompt = f"""
            너는 미드저니(Midjourney) 로고 프롬프트 전문 엔지니어다.
            사용자의 요청을 바탕으로 최고의 로고를 뽑을 수 있는 영문 프롬프트를 작성해라.
            
            [선택된 스타일]: {style_key}
            [사용자 요청]: {user_input}
            
            [작성 규칙]
            1. 사용자의 요청을 완벽한 영어로 번역해서 반영해라.
            2. 선택된 스타일에 맞는 전문 디자인 용어(Vector, Flat, Minimalist 등)를 반드시 포함해라.
            3. 배경은 항상 'white background'로 설정해라.
            4. 결과물은 오직 프롬프트 명령어만 출력해라. (설명 금지)
            5. 문장 끝에는 --v 6.0 을 붙여라.
            """
            
            with st.spinner("AI가 최적의 프롬프트를 설계 중입니다..."):
                response = model.generate_content(system_prompt)
                final_prompt = response.text
                
                # 혹시 모를 설명 문구 제거 후 명령어 포맷팅
                final_prompt = final_prompt.replace("/imagine prompt:", "").strip()
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
