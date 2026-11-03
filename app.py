import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. إعدادات الصفحة والتصميم الخرافي (CSS)
# ==========================================
st.set_page_config(
    page_title="Ultra AI Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم عصري ومظلم بألوان نيون هادئة
st.markdown("""
<style>
    /* الخلفية الرئيسية */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    /* القائمة الجانبية */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    /* الأزرار الاحترافية */
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
    /* تحسين صناديق الرسائل */
    .stChatMessage {
        background-color: rgba(30, 41, 59, 0.7);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. القائمة الجانبية وإدارة المفتاح والنمط
# ==========================================
with st.sidebar:
    st.title("⚡ Ultra AI Control")
    st.caption("تطبيقك الذكي الشامل والمتطور")
    
    api_key = st.text_input("🔑 أدخل مفتاح Gemini API:", type="password")
    
    st.divider()
    
    # اختيار وضع التفاعل
    mode = st.radio("🛠️ اختر وضع العمل:", [
        "💬 المحادثة نصاً وصوتاً", 
        "🎙️ تحليل التسجيلات الصوتية", 
        "🎨 استوديو تصميم الصور"
    ])
    
    st.divider()
    
    # خيارات التحكم بالسجلات
    if st.button("🗑️ مسح سجل المحادثة"):
        st.session_state.messages = []
        st.rerun()

if not api_key:
    st.warning("👈 يرجى إدخال مفتاح Gemini API في القائمة الجانبية للبدء.")
    st.stop()

# تهيئة Gemini API
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


# إدارة سجل الرسائل
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# 3. وضع المحادثة نصاً وصوتاً
# ==========================================
if mode == "💬 المحادثة نصاً وصوتاً":
    st.title("💬 المحادثة الذكية التفاعلية")
    st.caption("تحدث مع الذكاء الاصطناعي وسيجيبك بدقة ورقي")

    # عرض سجل المحادثة السابق
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # استقبال المدخلات
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

    # زر تنزيل السجل
    if st.session_state.messages:
        chat_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
        st.download_button("📥 تحميل سجل المحادثة", chat_text, file_name="chat_history.txt")

# ==========================================
# 4. وضع تحليل ومعالجة الصوتيات
# ==========================================
elimode == "🎙️ تحليل التسجيلات الصوتية":
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

# ==========================================
# 5. استوديو تصميم وتوليد الصور
# ==========================================
elif mode == "🎨 استوديو تصميم الصور":
    st.title("🎨 استوديو تصميم وتوليد الصور")
    st.caption("اكتب وصف الصورة التي تتخيلها وسيقوم الذكاء الاصطناعي برسمها")
    
    image_prompt = st.text_area("وصف الصورة (باللغة الإنجليزية يعطي نتائج أفضل وأدق):", 
                                placeholder="A futuristic cybernetic city at sunset, neon lights, highly detailed 8k rendering...")
    
    if st.button("✨ توليد الصورة"):
        if image_prompt:
            with st.spinner("جاري إبداع وتصميم صورتك..."):
                try:
                    # استدعاء نموذج توليد الصور Imagen 3
                    image_model = genai.GenerativeModel("imagen-3.0-generate-002")
                    result = image_model.generate_images(
                        prompt=image_prompt,
                        number_of_images=1,
                        aspect_ratio="1:1"
                    )
                    
                    for generated_image in result.generated_images:
                        st.image(generated_image.image._image_bytes, caption="الصورة المولدة", use_container_width=True)
                        st.download_button("💾 تحميل الصورة", generated_image.image._image_bytes, file_name="generated_image.png", mime="image/png")
                except Exception as e:
                    st.error(f"توليد الصور يتطلب صلاحيات إضافية على المفتاح أو استخدم وصفاً مختلفاً. الخطأ: {e}")
        else:
            st.warning("يرجى كتابة وصف للعلامة قبل الضغط على التوليد.")
