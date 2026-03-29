import streamlit as st
from groq import Groq

# API Quraşdırılması
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("Xəta: GROQ_API_KEY tapılmadı! Secrets bölməsini yoxla.")
    st.stop()

client = Groq(api_key=api_key)

st.set_page_config(page_title="Zəka AI", page_icon="🇦🇿")

# --- GEMINI STİLİNDƏ DÜYMƏ ÜÇÜN XÜSUSİ CSS ---
st.markdown("""
    <style>
    /* 1. Sual qutusunun içinə soldan boşluq veririk ki, yazı düyməyə dəyməsin */
    [data-testid="stChatInput"] textarea {
        padding-left: 48px !important;
    }

    /* 2. Yükləmə qutusunu tam sual yazılan yerin üstünə, sol küncə gətiririk */
    [data-testid="stFileUploader"] {
        position: fixed;
        bottom: 30px; /* Sual qutusunun hündürlüyünə görə (əgər yuxarıda qalsa, 25px elə) */
        z-index: 999999;
        width: 40px !important;
    }

    /* 3. Ekranın ölçüsünə görə düymənin yerini tənzimləyirik (Mobil vs PC) */
    @media (min-width: 768px) {
        [data-testid="stFileUploader"] {
            left: calc(50% - 340px); /* Kompüterdə genişliyə görə tənzimləmə */
        }
    }
    @media (max-width: 767px) {
        [data-testid="stFileUploader"] {
            left: 20px; /* Telefonda tam sol küncə yapışsın */
        }
    }

    /* 4. Yükləmə qutusunun lazımsız "Browse files" yazılarını və xətlərini gizlədirik */
    [data-testid="stFileUploader"] section {
        padding: 0 !important;
        border: none !important;
        background: transparent !important;
    }
    [data-testid="stFileUploader"] label, 
    [data-testid="stFileUploader"] small {
        display: none !important;
    }

    /* 5. Düyməni şəkildəki kimi sadə və yuvarlaq "+" edirik */
    [data-testid="stFileUploader"] button {
        border-radius: 50% !important;
        width: 36px !important;
        height: 36px !important;
        min-height: 36px !important;
        padding: 0 !important;
        background: transparent !important;
        border: none !important;
        color: #5f6368 !important; /* Gemini-dəki tünd boz rəng */
        font-size: 26px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        transition: background-color 0.2s;
    }
    [data-testid="stFileUploader"] button:hover {
        background-color: #f0f2f6 !important; /* Üzərinə gələndə rəngi dəyişsin */
    }
    [data-testid="stFileUploader"] button span {
        display: none !important; /* Əsl yazını silirik */
    }
    [data-testid="stFileUploader"] button::after {
        content: "＋" !important;
        font-weight: 300 !important;
        margin-top: -2px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🇦🇿 Zəka AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları ekrana çıxar
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.text(message["content"]) # Sualındakı riyazi simvollar dağılmasın deyə
        else:
            st.markdown(message["content"])

# "+" Düyməsi (CSS ilə yeri dəyişdirilib, sən görməsən də kodda buradadır)
uploaded_file = st.file_uploader("Gizli_Yükləyici", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    st.info("📷 Şəkil yaddaşa alındı! İndi sualınızı yazın və göndərin.")

# Sual qutusu
if prompt := st.chat_input("Sualınızı bura yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.text(prompt)

    with st.chat_message("assistant"):
        try:
            # Əgər şəkil yüklənibsə Vision modelini işə sal, yoxsa normalını
            model = "llama-3.2-11b-vision-preview" if uploaded_file else "llama-3.3-70b-versatile"
            
            chat_completion = client.chat.completions.create(
                messages=[{"role": "system", "content": "Sən Zəka AI-san. Qısa, net və ağıllı cavablar ver."}] + st.session_state.messages,
                model=model,
            )
            response = chat_completion.choices[0].message.content
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Xəta baş verdi: {str(e)}")
