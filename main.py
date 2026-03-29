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
# 40-cı sətirdən (if prompt... altından) başlayaraq hər şeyi sil və bunu yapışdır:
    soru = prompt.lower()
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("A-Zeka neyronları skan edir..."):
            
            # --- SOSİAL ---
            if any(x in soru for x in ["salam", "sağ ol", "təşəkkür"]):
                cavab = "Salam! Mən A-Zeka. Abdullah Mikayılov tərəfindən yaradılmışam. Necə kömək edim?"
            
            elif any(x in soru for x in ["necesen", "nətərsən"]):
                cavab = "Mən rəqəmsal zəkayam, hər zaman işləməyə hazıram! Bəs sən necəsən?"

            # --- ELMİ QAYDALAR (1-11-ci Sinif) ---
            elif "viyet" in soru:
                cavab = "Viyet teoremi: $ax^2 + bx + c = 0$ tənliyində köklər cəmi $x_1+x_2 = -b/a$, köklər hasili $x_1 \\cdot x_2 = c/a$ olur."
            
            elif "heron" in soru:
                cavab = "Heron düsturu: Üçbucağın tərəfləri $a, b, c$ olduqda, sahə $S = \\sqrt{p(p-a)(p-b)(p-c)}$ (burada $p$ yarımperimetrdir)."
            
            elif "pifaqor" in soru:
                cavab = "Pifaqor teoremi: $a^2 + b^2 = c^2$. Hipotenuzun kvadratı katetlərin kvadratları cəminə bərabərdir."

            # --- RİYAZİ HESABLAMA ---
            elif any(char.isdigit() for char in soru) and any(op in soru for op in "+-*/^"):
                try:
                    calc = soru.replace("x", "*").replace("^", "**").replace(":", "/")
                    safe_expr = "".join(c for c in calc if c in "0123456789+-*/.**() ")
                    import math
                    res = eval(safe_expr)
                    cavab = f"Sənin üçün hesabladım: **{res}**"
                except:
                    cavab = "Riyazi ifadədə texniki xəta var, rəqəmləri yoxla."

            # --- DEFAULT CAVAB ---
            else:
                cavab = f"'{prompt}' sualı haqqında məlumatım hələ azdır, amma mən sürətlə inkişaf edirəm!"

            st.markdown(cavab)
            st.session_state.messages.append({"role": "assistant", "content": cavab})
