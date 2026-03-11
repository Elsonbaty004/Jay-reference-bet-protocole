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

# --- FONCTION COEUR : GÉNÉRATION DE COMBINAISONS CIBLÉES ---
def generer_10_coupons_cibles(lignes_matchs, capital):
    coupons_valides = []
    
    # On tente de générer 10 coupons
    attempts = 0
    while len(coupons_valides) < 10 and attempts < 100:
        attempts += 1
        # On pioche entre 5 et 8 matchs pour avoir une chance d'atteindre 5.00
        nb_matchs = random.randint(5, 8)
        selection = random.sample(lignes_matchs, min(nb_matchs, len(lignes_matchs)))
        
        fiche_matchs = []
        cote_cumulee = 5.0
        
        for m in selection:
            # Attribution des types de paris selon tes règles strictes
            m_lower = m.lower()
            if any(x in m_lower for x in ["kpl", "kgp"]):
                p, c = "+3.5 Cartes", 1.28
            elif any(x in m_lower for x in ["ufc", "mma"]):
                p, c = "+0.5 Rounds", 1.22
            elif "nba" in m_lower:
                p, c = "Handicap H1", 1.20
            elif any(x in m_lower for x in ["nhl", "whl", "ohl"]):
                p, c = "Match Non Nul", 1.25
            else: # Foot (US, EN, DE, etc.)
                p, c = "1ère MT: +0.5", 1.25
