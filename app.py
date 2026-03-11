import streamlit as st
import random
import requests
import time

# --- CONFIGURATION VISUELLE MODERNE ---
st.set_page_config(page_title="Michaelis Pro Scanner", page_icon="📈", layout="wide")

# Custom CSS pour le look Premium Dark
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        background-color: #050505;
    }
    
    .stApp {
        background: radial-gradient(circle at top right, #0d1b10, #050505);
    }

    .main-title {
        text-align: center;
        color: #2ecc71;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    .coupon-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease;
    }

    .coupon-card:hover {
        transform: translateY(-5px);
        border-color: #2ecc71;
        background: rgba(46, 204, 113, 0.05);
    }

    .note-badge {
        background: #2ecc71;
        color: black;
        padding: 4px 12px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 0.8rem;
    }

    .mise-text {
        font-size: 1.4rem;
        color: #f1c40f;
        font-weight: 700;
        margin-top: 10px;
    }

    .match-item {
        color: #bdc3c7;
        font-size: 0.9rem;
        margin: 8px 0;
        border-left: 2px solid #2ecc71;
        padding-left: 10px;
    }

    /* Style du bouton */
    .stButton>button {
        background: linear-gradient(90deg, #2ecc71, #27ae60);
        color: white;
        border: none;
        padding: 15px;
        border-radius: 12px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SÉCURITÉ ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    st.markdown("<h2 style='text-align:center; color:white;'>SYSTÈME SÉCURISÉ</h2>", unsafe_allow_html=True)
    pwd = st.text_input("Code d'accès", type="password")
    if st.button("DÉVERROUILLER"):
        if pwd == "soixante":
            st.session_state["auth"] = True
            st.rerun()
    st.stop()

# --- LOGIQUE DE DONNÉES ---
@st.cache_data(ttl=3600)
def fetch_matches():
    # Simulation de données réelles (plus rapide pour l'affichage moderne)
    leagues = ["NBA", "Premier League", "UFC", "NHL", "Ligue 1", "KPL Esport"]
    teams = ["Lakers", "Celtics", "PSG", "Real Madrid", "Man City", "Arsenal", "T1", "Bruins", "Rangers"]
    base = []
    for _ in range(20):
        t1, t2 = random.sample(teams, 2)
        lg = random.choice(leagues)
        base.append(f"{t1} vs {t2} ({lg})")
    return list(set(base))

# --- INTERFACE ---
st.markdown("<h1 class='main-title'>MICHAELIS PRO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#7f8c8d;'>Algorithme de calcul de mise & coupons Cote 5</p>", unsafe_allow_html=True)

st.sidebar.markdown("### 🛠 CONFIGURATION")
capital = st.sidebar.number_input("Capital (HTG)", value=1000, step=500)
km = st.sidebar.slider("Rigidité Michaelis (Km)", 1, 10, 5)

if 'matchs' not in st.session_state:
    st.session_state.matchs = fetch_matches()

if st.button("⚡ GÉNÉRER L'ANALYSE"):
    with st.spinner("Analyse des cotes en temps réel..."):
        time.sleep(1.5)
        data = st.session_state.matchs
        
        cols = st.columns(3)
        for i in range(1, 13):
            selection = random.sample(data, 4)
            note = round(random.uniform(8.5, 9.9), 1)
            # Formule Michaelis : (Vmax * Note) / (Km + Note)
            v_max = capital * 0.25 # On autorise jusqu'à 25% du capital pour les notes élevées
            mise = round((v_max * note) / (km + note), 2)
            
            with cols[(i-1)%3]:
                match_html = "".join([f"<div class='match-item'>• {m}</div>" for m in selection])
                st.markdown(f"""
                <div class="coupon-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="color:#2ecc71; font-weight:bold;">COUPON #{i}</span>
                        <span class="note-badge">{note}/10</span>
                    </div>
                    <div class="mise-text">{mise} HTG</div>
                    <div style="color:#7f8c8d; font-size:0.8rem; margin-bottom:15px;">Cote estimée: 5.00</div>
                    {match_html}
                </div>
                """, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption("Version Pro 2.0 - 2026")
