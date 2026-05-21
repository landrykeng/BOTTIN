"""
Données simulées reflétant fidèlement le marché des valeurs du Trésor CEMAC
Pays : Cameroun, Gabon, Congo, RCA, Guinée Équatoriale, Tchad
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

PAYS_CEMAC = {
    "CMR": {"nom": "Cameroun",           "code": "CMR", "devise": "XAF"},
    "GAB": {"nom": "Gabon",              "code": "GAB", "devise": "XAF"},
    "COG": {"nom": "Congo",              "code": "COG", "devise": "XAF"},
    "RCA": {"nom": "Rép. Centrafricaine","code": "RCA", "devise": "XAF"},
    "GNQ": {"nom": "Guinée Équatoriale", "code": "GNQ", "devise": "XAF"},
    "TCD": {"nom": "Tchad",              "code": "TCD", "devise": "XAF"},
}

MATURITES_BTA = [13, 26, 52]   # semaines
MATURITES_OTA = [2, 3, 5, 7, 10, 15]  # ans

SVT_DATA = [
    {"raison_sociale": "Société Générale Cameroun",      "pays": "CMR", "type": "SVT", "statut": "Actif", "date_convention": "2023-01-15", "front_contact": "s.mbarga@sgcam.cm",    "middle_contact": "operations@sgcam.cm",    "back_contact": "backoffice@sgcam.cm"},
    {"raison_sociale": "Afriland First Bank",             "pays": "CMR", "type": "SVT", "statut": "Actif", "date_convention": "2022-06-10", "front_contact": "trading@afriland.cm",  "middle_contact": "midoff@afriland.cm",     "back_contact": "back@afriland.cm"},
    {"raison_sociale": "Ecobank Cameroun",                "pays": "CMR", "type": "SVT", "statut": "Actif", "date_convention": "2023-03-20", "front_contact": "market@ecobank.cm",    "middle_contact": "ops@ecobank.cm",         "back_contact": "settlement@ecobank.cm"},
    {"raison_sociale": "BGFI Bank Gabon",                 "pays": "GAB", "type": "SVT", "statut": "Actif", "date_convention": "2022-09-05", "front_contact": "tresor@bgfi.ga",      "middle_contact": "middle@bgfi.ga",         "back_contact": "back@bgfi.ga"},
    {"raison_sociale": "Union Gabonaise de Banque",       "pays": "GAB", "type": "SVT", "statut": "Actif", "date_convention": "2023-07-12", "front_contact": "trading@ugb.ga",      "middle_contact": "ops@ugb.ga",             "back_contact": "settle@ugb.ga"},
    {"raison_sociale": "LCB Bank Congo",                  "pays": "COG", "type": "SVT", "statut": "Actif", "date_convention": "2022-11-30", "front_contact": "front@lcbbank.cg",    "middle_contact": "mid@lcbbank.cg",         "back_contact": "back@lcbbank.cg"},
    {"raison_sociale": "Ecobank Congo",                   "pays": "COG", "type": "SVT", "statut": "Actif", "date_convention": "2023-02-14", "front_contact": "market@ecobank.cg",   "middle_contact": "ops@ecobank.cg",         "back_contact": "back@ecobank.cg"},
    {"raison_sociale": "BGFI Bank Guinée Équatoriale",    "pays": "GNQ", "type": "SVT", "statut": "Actif", "date_convention": "2023-04-01", "front_contact": "tresor@bgfi.gq",      "middle_contact": "middle@bgfi.gq",         "back_contact": "back@bgfi.gq"},
    {"raison_sociale": "Banque de Développement des États de l'Afrique Centrale", "pays": "CMR", "type": "SVT", "statut": "Suspendu", "date_convention": "2021-05-20", "front_contact": "tresor@bdeac.org", "middle_contact": "ops@bdeac.org", "back_contact": "back@bdeac.org"},
    {"raison_sociale": "Commercial Bank Tchad",           "pays": "TCD", "type": "SVT", "statut": "Actif", "date_convention": "2023-08-10", "front_contact": "market@cbt.td",       "middle_contact": "ops@cbt.td",             "back_contact": "back@cbt.td"},
]

SGP_DATA = [
    {"denomination": "CGF Bourse",              "pays": "CMR", "type": "SGP", "agrement": "CMF-SGP-001", "contact": "info@cgfbourse.cm",     "statut": "Actif"},
    {"denomination": "EDC Investments",         "pays": "CMR", "type": "SGP", "agrement": "CMF-SGP-002", "contact": "invest@edcgroup.cm",    "statut": "Actif"},
    {"denomination": "Africaine des Marchés",   "pays": "GAB", "type": "SGP", "agrement": "COB-SGP-001", "contact": "contact@afmarchés.ga",  "statut": "Actif"},
    {"denomination": "Atlantic Finance",         "pays": "COG", "type": "SGP", "agrement": "CMF-SGP-003", "contact": "info@atlanticfin.cg",   "statut": "Actif"},
]

SDB_DATA = [
    {"denomination": "Douala Stock Exchange",   "pays": "CMR", "type": "SDB", "agrement": "DSX-001", "contact": "info@douala-stock-exchange.com", "statut": "Actif"},
    {"denomination": "Bourse des Valeurs Mobilières de l'Afrique Centrale", "pays": "GAB", "type": "SDB", "agrement": "BVMAC-001", "contact": "contact@bvmac.org", "statut": "Actif"},
]

INVESTISSEURS_INST = [
    {"denomination": "CNPS Cameroun",         "pays": "CMR", "type": "Caisse de prévoyance", "point_focal": "invest@cnps.cm",       "statut": "Actif"},
    {"denomination": "CNAMGS Gabon",          "pays": "GAB", "type": "Caisse de prévoyance", "point_focal": "finance@cnamgs.ga",    "statut": "Actif"},
    {"denomination": "Activa Assurances",     "pays": "CMR", "type": "Assurance",            "point_focal": "tresor@activa.cm",     "statut": "Actif"},
    {"denomination": "Prudential Gabon",      "pays": "GAB", "type": "Assurance",            "point_focal": "invest@prudential.ga", "statut": "Actif"},
    {"denomination": "BEAC Réserves",         "pays": "CMR", "type": "Institution publique", "point_focal": "reserves@beac.int",    "statut": "Actif"},
    {"denomination": "Fonds de Garantie CEMAC","pays": "CMR", "type": "Institution publique","point_focal": "fgc@cemac.int",        "statut": "Actif"},
]


def get_svt_dataframe():
    return pd.DataFrame(SVT_DATA)

def get_sgp_dataframe():
    return pd.DataFrame(SGP_DATA)

def get_sdb_dataframe():
    return pd.DataFrame(SDB_DATA)

def get_investisseurs_dataframe():
    return pd.DataFrame(INVESTISSEURS_INST)

def get_bottin_complet():
    svt = pd.DataFrame(SVT_DATA)[["raison_sociale","pays","type","statut","date_convention","front_contact"]]
    svt.columns = ["Dénomination","Pays","Type","Statut","Date convention","Contact"]
    sgp = pd.DataFrame(SGP_DATA)[["denomination","pays","type","statut","agrement","contact"]]
    sgp.columns = ["Dénomination","Pays","Type","Statut","Agrément","Contact"]
    sdb = pd.DataFrame(SDB_DATA)[["denomination","pays","type","statut","agrement","contact"]]
    sdb.columns = ["Dénomination","Pays","Type","Statut","Agrément","Contact"]
    inv = pd.DataFrame(INVESTISSEURS_INST)[["denomination","pays","type","statut","point_focal"]]
    inv.columns = ["Dénomination","Pays","Type","Statut","Contact"]
    return {"SVT": svt, "SGP": sgp, "SDB": sdb, "Investisseurs": inv}


def generer_encours_mensuels(nb_mois=24):
    """Génère un historique d'encours mensuels par pays et instrument"""
    records = []
    date_fin = datetime.now().replace(day=1)
    
    encours_base = {
        "CMR": {"BTA": 850_000, "OTA": 1_200_000},
        "GAB": {"BTA": 420_000, "OTA": 680_000},
        "COG": {"BTA": 180_000, "OTA": 290_000},
        "RCA": {"BTA": 45_000,  "OTA": 60_000},
        "GNQ": {"BTA": 95_000,  "OTA": 130_000},
        "TCD": {"BTA": 120_000, "OTA": 170_000},
    }
    
    for i in range(nb_mois, -1, -1):
        date = date_fin - timedelta(days=i*30)
        for pays_code, instruments in encours_base.items():
            for instrument, base in instruments.items():
                trend = 1 + (nb_mois - i) * 0.008
                bruit = np.random.normal(1, 0.03)
                montant = int(base * trend * bruit)
                records.append({
                    "date": date.strftime("%Y-%m"),
                    "pays": pays_code,
                    "pays_nom": PAYS_CEMAC[pays_code]["nom"],
                    "instrument": instrument,
                    "encours": montant,  # en millions XAF
                })
    
    return pd.DataFrame(records)


def generer_adjudications(nb=80):
    """Génère un historique d'adjudications réalistes"""
    records = []
    date_debut = datetime.now() - timedelta(days=365*2)
    
    taux_base_bta = {"13s": 3.2, "26s": 4.1, "52s": 5.0}
    taux_base_ota = {"2a": 5.8, "3a": 6.3, "5a": 7.1, "7a": 7.6, "10a": 8.2, "15a": 8.9}
    
    for _ in range(nb):
        pays_code = random.choice(list(PAYS_CEMAC.keys()))
        is_bta = random.random() > 0.4
        
        if is_bta:
            mat_key = random.choice(list(taux_base_bta.keys()))
            maturite = mat_key
            taux_ref = taux_base_bta[mat_key]
            instrument = "BTA"
            montant_emis = random.randint(5_000, 50_000)
        else:
            mat_key = random.choice(list(taux_base_ota.keys()))
            maturite = mat_key
            taux_ref = taux_base_ota[mat_key]
            instrument = "OTA"
            montant_emis = random.randint(20_000, 150_000)
        
        taux_marginal = round(taux_ref + np.random.normal(0, 0.3), 2)
        taux_moyen = round(taux_marginal - np.random.uniform(0.05, 0.3), 2)
        taux_couverture = round(random.uniform(0.8, 3.5), 2)
        montant_souscrit = int(montant_emis * taux_couverture)
        montant_retenu = int(montant_emis * random.uniform(0.8, 1.0))
        
        jours = random.randint(0, 730)
        date_adj = date_debut + timedelta(days=jours)
        
        records.append({
            "date": date_adj.strftime("%Y-%m-%d"),
            "pays": pays_code,
            "pays_nom": PAYS_CEMAC[pays_code]["nom"],
            "instrument": instrument,
            "maturite": maturite,
            "montant_emis": montant_emis,
            "montant_souscrit": montant_souscrit,
            "montant_retenu": montant_retenu,
            "taux_marginal": taux_marginal,
            "taux_moyen": taux_moyen,
            "taux_couverture": taux_couverture,
            "code_isin": f"XA{pays_code}{instrument}{random.randint(1000,9999)}",
            "statut": random.choices(["Résultat publié","Résultat publié","Confirmé","Prévisionnel"], weights=[60,20,10,10])[0],
        })
    
    df = pd.DataFrame(records).sort_values("date", ascending=False).reset_index(drop=True)
    return df


def generer_calendrier(nb_futur=15):
    """Génère le calendrier des émissions à venir"""
    records = []
    today = datetime.now()
    
    for i in range(nb_futur):
        jours = random.randint(3, 90)
        date_adj = today + timedelta(days=jours)
        pays_code = random.choice(list(PAYS_CEMAC.keys()))
        instrument = random.choice(["BTA", "OTA"])
        
        if instrument == "BTA":
            maturite = random.choice(["13 semaines", "26 semaines", "52 semaines"])
            montant = random.randint(5_000, 40_000)
        else:
            maturite = random.choice(["2 ans", "3 ans", "5 ans", "7 ans", "10 ans"])
            montant = random.randint(20_000, 120_000)
        
        statut = "Confirmé" if jours < 15 else ("Prévisionnel" if jours > 45 else "Confirmé")
        
        records.append({
            "date": date_adj.strftime("%Y-%m-%d"),
            "heure_limite": "11:00",
            "pays": pays_code,
            "pays_nom": PAYS_CEMAC[pays_code]["nom"],
            "instrument": instrument,
            "maturite": maturite,
            "montant_indicatif": montant,
            "statut": statut,
        })
    
    df = pd.DataFrame(records).sort_values("date").reset_index(drop=True)
    return df


def stats_marche_public():
    """Chiffres clés pour l'espace public"""
    return {
        "encours_global": "4 825,3 Mds XAF",
        "nb_svt_actifs": 9,
        "nb_pays": 6,
        "dernier_taux_bta_13s": "3,45%",
        "volumes_annuels": "1 230,6 Mds XAF",
        "nb_adjudications_annee": 142,
        "taux_couverture_moyen": "1,87x",
        "instruments_codes": 312,
    }


def get_courbe_taux():
    """Courbe de taux par maturité (moyenne CEMAC)"""
    maturites = [0.25, 0.5, 1, 2, 3, 5, 7, 10, 15]
    labels = ["13s", "26s", "52s", "2a", "3a", "5a", "7a", "10a", "15a"]
    taux = [3.2, 4.1, 5.0, 5.8, 6.3, 7.1, 7.6, 8.2, 8.9]
    # Ajout bruit réaliste
    taux_actuels = [round(t + np.random.normal(0, 0.15), 2) for t in taux]
    taux_n1 = [round(t - 0.4 + np.random.normal(0, 0.15), 2) for t in taux]
    return pd.DataFrame({
        "maturite": labels,
        "maturite_num": maturites,
        "taux_actuel": taux_actuels,
        "taux_n1": taux_n1,
    })


def repartition_detenteurs():
    """Ventilation des encours par catégorie de détenteurs"""
    return {
        "SVT": 42.3,
        "Autres banques": 18.7,
        "Institutionnels non-bancaires": 24.1,
        "Personnes physiques": 8.4,
        "Autres": 6.5,
    }


def encours_par_pays():
    """Encours consolidé par pays (en Mds XAF)"""
    return pd.DataFrame([
        {"pays": "Cameroun",           "BTA": 850, "OTA": 1200, "total": 2050},
        {"pays": "Gabon",              "BTA": 420, "OTA": 680,  "total": 1100},
        {"pays": "Congo",              "BTA": 180, "OTA": 290,  "total": 470},
        {"pays": "Guinée Équatoriale", "BTA": 95,  "OTA": 130,  "total": 225},
        {"pays": "Tchad",              "BTA": 120, "OTA": 170,  "total": 290},
        {"pays": "Rép. Centrafricaine","BTA": 45,  "OTA": 60,   "total": 105},
    ])


def get_publications():
    """Liste des publications disponibles"""
    pubs = []
    categories = ["Bulletin trimestriel", "Rapport annuel", "Note de marché", "Réglementation", "Statistiques"]
    for i in range(20):
        date = datetime.now() - timedelta(days=random.randint(0, 500))
        cat = random.choice(categories)
        pubs.append({
            "titre": f"{cat} — {date.strftime('%B %Y')}",
            "categorie": cat,
            "date": date.strftime("%Y-%m-%d"),
            "taille": f"{random.randint(200, 5000)} Ko",
            "acces": "Public" if cat in ["Bulletin trimestriel","Rapport annuel"] else "Restreint",
        })
    return pd.DataFrame(pubs).sort_values("date", ascending=False).reset_index(drop=True)


def get_faq():
    return [
        {"question": "Qu'est-ce qu'une valeur du Trésor ?",
         "reponse": "Une valeur du Trésor est un titre de créance émis par un État membre de la CEMAC pour financer ses besoins de trésorerie (BTA) ou ses investissements à moyen/long terme (OTA). Ces titres sont garantis par l'État et considérés comme sans risque de défaut dans la zone CEMAC."},
        {"question": "Quelle est la différence entre un BTA et une OTA ?",
         "reponse": "Les Bons du Trésor Assimilables (BTA) sont des instruments à court terme (13, 26 ou 52 semaines) utilisés pour la gestion de la trésorerie. Les Obligations du Trésor Assimilables (OTA) sont des instruments à moyen et long terme (2 à 15 ans) destinés au financement d'investissements publics."},
        {"question": "Comment devenir investisseur sur le marché ?",
         "reponse": "Pour accéder au marché primaire, vous devez être un investisseur qualifié et passer par un Spécialiste en Valeurs du Trésor (SVT) accrédité par la BEAC. Créez un compte sur cette plateforme pour accéder au Bottin des SVT et aux informations de contact."},
        {"question": "Comment sont organisées les adjudications ?",
         "reponse": "Les adjudications se tiennent selon un calendrier préétabli publié sur cette plateforme. Elles sont réalisées par voie électronique. Les offres sont soumises par les SVT au nom de leurs clients avant l'heure limite. Les résultats (taux marginal, montant retenu, taux de couverture) sont publiés le même jour."},
        {"question": "Les investisseurs de la diaspora peuvent-ils participer ?",
         "reponse": "Oui, les investisseurs non-résidents et de la diaspora peuvent participer au marché via un SVT accrédité. Ils doivent s'inscrire sur la plateforme, fournir les pièces justificatives demandées, et attendre la validation de leur compte par l'administrateur BEAC."},
        {"question": "Quelle est la fiscalité applicable aux valeurs du Trésor ?",
         "reponse": "La fiscalité varie selon le pays émetteur et le statut de l'investisseur. Consultez la section Réglementation ou rapprochez-vous d'un SVT ou d'un conseiller fiscal pour obtenir des informations précises sur votre situation."},
    ]
