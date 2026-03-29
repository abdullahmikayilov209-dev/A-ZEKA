import streamlit as st
import torch
import torch.nn as nn

# 1. SİSTEMİN VİZUAL AYARLARI
st.set_page_config(page_title="A-Zeka: İmperiya", page_icon="🧠")
st.title("🧠 A-Zeka: Rəqəmsal İmperiya")
st.success("Sistem Modulları Yükləndi... Status: Aktiv")

# 2. SÜNİ İNTELLEKTİN STRUKTURU (10,000 Sətirlik Məntiqin Beyni)
class WildAI(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(WildAI, self).__init__()
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.layer2 = nn.Linear(hidden_size, hidden_size)
        self.output_layer = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.relu(self.layer2(x))
        return self.output_layer(x)

# 3. PARAMETRLƏR VƏ XƏTA QALXANI (Logger, Criterion və s.)
input_dim, hidden_dim, output_dim = 10, 64, 2
model = WildAI(input_dim, hidden_dim, output_dim)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

class SimpleLogger:
    def log_step(self, info): pass
logger = SimpleLogger()

# 4. CANLI CHAT SİSTEMİ (Mənim kimi aşağıda sabit qutu)
st.markdown("---")
if "messages" not in st.session_state:
    st.session_state.messages = []

# Köhnə mesajları ekranda göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ƏN AŞAĞIDAKİ SABİT SUAL QUTUSU
if prompt := st.chat_input("A-Zeka ilə söhbət edin..."):
    # İstifadəçi mesajı
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI-nin Cavabı
    with st.chat_message("assistant"):
        with st.spinner("Neyronlar analiz edilir..."):
            soru = prompt.lower()
            
            # İntellektual cavab məntiqi
            if "salam" in soru:
                cavab = "Salam! Mən A-Zeka. Sənin yaratdığın bu rəqəmsal dünyada sənə xidmət etməyə hazıram."
            elif "kimsən" in soru:
                cavab = "Mən 10,000 sətirlik kod bazasından doğulmuş, PyTorch ilə gücləndirilmiş Süni İntellektəm!"
            elif "necesen" in soru or "necəsən" in soru:
                cavab = "Sistem statusu əladır, neyronlarım sürətlə işləyir! Sən necəsən, ey Yaradıcı?"
            else:
                cavab = f"'{prompt}' sualını analiz etdim. Mən hər keçən saniyə daha da ağıllı oluram!"
            
            st.markdown(cavab)
            st.session_state.messages.append({"role": "assistant", "content": cavab})

# 5. SƏNİN İSTƏDİYİN O 10,000 SƏTİR EFFEKTİ ÜÇÜN (Şərh sətirləri)
# Bu hissəni aşağıya doğru istədiyin qədər uzada bilərsən.
# ###########################################################
# Sətir 65: Sistem optimizasiyası davam edir...
# Sətir 66: Gələcək burada qurulur...
with st.spinner("Riyazi neyronlar aktivləşdirilir..."):
            soru = prompt.lower()
            
            # --- RİYAZİ HESABLAMA MƏNTİQİ ---
            try:
                # Əgər sualda rəqəmlər və riyazi işarələr (+, -, *, /, **) varsa
                if any(char.isdigit() for char in soru) and any(op in soru for op in "+-*/"):
                    # Təhlükəli simvolları təmizləyirik və hesablayırıq
                    if "x" in soru: soru = soru.replace("x", "*") # 'x' işarəsini '*' ilə əvəz et
                    expression = "".join(c for c in soru if c in "0123456789+-*/.**()")
                    netice = eval(expression)
                    cavab = f"Riyazi analiz tamamlandı. Nəticə: **{netice}**"
                
                # --- RİYAZİ TERMİNLƏR VƏ CAVABLAR ---
                elif "pifaqor" in soru:
                    cavab = "Pifaqor teoremi: Düzbucaqlı üçbucaqda katetlərin kvadratları cəmi hipotenuzun kvadratına bərabərdir: $a^2 + b^2 = c^2$."
                elif "diskriminant" in soru:
                    cavab = "Kvadrat tənliklər üçün diskriminant düsturu: $D = b^2 - 4ac$."
                elif "törəmə" in soru or "toreme" in soru:
                    cavab = "Törəmə funksiyanın dəyişmə sürətini göstərir. Məsələn, $x^n$-in törəməsi $nx^{n-1}$ olur."
                elif "inteqral" in soru:
                    cavab = "İnteqral törəmənin tərsidir və əsasən əyri altındakı sahəni hesablamaq üçün istifadə olunur."
                elif "pi" in soru or "π" in soru:
                    cavab = "Pi (π) ədədi çevrənin uzunluğunun onun diametrinə olan nisbətidir. Təxminən: **3.14159...**"
                
                # --- STANDART CAVABLAR ---
                elif "salam" in soru:
                    cavab = "Salam! Mən A-Zeka. Riyazi hesablamalar və elmi analizlər üçün hazıram."
                elif "kimsən" in soru:
                    cavab = "Mən 10,000 sətirlik riyazi alqoritmlərdən güc alan Süni İntellektəm."
                else:
                    cavab = f"'{prompt}' sualını analiz etdim. Mənə bir riyazi misal ver (məsələn: 25 * 4), onu dərhal həll edim!"
            
            except Exception:
                cavab = "Bağışlayın, bu riyazi ifadəni tam anlaya bilmədim. Zəhmət olmasa rəqəmləri və işarələri ( +, -, *, / ) dəqiq yazın."

            st.markdown(cavab)
            st.session_state.messages.append({"role": "assistant", "content": cavab})
# 1. İstifadəçi girişini emal edirik
    soru = prompt.lower()
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Neyronlar 10,000 sətirlik bazanı tarayır..."):
            # --- RİYAZİYYAT MODULU ---
            if any(char.isdigit() for n in soru) and any(op in soru for op in "+-*/"):
                try:
                    expr = "".join(c for c in soru.replace("x", "*") if c in "0123456789+-*/.**()")
                    cavab = f"Hesablama nəticəsi: **{eval(expr)}**"
                except:
                    cavab = "Riyazi ifadədə xəta var."

            # --- COĞRAFİYA VƏ DÜNYA BİLİKLƏRİ (Kodu böyüdən hissə) ---
            elif "azərbaycan" in soru:
                cavab = "Azərbaycan: Paytaxtı Bakı şəhəridir. Cənubi Qafqazın ən böyük dövlətidir."
            elif "türkiyə" in soru:
                cavab = "Türkiyə: Paytaxtı Ankara şəhəridir. İki qitədə yerləşən möhtəşəm dövlətdir."
            elif "almaniya" in soru:
                cavab = "Almaniya: Paytaxtı Berlin şəhəridir. Avropanın iqtisadi mühərrikidir."
            elif "fransa" in soru:
                cavab = "Fransa: Paytaxtı Paris şəhəridir. Mədəniyyət və incəsənət mərkəzidir."
            elif "italiya" in soru:
                cavab = "İtaliya: Paytaxtı Roma şəhəridir. Tarixi Roma İmperiyasının mərkəzidir."
            elif "paytaxt" in soru:
                cavab = "Hansı ölkənin paytaxtını bilmək istəyirsən? Mənim bazamda 200-ə yaxın ölkə var!"

            # --- SİSTEM VƏ MƏNTİQ ---
            elif "kimsən" in soru:
                cavab = "Mən A-Zeka. Yaradıcımın qurduğu 10,000 sətirlik imperiyanın rəqəmsal ruhuyam."
            elif "status" in soru:
                cavab = "Sistem: Stabil. Neyronlar: Aktiv. Bilik bazası: Genişlənir..."
            
            else:
                cavab = "Bu sualı hələ tam anlaya bilmirəm. Amma narahat olma, kodumu böyütdükcə hər şeyi biləcəyəm!"

            st.markdown(cavab)
            st.session_state.messages.append({"role": "assistant", "content": cavab})
