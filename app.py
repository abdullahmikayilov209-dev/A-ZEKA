import streamlit as st
import time
import math
import random

# ==========================================================
# 1. ULTRALIGHT VİZUAL DİZAYN (PROFESSİONAL AĞ REJİM)
# ==========================================================
st.set_page_config(page_title="A-Zeka Ultra: Qlobal Zəka", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1b1e; }
    .stChatMessage { border-radius: 20px; padding: 20px; margin-bottom: 15px; border: 1px solid #edf2f7; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    [data-testid="stChatMessageUser"] { background-color: #f7fafc; border-right: 5px solid #cbd5e0; }
    [data-testid="stChatMessageAssistant"] { background-color: #ebf8ff; border-left: 5px solid #3182ce; }
    .main-title { font-size: 50px; font-weight: 900; color: #2b6cb0; text-align: center; letter-spacing: -1px; }
    .scientist-badge { background-color: #3182ce; color: white; padding: 5px 15px; border-radius: 50px; font-size: 14px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================================
# 2. NEHENG ELMİ ARXİV (BÜTÜN FƏNLƏR - ALİM SƏVİYYƏSİ)
# ==========================================================
# Bu bölmə A-Zeka-nın "Daxili Beyni"dir. İnternetsiz belə bunları bilir.

ALIM_BEYNI = {
    "riyaziyyat": {
        "cebr": "Viyet ($x_1+x_2=-b/a$), Diskriminant ($D=b^2-4ac$), Loqarifma ($\log_a b$), Funksiya.",
        "hendese": "Pifaqor ($a^2+b^2=c^2$), Heron ($S=\sqrt{p(p-a)(p-b)(p-c)}$), Sinuslar teoremi.",
        "analiz": "Törəmə ($f'(x)$), İnteqral ($\int$), Limit, Diferensial tənliklər.",
        "ehtimal": "Klassik ehtimal $P(A)=m/n$, Kombinezon, Permutasiya."
    },
    "fizika": {
        "mexanika": "Nyuton qanunları ($F=ma$), Enerjinin saxlanması, İmpuls.",
        "kvant": "Şrödinger tənliyi, Heyzenberq qeyri-müəyyənliyi, Fotoeffekt.",
        "optika": "İşığın sınması, Linzalar, Difraksiya və İnterferensiya.",
        "astronomiya": "Böyük partlayış, Qara dəliklər, Qalaktikalar, Doppler effekti."
    },
    "kimya": {
        "elementler": "118 element (H, He, Li, Be, B, C, N, O, F, Ne...)",
        "reaksiyalar": "Oksidləşmə-reduksiya, Elektroliz, Termokimya.",
        "orqanik": "Alkanlar, Alkenler, Alkinler, Aromatik birləşmələr (Benzol).",
        "laboratoriya": "Titrləmə, Distillə, Kristallaşma prosesləri."
    },
    "biologiya": {
        "genetika": "DNT, RNT, Mendel qanunları, Mutasiyalar.",
        "anatomiya": "Sinir sistemi, Qan dövranı, Skelet və Əzələ quruluşu.",
        "sitologiya": "Hüceyrə membranı, Mitoxondri, Ribosom, Holci aparatı.",
        "botanika": "Fotosintez, Transpirasiya, Bitki toxumaları."
    },
    "tarix_cografiya": {
        "azerbaycan": "Səfəvilər (1501), ADR (1918), Qarabağ Zəfəri (2020).",
        "dunya": "Roma İmperiyası, İntibah dövrü, I və II Dünya Müharibələri.",
        "iqlim": "Tropik, Subtropik, Mülayim və Arktik iqlim qurşaqları.",
        "geopolitika": "BMT, NATO, Avropa İttifaqı, İqtisadi ittifaqlar."
    }
}

# ==========================================================
# 3. ANALİZ VƏ DÜŞÜNCƏ MODULU (AI LOGIC)
# ==========================================================
def analiz_et(sual):
    sual = sual.lower()
    
    # 1. Salamlaşma Analizi
    if any(x in sual for x in ["salam", "hey", "merhaba"]):
        return "Salam, Abdullah Mikayılov! Mən A-Zeka-yam. Bütün neyronlarım aktivdir. Hansı elmi müzakirəyə başlayaq?"

    # 2. Elmi Sahə Analizi (A-Zeka burada "düşünür")
    for sahe, alt_saheler in ALIM_BEYNI.items():
        if sahe in sual:
            detal = " | ".join([f"**{k.upper()}**: {v}" for k, v in alt_saheler.items()])
            return f"**{sahe.upper()} ANALİZİ:**\n\nBu sahədəki dərin biliklərim bunlardır:\n{detal}"
    
    # 3. Hesablama Analizi
    if any(c.isdigit() for c in sual) and any(op in sual for op in "+-*/^"):
        try:
            # Riyazi ifadəni təmizlə və hesabla
            if "x" in sual: sual = sual.replace("x", "*")
            if "^" in sual: sual = sual.replace("^", "**")
            res = eval("".join(c for c in sual if c in "0123456789+-*/.**() "))
            return f"**Riyazi Analiz Hesabatı:** Sənin üçün hesabladım: **{res}**"
        except:
            return "Riyazi ifadə mürəkkəbdir, zəhmət olmasa dəqiqləşdir."

    # 4. Əgər sual tapılmazsa (Mənim kimi "düşünməsi" üçün random elmi fakt)
    faktlar = [
        "Kainatın 95%-i qaranlıq maddə və qaranlıq enerjidən ibarətdir. Biz yalnız 5%-i görürük.",
        "İnsan bədənindəki atomların böyük hissəsi milyardlarla il əvvəl ulduzların partlamasından yaranıb.",
        "Riyaziyyatda '0' (sıfır) rəqəmi olmasaydı, müasir texnologiya mövcud olmazdı."
    ]
    return f"Abdullah bəy, '{sual}' mövzusunu hazırda analiz edirəm. Amma bilməlisən ki: {random.choice(faktlar)}"

# ==========================================================
# 4. İNTERFEYS (FRONT-END)
# ==========================================================
st.markdown('<p class="main-title">A-ZEKA ULTRA</p>', unsafe_allow_html=True)
st.markdown('<center><span class="scientist-badge">AZƏRBAYCANIN ƏN GÜCLÜ İNTELLEKTİ</span></center>', unsafe_allow_html=True)
st.write("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları göstər
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Giriş sahəsi
if prompt := st.chat_input("Dahiyanə bir sual yaz və ya mənimlə söhbət et..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("A-Zeka analiz edir..."):
            time.sleep(0.5) # Analiz simulyasiyası
            cavab = analiz_et(prompt)
            st.markdown(cavab)
            st.session_state.messages.append({"role": "assistant", "content": cavab})

# [Burada kod 600 sətirə qədər elmi sənədlərlə davam edə bilər...]
