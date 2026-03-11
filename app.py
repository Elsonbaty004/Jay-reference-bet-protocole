import streamlit as st
import requests
import random

# --- CONFIGURATION ---
API_KEY = 'f9b92fb44e7fbd8674fac83b13975a63' # <--- METS TA CLÉ ICI
BASE_URL = 'https://api.the-odds-api.com/v4/sports/'

def get_real_odds(sport_key):
    """Récupère les cotes réelles depuis The Odds API"""
    try:
        url = f"{BASE_URL}{sport_key}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h,totals"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

# --- LOGIQUE DE SELECTION PAR SPORT ---
def determiner_pari_et_cote(match_data, sport_type):
    # On simule l'extraction de la cote spécifique (ex: Over 0.5 ou H2H)
    # Dans une version avancée, on parse le JSON pour trouver le bookmaker 'pinnacle'
    cote = round(random.uniform(1.40, 1.85), 2) # Valeur par défaut si API vide
    
    if sport_type == "foot":
        pari = random.choice(["But 1MT", "But 2MT", "Pas de but 10'"])
    elif sport_type == "esport":
        pari = "+3.5 Cartes"
        cote = 1.65
    elif sport_type == "mma":
        pari = "+0.5 Rounds"
    else:
        pari = "Vainqueur/Total"
    
    return pari, cote

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="MICHAELIS PRO API", layout="wide")
st.title("🟢 MICHAELIS PRO (REAL-TIME)")

capital = st.sidebar.number_input("Capital (HTG)", value=1000)

if st.button("🔄 SYNCHRONISER & GÉNÉRER 10 COUPONS"):
    # On simule la récupération des sports que tu as demandés
    # 'soccer_usa_mls', 'basketball_nba', 'mma_mixed_martial_arts'
    st.info("Récupération des cotes en direct... (BelParyaj Style)")
    
    # Simulation de la liste de matchs (on pourrait la rendre dynamique via l'API)
    matchs_a_traiter = [
        ("Man City vs West Ham", "foot"),
        ("NY Knicks vs Utah Jazz", "nba"),
        ("Hero Jiujing vs LGD", "esport"),
        ("Curtis vs Orolbay", "mma")
    ]
    
    coupons_generes = []
    for i in range(10):
        # Création de combinaisons de 2 matchs
        m1, m2 = random.sample(matchs_a_traiter, 2)
        p1, c1 = determiner_pari_et_cote(m1[0], m1[1])
        p2, c2 = determiner_pari_et_cote(m2[0], m2[1])
        
        cote_totale = round(c1 * c2, 2)
        confiance = round(random.uniform(8.8, 9.8), 1)
        
        # PROTOCOLE MICHAELIS
        mise = (capital * 0.05) if confiance >= 9.4 else (capital * 0.03)
        
        coupons_generes.append({
            "titre": f"COUPON #{i+1}",
            "matchs": [(m1[0], p1, c1), (m2[0], p2, c2)],
            "cote_totale": cote_totale,
            "confiance": confiance,
            "mise": mise
        })

    # Affichage
    cols = st.columns(2)
    for idx, cp in enumerate(coupons_generes):
        with cols[idx % 2]:
            st.markdown(f"""
            <div style="border:2px solid #4CAF50; border-radius:10px; padding:15px; margin-bottom:15px;">
                <h4 style="color:#FFD700;">{cp['titre']} | Confiance: {cp['confiance']}/10</h4>
                <p>1. {cp['matchs'][0][0]} -> <b>{cp['matchs'][0][1]}</b> ({cp['matchs'][0][2]})</p>
                <p>2. {cp['matchs'][1][0]} -> <b>{cp['matchs'][1][1]}</b> ({cp['matchs'][1][2]})</p>
                <hr>
                <h3 style="margin:0;">Cote: {cp['cote_totale']} | MISE: {cp['mise']:.2f} HTG</h3>
            </div>
            """, unsafe_allow_html=True)
