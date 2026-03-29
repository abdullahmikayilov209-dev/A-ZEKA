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
