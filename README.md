# CTDAM-CEMAC — Bottin des Investisseurs
## Plateforme digitale du marché des valeurs du Trésor CEMAC
**BEAC / CRCT — v1.0 — Mars 2026**

---

## Structure du projet

```
ctdam_cemac/
├── app.py                      # Point d'entrée principal
├── Authentification.py         # Module d'authentification (ton fichier)
├── requirements.txt
├── users.json                  # Créé automatiquement au 1er lancement
├── assets/
│   └── style.css               # Thème BEAC (ton fichier CSS)
├── Picture/
│   ├── Nouveau_logo_BEAC.jpg   # À placer manuellement
│   └── logo_dash.png           # À placer manuellement
├── data/
│   ├── __init__.py
│   └── simulations.py          # Données CEMAC simulées
└── pages/
    ├── __init__.py
    ├── accueil.py
    ├── statistiques_publiques.py
    ├── reglementation.py
    ├── guide_investisseur.py
    ├── publications.py
    ├── faq.py
    ├── inscription.py
    ├── connexion.py
    ├── bottin.py
    ├── donnees_historiques.py
    ├── calendrier.py
    ├── simulation.py
    ├── documents.py
    ├── alertes.py
    └── admin.py
```

---

## Installation

### 1. Prérequis
- Python 3.10 ou supérieur
- pip

### 2. Installation des dépendances
```bash
pip install -r requirements.txt
```

### 3. Ajouter les images
Placez vos images dans le dossier `Picture/` :
- `Nouveau_logo_BEAC.jpg` — Logo officiel BEAC
- `logo_dash.png` — Illustration page de connexion

### 4. Lancement
```bash
streamlit run app.py
```

L'application sera accessible à l'adresse : **http://localhost:8501**

---

## Profils utilisateurs

| Profil | Statut JSON | Accès |
|--------|-------------|-------|
| Visiteur public | — | Pages publiques uniquement |
| Investisseur validé | `Utilisateur` | Espace restreint complet |
| Opérateur de marché | `Superviseur` | Espace restreint + mise à jour Bottin |
| Administrateur BEAC | `Administrateur` | Accès total + back-office |

### Créer le 1er compte administrateur
Au premier lancement, `users.json` est vide. Utilisez le formulaire d'inscription
et modifiez manuellement `users.json` pour passer le statut à `"Administrateur"` :

```json
{
  "users": {
    "admin_beac": {
      "password": "<hash_sha256>",
      "email": "admin@beac.int",
      "status": "Administrateur",
      "active": true
    }
  }
}
```

Ou utilisez `import_users_from_excel("Data/Connexion.xlsx")` si vous avez le fichier Excel.

---

## Fonctionnalités implémentées

### Espace public (sans authentification)
- [x] Page d'accueil avec chiffres clés et graphique encours par pays
- [x] Statistiques agrégées (encours, courbe de taux, répartition détenteurs)
- [x] Réglementation (bibliothèque de textes filtrables)
- [x] Guide de l'investisseur (procédures, instruments, éligibilité, glossaire)
- [x] Publications officielles
- [x] FAQ interactive
- [x] Formulaire d'inscription avec validation

### Espace restreint (avec authentification)
- [x] Bottin des investisseurs (SVT, SGP, SDB, institutionnels) avec filtres et export CSV
- [x] Données historiques (encours mensuels, adjudications, courbe de taux)
- [x] Calendrier des émissions
- [x] Outils de simulation (calculateur rendement, simulateur investissement, comparateur)
- [x] Espace documentaire
- [x] Alertes personnalisées et newsletter

### Espace d'administration (Admin BEAC uniquement)
- [x] Gestion des utilisateurs (via module Authentification.py)
- [x] Import données marché (Excel/CSV)
- [x] Gestion du Bottin (validation des mises à jour)
- [x] Gestion du calendrier des émissions et publication des résultats
- [x] Tableau de bord d'utilisation
- [x] Journal d'activité

---

## Données simulées
Les données sont générées dans `data/simulations.py` et reflètent fidèlement
la réalité du marché CEMAC :
- 6 pays membres (CMR, GAB, COG, RCA, GNQ, TCD)
- 10 SVT, 4 SGP, 2 SDB, 6 investisseurs institutionnels
- 24 mois d'historique d'encours (BTA + OTA)
- 80 adjudications simulées avec taux réalistes
- Courbe de taux complète (13 semaines à 15 ans)
- Calendrier d'émissions à venir

**Pour connecter de vraies données**, remplacez les fonctions dans `data/simulations.py`
par des appels à votre base de données ou à vos fichiers Excel.

---

## Support
BEAC / CRCT — crct@beac.int
