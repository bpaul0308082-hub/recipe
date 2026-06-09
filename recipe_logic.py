import streamlit as st
from openai import OpenAI

def get_recipe(items):
    # 1. 데이터 유효성 검사
    if not items:
        return "냉장고에 재료가 없습니다.", None
    
    # 2. 유통기한 임박순 정렬
    try:
        sorted_items = sorted([item for item in items if 'dDay' in item], key=lambda x: x['dDay'])
    except Exception as e:
        return f"데이터 형식 오류: {str(e)}", None

    if not sorted_items:
        return "유효한 재료 데이터가 없습니다.", None
        
    urgent_items = [item['name'] for item in sorted_items[:3]]
    
    # 3. OpenAI를 통해 레시피 및 관련 블로그/유튜브 추천 요청
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    prompt = f"""
    냉장고에 있는 재료들: {', '.join(urgent_items)}
    이 재료들을 활용하여 만들 수 있는 간단한 자취생 요리 레시피를 1개 추천해줘.
    
    요구사항:
    1. 요리 이름과 간단한 요리 순서를 작성해줘.
    2. 이 요리를 찾아볼 수 있는 네이버 블로그 검색 키워드나 유튜브 검색어를 1개씩 추천해줘.
    3. 정중하고 친절한 어조로 작성해줘.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        recipe_text = response.choices[0].message.content
        
        # 실제 URL은 아니지만, 검색을 유도할 수 있는 키워드를 포함한 텍스트 반환
        return recipe_text, None 
    except Exception as e:
        return f"서비스 호출 오류: {str(e)}", None
