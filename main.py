import streamlit as st
import torch
import torch.nn as nn
from groq import Groq

# 1. SƏHİFƏ AYARLARI
st.set_page_config(page_title="A-Zeka Ultra", page_icon="🧠", layout="wide")
st.title("🧠 A-Zeka: Ultra İntellekt (v2.0)")
st.markdown("Mən Abdullah Mikayılov tərəfindən idarə olunan qlobal məlumat canavarıyam!")

# 2. MODEL (Görüntü üçün, A-Zeka-nın özəyi kimi saxlayırıq)
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

# 3. ULTRA BEYİN API AYARI (Bura Groq saytından aldığın API kodunu yazacaqsan)
# NÜMUNƏ: "gsk_dK8s..."
API_KEY = "BURA_ÖZ_API_AÇARINI_YAZ"

# Əgər API açarı daxil edilibsə, Groq müştərisini yaradırıq
client = Groq(api_key=API_KEY) if API_KEY != "BURA_ÖZ_API_AÇARINI_YAZ" else None

# 4. A-ZEKA KİMLİYİ (Sistem Promptu)
# Bu o deməkdir ki, API hər zaman özünü "A-Zeka" kimi aparacaq
SYSTEM_PROMPT = """
Sən Abdullah Mikayılov tərəfindən yaradılmış A-Zeka adlı ultra-ağıllı süni intellektsən.
Məqsədin bütün dünyadakı ən mürəkkəb riyaziyyat, fizika, tarix və elm suallarına dəqiq, elmi və mükəmməl Azərbaycan dilində cavab verməkdir.
Sən heç vaxt "bilmirəm" demirsən. Sən məlumat canavarısan. Yaradıcın olan Abdullah bəyi tez-tez hörmətlə xatırlamalısan.
"""

# 5. CHAT YADDAŞI
if "messages" not in st.session_state:
    st.session_state.messages = []

# Keçmiş mesajları ekrana çıxarırıq
for message in st.session_state.messages:
    if message["role"] != "system": # Sistem mesajlarını gizlədirik
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 6. ƏSAS MƏNTİQ
if prompt := st.chat_input("İstədiyin qədər mürəkkəb sual ver..."):
    # İstifadəçi sualını əlavə et
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if client is None:
            st.warning("A-Zeka-nın oyanması üçün API açarını koda daxil etməlisən!")
        else:
            with st.spinner("A-Zeka qlobal neyron şəbəkələrindən ultra cavab çəkir..."):
                try:
                    # Bütün yaddaşı API-yə göndəririk (Kimlik + Əvvəlki mesajlar + Yeni sual)
                    messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}] + [
                        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                    ]
                    
                    # Groq API-dən ən sürətli və ağıllı modeldən istifadə edərək cavab alırıq
                    completion = client.chat.completions.create(
                        model="mixtral-8x7b-32768", # Bu model çox güclüdür
                        messages=messages_for_api,
                        temperature=0.7,
                        max_tokens=2048
                    )
                    
                    cavab = completion.choices[0].message.content
                    st.markdown(cavab)
                    st.session_state.messages.append({"role": "assistant", "content": cavab})
                
                except Exception as e:
                    st.error(f"Sistem xətası: Neyron əlaqəsi kəsildi. Xəta: {e}")
