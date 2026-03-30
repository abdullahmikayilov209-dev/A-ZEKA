import streamlit as st
from groq import Groq
import base64

# ==========================================================
# 1. API SETUP
# ==========================================================
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("API Key tapılmadı!")
    st.stop()

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# ==========================================================
# 2. BÜTÜN ARTIQ YAZILARI (BROWSE FİLES+) SİLƏN CSS
# ==========================================================
st.markdown("""
    <style>
    /* Sual qutusunun solunda yer açırıq */
    .stChatInputContainer textarea { padding-left: 50px !important; }

    /* Uploader-i sual qutusunun üzərinə bərkidirik */
    [data-testid="stFileUploader"] {
        position: fixed;
        bottom: 33px !important; 
        left: 45px !important;
        width: 40px !important;
        z-index: 1000000 !important;
    }

    /* BÜTÜN ARTIQ YAZILARI VƏ ÇƏRÇİVƏNİ SİLİRİK */
    [data-testid="stFileUploader"] section {
        padding: 0 !important;
        border: none !important;
        background: transparent !important;
    }
    
    /* HAMISINI GİZLƏDİRİK: Drag-drop, Browse files, Limit, və s. */
    [data-testid="stFileUploader"] label, 
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploaderText"],
    [data-testid="stFileUploaderDropzoneInstructions"],
    .st-emotion-cache-1ae8k9d, 
    .st-emotion-cache-9ycgxx,
    .st-emotion-cache-629ovp,
    .st-emotion-cache-1vt4yug { /* O inadkar 'browse files' yazısı üçün əlavə class */
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }

    /* Düyməni sadəcə bir "+" simvolu edirik */
    [data-testid="stFileUploader"] button {
        background-color: transparent !important;
        border: none !important;
        color: #5f6368 !important;
        font-size: 35px !important; 
        font-weight: 100 !important;
        width: 40px !important;
        height: 40px !important;
        box-shadow: none !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }

    /* Düymənin daxilindəki HƏR ŞEYİ silirik */
    [data-testid="stFileUploader"] button * {
        display: none !important;
    }
    
    /* Düyməyə təmiz "+" əlavə edirik */
    [data-testid="stFileUploader"] button::after {
        content: "+" !important;
        visibility: visible !important;
        display: block !important;
        position: absolute !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 3. İNTERFEYS
# ==========================================================
st.title("🇦🇿 Zəka AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# BALACA "+" DÜYMƏSİ
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], key="plus_btn")

if uploaded_file:
    st.toast("Şəkil seçildi!")

# ==========================================================
# 4. SÖHBƏT (accept_file=True ilə)
# ==========================================================
prompt = st.chat_input("Dahi alimə sual ver və ya '+' vurub şəkil at...", accept_file=True)

if prompt:
    user_text = prompt.text
    active_file = None
    if prompt.files:
        active_file = prompt.files[0]
    elif uploaded_file:
        active_file = uploaded_file

    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        try:
            if active_file:
                base64_image = encode_image(active_file)
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": user_text},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                                },
                            ],
                        }
                    ],
                    model="llama-3.2-11b-vision-preview",
                )
            else:
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "system", "content": "Sən Mingəçevirdə Abdullah tərəfindən yaradılan Zəka AI-san."}] + st.session_state.messages,
                    model="llama-3.3-70b-versatile",
                )
            
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        except Exception as e:
            st.error(f"Xəta: {str(e)}")
