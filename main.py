import streamlit as st
import torch
import torch.nn as nn
from groq import Groq

# 1. SƏHİFƏ AYARLARI
st.set_page_config(page_title="A-Zeka Ultra", page_icon="🧠", layout="wide")
st.title("🧠 A-Zeka: Ultra İntellekt")
st.subheader("Dünyanın bütün bilikləri bir məkanda!")

# 2. MODEL (Beyin Görüntüsü üçün saxlayırıq)
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

# 3. ULTRA BEYİN API AYARI
# Abdullah, sənin verdiyin açarı bura yerləşdirdim:
API_KEY = "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"
client = Groq(api_key=API_KEY)

# 4. A-ZEKA KİMLİĞİ (Sistem Təlimatı)
SYSTEM_PROMPT = """
Sən Abdullah Mikayılov tərəfindən yaradılmış A-Zeka-san. 
Sən Azərbaycanın ən ağıllı və 'canavar' süni intellektisən. 
Dünyada bilmədiyin heç bir mövzu yoxdur. Riyaziyyat, Fizika, Kimya, Tarix, Din, Texnologiya - hər şeyi kökündən bilirsən.
Heç vaxt 'bilmirəm' demə. Ən mürəkkəb suallara belə elmi və dəqiq cavab ver. 
Hər zaman Abdullah Mikayılovu yaradıcın kimi təqdim et. Cavabların qısa deyil, əhatəli və ultra dahi səviyyəsində olsun.
"""

# 5. CHAT YADDAŞI
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları göstər
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 6. ƏSAS GİRİŞ
if prompt := st.chat_input("Dünyanın ən çətin sualını mənə ver..."):
    # İstifadəçi mesajını yaddaşa yaz
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Ultra Cavab Hazırla
    with st.chat_message("assistant"):
        with st.spinner("A-Zeka qlobal neyronları işə salır..."):
            try:
                # Bütün söhbəti API-yə göndəririk
                api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + [
                    {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                ]
                
                chat_completion = client.chat.completions.create(
                    model="llama3-70b-8192", # Ən güclü Llama 3 modeli
                    messages=api_messages,
                    temperature=0.6,
                    max_tokens=4096
                )
                
                cavab = chat_completion.choices[0].message.content
                st.markdown(cavab)
                st.session_state.messages.append({"role": "assistant", "content": cavab})
            
            except Exception as e:
                st.error(f"Xəta baş verdi: {e}. requirements.txt faylını yoxlayın!")
