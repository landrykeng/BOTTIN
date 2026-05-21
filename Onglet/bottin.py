import streamlit as st
import pandas as pd
from data.simulations import get_bottin_complet, PAYS_CEMAC

def show():
    if not st.session_state.get("authenticated", False):
        st.warning(":material/lock: Cette section est réservée aux utilisateurs enregistrés et validés.")
        if st.button(":material/login: Se connecter"):
            st.session_state["page"] = "Connexion"; st.rerun()
        return

    st.title("Bottin des investisseurs")
    st.caption("Répertoire central de tous les acteurs du marché des valeurs du Trésor de la CEMAC.")

    bottin = get_bottin_complet()

    tab_svt, tab_sgp, tab_sdb, tab_inv = st.tabs([
        ":material/account_balance: SVT",
        ":material/trending_up: SGP",
        ":material/store: SDB",
        ":material/groups: Investisseurs institutionnels",
    ])

    pays_list = ["Tous"] + [v["nom"] for v in PAYS_CEMAC.values()]
    statut_list = ["Tous", "Actif", "Suspendu"]

    def filtres(prefix):
        c1, c2, c3 = st.columns([2,1,2])
        with c1:
            pays = st.selectbox(":material/public: Pays", pays_list, key=f"{prefix}_pays")
        with c2:
            statut = st.selectbox(":material/toggle_on: Statut", statut_list, key=f"{prefix}_statut")
        with c3:
            search = st.text_input(":material/search: Rechercher", placeholder="Nom, contact...", key=f"{prefix}_search")
        return pays, statut, search

    def afficher_bottin(df, prefix):
        pays, statut, search = filtres(prefix)
        df_f = df.copy()
        if pays != "Tous": df_f = df_f[df_f["Pays"] == [k for k,v in PAYS_CEMAC.items() if v["nom"]==pays][0] if pays in [v["nom"] for v in PAYS_CEMAC.values()] else pays]
        if statut != "Tous": df_f = df_f[df_f["Statut"] == statut]
        if search: df_f = df_f[df_f.apply(lambda r: search.lower() in r.to_string().lower(), axis=1)]

        st.markdown(f"<div style='font-size:0.82rem; color:#8C8C8C; margin-bottom:0.5rem;'>{len(df_f)} entrée(s)</div>", unsafe_allow_html=True)
        st.dataframe(df_f, use_container_width=True, hide_index=True)

        col_dl, _ = st.columns([1,4])
        with col_dl:
            csv = df_f.to_csv(index=False).encode("utf-8")
            st.download_button(":material/download: Exporter CSV", csv, "bottin_export.csv", "text/csv", key=f"{prefix}_dl")

    with tab_svt:
        st.markdown("### Spécialistes en Valeurs du Trésor (SVT)")
        st.markdown("Les SVT sont les intermédiaires obligatoires sur le marché primaire. Ils soumettent les offres pour le compte de leurs clients lors des adjudications.")
        afficher_bottin(bottin["SVT"], "svt")

        st.markdown("---")
        st.markdown("#### Réseaux nationaux de SVT par pays")
        from data.simulations import get_svt_dataframe
        df_svt = get_svt_dataframe()
        svt_actifs = df_svt[df_svt["statut"] == "Actif"]
        cols = st.columns(3)
        for i, (code, info) in enumerate(PAYS_CEMAC.items()):
            nb = len(svt_actifs[svt_actifs["pays"] == code])
            with cols[i % 3]:
                st.markdown(f"""
                <div class="metric-card" style="margin-bottom:0.8rem;">
                    <div class="metric-value">{nb}</div>
                    <div class="metric-label">{info['nom']}</div>
                </div>
                """, unsafe_allow_html=True)

    with tab_sgp:
        st.markdown("### Sociétés de Gestion et de Portefeuille (SGP)")
        afficher_bottin(bottin["SGP"], "sgp")

    with tab_sdb:
        st.markdown("### Sociétés de Bourse (SDB)")
        afficher_bottin(bottin["SDB"], "sdb")

    with tab_inv:
        st.markdown("### Investisseurs institutionnels")
        st.caption("Liste des investisseurs institutionnels enregistrés et validés sur le marché CEMAC.")
        afficher_bottin(bottin["Investisseurs"], "inv")
