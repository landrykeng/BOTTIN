import streamlit as st
from data.simulations import get_publications, get_faq
import pandas as pd
import numpy as np

# ── Réglementation ────────────────────────────────────────────────────────────
def show_reglementation():
    st.title("Réglementation applicable")
    st.markdown("Bibliothèque des textes réglementaires du marché des valeurs du Trésor CEMAC.")

    docs = [
        {"categorie": "Règlement",      "titre": "Règlement n°01/24/CEMAC/UMAC — Émission des valeurs du Trésor",       "date": "2024-01-15", "ref": "CEMAC/01/2024"},
        {"categorie": "Instruction",    "titre": "Instruction n°03/23 — Procédures d'adjudication sur le marché primaire", "date": "2023-07-10", "ref": "BEAC/CRCT/003/2023"},
        {"categorie": "Circulaire",     "titre": "Circulaire n°12/23 — Accréditation des Spécialistes en Valeurs du Trésor","date": "2023-09-01","ref": "BEAC/CRCT/012/2023"},
        {"categorie": "Règle de cotation","titre":"Règles de cotation des valeurs du Trésor sur le marché secondaire CEMAC","date":"2022-03-15","ref":"BVMAC/RC/2022/01"},
        {"categorie": "Instruction",    "titre": "Instruction n°05/22 — Conditions d'accès au marché pour les non-résidents","date":"2022-06-20","ref":"BEAC/CRCT/005/2022"},
        {"categorie": "Règlement",      "titre": "Règlement n°04/21/CEMAC — Surveillance du marché des valeurs mobilières","date":"2021-11-05","ref":"CEMAC/04/2021"},
        {"categorie": "Circulaire",     "titre": "Circulaire n°08/21 — Reporting des SVT et obligations déclaratives",      "date":"2021-04-20","ref":"BEAC/CRCT/008/2021"},
        {"categorie": "Instruction",    "titre": "Instruction n°02/20 — Modalités de règlement-livraison des titres",       "date":"2020-09-12","ref":"BEAC/CRCT/002/2020"},
    ]

    cat_filter = st.selectbox(":material/filter_list: Filtrer par catégorie", ["Tous"] + list({d["categorie"] for d in docs}))
    docs_f = docs if cat_filter == "Tous" else [d for d in docs if d["categorie"] == cat_filter]

    for doc in docs_f:
        badge_colors = {
            "Règlement":       "#003366",
            "Instruction":     "#C8A84B",
            "Circulaire":      "#004080",
            "Règle de cotation":"#9E7B28",
        }
        color = badge_colors.get(doc["categorie"], "#8C8C8C")
        with st.expander(f"**{doc['titre']}**"):
            col1, col2, col3 = st.columns([2,1,1])
            with col1:
                st.markdown(f"<span style='background:{color};color:white;padding:3px 10px;border-radius:3px;font-size:0.75rem;font-weight:700'>{doc['categorie']}</span>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**Référence :** {doc['ref']}")
            with col3:
                st.markdown(f"**Date :** {doc['date']}")
            st.markdown("*Ce document est disponible en téléchargement pour les utilisateurs enregistrés.*")
            st.button(":material/download: Télécharger (PDF)", key=f"dl_{doc['ref']}", disabled=not st.session_state.get("authenticated", False))


# ── Guide de l'investisseur ───────────────────────────────────────────────────
def show_guide():
    st.title("Guide de l'investisseur")
    st.markdown("*Section pédagogique à destination des investisseurs souhaitant participer au marché des valeurs du Trésor de la CEMAC.*")

    tabs = st.tabs([
        ":material/info: Présentation du marché",
        ":material/assignment: Procédures",
        ":material/description: Instruments",
        ":material/person_add: Critères d'éligibilité",
        ":material/glossary: Glossaire",
    ])

    with tabs[0]:
        st.markdown("### Le marché des valeurs du Trésor CEMAC")
        st.markdown("""
Le marché des valeurs du Trésor de la CEMAC est le cadre dans lequel les États membres de la Communauté 
émettent des titres de créance pour financer leurs besoins de trésorerie et leurs investissements. Il est 
organisé et supervisé par la **BEAC** via le **CRCT** (Comité de Règlement, de Compensation et de Trésorerie).

**Les acteurs principaux :**
- **BEAC/CRCT** : Organisateur des adjudications et garant de la transparence du marché
- **SVT (Spécialistes en Valeurs du Trésor)** : Institutions financières agréées, intermédiaires obligatoires sur le marché primaire
- **SGP (Sociétés de Gestion et de Portefeuille)** : Gestionnaires d'actifs intervenant sur le marché secondaire
- **SDB (Sociétés de Bourse)** : Intermédiaires agréés sur les bourses régionales
- **Investisseurs** : Institutionnels, banques, entreprises, personnes physiques qualifiées
        """)

    with tabs[1]:
        st.markdown("### Comment participer aux adjudications")
        steps = [
            (":material/how_to_reg:", "1. Créer un compte",      "Remplissez le formulaire d'inscription sur cette plateforme et joignez vos pièces justificatives."),
            (":material/verified:",   "2. Validation BEAC",      "L'administrateur BEAC examine votre dossier et valide votre compte sous 5 jours ouvrés."),
            (":material/contacts:",   "3. Choisir un SVT",       "Identifiez un Spécialiste en Valeurs du Trésor accrédité dans le Bottin et ouvrez un compte auprès de lui."),
            (":material/gavel:",      "4. Soumettre une offre",  "Transmettez votre offre (montant, taux) à votre SVT avant l'heure limite de chaque adjudication."),
            (":material/receipt:",    "5. Résultats",            "Les résultats sont publiés le jour même. Votre SVT vous notifie de l'allocation obtenue."),
        ]
        for icon, titre, desc in steps:
            st.markdown(f"""
            <div class="app-card" style="margin-bottom:0.8rem; display:flex; align-items:flex-start; gap:1rem;">
                <div style="font-size:1.5rem; color:#003366; min-width:40px;">{icon}</div>
                <div>
                    <div style="font-weight:700; color:#003366;">{titre}</div>
                    <div style="font-size:0.9rem; color:#4A4A4A;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tabs[2]:
        st.markdown("### Les instruments disponibles")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="app-card">
                <div style="font-weight:700; color:#003366; font-size:1rem; margin-bottom:0.5rem;">:material/timer: Bons du Trésor Assimilables (BTA)</div>
                <div style="font-size:0.88rem; color:#4A4A4A; line-height:1.6;">
                    <b>Maturités :</b> 13, 26 ou 52 semaines<br>
                    <b>Usage :</b> Financement de la trésorerie à court terme<br>
                    <b>Taux :</b> Déterminé par adjudication<br>
                    <b>Marché :</b> Primaire (adjudication) + Secondaire<br>
                    <b>Minimum :</b> 1 000 000 XAF
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="app-card">
                <div style="font-weight:700; color:#003366; font-size:1rem; margin-bottom:0.5rem;">:material/event: Obligations du Trésor Assimilables (OTA)</div>
                <div style="font-size:0.88rem; color:#4A4A4A; line-height:1.6;">
                    <b>Maturités :</b> 2, 3, 5, 7, 10 ou 15 ans<br>
                    <b>Usage :</b> Financement des investissements publics<br>
                    <b>Coupon :</b> Annuel, taux fixe<br>
                    <b>Marché :</b> Primaire (adjudication) + Secondaire<br>
                    <b>Minimum :</b> 5 000 000 XAF
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tabs[3]:
        st.markdown("### Qui peut investir ?")
        profils = [
            ("Investisseurs institutionnels","Compagnies d'assurance, caisses de prévoyance, fonds de pension, OPCVMs. Accès direct via SVT.","Actif"),
            ("Banques commerciales","Établissements de crédit agréés dans la zone CEMAC ou hors zone avec accréditation BEAC.","Actif"),
            ("Entreprises","Sociétés commerciales souhaitant placer leur trésorerie. Accès via SVT ou SDB.","Actif"),
            ("Personnes physiques qualifiées","Investisseurs individuels disposant d'un patrimoine financier significatif. Dossier d'éligibilité requis.","Restreint"),
            ("Investisseurs non-résidents et diaspora","Tout investisseur hors CEMAC souhaitant participer au marché. Processus de validation renforcé.","Restreint"),
        ]
        for nom, desc, acc in profils:
            badge = f"<span style='background:{'#003366' if acc=='Actif' else '#C8A84B'};color:white;padding:2px 8px;border-radius:3px;font-size:0.72rem;'>{acc}</span>"
            with st.expander(f"**{nom}** {badge}", expanded=False):
                st.markdown(desc)

    with tabs[4]:
        st.markdown("### Glossaire des termes clés")
        termes = [
            ("Adjudication", "Processus par lequel les émetteurs attribuent des titres aux investisseurs selon les offres reçues, en retenant celles présentant le taux le plus favorable."),
            ("Taux marginal","Taux limite à partir duquel les offres sont retenues lors d'une adjudication. Toutes les offres présentant un taux inférieur ou égal sont servies."),
            ("Taux de couverture","Ratio entre le montant total des offres reçues et le montant mis en adjudication. Un taux > 1 indique une demande excédant l'offre."),
            ("Taux moyen pondéré (TMP)","Moyenne des taux de toutes les offres retenues, pondérée par les montants correspondants."),
            ("Code ISIN","Identifiant international unique à 12 caractères attribué à chaque émission de titre."),
            ("Marché primaire","Marché sur lequel les nouvelles émissions de titres sont vendues pour la première fois."),
            ("Marché secondaire","Marché sur lequel les titres déjà émis sont négociés entre investisseurs."),
            ("SVT","Spécialiste en Valeurs du Trésor — institution financière agréée par la BEAC comme intermédiaire obligatoire sur le marché primaire."),
            ("Encours","Montant total des titres en circulation à une date donnée, non encore remboursés."),
            ("Duration","Mesure de la sensibilité du prix d'un titre aux variations de taux d'intérêt, exprimée en années."),
        ]
        for terme, definition in termes:
            with st.expander(f"**{terme}**"):
                st.markdown(definition)


# ── Publications ──────────────────────────────────────────────────────────────
def show_publications():
    st.title("Publications officielles")
    st.caption("Bulletins trimestriels, rapports annuels et notes de marché en accès libre.")

    df_pubs = get_publications()
    df_pub_pub = df_pubs[df_pubs["acces"] == "Public"].copy()

    col1, col2 = st.columns([1,2])
    with col1:
        cat_sel = st.multiselect(":material/filter_list: Catégorie",
            options=df_pub_pub["categorie"].unique().tolist(),
            default=df_pub_pub["categorie"].unique().tolist()[:2])
    with col2:
        search = st.text_input(":material/search: Rechercher", placeholder="Mot-clé...")

    df_f = df_pub_pub.copy()
    if cat_sel:
        df_f = df_f[df_f["categorie"].isin(cat_sel)]
    if search:
        df_f = df_f[df_f["titre"].str.contains(search, case=False)]

    for _, row in df_f.iterrows():
        col_i, col_t, col_d = st.columns([1,4,1])
        with col_i:
            st.markdown(f"<span class='badge-nouveau'>{row['categorie']}</span>", unsafe_allow_html=True)
        with col_t:
            st.markdown(f"**{row['titre']}** — {row['date']} · {row['taille']}")
        with col_d:
            st.button(":material/download: PDF", key=f"pub_{row['titre'][:20]} {np.random.randint(1,1000)}", disabled=True)  # Disabled as we don't have real files
        st.markdown("<hr style='margin:0.4rem 0; border:none; border-top:1px solid #EAE8E2;'>", unsafe_allow_html=True)


# ── FAQ ───────────────────────────────────────────────────────────────────────
def show_faq():
    st.title("Foire Aux Questions")
    st.markdown("*Réponses aux questions fréquentes sur le marché des valeurs du Trésor de la CEMAC.*")

    faqs = get_faq()
    search = st.text_input(":material/search: Rechercher dans la FAQ", placeholder="Ex : BTA, adjudication, investisseur...")

    faqs_f = faqs if not search else [f for f in faqs if search.lower() in f["question"].lower() or search.lower() in f["reponse"].lower()]

    for faq in faqs_f:
        with st.expander(f":material/help: **{faq['question']}**"):
            st.markdown(faq["reponse"])

    st.markdown("---")
    st.info(":material/mail: Vous ne trouvez pas votre réponse ? Contactez-nous à l'adresse **crct@beac.int**")
