import streamlit as st
from openai import OpenAI
from tavily import TavilyClient

def get_recipe(items):
    # 유통기한 임박순 정렬
    sorted_items = sorted(items, key=lambda x: x['dDay'])
    urgent_items = [item['name'] for item in sorted_items[:3]]
    
    # OpenAI 설정
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    # 레시피 추천 받기
    prompt = f"냉장고에 있는 재료들: {', '.join(urgent_items)}. 이를 활용한 간단한 레시피와 요약 과정을 알려줘."
    response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
    recipe_text = response.choices[0].message.content
    
    # Tavily 검색 (출처 확보)
    tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
    search_result = tavily.search(query=f"{urgent_items[0]} 레시피", search_depth="basic")
    top_link = search_result['results'][0]['url'] if search_result['results'] else "https://www.google.com"
    
    return recipe_text, top_link
