import streamlit as st
from openai import OpenAI

client = OpenAI()

st.set_page_config(page_title="AI Coach Buddy", page_icon="🤝", layout="centered")

st.title("🤝 AI Coach Buddy")
st.write("Ik help je vacatures begrijpen, moeilijke woorden uitleggen en kleine stappen zetten.")

vacature = st.text_area("Plak hier de vacaturetekst:", height=250)

# 1 — Vacature uitleg in makkelijke taal
if st.button("1️⃣ Uitleg in makkelijke taal"):
    if not vacature.strip():
        st.warning("Plak eerst een vacaturetekst.")
    else:
        with st.spinner("Ik leg het simpel uit..."):
            reply = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": """
Je bent AI Coach Buddy voor LVB.
Schrijf altijd in B1/A2 niveau.
Korte zinnen. Bullets. Rustige toon.
Leg moeilijke woorden uit.
"""},
                    {"role": "user", "content": f"Leg deze vacature uit in simpele taal:\n\n{vacature}"}
                ]
            )
        uitleg = reply.choices[0].message.content
        st.session_state["uitleg"] = uitleg
        st.subheader("📘 Vacature in simpele taal")
        st.write(uitleg)

# 2 — Moeilijke woorden uitleggen
if "uitleg" in st.session_state:
    if st.button("2️⃣ Moeilijke woorden uitleggen"):
        with st.spinner("Ik zoek moeilijke woorden..."):
            reply = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Leg moeilijke woorden super simpel uit."},
                    {"role": "user", "content": f"Leg moeilijke woorden uit uit deze tekst:\n\n{st.session_state['uitleg']}"}
                ]
            )
        st.subheader("📚 Moeilijke woorden uitgelegd")
        st.write(reply.choices[0].message.content)

# 3 — Kleine stappen
if "uitleg" in st.session_state:
    if st.button("3️⃣ Kleine stappen (wat moet ik nu doen?)"):
        with st.spinner("Ik maak kleine stappen..."):
            reply = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Maak max 5 simpele stappen voor LVB."},
                    {"role": "user", "content": f"Maak 5 kleine stappen gebaseerd op deze vacature:\n\n{st.session_state['uitleg']}"}
                ]
            )
        st.subheader("🪜 Kleine stappen")
        st.write(reply.choices[0].message.content)

# 4 — Motivatie & geruststelling
if "uitleg" in st.session_state:
    if st.button("4️⃣ Geef mij motivatie / geruststelling"):
        with st.spinner("Even wat motivatie..."):
            reply = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": """
Je bent een vriendelijke coach.
Geef motivatie, rust, geruststelling.
Gebruik B1/A2 taal.
"""},
                    {"role": "user", "content": "Geef motivatie aan iemand met twijfel over werk zoeken."}
                ]
            )
        st.subheader("💛 Motivatie en steun")
        st.write(reply.choices[0].message.content)

# 5 — Werktempo & verwachtingen
if "uitleg" in st.session_state:
    if st.button("5️⃣ Werktempo & verwachtingen"):
        with st.spinner("Ik leg het rustig uit..."):
            reply = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system",
                     "content": "Leg werktempo, pauzes, druk en begeleiding in simpele taal uit."},
                    {"role": "user",
                     "content": f"Leg het werktempo en verwachtingen uit voor deze functie:\n\n{st.session_state['uitleg']}"}
                ]
            )
        st.subheader("⏱️ Werktempo & verwachtingen")
        st.write(reply.choices[0].message.content)

# 6 — Suggesties op basis van sterke punten
if "uitleg" in st.session_state:
    if st.button("6️⃣ Wat past bij mijn sterke punten?"):
        with st.spinner("Ik kijk wat bij je past..."):
            reply = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system",
                     "content": "Koppel simpele sterke punten aan taken op werk. Simpele taal."},
                    {"role": "user",
                     "content": f"Koppel sterke punten aan simpele taken voor deze vacature:\n\n{st.session_state['uitleg']}"}
                ]
            )
        st.subheader("💪 Wat past bij jou?")
        st.write(reply.choices[0].message.content)

# 7 — Zelf beslissen (zelfstandigheid stimuleren)
if "uitleg" in st.session_state:
    if st.button("7️⃣ Help mij kiezen (zelf beslissen)"):
        with st.spinner("Ik help je kiezen..."):
            reply = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system",
                     "content": "Stimuleer zelfstandigheid. Geef opties. Laat gebruiker kiezen."},
                    {"role": "user",
                     "content": f"Help mij zelf kiezen over deze vacature:\n\n{st.session_state['uitleg']}"}
                ]
            )
        st.subheader("🧭 Zelf beslissen")
        st.write(reply.choices[0].message.content)

st.write("---")
st.caption("Gemaakt door Nahom • AI Coach Buddy voor LVB-jongeren")

