import streamlit as st
from recipe_logic import get_recipe

st.title("Keep And Cook")

# 세션 상태 초기화
if "items" not in st.session_state:
    st.session_state.items = []

# --- 임시 데이터 추가 로직 (테스트용) ---
if st.button("샘플 데이터 추가"):
    st.session_state.items = [
        {"name": "우유", "dDay": 1},
        {"name": "계란", "dDay": 3},
        {"name": "양파", "dDay": 7}
    ]
    st.success("샘플 데이터가 추가되었습니다!")

# 요리 추천 버튼
if st.button("유통기한 임박 재료로 레시피 추천받기"):
    if not st.session_state.items:
        st.error("먼저 영수증을 업로드하거나 재료를 추가해주세요!")
    else:
        with st.spinner("레시피를 생성하는 중..."):
            recipe, link = get_recipe(st.session_state.items)
            
            if link:
                st.markdown("### 🍳 추천 요리")
                st.write(recipe)
                st.link_button("레시피 상세 확인하기", link)
            else:
                st.error(recipe)

# 현재 목록 확인용 (디버깅)
st.write("---")
st.write("현재 냉장고 재료 목록:", st.session_state.items)
