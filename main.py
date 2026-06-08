import streamlit as st
from recipe_logic import get_recipe

st.title("Keep And Cook")

# 1. 완벽하게 초기화 (기존 잘못된 데이터 제거)
if "items" not in st.session_state or not isinstance(st.session_state.items, list):
    st.session_state.items = []

# --- 샘플 데이터 추가 로직 ---
if st.button("샘플 데이터 추가"):
    # 여기서 확실하게 리스트 형식으로 저장
    st.session_state.items = [
        {"name": "우유", "dDay": 1},
        {"name": "계란", "dDay": 3},
        {"name": "양파", "dDay": 7}
    ]
    st.rerun() # 데이터를 업데이트하고 즉시 새로고침

# 요리 추천 버튼
if st.button("유통기한 임박 재료로 레시피 추천받기"):
    # 2. 데이터 타입 명시적 체크
    if isinstance(st.session_state.items, list) and len(st.session_state.items) > 0:
        with st.spinner("레시피를 생성하는 중..."):
            recipe, link = get_recipe(st.session_state.items)
            
            if link:
                st.markdown("### 🍳 추천 요리")
                st.write(recipe)
                st.link_button("레시피 상세 확인하기", link)
            else:
                st.error(recipe)
    else:
        st.error("데이터가 리스트 형식이 아니거나 비어있습니다. 샘플을 추가해주세요.")

# 디버깅: 타입 확인
st.write("---")
st.write(f"현재 데이터 타입: {type(st.session_state.items)}")
st.write("현재 내용:", st.session_state.items)
