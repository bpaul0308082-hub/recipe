import streamlit as st
from openai import OpenAI
from tavily import TavilyClient

def get_recipe(items):
    # 1. 데이터 유효성 검사
    if not items:
        return "냉장고에 재료가 없습니다.", None
    
    # 2. 유통기한 임박순 정렬 (데이터 검증 포함)
    try:
        # 데이터가 딕셔너리 리스트인지 확인하고 dDay 기준으로 정렬
        sorted_items = sorted([item for item in items if 'dDay' in item], key=lambda x: x['dDay'])
    except Exception as e:
        return f"데이터 형식 오류: {str(e)}", None

    if not sorted_items:
        return "유효한 재료 데이터가 없습니다.", None
        
    urgent_items = [item['name'] for item in sorted_items[:3]]
    
    # 3. OpenAI를 통해 레시피 생성
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    prompt = f"""
    냉장고에 있는 재료들: {', '.join(urgent_items)}
    이 재료들을 활용하여 만들 수 있는 간단한 자취생 요리 레시피를 1개 추천해줘.
    요약된 요리 순서와 함께 정중한 어조로 알려줘.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        recipe_text = response.choices[0].message.content
        
        # 4. Tavily를 사용해 실제 링크 검색
        tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
        search_result = tavily.search(query=f"{urgent_items[0]} 레시피 추천", search_depth="basic")
        top_link = search_result['results'][0]['url'] if search_result['results'] else "https://www.google.com"
        
        return recipe_text, top_link
    except Exception as e:
        return f"서비스 호출 오류: {str(e)}", None
