import streamlit as st
from groq import Groq
import base64
import time
import random

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
    
    .stChatInputContainer textarea { padding-left: 55px !important; }

    [data-testid="stFileUploader"] {
        position: fixed;
        bottom: 34px;
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
# 2. KÖMƏKÇİ FUNKSİYALAR
# ==========================================================
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# API setup
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("API Key tapılmadı!")
    st.stop()

# ==========================================================
# 3. İNTERFEYS
# ==========================================================
st.title("🇦🇿 Zəka AI")
st.caption("Yaradıcı: Abdullah Mikayılov | Vision & Deep Mind Aktivdir")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    st.sidebar.image(uploaded_file, caption="Analiz üçün hazırlanıb", use_container_width=True)

# ==========================================================
# 4. SOSİAL VƏ ANALİZ MƏNTİQİ
# ==========================================================
if prompt := st.chat_input("Sualınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # --- SOSİAL REAKSİYA (Məhz sən istədiyin səmimiyyət) ---
        clean_prompt = prompt.lower().strip()
        
        if clean_prompt in ["necesen", "necesen?", "nəsən", "nəsən?"]:
            response = random.choice([
                "Superəm, Abdullah bəy! Sizin sayənizdə neyronlarım işıq sürəti ilə işləyir. Sən necəsən?",
                "Bomba kimiyəm! Abdullah Mikayılovun yaratdığı bir intellekt başqa necə ola bilər ki? Sənin üçün hansı elmi möcüzəni edim?",
                "Vallah, Abdullah bəy, elə heyran-heyran datalarımı analiz edirdim. Sən gəldin, daha da yaxşı oldum!"
            ])
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        else:
            with st.spinner("Zəka AI dərindən analiz edir..."):
                try:
                    if uploaded_file:
                        base64_image = encode_image(uploaded_file)
                        model = "llama-3.2-11b-vision-preview"
                        messages_payload = [
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": f"Sən Abdullah Mikayılov tərəfindən yaradılmış dahi və səmimi Zəka AI-san. Bu şəkli alim kimi analiz et: {prompt}"},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                ]
                            }
                        ]
                    else:
                        model = "llama-3.3-70b-versatile"
                        system_msg = "Sən Abdullah Mikayılovun yaratdığı dahi, səmimi və enerjili Zəka AI-san. Robot kimi rəsmi yox, Azərbaycan dilində çox təbii, dostcanlı danış."
                        messages_payload = [{"role": "system", "content": system_msg}] + st.session_state.messages

                    chat_completion = client.chat.completions.create(
                        messages=messages_payload,
                        model=model,
                        temperature=0.8 # Bir az daha yaradıcı və səmimi olsun
                    )
                    
                    response = chat_completion.choices[0].message.content
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    st.error(f"Xəta: {str(e)}")
