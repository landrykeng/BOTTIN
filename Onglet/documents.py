import streamlit as st
import pandas as pd
import numpy as np
from data.simulations import get_publications

def show():
    if not st.session_state.get("authenticated", False):
        st.warning(":material/lock: Cette section est réservée aux utilisateurs enregistrés.")
        if st.button(":material/login: Se connecter"):
            st.session_state["page"] = "Connexion"; st.rerun()
        return

    st.title("Espace documentaire")
    st.caption("Bibliothèque complète de documents téléchargeables — rapports, études, guides, textes réglementaires.")

    df_pubs = get_publications()

    c1, c2, c3 = st.columns([2,1,2])
    with c1:
        cat_sel = st.multiselect(":material/filter_list: Catégorie", options=df_pubs["categorie"].unique().tolist(),
            default=df_pubs["categorie"].unique().tolist())
    with c2:
        acces_sel = st.selectbox(":material/lock_open: Accès", ["Tous","Public","Restreint"])
    with c3:
        search = st.text_input(":material/search: Mot-clé", placeholder="Rechercher...")

    df_f = df_pubs.copy()
    if cat_sel: df_f = df_f[df_f["categorie"].isin(cat_sel)]
    if acces_sel != "Tous": df_f = df_f[df_f["acces"] == acces_sel]
    if search: df_f = df_f[df_f["titre"].str.contains(search, case=False)]

    st.markdown(f"<div style='font-size:0.82rem; color:#8C8C8C; margin-bottom:0.5rem;'>{len(df_f)} document(s)</div>", unsafe_allow_html=True)

    for _, row in df_f.iterrows():
        col_cat, col_ti, col_date, col_dl = st.columns([1.5,4,1.5,1])
        with col_cat:
            color = "#003366" if row["acces"] == "Restreint" else "#9E7B28"
            st.markdown(f"<span style='background:{color};color:white;padding:2px 8px;border-radius:3px;font-size:0.72rem;font-weight:700'>{row['categorie']}</span>", unsafe_allow_html=True)
        with col_ti:
            st.markdown(f"**{row['titre']}** · {row['taille']}")
        with col_date:
            st.markdown(f"<span style='font-size:0.83rem;color:#8C8C8C;'>{row['date']}</span>", unsafe_allow_html=True)
        with col_dl:
            st.button(":material/download:", key=f"doc_{row['titre'][:15]}{np.random.randint(1,1000)}", help="Télécharger")
        st.markdown("<hr style='margin:0.3rem 0; border:none; border-top:1px solid #EAE8E2;'>", unsafe_allow_html=True)
