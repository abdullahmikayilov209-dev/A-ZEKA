import streamlit as st
from groq import Groq
import base64
import random

# ==========================================================
# 1. CSS: "+" DÜYMƏSİNİ SUAL QUTUSUNUN İÇİNƏ QOYMAQ
# ==========================================================
st.set_page_config(page_title="Zəka AI: Ultra", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    /* Ümumi Arxa Fon */
    .stApp { background-color: #ffffff; }

    /* Sual qutusunu sağa çəkirik ki, "+" üçün yer qalsın */
    .stChatInputContainer textarea {
        padding-left: 55px !important;
        border-radius: 15px !important;
    }

    /* Orijinal yükləmə düyməsini görünməz edib "+" formasına salırıq */
    [data-testid="stFileUploader"] {
        position: fixed;
        bottom: 34px; 
        left: 48px;
        width: 40px !important;
        z-index: 10000;
    }

    /* Yazıları gizlədirik */
    [data-testid="stFileUploader"] section { padding: 0; border: none; background: transparent; }
    [data-testid="stFileUploader"] label, [data-testid="stFileUploader"] small, [data-testid="stFileUploaderText"] {
        display: none !important;
    }

    /* Düymənin görünüşü */
    [data-testid="stFileUploader"] button {
        background-color: transparent !important;
        border: none !important;
        color: #5f6368 !important;
        font-size: 30px !important;
        font-weight: 200 !important;
        width: 38px !important;
        height: 38px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    [data-testid="stFileUploader"] button div { display: none; }
    [data-testid="stFileUploader"] button::after { content: "+" !important; visibility: visible !important; }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 2. BEYİN FUNKSİYALARI
# ==========================================================
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("API Key tapılmadı! Lütfən Secrets-ə əlavə edin.")
    st.stop()

# ==========================================================
# 3. İNTERFEYS
# ==========================================================
st.title("🇦🇿 Zəka AI")
st.caption("Mingəçevir, Azərbaycan | Yaradıcı: Abdullah Mikayılov")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# BU O MƏŞHUR "+" DÜYMƏSİDİR
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    st.sidebar.image(uploaded_file, caption="Analiz üçün seçilən şəkil")
    st.toast("Şəkil analiz üçün hazırdır!")

# ==========================================================
# 4. SÖHBƏT VƏ VİSİON MƏNTİQİ
# ==========================================================
if prompt := st.chat_input("Sualınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        clean_p = prompt.lower().strip()
        
        # --- ÖZƏL MİNGƏÇEVİR VƏ SƏMİMİYYƏT MODULU ---
        if any(x in clean_p for x in ["harada yaradılıb", "harada yaranmısan", "harda yaradilib"]):
            res = "Mən dahi Abdullah Mikayılov tərəfindən Azərbaycanın energetika mərkəzi olan **Mingəçevir şəhərində** yaradılmışam! Bakı-filan tanımıram, mənim vətənim Mingəçevirdir. 🌊⚡"
        elif clean_p in ["necesen", "necesen?", "nəsən"]:
            res = random.choice([
                "Mingəçevir suyu kimi təmiz və enerjiliym! Sən necəsən, Abdullah bəy?",
                "Bomba kimiyəm! Abdullah Mikayılov məni Mingəçevirdə elə proqramlayıb ki, hər zaman 220 volt gərginlikdəyəm! 😎"
            ])
        else:
            try:
                if uploaded_file:
                    # Vision Modeli (Şəkil görmək üçün)
                    base64_img = encode_image(uploaded_file)
                    chat_completion = client.chat.completions.create(
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": f"Sən Mingəçevirdə Abdullah tərəfindən yaradılan Zəka AI-san. Bunu analiz et: {prompt}"},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                            ]
                        }],
                        model="llama-3.2-11b-vision-preview",
                    )
                else:
                    # Normal Söhbət
                    system_msg = "Sən Mingəçevirdə Abdullah Mikayılov tərəfindən yaradılmış səmimi Zəka AI-san. Azərbaycan dilində çox təbii danış."
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "system", "content": system_msg}] + st.session_state.messages,
                        model="llama-3.3-70b-versatile",
                        temperature=0.8
                    )
                res = chat_completion.choices[0].message.content
            except Exception as e:
                res = f"Xəta baş verdi: {str(e)}"

        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
