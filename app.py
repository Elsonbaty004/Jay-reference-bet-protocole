import streamlit as st
import random

# --- CONFIGURATION DU PROTOCOLE MICHAELIS ---
def calculer_mise_michaelis(capital, niveau_confiance):
    # Le protocole Michaelis adapte la mise selon la confiance (score /10)
    # Plus le score est haut, plus on s'approche du plafond de 5% du capital
    base_pct = 0.02 # 2% minimum
    if niveau_confiance >= 9:
        base_pct = 0.05
    elif niveau_confiance >= 8:
        base_pct = 0.035
    
    return capital * base_pct

# --- MOTEUR DE DÉCISION IA PAR CHAMPIONNAT ---
def generer_pari_ia(match_text):
    m = match_text.lower()
    
    # 1. Esport (KPL, KGP)
    if any(x in m for x in ["kpl", "kgp", "esport"]):
        return "🎮 Plus de 3.5 Cartes", random.uniform(8.5, 9.8)
    
    # 2. Foot (US, EN, DE, EU, SCO, INT)
    elif any(x in m for x in ["foot", "soccer", "mls", "premier", "bundes", "ligue", "euro", "écossais", "international"]):
        options = [
            "⚽ But en 1ère mi-temps", 
            "⚽ But en 2e mi-temps", 
            "⚽ Pas de but dans les 10 premières minutes"
        ]
        return random.choice(options), random.uniform(7.8, 9.5)
    
    # 3. Basket (NBA)
    elif "nba" in m or "basket" in m:
        options = ["🏀 Victoire Directe", "🏀 Nombre total de points", "🏀 Handicap"]
        return random.choice(options), random.uniform(8.0, 9.2)
    
    # 4. Hockey (NHL, WHL, OHL)
    elif any(x in m for x in ["nhl", "whl", "ohl", "hockey"]):
        return "🏒 Match Non Nul (12)", random.uniform(7.5, 8.8)
    
    # 5. MMA (UFC FN)
    elif "ufc" in m or "mma" in m:
        return "🥊 Plus de 0.5 Rounds", random.uniform(8.2, 9.9)
    
    # Par défaut
    return "🎲 Analyse en cours...", 7.0

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="MICHAELIS PRO", layout="wide")
st.title("🟢 MICHAELIS PRO v2.0")
st.markdown("---")

col_input, col_stats = st.columns([2, 1])

with col_input:
    matches_input = st.text_area("📋 Colle tes matchs ici (un par ligne)", height=150, 
                                 placeholder="Ex: PSG vs Real (Foot)\nLakers vs Bulls (NBA)\nKPL Hero vs Team (KPL)")
    capital = st.number_input("Capital disponible (HTG)", value=1000)

if st.button("🚀 GÉNÉRER L'ANALYSE PROTOCOLE"):
    lines = [l.strip() for l in matches_input.split('\n') if "vs" in l.lower()]
    
    if lines:
        st.subheader("📊 Coupons de Mise Optimisés")
        cols = st.columns(3)
        
        for i, match in enumerate(lines):
            pari, confiance = generer_pari_ia(match)
            mise = calculer_mise_michaelis(capital, confiance)
            
            with cols[i % 3]:
                st.markdown(f"""
                <div style="border:2px solid #4CAF50; border-radius:10px; padding:15px; margin-bottom:10px; background-color:#1E1E1E;">
                    <div style="display:flex; justify-content:space-between;">
                        <span style="color:#888;">COUPON #{i+1}</span>
                        <span style="background:#4CAF50; padding:2px 8px; border-radius:5px; font-size:12px;">{confiance:.1f}/10</span>
                    </div>
                    <h3 style="color:#FFD700; margin:10px 0;">{mise:.2f} HTG</h3>
                    <p style="font-weight:bold; font-size:14px;">{match.upper()}</p>
                    <p style="color:#00E5FF; font-size:15px;">➡️ {pari}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("Veuillez entrer des matchs valides avec 'vs'.")
