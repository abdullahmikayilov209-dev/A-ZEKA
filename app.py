import streamlit as st
from groq import Groq
import base64
import time

# ==========================================================
# 1. CSS VƏ VİZUAL AYARLAR (AĞ REJİM + "+" DÜYMƏSİ)
# ==========================================================
st.set_page_config(page_title="Zəka AI: Ultra", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1b1e; }
    .stChatMessage { border-radius: 20px; padding: 20px; border: 1px solid #edf2f7; }
    [data-testid="stChatMessageUser"] { background-color: #f7fafc; }
    [data-testid="stChatMessageAssistant"] { background-color: #ebf8ff; }
    
    /* Sual qutusunun daxili boşluğu */
    .stChatInputContainer textarea { padding-left: 55px !important; }

    /* "+" Düyməsinin dəqiq yerləşdirilməsi (Sənin istədiyin kimi) */
    [data-testid="stFileUploader"] {
        position: fixed;
        bottom: 34px; /* Sual qutusunun tam sol küncü */
        left: 48px;
        width: 40px !important;
        z-index: 1000;
    }
    [data-testid="stFileUploader"] section { padding: 0; border: none; background: transparent; }
    [data-testid="stFileUploader"] label, [data-testid="stFileUploader"] small, [data-testid="stFileUploaderText"] {
        display: none !important;
    }
    [data-testid="stFileUploader"] button {
        background-color: transparent !important;
        border: none !important;
        color: #5f6368 !important;
        font-size: 30px !important;
        font-weight: 200 !important;
        width: 35px !important;
        height: 35px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    [data-testid="stFileUploader"] button div { display: none; }
    [data-testid="stFileUploader"] button::after { content: "+" !important; visibility: visible !important; }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 2. KÖMƏKÇİ FUNKSİYALAR (ŞƏKİL ANALİZİ ÜÇÜN)
# ==========================================================
def encode_image(image_file):
    """Şəkli modelin başa düşəcəyi koda çevirir"""
    return base64.b64encode(image_file.read()).decode('utf-8')

# API setup
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("API Key tapılmadı! Secrets hissəsinə 'GROQ_API_KEY' əlavə edin.")
    st.stop()

# ==========================================================
# 3. İNTERFEYS
# ==========================================================
st.title("🇦🇿 Zəka AI")
st.caption("Müəllif: Abdullah Mikayılov | Vision Modulu Aktivdir")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Söhbət tarixçəsini göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Sənin istədiyin "+" düyməsi (Şəkil seçmək üçün)
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    # Şəkli ekranda balaca göstərək ki, istifadəçi nə yüklədiyini bilsin
    st.sidebar.image(uploaded_file, caption="Analiz ediləcək şəkil", use_container_width=True)
    st.toast("Şəkil analiz üçün hazırdır!")

# ==========================================================
# 4. ANALİZ VƏ CAVAB MƏNTİQİ
# ==========================================================
if prompt := st.chat_input("Sualınızı yazın və ya şəkli analiz etdirin..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Zəka AI düşünür və analiz edir..."):
            try:
                # Ssenari A: İstifadəçi şəkil yükləyib
                if uploaded_file:
                    base64_image = encode_image(uploaded_file)
                    # Vision üçün Llama 3.2 istifadə edirik
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": f"Sən Abdullah Mikayılovun yaratdığı dahi Zəka AI-san. Bu şəkli alim kimi analiz et: {prompt}"},
                                    {
                                        "type": "image_url",
                                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                                    }
                                ]
                            }
                        ],
                        model="llama-3.2-11b-vision-preview",
                    )
                # Ssenari B: Sadəcə mətnlə sual soruşur
                else:
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Sən Abdullah Mikayılovun yaratdığı dahi Zəka AI-san."}
                        ] + st.session_state.messages,
                        model="llama-3.3-70b-versatile",
                    )
                
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"Sistemdə xəta: {str(e)}")
