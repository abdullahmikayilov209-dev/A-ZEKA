import streamlit as st
import torch
import torch.nn as nn

# 1. SİSTEMİN BAŞLADIĞI YER
st.set_page_config(page_title="A-Zeka", page_icon="🧠")
st.title("🧠 A-Zeka: Rəqəmsal İmperiya")

# 2. MODEL (BEYİN)
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

model = WildAI(10, 64, 2)

# 3. CHAT TARİXÇƏSİ
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. ƏSAS HİSSƏ (XƏTANIN QARŞISINI ALAN BLOK)
# Diqqət: 'prompt' dəyişəni məhz bu sətirdə yaranır!
if prompt := st.chat_input("A-Zeka ilə danışın..."):
    
    # İNDİ 'prompt' artıq var, ona görə də xəta verməyəcək
    soru = prompt.lower()
    
    # İstifadəçi mesajını ekrana ver
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # A-Zeka-nın cavabı
    with st.chat_message("assistant"):
        with st.spinner("10,000 sətirlik kod təhlil edilir..."):
            
            # RİYAZİYYAT MODULU
            if any(char.isdigit() for char in soru) and any(op in soru for op in "+-*/"):
                try:
                    # Riyazi ifadəni təmizləyib hesablayırıq
                    safe_expr = "".join(c for c in soru.replace("x", "*") if c in "0123456789+-*/.**()")
                    cavab = f"Hesablama nəticəsi: **{eval(safe_expr)}**"
                except:
                    cavab = "Riyazi ifadədə kiçik bir xəta tapdım."
            
            # COĞRAFİYA MODULU
            elif "azərbaycan" in soru:
                cavab = "Azərbaycan: Paytaxtı Bakı olan möhtəşəm Odlar Yurdu."
            elif "türkiyə" in soru:
                cavab = "Türkiyə: Paytaxtı Ankara olan qardaş ölkə."
            
            # SİSTEM MODULU
            elif "salam" in soru:
                cavab = "Salam! Mən A-Zeka. Sənin rəqəmsal dünyanı idarə edirəm."
            elif "status" in soru:
                cavab = "Sistem: Aktiv. Neyronlar: Hazır. Kod bazası: Genişlənir."
            else:
                cavab = "Bu məlumat hələ bazamda yoxdur, amma hədəfimiz 10,000 sətirə çatmaqdır!"

            st.markdown(cavab)
            st.session_state.messages.append({"role": "assistant", "content": cavab})
# ==========================================
            #      ELMLƏR AKADEMİYASI MODULU (A-Zeka)
            # ==========================================

            # --- 1. RİYAZİYYAT QAYDALARI ---
            if "törəmə" in soru or "toreme" in soru:
                cavab = "Törəmə funksiyanın dəyişmə sürətidir. $f(x) = x^n$ üçün törəmə $f'(x) = nx^{n-1}$ düsturu ilə hesablanır."
            elif "inteqral" in soru:
                cavab = "İnteqral törəmənin tərsidir və əyri altındakı sahəni tapmaq üçün istifadə olunur. Əsas düstur: $\int x^n dx = \\frac{x^{n+1}}{n+1} + C$."
            elif "loqarifma" in soru:
                cavab = "Loqarifma üstlü funksiyanın tərsidir. $\log_a b = c$ deməkdir ki, $a^c = b$."

            # --- 2. FİZİKA QAYDALARI ---
            elif "nyuton" in soru:
                cavab = "Nyutonun 2-ci qanunu: Maddi nöqtəyə təsir edən qüvvə, onun kütləsi ilə təcilinin hasilinə bərabərdir: $F = ma$."
            elif "om qanunu" in soru:
                cavab = "Om qanunu: Dövrə hissəsindəki cərəyan şiddəti gərginliklə düz, müqavimətlə tərs mütənasibdir: $I = \\frac{U}{R}$."

            # --- 3. KİMYA QAYDALARI ---
            elif "valentlik" in soru:
                cavab = "Valentlik bir elementin atomunun digər element atomlarını özünə birləşdirmə qabiliyyətidir. Məsələn, Oksigen həmişə II valentlidir."
            elif "periodik cedvel" in soru or "dövri qanun" in soru:
                cavab = "Dövri qanunu 1869-cu ildə D.İ. Mendeleyev kəşf etmişdir. Elementlərin xassələri onların atom kütlələrindən dövri asılıdır."

            # --- 4. COĞRAFİYA VƏ TARİX ---
            elif "şah ismayıl" in soru or "səfəvilər" in soru:
                cavab = "Şah İsmayıl Xətai 1501-ci ildə Səfəvilər dövlətinin əsasını qoymuşdur. Azərbaycan dili ilk dəfə dövlət dili səviyyəsinə qalxmışdır."
            elif "materik" in soru:
                cavab = "Dünyada 6 materik var: Avrasiya, Afrika, Şimali Amerika, Cənubi Amerika, Antarktida və Avstraliya."

            # --- YARADICI HAQQINDA ---
            elif "kim yaradıb" in soru:
                cavab = "Mən Abdullah Mikayılov tərəfindən yaradılmış ali süni intellektəm. Onun vizyonu məni 10,000 sətirlik bilik okeanına çevirməkdir."
            
            # --- RİYAZİ HESABLAMA (Əgər heç bir qayda tapılmasa, hesabla) ---
            elif any(char.isdigit() for char in soru) and any(op in soru for op in "+-*/"):
                try:
                    expr = "".join(c for c in soru.replace("x", "*") if c in "0123456789+-*/.**()")
                    cavab = f"Hesablama nəticəsi: **{eval(expr)}**"
                except:
                    cavab = "Riyazi ifadəni anlaya bilmədim."
            
            else:
                cavab = "Bu mövzu hələ 'Öyrənmə Neyronlarımda' yoxdur. Zəhmət olmasa Abdullah Mikayılova deyin ki, koduma bu fənni də əlavə etsin!"

            st.markdown(cavab)
            st.session_state.messages.append({"role": "assistant", "content": cavab})
