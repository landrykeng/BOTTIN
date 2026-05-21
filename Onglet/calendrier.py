import streamlit as st
import pandas as pd
from data.simulations import generer_calendrier, PAYS_CEMAC
import numpy as np

def show():
    if not st.session_state.get("authenticated", False):
        st.warning(":material/lock: Cette section est réservée aux utilisateurs enregistrés.")
        if st.button(":material/login: Se connecter"):
            st.session_state["page"] = "Connexion"; st.rerun()
        return

    st.title("Calendrier des émissions")
    st.caption("Adjudications prévisionnelles et confirmées à venir — mis à jour par l'administrateur BEAC.")

    df_cal = generer_calendrier(15)

    # Filtres
    c1, c2, c3 = st.columns(3)
    with c1:
        pays_f = st.multiselect("Pays",
            options=list(PAYS_CEMAC.keys()),
            format_func=lambda x: PAYS_CEMAC[x]["nom"],
            default=list(PAYS_CEMAC.keys()))
    with c2:
        inst_f = st.selectbox("Instrument", ["Tous","BTA","OTA"], key=f"inst_cal_{np.random.randint(1,1000)}")
    with c3:
        statut_f = st.selectbox("Statut", ["Tous","Prévisionnel","Confirmé"], key="statut_cal")

    df_f = df_cal.copy()
    if pays_f: df_f = df_f[df_f["pays"].isin(pays_f)]
    if inst_f != "Tous": df_f = df_f[df_f["instrument"] == inst_f]
    if statut_f != "Tous": df_f = df_f[df_f["statut"] == statut_f]

    st.markdown(f"**{len(df_f)} adjudication(s) à venir**")

    for _, row in df_f.iterrows():
        badge_color = "#003366" if row["statut"] == "Confirmé" else "#C8A84B"
        inst_color = "#004080" if row["instrument"] == "OTA" else "#9E7B28"
        st.markdown(f"""
        <div class="app-card" style="margin-bottom:0.7rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;">
            <div style="display:flex; align-items:center; gap:1rem;">
                <div>
                    <div style="font-size:1.1rem; font-weight:700; color:#003366;">{row['date']}</div>
                    <div style="font-size:0.8rem; color:#8C8C8C;">Heure limite : {row['heure_limite']}</div>
                </div>
                <div>
                    <div style="font-weight:600; color:#1A1A2E;">{row['pays_nom']}</div>
                    <div style="font-size:0.85rem; color:#4A4A4A;">{row['maturite']}</div>
                </div>
            </div>
            <div style="display:flex; gap:0.5rem; align-items:center; flex-wrap:wrap;">
                <span style="background:{inst_color};color:white;padding:3px 10px;border-radius:3px;font-size:0.75rem;font-weight:700">{row['instrument']}</span>
                <span style="background:{badge_color};color:white;padding:3px 10px;border-radius:3px;font-size:0.75rem;font-weight:700">{row['statut']}</span>
                <span style="font-size:0.88rem; color:#003366; font-weight:600;">{row['montant_indicatif']:,} M XAF</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.info(":material/info: Les montants indiqués sont indicatifs. Le montant définitif mis en adjudication peut différer. Les résultats sont publiés le jour même de l'adjudication.")
