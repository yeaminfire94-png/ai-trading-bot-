import streamlit as st
from PIL import Image
import google.generativeai as genai

st.set_page_config(page_title="AI Trading Signal Analyzer", layout="wide")
st.title("📊 AI Trading Signal Analyzer")

st.sidebar.header("⚙️ Settings")
api_key = st.sidebar.text_input("Gemini API Key:", type="password")

uploaded_file = st.file_uploader("Upload Chart", type=["jpg", "png", "jpeg"])

if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Chart", use_container_width=True)
    if st.button("Analyze Chart"):
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(["Analyze this chart and give trading signals with reasoning in Bengali.", image])
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.info("API Key দিন এবং ছবি আপলোড করুন।")
    
