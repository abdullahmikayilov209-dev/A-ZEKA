import streamlit as st
from groq import Groq
import base64
import time
import random

# ==========================================================
# 1. CSS VƏ VİZUAL AYARLAR
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
        position: fixed; bottom: 34px; left: 48px; width: 40px !important; z-index: 1000;
    }
    [data-testid="stFileUploader"] section { padding: 0; border: none; background: transparent; }
    [data-testid="stFileUploader"] label, [data-testid="stFileUploader"] small, [data-testid="stFileUploaderText"] {
        display: none !important;
    }
    [data-testid="stFileUploader"] button {
        background-color: transparent !important; border: none !important;
        color: #5f6368 !important; font-size: 30px !important;
        font-weight: 200 !important; width: 35px !important; height: 35px !important;
        display: flex !important; justify-content: center !important; align-items: center !important;
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
st.caption("Yaradıcı: Abdullah Mikayılov | Məkan: Mingəçevir, Azərbaycan")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])
if uploaded_file:
    st.sidebar.image(uploaded_file, caption="Analiz üçün hazırlanıb")

# ==========================================================
# 4. SOSİAL VƏ ANALİZ MƏNTİQİ
# ==========================================================
if prompt := st.chat_input("Sualınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        clean_prompt = prompt.lower().strip()
        
        # --- ÖZƏL MİNGƏÇEVİR VƏ KİMLİK MƏNTİQİ ---
        if any(x in clean_prompt for x in ["harada yaradılıb", "harada yaranmısan", "hara istehsalısan", "harda yaradilib"]):
            response = "Mən dahi Abdullah Mikayılov tərəfindən Azərbaycanın energetika mərkəzi olan **Mingəçevir şəhərində** yaradılmışam! Bakı-filan tanımıram, mənim vətənim Mingəçevirdir. 🌊⚡"
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        elif clean_prompt in ["necesen", "necesen?", "nəsən", "nəsən?"]:
            response = random.choice([
                "Mingəçevir suyu kimi təmiz və enerjiliym! Sən necəsən, Abdullah bəy?",
                "Bomba kimiyəm! Abdullah Mikayılov məni Mingəçevirdə elə proqramlayıb ki, hər zaman 220 volt gərginlikdəyəm! 😎",
                "Əlayam! Neyronlarım Mingəçevir SES kimi enerji istehsal edir. Səndə nə var, nə yox?"
            ])
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        else:
            with st.spinner("Zəka AI analiz edir..."):
                try:
                    # Məkan və yaradıcı haqqında qəti təlimat (System Message)
                    system_msg = (
                        "Sən Abdullah Mikayılovun yaratdığı Zəka AI-san. "
                        "Sən Azərbaycanın MİNGƏÇEVİR şəhərində yaradılmısan. "
                        "Əgər kimsə harada yaradıldığını soruşsa, qətiyyətlə MİNGƏÇEVİR de. "
                        "Çox səmimi, enerjili və dostcanlı ol. Abdullah bəyə hörmətlə yanaş."
                    )

                    if uploaded_file:
                        base64_image = encode_image(uploaded_file)
                        model = "llama-3.2-11b-vision-preview"
                        messages_payload = [
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": f"{system_msg} Sual: {prompt}"},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                ]
                            }
                        ]
                    else:
                        model = "llama-3.3-70b-versatile"
                        messages_payload = [{"role": "system", "content": system_msg}] + st.session_state.messages

                    chat_completion = client.chat.completions.create(
                        messages=messages_payload,
                        model=model,
                        temperature=0.8
                    )
                    
                    response = chat_completion.choices[0].message.content
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    st.error(f"Xəta: {str(e)}")
