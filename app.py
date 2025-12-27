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

# 스타일 목록 정의
style_options = [
    "심플/미니멀 심볼 (아이콘)", 
    "미니멀 라인 (선으로 그린 느낌)", 
    "문구 조합형 (알파벳+그림 결합)", 
    "캐릭터/마스코트 (레트로)", 
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

# ---------------------------------------------------------
# [핵심 기능] 선택된 스타일에 따라 '예시 문구'가 자동으로 바뀜
# ---------------------------------------------------------
placeholders = {
    "심플/미니멀 심볼 (아이콘)": "예시: 사과모양의 아주 심플한 아이콘을 원해.",
    "미니멀 라인 (선으로 그린 느낌)": "예시: 꽃집 로고를 만들고 싶어. 장미 한 송이를 끊어지지 않는 하나의 선으로 그린 느낌",
    "문구 조합형 (알파벳+그림 결합)": "예시: '프비연'이라는 AI 교육 브랜드야. 알파벳 'P'와 학사모가 결합된 심볼",
    "캐릭터/마스코트 (레트로)": "예시: 오토바이를 타고있고 썬글라스를 낀 강아지 캐릭터",
    "텍스트 형태 (이니셜 강조)": "예시: 브랜드 이름이 'Max'야. 알파벳 'M'을 강조해서 아주 심플하고 모던하게 만들어줘.",
    "테크/퓨처리스틱 (IT, 네온)": "예시: 블록체인 스타트업이야. 뇌와 회로가 연결된 느낌으로 네온 컬러를 써서 미래지향적으로 만들어줘."
}

# 선택된 스타일이 없으면 기본 문구, 있으면 해당 스타일의 예시 문구 가져오기
selected_placeholder = placeholders.get(style_key, "위에서 스타일을 먼저 선택하시면, 맞춤형 예시를 보여드립니다!")

user_input = st.text_area(
    "의뢰 내용만 한글로 입력하세요. 미드저니용 고퀄리티 영어 프롬프트를 자동으로 만들어드립니다.", 
    height=150,
    # [수정 완료] 아까 에러나던 변수명을 올바르게 고쳤습니다!
    placeholder=selected_placeholder
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
            # Secrets에서 키를 가져옴
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            
            # [요청하신 대로 2.5 버전 유지!]
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # ---------------------------------------------------------
            # [핵심] 대표님의 프롬프트 공식 (System Prompt 설계)
            # ---------------------------------------------------------
            
base_keywords = "vector graphic, simple, minimal, white background"
    base_negative = "--no realistic, shadow, shading, gradient, text"
    formula = ""

    if style_key == "심플/미니멀 심볼 (아이콘)":
        formula = f"flat vector logo, minimalist, pictograph, Paul Rand style, negative space, geometric, less is more, iconic, [SUBJECT], {base_keywords} {base_negative}"

    elif style_key == "미니멀 라인 (선으로 그린 느낌)":
        formula = f"minimal line logo of a [SUBJECT], vector, {base_keywords} {base_negative} --v 6.0"

    elif style_key == "문구 조합형 (알파벳+그림 결합)":
        formula = f"vector logo for [INDUSTRY] where the letter [LETTER] is [DESCRIPTION], black and white, minimalist, modern, not cartoonish, white background --no realistic, shading, gradient"

    elif style_key == "캐릭터/마스코트 (레트로)":
        formula = f"Minimal retro mascot logo of cartoon [SUBJECT] [ACTION], [PROPS], [EXPRESSION]. Simple clean black outlines only, flat line art style, no shading, no halftone, white background, no text or typography"

    elif style_key == "텍스트 형태 (이니셜 강조)":
        formula = f"modern and simple logo design, [LETTER], letter [LETTER], one color, vector, white background {base_negative}"

    elif style_key == "테크/퓨처리스틱 (IT, 네온)":
        formula = f"tech logo, futuristic, gradient, app icon, neon glow, cyber style, connected nodes, data flow, modern, [SUBJECT], white background --no realistic, text, shadow"

            # 최종 시스템 프롬프트 조합
system_prompt = f"""
너는 미드저니 전문 프롬프트 엔지니어다.
사용자의 [의뢰 내용]을 분석해서 아래의 [제공된 공식]에 맞춰서 영어 프롬프트 한 줄만 만들어라.

[의뢰 내용]: {user_input}
[제공된 공식]: {formula}

[작성 규칙]:
1. [ ]로 표시된 대괄호 부분을 사용자의 의뢰 내용에 맞게 영어로 번역해서 채워 넣어라.
2. 공식에 있는 단어들은 하나도 빠뜨리지 말고 그대로 유지하라.
3. 출력은 반드시 영어로 된 프롬프트 한 줄만 하며, 설명이나 인사말은 절대 하지 마라.
"""
            
            with st.spinner("AI가 최적의 프롬프트를 설계 중입니다..."):
                response = model.generate_content(system_prompt)
                final_prompt = response.text
                
                # 후처리
                final_prompt = final_prompt.replace("`", "").strip()

            # 6. 결과 출력
            st.success("🎉 생성 완료! 아래 프롬프트를 복사해서 사용하세요.")
            st.code(final_prompt, language="bash")
            
        except Exception as e:
            st.error(f"에러가 발생했습니다: {e}")

# 7. 하단 푸터
st.markdown("---")
st.caption("Created by 프비연")
