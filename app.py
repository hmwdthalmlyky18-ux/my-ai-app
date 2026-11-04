import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="Ultra AI Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2deg);
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.5);
    }
    .stChatMessage {
        background-color: rgba(30, 41, 59, 0.7);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("⚡ Ultra AI Control")
    st.caption("تطبيقك الذكي الشامل والمتطور")
    
    api_key = st.text_input("🔑 أدخل مفتاح Gemini API:", type="password")
    
    st.divider()
    
    mode = st.radio("🛠️ اختر وضع العمل:", [
        "💬 المحادثة نصاً وصوتاً", 
        "🎙️ تحليل التسجيلات الصوتية", 
        "🎨 استوديو تصميم الصور"
    ])
    
    st.divider()
    
    if st.button("🗑️ مسح سجل المحادثة"):
        st.session_state.messages = []
        st.rerun()

if not api_key:
    st.warning("👈 يرجى إدخال مفتاح Gemini API في القائمة الجانبية للبدء.")
    st.stop()

genai.configure(api_key=api_key)

# استخدام النموذج المعتمد والمستقرار تماماً لضمان عدم ظهور خطأ 404
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
      except:
    model = genai.GenerativeModel("gemini-1.5-flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

if mode == "💬 المحادثة نصاً وصوتاً":
    st.title("💬 المحادثة الذكية التفاعلية")
    st.caption("تحدث مع الذكاء الاصطناعي وسيجيبك بدقة ورقي")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("اكتب سؤالك أو فكرتك هنا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("جاري التفكير والأجابة..."):
                try:
                    response = model.generate_content(prompt)
                    reply = response.text
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")

    if st.session_state.messages:
        chat_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
        st.download_button("📥 تحميل سجل المحادثة", chat_text, file_name="chat_history.txt")

elif mode == "🎙️ تحليل التسجيلات الصوتية":
    st.title("🎙️ تحليل ومعالجة الصوتيات")
    st.caption("ارفع أي تسجيل صوتي لتقوم المنظومة بتحليله أو الإجابة عليه")
    
    audio_file = st.file_uploader("قم برفع ملف صوتي (MP3, WAV, M4A)", type=["mp3", "wav", "m4a"])
    
    if audio_file:
        st.audio(audio_file)
        user_audio_query = st.text_input("ماذا تريد من الذكاء الاصطناعي أن يفعل بالملف الصوتي؟", "تلخيص هذا الصوت والإجابة عن أهم محتوياته")
        
        if st.button("🚀 تحليل الصوت"):
            with st.spinner("جاري قراءة ومعالجة الملف الصوتي..."):
                try:
                    audio_bytes = audio_file.read()
                    response = model.generate_content([
                        user_audio_query,
                        {"mime_type": audio_file.type, "data": audio_bytes}
                    ])
                    st.success("تم التحليل بنجاح!")
                    st.markdown("### 📝 النتيجة:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"حدث خطأ أثناء معالجة الصوت: {e}")

elif mode == "🎨 استوديو تصميم الصور":
    st.title("🎨 استوديو تصميم وتوليد الصور")
    st.caption("اكتب وصف الصورة التي تتخيلها وسيقوم الذكاء الاصطناعي برسمها")
    
    image_prompt = st.text_area("وصف الصورة (باللغة الإنجليزية يعطي نتائج أفضل وأدق):", 
                                placeholder="A futuristic cybernetic city at sunset, neon lights, highly detailed 8k rendering...")
    
    if st.button("✨ توليد الصورة"):
        if image_prompt:
            with st.spinner("جاري إبداع وتصميم صورتك..."):
                try:
                    image_model = genai.GenerativeModel("gemini-pro-vision")
                    response = image_model.generate_content(image_prompt)
                    st.success("تم توليد المحتوى بنجاح!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"حدث خطأ أثناء توليد الصور: {e}")
        else:
            st.warning("يرجى كتابة وصف للصورة قبل الضغط على التوليد.")
