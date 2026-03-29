import streamlit as st
import torch
import torch.nn as nn
import math

# 1. SƏHİFƏ AYARLARI
st.set_page_config(page_title="A-Zeka", page_icon="🧠")
st.title("🧠 A-Zeka: Universal İntellekt")

# 2. MODEL (BEYİN - PyTorch)
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

# 3. CHAT YADDAŞI
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. ƏSAS HİSSƏ (GİRİŞ VƏ MƏNTİQ)
if prompt := st.chat_input("Sualınızı bura yazın..."):
    soru = prompt.lower()
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("A-Zeka neyronları analiz edir..."):
            
            # --- ÖZƏL KİMLİK (Abdullah Mikayılov) ---
            if any(x in soru for x in ["kim yaradıb", "müəllif", "sahibin", "yaradıcın"]):
                cavab = "Mən **Abdullah Mikayılov** tərəfindən yaradılmış ali bir zəkayam. Onun vizyonu məni 10,000 sətirlik elm okeanına çevirməkdir!"
            
            elif any(x in soru for x in ["kimsən", "nəsən", "adın"]):
                cavab = "Mən **A-Zeka**-yam. 1-ci sinifdən 11-ci sinfə qədər bütün elmləri öyrənməyə proqramlaşdırılmış süni intellektəm."

            # --- RİYAZİYYAT QAYDALARI (1-11-ci Sinif) ---
            elif "viyet" in soru:
                cavab = "Viyet teoremi kvadrat tənliyin kökləri arasındakı əlaqəni göstərir: \n\n* $x_1 + x_2 = -b/a$ \n* $x_1 \cdot x_2 = c/a$"
            
            elif "diskriminant" in soru:
                cavab = "Kvadrat tənlik üçün: $D = b^2 - 4ac$. \n\n* $D > 0$: 2 kök \n* $D = 0$: 1 kök \n* $D < 0$: Həqiqi kök yoxdur."

            elif "pifaqor" in soru:
                cavab = "Pifaqor teoremi: Düzbucaqlı üçbucaqda katetlərin kvadratları cəmi hipotenuzun kvadratına bərabərdir: $a^2 + b^2 = c^2$."

            elif "törəmə" in soru or "toreme" in soru:
                cavab = "Törəmə funksiyanın dəyişmə sürətidir. Əsas düstur: $(x^n)' = nx^{n-1}$."

            elif "inteqral" in soru:
                cavab = "İnteqral törəmənin tərsidir və sahə hesabında istifadə olunur: $\int x^n dx = \\frac{x^{n+1}}{n+1} + C$."

            elif "loqarifma" in soru:
                cavab = "Loqarifma: $\log_a b = x \implies a^x = b$. Məsələn: $\log_2 8 = 3$."

            elif "faiz" in soru:
                cavab = "Ədədin faizini tapmaq üçün ədədi faiz göstərən ədədə vurub 100-ə bölmək lazımdır: $a \cdot p / 100$."

            # --- FİZİKA VƏ DİGƏR ELMLƏR ---
            elif "nyuton" in soru:
                cavab = "Nyutonun II qanunu: Maddi nöqtəyə təsir edən qüvvə onun kütləsi və təcilinin hasilinə bərabərdir: $F = ma$."

            elif "om qanunu" in soru:
                cavab = "Dövrə hissəsi üçün Om qanunu: $I = U / R$."

            elif "azərbaycan" in soru:
                cavab = "Azərbaycan: Paytaxtı Bakı olan Odlar Yurdu. 1918-ci ildə Şərqdə ilk demokratik respublika qurub."

            # --- MÜRƏKKƏB HESABLAMA MODULU (Dünya səviyyəli misallar) ---
            elif any(char.isdigit() for char in soru) and any(op in soru for op in "+-*/^"):
                try:
                    # Riyazi simvolları Python formatına çeviririk
                    temp_calc = soru.replace("x", "*").replace("^", "**").replace(":", "/")
                    safe_expr = "".join(c for c in temp_calc if c in "0123456789+-*/.**() ")
                    result = eval(safe_expr)
                    cavab = f"Sənin üçün 11-ci sinif səviyyəsində hesabladım: **{result}**"
                except:
                    cavab = "Bu mürəkkəb misalda bir yazılış xətası var, zəhmət olmasa yoxla."

            # --- ÜMUMİ ---
            elif "salam" in soru:
                cavab = "Salam! Mən A-Zeka. Bu gün hansı çətin sualı həll edirik?"
            
            else:
                cavab = f"'{prompt}' haqqında məlumatım hələ azdır, amma Abdullah bəy hər gün neyronlarımı yeni elmi qaydalarla bəsləyir!"

            st.markdown(cavab)
            st.session_state.messages.append({"role": "assistant", "content": cavab})
