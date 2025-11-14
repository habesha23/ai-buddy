import streamlit as st
from openai import OpenAI

client = OpenAI()

st.set_page_config(page_title="AI Coach Buddy", page_icon="🤝", layout="centered")

st.title("🤝 AI Coach Buddy")
st.write("Ik help je vacatures begrijpen, moeilijke woorden uitleggen en kleine stappen zetten.")

# --- INPUT ---
vacature = st.text_area("Plak hier de vacaturetekst:", height=250)

# --- KNOP 1: VACATURE IN MAKKELIJKE TAAL ---
if st.button("Uitleg in makkelijke taal"):
    if not vacature.strip():
        st.warning("Plak eerst een vacaturetekst.")
    else:
        with st.spinner("Vacature wordt uitgelegd..."):
            reply = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system",
                     "content": """
Je bent een AI Coach Buddy voor mensen met een LVB.
- Schrijf altijd op A2/B1 niveau.
- Gebruik korte zinnen.
- Gebruik bullets en duidelijke kopjes.
- Leg moeilijke woorden uit.
- Wees vriendelijk en rustig.
"""},

                    {"role": "user",
                     "content": f"Leg deze vacature uit in simpele taal:\n\n{vacature}"}
                ]
            )

        uitleg = reply.choices[0].message.content
        st.subheader("📘 Vacature in eenvoudige taal")
        st.write(uitleg)
        st.session_state["uitleg"] = uitleg

# --- KNOP 2: MOEILIJKE WOORDEN ---
if "uitleg" in st.session_state:
    if st.button("Leg moeilijke woorden uit"):
        with st.spinner("Woorden worden uitgelegd..."):
            reply = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system",
                     "content": "Je legt moeilijke woorden uit in super simpele taal."},
                    {"role": "user",
                     "content": f"Leg alle moeilijke woorden uit uit deze tekst:\n\n{st.session_state['uitleg']}"}
                ]
            )
        st.subheader("📚 Moeilijke woorden uitgelegd")
        st.write(reply.choices[0].message.content)

# --- KNOP 3: STAP-VOOR-STAP ---
if "uitleg" in st.session_state:
    if st.button("Geef mij stappen wat ik nu moet doen"):
        with st.spinner("Stappen worden gemaakt..."):
            reply = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Je maakt kleine stappen. Max 5 stappen."},
                    {"role": "user",
                     "content": f"Geef mij 5 rustige, kleine stappen gebaseerd op deze vacature:\n\n{st.session_state['uitleg']}"}
                ]
            )
        st.subheader("🪜 Kleine stappen")
        st.write(reply.choices[0].message.content)

# --- KNOP 4: PAST DEZE BAAN BIJ MIJ? ---
if "uitleg" in st.session_state:
    if st.button("Past deze baan bij mij?"):
        with st.spinner("We controleren dit..."):
            reply = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system",
                     "content": "Maak 5 ja/nee vragen en geef daarna advies."},
                    {"role": "user",
                     "content": f"Maak een match-check voor deze vacature:\n\n{st.session_state['uitleg']}"}
                ]
            )
        st.subheader("🔍 Past deze baan bij jou?")
        st.write(reply.choices[0].message.content)

st.write("---")
st.caption("Gemaakt door Nahom • AI Coach Buddy voor LVB-jongeren")
