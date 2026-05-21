import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from data.simulations import generer_adjudications, generer_encours_mensuels, get_courbe_taux, PAYS_CEMAC

def show():
    if not st.session_state.get("authenticated", False):
        st.warning(":material/lock: Cette section est réservée aux utilisateurs enregistrés et validés.")
        if st.button(":material/login: Se connecter"):
            st.session_state["page"] = "Connexion"; st.rerun()
        return

    st.title("Données historiques du marché")
    st.caption("Historique complet des données de marché — encours, adjudications, taux.")

    tab1, tab2, tab3 = st.tabs([
        ":material/storage: Encours par État et instrument",
        ":material/gavel: Résultats des adjudications",
        ":material/show_chart: Taux de souscription et rendements",
    ])

    df_enc = generer_encours_mensuels(24)
    df_adj = generer_adjudications(80)

    with tab1:
        st.markdown("### Évolution des encours mensuels")

        c1, c2, c3 = st.columns(3)
        with c1:
            pays_sel = st.multiselect("Pays",
                options=list(PAYS_CEMAC.keys()),
                format_func=lambda x: PAYS_CEMAC[x]["nom"],
                default=list(PAYS_CEMAC.keys()),
                key="enc_pays")
        with c2:
            inst_sel = st.selectbox("Instrument", ["Tous","BTA","OTA"], key="enc_inst")
        with c3:
            periode = st.slider("Nombre de mois", 3, 24, 12)

        df_f = df_enc.copy()
        if pays_sel: df_f = df_f[df_f["pays"].isin(pays_sel)]
        if inst_sel != "Tous": df_f = df_f[df_f["instrument"] == inst_sel]
        dates = sorted(df_f["date"].unique())[-periode:]
        df_f = df_f[df_f["date"].isin(dates)]

        df_pivot = df_f.groupby(["date","pays_nom"])["encours"].sum().reset_index()

        fig = px.area(df_pivot, x="date", y="encours", color="pays_nom",
            color_discrete_sequence=["#003366","#C8A84B","#004080","#9E7B28","#0055a5","#E2C97A"],
            labels={"date":"Mois","encours":"Encours (M XAF)","pays_nom":"Pays"})
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Source Sans 3", size=12),
            xaxis=dict(tickangle=-30, gridcolor="#EAE8E2"),
            yaxis=dict(gridcolor="#EAE8E2"), height=380,
            legend=dict(title=""), margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Tableau détaillé")
        df_table = df_f.groupby(["date","pays_nom","instrument"])["encours"].sum().reset_index()
        df_table.columns = ["Mois","Pays","Instrument","Encours (M XAF)"]
        df_table["Encours (M XAF)"] = df_table["Encours (M XAF)"].apply(lambda x: f"{x:,}")
        st.dataframe(df_table, use_container_width=True, hide_index=True)

        csv = df_f.to_csv(index=False).encode("utf-8")
        st.download_button(":material/download: Exporter en CSV", csv, "encours_historique.csv", key="dl_enc")

    with tab2:
        st.markdown("### Résultats des adjudications")

        c1, c2, c3 = st.columns(3)
        with c1:
            pays_a = st.multiselect("Pays",
                options=list(PAYS_CEMAC.keys()),
                format_func=lambda x: PAYS_CEMAC[x]["nom"],
                default=list(PAYS_CEMAC.keys()),
                key="adj_pays")
        with c2:
            inst_a = st.selectbox("Instrument", ["Tous","BTA","OTA"], key="adj_inst")
        with c3:
            statut_a = st.selectbox("Statut", ["Tous","Résultat publié","Confirmé","Prévisionnel"], key="adj_statut")

        df_af = df_adj.copy()
        if pays_a: df_af = df_af[df_af["pays"].isin(pays_a)]
        if inst_a != "Tous": df_af = df_af[df_af["instrument"] == inst_a]
        if statut_a != "Tous": df_af = df_af[df_af["statut"] == statut_a]

        def color_statut(val):
            colors = {"Résultat publié": "#003366","Confirmé":"#C8A84B","Prévisionnel":"#8C8C8C"}
            c = colors.get(val, "#8C8C8C")
            return f"color:{c}; font-weight:600"

        st.dataframe(
            df_af[["date","pays_nom","instrument","maturite","montant_emis","montant_souscrit","montant_retenu","taux_marginal","taux_moyen","taux_couverture","code_isin","statut"]].rename(columns={
                "date":"Date","pays_nom":"Pays","instrument":"Instrument","maturite":"Maturité",
                "montant_emis":"Émis (M)","montant_souscrit":"Souscrit (M)","montant_retenu":"Retenu (M)",
                "taux_marginal":"Tx marginal (%)","taux_moyen":"TMP (%)","taux_couverture":"Couverture",
                "code_isin":"Code ISIN","statut":"Statut"
            }),
            use_container_width=True, hide_index=True
        )

        csv2 = df_af.to_csv(index=False).encode("utf-8")
        st.download_button(":material/download: Exporter en CSV", csv2, "adjudications.csv", key="dl_adj")

    with tab3:
        st.markdown("### Courbe de taux interactive")
        df_taux = get_courbe_taux()

        fig2 = go.Figure()
        fig2.add_scatter(x=df_taux["maturite"], y=df_taux["taux_actuel"],
            mode="lines+markers", name="Taux actuel",
            line=dict(color="#003366", width=2.5),
            marker=dict(size=8, color="#C8A84B", line=dict(color="#003366",width=1.5)))
        fig2.add_scatter(x=df_taux["maturite"], y=df_taux["taux_n1"],
            mode="lines+markers", name="N-1",
            line=dict(color="#8C8C8C", width=1.5, dash="dot"),
            marker=dict(size=5))
        fig2.update_layout(plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Source Sans 3", size=12),
            xaxis=dict(title="Maturité", gridcolor="#EAE8E2"),
            yaxis=dict(title="Taux (%)", gridcolor="#EAE8E2"),
            height=350, margin=dict(l=0,r=0,t=20,b=0),
            legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### Évolution du taux marginal par adjudication")
        df_rp = df_adj[df_adj["statut"] == "Résultat publié"].copy()
        fig3 = px.scatter(df_rp, x="date", y="taux_marginal", color="instrument",
            size="montant_retenu", hover_data=["pays_nom","maturite","taux_couverture"],
            color_discrete_map={"BTA":"#003366","OTA":"#C8A84B"},
            labels={"date":"Date","taux_marginal":"Taux marginal (%)","instrument":"Instrument"})
        fig3.update_layout(plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Source Sans 3"), height=340,
            xaxis=dict(gridcolor="#EAE8E2", tickangle=-30),
            yaxis=dict(gridcolor="#EAE8E2"), margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig3, use_container_width=True)
