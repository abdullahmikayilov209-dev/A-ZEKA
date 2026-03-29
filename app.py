import streamlit as st
import random

# ==========================================================
# 1. ULTRALIGHT DİZAYN (Ağ və Professional)
# ==========================================================
st.set_page_config(page_title="A-Zeka: Qlobal Alim", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1a1a; }
    .stChatMessage { border-radius: 15px; padding: 18px; margin-bottom: 12px; border: 1px solid #dee2e6; font-family: 'Segoe UI', sans-serif; }
    [data-testid="stChatMessageUser"] { background-color: #f1f3f5; border-left: 5px solid #6c757d; }
    [data-testid="stChatMessageAssistant"] { background-color: #e7f3ff; border-left: 5px solid #007bff; }
    .header-text { font-size: 42px; font-weight: 800; color: #0056b3; text-align: center; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="header-text">🧠 A-ZEKA: GLOBAL SCIENTIST</p>', unsafe_allow_html=True)
st.sidebar.markdown("<h2 style='text-align: center;'>A-Zeka Lab</h2>", unsafe_allow_html=True)
st.sidebar.write("---")
st.sidebar.success("Yaradıcı: Abdullah Mikayılov")
st.sidebar.info("Səviyyə: Universal Alim (Bütün Fənlər)")

# ==========================================================
# 2. MULTİ-FƏNN BİLGİ BAZASI (Nəhəng Alim Yaddaşı)
# ==========================================================
DATA_BASE = {
    # RİYAZİYYAT
    "riyaziyyat": "Riyaziyyat kainatın dilidir. Pifaqor: $a^2+b^2=c^2$, Viyet: $x_1+x_2=-b/a$, Törəmə: $(x^n)'=nx^{n-1}$, İnteqral: $\int x^n dx$.",
    # FİZİKA
    "fizika": "Fizika maddə və enerjini öyrənir. Nyuton: $F=ma$, Eynşteyn: $E=mc^2$, Om qanunu: $I=U/R$, Kvant: $E=hf$.",
    # KİMYA
    "kimya": "Kimya maddələrin tərkibidir. Periyodik cədvəl 118 elementdən ibarətdir. Su: $H_2O$, Sulfat turşusu: $H_2SO_4$, Metan: $CH_4$.",
    # BİOLOGİYA
    "biologiya": "Biologiya həyat elmidir. DNT həyatın kodudur. Mitoxondri hüceyrənin enerji mərkəzidir. Fotosintez: $6CO_2 + 6H_2O \\to C_6H_{12}O_6 + 6O_2$.",
    # TARİX
    "tarix": "Tarix bəşəriyyətin yaddaşıdır. 1501 Səfəvilər, 1918 ADR-in qurulması, 1945 II Dünya Müharibəsinin sonu.",
    # COĞRAFİYA
    "coğrafiya": "Yer kürəsi 7 qitədən ibarətdir. Ən hündür zirvə Everest (8848m), ən dərin yer Marian çökəkliyi (11022m).",
    # ASTRONOMİYA
    "astronomiya": "Kainat 13.8 milyard yaşındadır. Günəş sistemi 8 planetdən ibarətdir. Süd yolu bizim qalaktikamızdır."
}

# ==========================================================
# 3. İMKANSIZ SUALLAR (Alim Təfəkkürü)
# ==========================================================
IMPOSSIBLE_FACTS = [
    "İşıq sürəti saniyədə 299,792,458 metrdir. Heç bir kütləsi olan cisim bu sürəti keçə bilməz.",
    "İnsan beyni hər saniyədə 11 milyon bit məlumat qəbul edir, lakin yalnız 40 bitini dərk edir.",
    "Mütləq sıfır temperaturu (-273.15°C) maddənin hərəkətinin dayandığı nöqtədir.",
    "Əgər Günəş indi sönsə, biz bunu yalnız 8 dəqiqə 20 saniyə sonra biləcəyik."
]

# ==========================================================
# 4. CHAT SİSTEMİ
# ==========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("İstənilən fəndən sual ver..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    soru = prompt.lower().strip()
    
    with st.chat_message("assistant"):
        found = False
        
        # SALAMLAŞMA
        if any(x in soru for x in ["salam", "merhaba", "hey"]):
            cavab = "Salam, hörmətli elm adamı Abdullah! Mən A-Zeka Universal. Hansı fəndən araşdırma edək?"
            found = True
        elif "necesen" in soru:
            cavab = "Sistemlərim stabil, bilik bazam yenilənib. Sizin üçün hazıram!"
            found = True
            
        # FƏNNLƏRİN YOXLANIŞI
        if not found:
            for key in DATA_BASE:
                if key in soru:
                    cavab = f"**{key.capitalize()} Elmi Analizi:** {DATA_BASE[key]}"
                    found = True
                    break
        
        # ÖZƏL KOMANDA: "SİRR VER" VƏ YA "İMKANSİZ"
        if not found and any(x in soru for x in ["sirr", "imkansiz", "maraqli", "fakt"]):
            cavab = f"**Alimdən bir fakt:** {random.choice(IMPOSSIBLE_FACTS)}"
            found = True

        # HESABLAMA MODULU
        if not found and any(c.isdigit() for c in soru) and any(op in soru for op in "+-*/"):
            try:
                res = eval("".join(c for c in soru.replace("x","*") if c in "0123456789+-*/.**() "))
                cavab = f"Hesablamanın nəticəsi: **{res}**"
                found = True
            except: pass

        # DEFAULT CAVAB
        if not found:
            cavab = f"'{prompt}' sualı üzərində Abdullah bəy hazırda mənə yeni elmi dərslər keçir. Mən hələlik bu fənləri mükəmməl bilirəm: Riyaziyyat, Fizika, Kimya, Biologiya, Tarix, Coğrafiya."

        st.markdown(cavab)
        st.session_state.messages.append({"role": "assistant", "content": cavab})

# ==========================================================
# KODUN SƏTİR SAYINI VƏ ELMİ DƏYƏRİNİ ARTIRAN BÖLMƏ
# (Buraya hər fəndən 100-lərlə sətir məlumat əlavə etmək olar)
# ==========================================================
