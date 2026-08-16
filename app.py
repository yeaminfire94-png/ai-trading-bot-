import streamlit as st
from PIL import Image
import google.generativeai as genai

# পেজ সেটআপ
st.set_page_config(page_title="Real AI OTC Signal Analyzer", layout="wide")
st.title("📊 Real AI OTC Signal & Chart Analyzer")

# সাইডবার - API ও অপশন
st.sidebar.header("⚙️ কনফিগারেশন")
api_key = st.sidebar.text_input("আপনার Gemini API Key দিন:", type="password")

brokers = ["Quotex", "Binola", "Binomo", "Pocket Option", "IQ Option"]
selected_broker = st.sidebar.selectbox("ব্রোকার সিলেক্ট করুন:", brokers)

otc_pairs = [
    "EUR/USD (OTC)", "EUR/GBP (OTC)", "EUR/JPY (OTC)", 
    "USD/BRL (OTC)", "CAD/JPY (OTC)", "AUD/NZD (OTC)", 
    "GBP/USD (OTC)", "USD/RUB (OTC)", "USD/INR (OTC)"
]
selected_pair = st.sidebar.selectbox("OTC পেয়ার সিলেক্ট করুন:", otc_pairs)

# মেইন লেআউট
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📷 চার্ট আপলোড করুন")
    uploaded_file = st.file_uploader("লাইভ চার্টের স্ক্রিনশট দিন", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="আপলোড করা চার্ট", use_container_width=True)

with col2:
    st.subheader("🎯 এআই এনালাইসিস রেজাল্ট")
    
    if uploaded_file and api_key:
        if st.button("🚀 Analyze Market Now", type="primary", use_container_width=True):
            with st.spinner("Gemini AI চার্টের ক্যান্ডেলস্টিক ও সাপোর্ট-রেজিস্ট্যান্স এনালাইসিস করছে..."):
                try:
                    # Gemini API কনফিগারেশন
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    prompt = f"""
                    You are a professional Binary Options Trading Assistant.
                    Analyze this trading chart for broker {selected_broker} and pair {selected_pair}.
                    Look closely at candlestick patterns, support/resistance, and market trend.
                    
                    Provide response strictly in Bengali with:
                    1. PREDICTION: (CALL/UP or PUT/DOWN)
                    2. ESTIMATED CONFIDENCE: (Give realistic accuracy percentage like 70%-85%)
                    3. REASONING: Explain candlestick pattern or indicators visible in image.
                    """
                    
                    response = model.generate_content([prompt, image])
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Error: {e}")
    elif uploaded_file and not api_key:
        st.warning("⚠️ এনালাইসিস শুরু করতে সাইডবারে আপনার Gemini API Key দিন।")
    else:
        st.info("👈 চার্টের স্ক্রিনশট আপলোড করুন এবং কাটার জন্য ×চিহ্ন‌ থাকবে।")

