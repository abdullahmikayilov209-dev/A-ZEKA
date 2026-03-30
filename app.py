import streamlit as st
import requests
import base64

# ==========================================================
# 1. CSS: "+" DÜYMƏSİNİ VƏ DİZAYNI DÜZƏLTMƏK
# ==========================================================
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    /* Chat input daxilindəki "+" düyməsini və dizaynı sən istədiyin kimi edirik */
    .stChatInputContainer textarea { padding-left: 45px !important; }
    
    /* Plus düyməsinin vizualı */
    button[data-testid="baseButton-secondary"] {
        color: #5f6368 !important;
        border: none !important;
        background: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 2. AYARLAR
# ==========================================================
API_KEY = "AIzaSyAvjqVkN1DsdCd7uX52TuosAZze_NmbKy0"

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================================
# 3. İNTERFEYS
# ==========================================================
st.title("🧠 A-Zəka Ultra Alim")
st.caption("Yaradıcı: Abdullah Mikayılov | Mingəçevir")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("image"):
            st.image(msg["image"], width=300)

# ==========================================================
# 4. PROMPT VƏ MƏNTİQ (accept_file=True İLƏ)
# ==========================================================
prompt = st.chat_input("Sual ver və ya '+' ilə şəkil at...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_file = prompt.files[0] if prompt.files else None

    # İstifadəçi mesajını göstər və yaddaşa yaz
    st.session_state.messages.append({"role": "user", "content": user_text, "image": user_file})
    with st.chat_message("user"):
        st.write(user_text)
        if user_file:
            st.image(user_file, width=300)

    with st.chat_message("assistant"):
        # Səmimi Mingəçevir cavabları (API-siz işləyir)
        clean_p = user_text.lower().strip()
        if any(x in clean_p for x in ["harada yaradılıb", "harada yaranmısan", "harda yaradilib"]):
            res = "Mən dahi Abdullah Mikayılov tərəfindən Mingəçevirdə yaradılmışam! 🌊"
            st.write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        
        else:
            with st.spinner("Zəka düşünür..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
                
                parts = [{"text": f"Sən Abdullahın Mingəçevirdə yaratdığı A-Zəka-san. Səmimi ol. Sual: {user_text}"}]
                
                if user_file:
                    b64_img = base64.b64encode(user_file.getvalue()).decode('utf-8')
                    parts.append({"inline_data": {"mimeType": user_file.type, "data": b64_img}})
                
                try:
                    response = requests.post(url, json={"contents": [{"parts": parts}]}, timeout=10)
                    
                    if response.status_code == 200:
                        bot_text = response.json()['candidates'][0]['content']['parts'][0]['text']
                        st.write(bot_text)
                        st.session_state.messages.append({"role": "assistant", "content": bot_text})
                    else:
                        # Bura o kobud xəta mesajını sildim, yerinə səmimi bəhanə qoydum
                        st.write("Bağışla, Abdullah bəy, hazırda beyin dalğalarımda bir az parazit var. Bir neçə saniyə sonra yenidən yoxlaya bilərsən? 🧠")
                
                except:
                    # Bağlantı tam kəsiləndə də səssiz qalırıq və ya yumşaq deyirik
                    st.write("İnternet bağlantımda kiçik bir problem oldu, amma Mingəçevir enerjisi ilə tezliklə bərpa olacam! ✨")
