import streamlit as st
import google.generativeai as genai

# Gemini API key (temporary, for learning only)
genai.configure(api_key="AIzaSyD3eVlWuVn1dYep2XOW3OaI6_g6oBy38Uk")

model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Bangkok Travel Assistant", page_icon="🌏")
st.title("🌆 Bangkok Travel Assistant")
st.markdown("Ask me anything about traveling in Bangkok — places to visit, food to eat, tips, and more!")

user_query = st.text_input("✈️ What do you want to know?")

if user_query:
    with st.spinner("Thinking..."):
        try:
            response = model.generate_content(user_query)
            st.markdown("**🤖 AI Assistant:**")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
