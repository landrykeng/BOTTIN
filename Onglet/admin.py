import streamlit as st
import pandas as pd
from datetime import datetime
from Authentification import admin_panel
from data.simulations import generer_adjudications, get_svt_dataframe, PAYS_CEMAC

def show(sous_page="Gestion des utilisateurs"):
    if not st.session_state.get("authenticated", False):
        st.error(":material/block: Accès refusé."); return

    user_status = st.session_state.get("status", "")
    if user_status not in ["Administrateur", "Admin BEAC"]:
        st.error(f":material/block: Accès réservé aux administrateurs BEAC. Votre profil : **{user_status}**")
        return

    st.markdown(f"""
    <div style="background:linear-gradient(90deg,#003366,#004080); color:white; padding:0.6rem 1.2rem; border-radius:6px; border-left:4px solid #C8A84B; margin-bottom:1.5rem;">
        <span style="font-size:0.8rem; text-transform:uppercase; letter-spacing:1px; color:#C8A84B;">Espace d'administration</span> &nbsp;|&nbsp; 
        <span style="font-weight:600;">{sous_page}</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Gestion des utilisateurs ────────────────────────────────────────────
    if sous_page == "Gestion des utilisateurs":
        st.title("Gestion des utilisateurs")
        admin_panel()

    # ── Import données marché ─────────────────────────────────────────────
    elif sous_page == "Import données marché":
        st.title("Import des données de marché")
        st.markdown("Importez les données d'encours mensuels et de résultats d'adjudications depuis les fichiers Excel/CSV fournis par la CRCT.")

        tab_enc, tab_adj = st.tabs([":material/upload_file: Encours mensuels", ":material/upload_file: Résultats d'adjudications"])

        with tab_enc:
            st.markdown("#### Import des encours mensuels")
            st.info(":material/info: Format attendu : colonnes [pays, instrument (BTA/OTA), maturite, encours_total, date_mois]")
            fichier = st.file_uploader("Choisir le fichier Excel ou CSV", type=["xlsx","csv"], key="enc_upload")
            if fichier:
                try:
                    if fichier.name.endswith(".csv"):
                        df = pd.read_csv(fichier)
                    else:
                        df = pd.read_excel(fichier)
                    st.success(f":material/check_circle: Fichier chargé : {len(df)} lignes, {len(df.columns)} colonnes")
                    st.dataframe(df.head(10), use_container_width=True, hide_index=True)
                    if st.button(":material/save: Valider l'import", type="primary"):
                        st.success(":material/check_circle: Données importées et indexées avec succès.")
                except Exception as e:
                    st.error(f":material/error: Erreur : {e}")

        with tab_adj:
            st.markdown("#### Import des résultats d'adjudications")
            st.info(":material/info: Format attendu : colonnes [date, pays, instrument, maturite, montant_emis, montant_souscrit, montant_retenu, taux_marginal, taux_moyen, taux_couverture, code_isin]")
            fichier2 = st.file_uploader("Choisir le fichier Excel ou CSV", type=["xlsx","csv"], key="adj_upload")
            if fichier2:
                try:
                    if fichier2.name.endswith(".csv"):
                        df2 = pd.read_csv(fichier2)
                    else:
                        df2 = pd.read_excel(fichier2)
                    st.success(f":material/check_circle: Fichier chargé : {len(df2)} lignes")
                    st.dataframe(df2.head(10), use_container_width=True, hide_index=True)
                    if st.button(":material/save: Valider l'import", type="primary", key="val_adj"):
                        st.success(":material/check_circle: Résultats d'adjudications importés.")
                except Exception as e:
                    st.error(f":material/error: Erreur : {e}")

    # ── Gestion du Bottin ─────────────────────────────────────────────────
    elif sous_page == "Gestion du Bottin":
        st.title("Gestion du Bottin des investisseurs")
        df_svt = get_svt_dataframe()

        tab_liste, tab_ajout = st.tabs([":material/list: Fiches existantes", ":material/add: Ajouter / Modifier"])

        with tab_liste:
            st.dataframe(df_svt, use_container_width=True, hide_index=True)
            st.info(":material/info: Les mises à jour soumises par les opérateurs SVT/SGP/SDB apparaissent ici pour validation avant publication.")

            demandes = [
                {"institution": "BGFI Bank Tchad", "type": "SVT", "modification": "Mise à jour email Front Office", "date": "2026-04-10", "statut": "En attente"},
                {"institution": "Afriland First Bank", "type": "SVT", "modification": "Nouveau responsable Middle Office", "date": "2026-04-12", "statut": "En attente"},
            ]
            st.markdown("#### Demandes de mise à jour en attente")
            for d in demandes:
                col1, col2, col3 = st.columns([4,1,1])
                with col1:
                    st.markdown(f"**{d['institution']}** ({d['type']}) — {d['modification']} · {d['date']}")
                with col2:
                    if st.button(":material/check: Valider", key=f"val_{d['institution']}"):
                        st.success("Validé")
                with col3:
                    if st.button(":material/close: Rejeter", key=f"rej_{d['institution']}"):
                        st.warning("Rejeté")

        with tab_ajout:
            with st.form("ajout_bottin"):
                c1, c2 = st.columns(2)
                with c1:
                    nom = st.text_input("Raison sociale *")
                    type_acteur = st.selectbox("Type", ["SVT","SGP","SDB","Investisseur institutionnel"])
                    pays = st.selectbox("Pays", [v["nom"] for v in PAYS_CEMAC.values()])
                with c2:
                    statut = st.selectbox("Statut", ["Actif","Suspendu"])
                    date_conv = st.date_input("Date de convention")
                    agrement = st.text_input("N° d'agrément")

                front = st.text_input("Email Front Office")
                middle = st.text_input("Email Middle Office")
                back = st.text_input("Email Back Office")

                if st.form_submit_button(":material/save: Enregistrer la fiche", type="primary"):
                    st.success(f":material/check_circle: Fiche **{nom}** enregistrée dans le Bottin.")

    # ── Gestion émissions ──────────────────────────────────────────────────
    elif sous_page == "Gestion émissions":
        st.title("Gestion du calendrier des émissions")

        tab_cal, tab_new, tab_res = st.tabs([
            ":material/calendar_month: Calendrier",
            ":material/add_circle: Nouvelle adjudication",
            ":material/edit_document: Publier un résultat",
        ])

        with tab_cal:
            from data.simulations import generer_calendrier
            df_cal = generer_calendrier(15)
            st.dataframe(df_cal, use_container_width=True, hide_index=True)

        with tab_new:
            with st.form("new_adjudication"):
                c1, c2 = st.columns(2)
                with c1:
                    pays_n = st.selectbox("Pays émetteur", [v["nom"] for v in PAYS_CEMAC.values()])
                    instrument_n = st.selectbox("Instrument", ["BTA","OTA"])
                    maturite_n = st.selectbox("Maturité", ["13 semaines","26 semaines","52 semaines","2 ans","3 ans","5 ans","7 ans","10 ans","15 ans"])
                with c2:
                    date_n = st.date_input("Date d'adjudication")
                    heure_n = st.time_input("Heure limite")
                    montant_n = st.number_input("Montant indicatif (M XAF)", value=10000, step=1000)

                statut_n = st.selectbox("Statut", ["Prévisionnel","Confirmé"])
                if st.form_submit_button(":material/add: Ajouter au calendrier", type="primary"):
                    st.success(f":material/check_circle: Adjudication {instrument_n} — {pays_n} ajoutée au calendrier ({statut_n}).")

        with tab_res:
            with st.form("publier_resultat"):
                adj_id = st.selectbox("Sélectionner l'adjudication", ["BTA 13s — Cameroun — 2026-04-20","OTA 5a — Gabon — 2026-04-22"])
                c1, c2, c3 = st.columns(3)
                with c1:
                    mont_souscrit = st.number_input("Montant souscrit (M XAF)", value=18000)
                    mont_retenu = st.number_input("Montant retenu (M XAF)", value=10000)
                with c2:
                    taux_marg = st.number_input("Taux marginal (%)", value=4.25, step=0.01)
                    taux_moy = st.number_input("Taux moyen pondéré (%)", value=4.18, step=0.01)
                with c3:
                    taux_couv = st.number_input("Taux de couverture", value=1.8, step=0.01)
                    code_isin = st.text_input("Code ISIN", value="XACMRBTA2026")
                if st.form_submit_button(":material/publish: Publier le résultat", type="primary"):
                    st.success(":material/check_circle: Résultat publié avec succès. Notifications envoyées aux abonnés.")

    # ── Tableau de bord admin ──────────────────────────────────────────────
    elif sous_page == "Tableau de bord admin":
        st.title("Tableau de bord d'utilisation")

        c1, c2, c3, c4 = st.columns(4)
        for col, val, label in [
            (c1,"1 247","Visiteurs (30j)"),
            (c2,"83","Comptes actifs"),
            (c3,"12","En attente validation"),
            (c4,"3 418","Téléchargements (30j)"),
        ]:
            with col:
                st.markdown(f"""<div class="metric-card"><div class="metric-value">{val}</div><div class="metric-label">{label}</div></div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Pages les plus consultées (30 derniers jours)")
        import plotly.express as px
        pages_data = {"Page": ["Accueil","Statistiques","Bottin","Calendrier","Documents","Simulation"],
                      "Visites": [520, 310, 280, 190, 175, 140]}
        fig = px.bar(pages_data, x="Visites", y="Page", orientation="h",
            color_discrete_sequence=["#003366"])
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Source Sans 3"), height=280,
            yaxis=dict(autorange="reversed"), margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True)

    # ── Journal d'activité ─────────────────────────────────────────────────
    elif sous_page == "Journal d'activité":
        st.title("Journal d'activité")
        st.caption("Historique de toutes les actions effectuées sur la plateforme.")

        journal = [
            {"date": "2026-04-14 09:12", "utilisateur": "admin_beac", "action": "Connexion", "détail": "Session ouverte"},
            {"date": "2026-04-14 09:15", "utilisateur": "admin_beac", "action": "Validation compte", "détail": "Compte investisseur 'sgcam_tresor' validé"},
            {"date": "2026-04-13 14:30", "utilisateur": "bgfi_gabon", "action": "Mise à jour Bottin", "détail": "Mise à jour email Front Office"},
            {"date": "2026-04-13 11:05", "utilisateur": "admin_beac", "action": "Import données", "détail": "Encours mensuels Mars 2026 importés (6 pays, 2 instruments)"},
            {"date": "2026-04-12 16:45", "utilisateur": "admin_beac", "action": "Publication résultat", "détail": "BTA 13s Cameroun — 10 000 M XAF — taux marginal 3.45%"},
            {"date": "2026-04-11 10:20", "utilisateur": "afriland_mid", "action": "Téléchargement", "détail": "Bulletin trimestriel T1 2026 téléchargé"},
        ]
        df_journal = pd.DataFrame(journal)
        search_j = st.text_input(":material/search: Filtrer le journal")
        if search_j:
            df_journal = df_journal[df_journal.apply(lambda r: search_j.lower() in r.to_string().lower(), axis=1)]
        st.dataframe(df_journal, use_container_width=True, hide_index=True)
        csv = df_journal.to_csv(index=False).encode("utf-8")
        st.download_button(":material/download: Exporter le journal", csv, "journal.csv", key="dl_journal")
