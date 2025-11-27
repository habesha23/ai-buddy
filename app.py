import streamlit as st
from openai import OpenAI

client = OpenAI()

st.set_page_config(page_title="AI Coach Buddy", page_icon="🤝", layout="centered")

# Session state defaults
if "profiel" not in st.session_state:
    st.session_state["profiel"] = ""
if "uitleg" not in st.session_state:
    st.session_state["uitleg"] = ""
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.title("🤝 AI Coach Buddy")
st.caption("Ik help je vacatures begrijpen, jouw profiel ontdekken en kleine stappen zetten.")


# ---------------------------
# TABS
# ---------------------------
tab_profiel, tab_vacature, tab_chat = st.tabs(
    ["🧍 Jouw profiel", "📄 Vacature coach", "💬 Praat met AI Buddy"]
)


# ---------------------------
# TAB 1: JOUW PROFIEL
# ---------------------------
with tab_profiel:
    st.subheader("🧍 Jouw profiel")
    st.write(
        "Kies wat bij jou past. Dit helpt mij om beter advies te geven over vacatures. "
        "Je antwoorden worden alleen in deze app gebruikt."
    )

    st.markdown("### 💪 Wat kan jij goed?")
    opties_sterk = [
        "Ik werk graag met mijn handen",
        "Ik kan goed doorwerken",
        "Ik ben rustig",
        "Ik ben sociaal (ik praat makkelijk met mensen)",
        "Ik kan goed herhaaltaken doen",
        "Ik hou van duidelijke regels",
        "Ik ben fysiek sterk",
        "Ik werk graag in een vast ritme",
    ]
    sterke_punten = st.multiselect("Kies je sterke punten:", opties_sterk)

    st.markdown("### 🙂 Wat vind jij leuk om te doen?")
    opties_leuk = [
        "Buiten werken",
        "Binnen werken",
        "In een magazijn / met dozen",
        "Met schoonmaken / opruimen",
        "Met koken / in de keuken",
        "Met techniek / gereedschap",
        "Met mensen helpen",
        "Met dieren werken",
    ]
    leuk_om_te_doen = st.multiselect("Kies wat je leuk vindt:", opties_leuk)

    st.markdown("### 🧩 Waar heb jij hulp bij nodig?")
    opties_hulp = [
        "Lange teksten lezen",
        "Snel werken",
        "Drukke plekken",
        "Rekenen",
        "Nieuwe situaties",
        "Veel praten in 1 keer",
    ]
    hulp_nodig_bij = st.multiselect("Kies wat je lastig vindt:", opties_hulp)

    st.markdown("### 🏢 Welke werkplek past bij jou?")
    opties_plek = [
        "Rustige werkplek",
        "Duidelijke uitleg",
        "Vaste taken",
        "Begeleiding op werk",
        "Klein team",
        "Groot team",
    ]
    fijne_plek = st.multiselect("Kies wat jij fijn vindt op werk:", opties_plek)

    if st.button("💾 Profiel opslaan"):
        profiel_tekst = "Sterke punten: " + (", ".join(sterke_punten) or "Geen gekozen") + "\n"
        profiel_tekst += "Leuk om te doen: " + (", ".join(leuk_om_te_doen) or "Geen gekozen") + "\n"
        profiel_tekst += "Hulp nodig bij: " + (", ".join(hulp_nodig_bij) or "Geen gekozen") + "\n"
        profiel_tekst += "Fijne werkplek: " + (", ".join(fijne_plek) or "Geen gekozen")

        st.session_state["profiel"] = profiel_tekst
        st.success("Je profiel is opgeslagen. Ik gebruik dit in mijn advies bij vacatures. ✅")

    if st.session_state["profiel"]:
        st.markdown("#### 📄 Samenvatting van jouw profiel")
        st.text(st.session_state["profiel"])


# ---------------------------
# TAB 2: VACATURE COACH
# ---------------------------
with tab_vacature:
    st.subheader("📄 Vacature coach")
    st.write("Plak hieronder een vacature. Ik gebruik jouw profiel (als je dat hebt ingevuld) om je te helpen.")

    vacature = st.text_area("Plak hier de vacaturetekst:", height=220)

    # 0 — Matchcheck: Past deze vacature bij mij?
    if st.button("0️⃣ Past deze vacature bij mij?"):
        if not vacature.strip():
            st.warning("Plak eerst een vacaturetekst.")
        else:
            profiel_tekst = st.session_state.get("profiel", "")
            with st.spinner("Ik kijk of deze baan bij jou past..."):
                reply = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": """
Je bent een loopbaancoach voor iemand met een LVB.
Je krijgt een profiel + vacature.
Je geeft een match-score en advies.

LET OP: geef ALTIJD exact dit formaat terug:
<score tussen 0 en 100>|||<advies in gewone tekst>

Voorbeeld:
75|||Deze baan past best goed bij je. Je sterke punten X en Y passen bij de taken...

Gebruik B1/B2 taal in het advies.
"""
                        },
                        {
                            "role": "user",
                            "content": f"""
Profiel van de gebruiker:
{profiel_tekst or 'Geen profiel ingevuld.'}

Vacaturetekst:
{vacature}

Geef een match-score tussen 0 en 100 en een kort advies.
"""
                        },
                    ],
                )

            raw = reply.choices[0].message.content.strip()
            score = None
            advice = raw

            if "|||" in raw:
                score_str, advice = raw.split("|||", 1)
                try:
                    score = int(score_str.strip())
                except ValueError:
                    score = None

            st.subheader("🧭 Match met jouw profiel")

            if score is not None:
                # Clamp score tussen 0 en 100
                score = max(0, min(100, score))
                st.write(f"**Score:** {score} / 100")
                st.progress(score / 100)

                if score >= 70:
                    st.write("😀 Dit lijkt goed bij je te passen.")
                elif score >= 40:
                    st.write("😐 Gedeeltelijk passend, lees het advies goed door.")
                else:
                    st.write("😟 Waarschijnlijk geen goede match, let goed op de punten in het advies hieronder.")

                st.markdown("**Advies:**")
                st.write(advice.strip())
            else:
                # Fallback als AI zich niet aan het formaat houdt
                st.write(raw)

    # 1 — Vacature uitleg in makkelijke taal
    if st.button("1️⃣ Uitleg in makkelijke taal"):
        if not vacature.strip():
            st.warning("Plak eerst een vacaturetekst.")
        else:
            profiel_tekst = st.session_state.get("profiel", "")
            with st.spinner("Ik leg de vacature simpel uit..."):
                messages = [
                    {
                        "role": "system",
                        "content": """
Je bent AI Coach Buddy voor mensen met een LVB.
Schrijf op B1/A2 niveau.
Gebruik korte zinnen, bullets en simpele voorbeelden.
Wees rustig, vriendelijk en duidelijk.
"""
                    },
                    {
                        "role": "user",
                        "content": f"""
Hier is (misschien) het profiel van de gebruiker:
{profiel_tekst or 'Geen profiel ingevuld.'}

Leg deze vacature uit in simpele taal voor deze persoon:

{vacature}
"""
                    },
                ]
                reply = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                )

            uitleg = reply.choices[0].message.content
            st.session_state["uitleg"] = uitleg
            st.subheader("📘 Vacature in simpele taal")
            st.write(uitleg)

    # 2 — Moeilijke woorden uitleggen
    if st.session_state.get("uitleg"):
        if st.butt

st.write("---")
st.caption("Gemaakt door Nahom • AI Coach Buddy voor LVB-jongeren")


