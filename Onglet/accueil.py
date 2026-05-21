import streamlit as st
from data.simulations import stats_marche_public, encours_par_pays, PAYS_CEMAC
import plotly.express as px
import plotly.graph_objects as go

def show():
    stats = stats_marche_public()

    st.title("Marché des Valeurs du Trésor de la CEMAC")
    st.markdown("""
    <p style="font-size:1.05rem; color:#4A4A4A; line-height:1.7; max-width:800px;">
    Bienvenue sur le portail officiel d'information et de répertoire du marché des valeurs 
    du Trésor de la Communauté Économique et Monétaire de l'Afrique Centrale (CEMAC), 
    géré par la <strong>BEAC</strong> et le <strong>CRCT</strong>.
    </p>
    """, unsafe_allow_html=True)

    # ── Chiffres clés ──────────────────────────────────────────────────────────
    st.markdown("## Chiffres clés du marché")
    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, stats["encours_global"],        "Encours global",         ":material/account_balance:"),
        (c2, str(stats["nb_svt_actifs"]),    "SVT accrédités actifs",  ":material/groups:"),
        (c3, stats["volumes_annuels"],        "Volumes émis (12 mois)", ":material/trending_up:"),
        (c4, stats["taux_couverture_moyen"], "Taux de couverture moy.", ":material/show_chart:"),
    ]
    for col, val, label, icon in cards:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size:1.6rem; color:#003366; margin-bottom:4px;">{icon}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c5, c6, c7, c8 = st.columns(4)
    cards2 = [
        (c5, str(stats["nb_pays"]),              "États membres CEMAC",       ":material/public:"),
        (c6, stats["dernier_taux_bta_13s"],      "Dernier taux BTA 13 sem.",  ":material/percent:"),
        (c7, str(stats["nb_adjudications_annee"]),"Adjudications (12 mois)",  ":material/gavel:"),
        (c8, str(stats["instruments_codes"]),     "Codes instruments actifs",  ":material/description:"),
    ]
    for col, val, label, icon in cards2:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size:1.6rem; color:#003366; margin-bottom:4px;">{icon}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Graphique encours par pays ─────────────────────────────────────────────
    col_g, col_t = st.columns([3, 2])

    with col_g:
        st.markdown("## Encours par État membre (Mds XAF)")
        df_pays = encours_par_pays()
        fig = go.Figure()
        fig.add_bar(x=df_pays["pays"], y=df_pays["BTA"], name="BTA", marker_color="#003366")
        fig.add_bar(x=df_pays["pays"], y=df_pays["OTA"], name="OTA", marker_color="#C8A84B")
        fig.update_layout(
            barmode="stack",
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(family="Source Sans 3", size=12),
            legend=dict(orientation="h", y=1.1),
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(tickfont=dict(size=11)),
            yaxis=dict(title="Mds XAF", gridcolor="#EAE8E2"),
            height=300,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_t:
        st.markdown("## Tableau récapitulatif")
        df_pays["BTA"] = df_pays["BTA"].apply(lambda x: f"{x:,} M")
        df_pays["OTA"] = df_pays["OTA"].apply(lambda x: f"{x:,} M")
        df_pays["total"] = df_pays["total"].apply(lambda x: f"{x:,} M")
        df_pays.columns = ["Pays","BTA","OTA","Total (XAF)"]
        st.dataframe(df_pays, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Modules de la plateforme ───────────────────────────────────────────────
    st.markdown("## Accès aux modules")
    modules_pub = [
        (":material/gavel:",        "Résultats des adjudications", "Consultez les derniers résultats publiés par pays et par instrument."),
        (":material/menu_book:",    "Réglementation",              "Accédez aux textes réglementaires, circulaires et règles de cotation."),
        (":material/school:",       "Guide de l'investisseur",     "Comprenez les procédures, les critères d'éligibilité et les instruments."),
        (":material/bar_chart:",    "Statistiques publiques",      "Volumes d'émissions, encours global par pays et graphiques de synthèse."),
        (":material/article:",      "Publications officielles",    "Bulletins trimestriels, rapports annuels en libre accès."),
        (":material/help:",         "FAQ",                         "Réponses aux questions fréquentes sur le marché des valeurs du Trésor."),
    ]
    cols = st.columns(3)
    for i, (icon, titre, desc) in enumerate(modules_pub):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="app-card" style="margin-bottom:1rem;">
                <div style="font-size:1.5rem; color:#003366; margin-bottom:0.5rem;">{icon}</div>
                <div style="font-weight:700; color:#003366; font-size:1rem; margin-bottom:0.3rem;">{titre}</div>
                <div style="font-size:0.87rem; color:#4A4A4A; line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
