"""
Module pour créer des graphiques avec streamlit-echarts
Auteur: LK
Date: 2025
"""

import random
from PIL import Image
import plotly.graph_objects as go
import io
import time
from shapely import bounds
import streamlit as st
from streamlit_echarts import st_echarts
import numpy as np
import geopandas as gpd
import pandas as pd
import folium
from datetime import datetime
from shapely.geometry import Point
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster,FastMarkerCluster
from streamlit_folium import folium_static
import branca.colormap as cm
import datetime as dt
import base64
import os
from pathlib import Path
from typing import Optional, Dict, List, Union
from My_Cspro_function import *
from math import radians, cos, sin, asin, sqrt
import streamlit.components.v1 as components
from folium import Choropleth, Marker, Icon





@st.fragment
def afficher_heure():
    time.sleep(60)
    st.session_state.position=1
    st.rerun()

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


#Fonction de mise à jour des donnée
def upgrade_data():
    with st.spinner("Mise à jour des données...", show_time=True):
        try:
            #dg.columns
            download_ftp_files()
            Unzip_All_Files()
            #st.session_state.df_rejet, st.session_state.df_synthese, st.session_state.df_initial =extraire_et_agreger_csdb("extracted_data")
            st.session_state.position=0
            st.success(f"Dernière mise à jour effectuée avec succès à {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            st.session_state.df_rejet=pd.read_excel("Data_collected.xlsx",sheet_name="Rejet")
            st.session_state.df_synthese=pd.read_excel("Data_collected.xlsx",sheet_name="Synthese")
            st.session_state.df_initial=pd.read_excel("Data_collected.xlsx",sheet_name="Initial")
            st.session_state.position=0
            st.warning("Erreur lors la mise à jour du tableau de bord : vérifiez votre connexion internet")

# Fonction pour calculer la distance entre deux points GPS


def haversine(lon1, lat1, lon2, lat2):
    # Convertir les degrés en radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # Formule de Haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Rayon de la Terre en mètres
    r = 6371000  
    return c * r

#3. Fonction d'affichage des métriques version 1
def display_single_metric_advanced(label, value, delta, unit="", caption="", color_scheme="blue",delta_label="Progress"):
    """Affiche une seule métrique avec un style avancé et personnalisable."""

    color = {
        "blue": {"bg": "#e6f2ff", "text": "#336699", "delta_pos": "#007bff", "delta_neg": "#dc3545"},
        "green": {"bg": "#e6ffe6", "text": "#28a745", "delta_pos": "#28a745", "delta_neg": "#dc3545"},
        "red": {"bg": "#ffe6e6", "text": "#dc3545", "delta_pos": "#28a745", "delta_neg": "#dc3545"},
        "yellow": {"bg": "#fff3cd", "text": "#856404", "delta_pos": "#28a745", "delta_neg": "#dc3545"},
        "purple": {"bg": "#f8d7da", "text": "#6f42c1", "delta_pos": "#28a745", "delta_neg": "#dc3545"},
        "orange": {"bg": "#fff3cd", "text": "#856404", "delta_pos": "#28a745", "delta_neg": "#dc3545"},
        "pink": {"bg": "#f8d7da", "text": "#d63384", "delta_pos": "#28a745", "delta_neg": "#dc3545"},
        "teal": {"bg": "#e6f2ff", "text": "#20c997", "delta_pos": "#28a745", "delta_neg": "#dc3545"},
        "gray": {"bg": "#f0f0f0", "text": "#6c757d", "delta_pos": "#28a745", "delta_neg": "#dc3545"},
    }.get(color_scheme, {"bg": "#f0f0f0", "text": "#333", "delta_pos": "#28a745", "delta_neg": "#dc3545"})

    delta_color = "green" if delta >= 0 else "red"
    st.markdown(
        f"""
        <div style="
            display: flex;
            flex-direction: column;
            align-items: top;
            justify-content: top;
            background: linear-gradient(135deg, {color['bg']} 30%, rgba(255,255,255,0.8) 100%);
            padding: 5px;
            border-radius: 20px;
            box-shadow: 0 4px 5px rgba(0,0,0,0.2);
            text-align: top;
            font-size: 8px;
            transition: all 0.3s ease;
        "
        onmouseover="this.style.transform='scale(1.1)'; this.style.boxShadow='0 6px 12px rgba(0,0,0,0.3)'; this.style.backgroundColor='rgba(255,255,255,0.9)';"
        onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.2)'; this.style.backgroundColor='rgba(255,255,255,0.8)';">
            <h5 style="color: {color['text']}; margin-bottom: 3px; font-family: Arial, sans-serif; font-weight: bold;">
                {label}
            </h5>
            <div style="font-size: 15px; font-weight: bold; color: {color['text']};">
                <h3 class="dashboard-main-title", margin-bottom: 1px; style="font-family: Arial, sans-serif; font-weight: bold; position: relative; top: 0px;"> 
                {value} {unit}
                </h4>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def display_single_metric_advanced2(label, value, delta, unit="", caption="", color_scheme="blue", delta_label="Progress"):
    """Affiche une seule métrique avec un style avancé et personnalisable."""

    color = {
        "blue": {"bg": "#e6f2ff", "text": "#336699", "delta_pos": "#007bff", "delta_neg": "#dc3545"},
        "green": {"bg": "#e6ffe6", "text": "#28a745", "delta_pos": "#28a745", "delta_neg": "#dc3545"},
        "red": {"bg": "#ffe6e6", "text": "#dc3545", "delta_pos": "#28a745", "delta_neg": "#dc3545"},
        "yellow": {"bg": "#fff3cd", "text": "#856404", "delta_pos": "#28a745", "delta_neg": "#dc3545"},
        "purple": {"bg": "#f8d7da", "text": "#6f42c1", "delta_pos": "#28a745", "delta_neg": "#dc3545"},
        "orange": {"bg": "#fff3cd", "text": "#856404", "delta_pos": "#28a745", "delta_neg": "#dc3545"},
        "pink": {"bg": "#f8d7da", "text": "#d63384", "delta_pos": "#28a745", "delta_neg": "#dc3545"},
        "teal": {"bg": "#e6f2ff", "text": "#20c997", "delta_pos": "#28a745", "delta_neg": "#dc3545"},
        "gray": {"bg": "#f0f0f0", "text": "#6c757d", "delta_pos": "#28a745", "delta_neg": "#dc3545"},
    }.get(color_scheme, {"bg": "#f0f0f0", "text": "#333", "delta_pos": "#28a745", "delta_neg": "#dc3545"})

    delta_color = "green" if delta >= 0 else "red"
    st.markdown(
        f"""
        <div style="
            display: flex;
            flex-direction: column;
            align-items: top;
            justify-content: top;
            background: linear-gradient(135deg, {color['bg']} 30%, rgba(255,255,255,0.8) 100%);
            padding: 15px;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            text-align: top;
            font-size: 20px;
            transition: all 0.3s ease;
            transform: translateY(0);
        "
        onmouseover="this.style.transform='translateY(-8px)'; this.style.boxShadow='0 12px 40px rgba(0,0,0,0.2)';"
        onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 32px rgba(0,0,0,0.1)';">
            <h4 style="color: {color['text']}; margin-bottom: 5px; font-family: Arial, sans-serif; font-weight: bold;">
                {label}
            </h4>
            <div style="font-size: 19px; font-weight: bold; color: {color['text']};">
                <h2 class="dashboard-main-title" style="font-family: Arial, sans-serif; font-weight: bold; position: relative; top: 0px; margin-bottom: 1px;"> 
                Nombre: {value} {unit}
                </h2>
            </div>
            <div style="font-size: 15.5px; color: {color['text'] if delta >= 0 else color['delta_neg']};">
                <h3>{delta_label}: {'▲' if delta >= 0 else '▼'} {abs(delta)} % </h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def graphique_barre_simple(df: pd.DataFrame, 
                          x_col: str, 
                          y_col: str, 
                          titre: str = "Graphique à barres",
                          horizontal: bool = False,
                          couleur: str = "#5470c6") -> None:
    """
    Crée un graphique à barres simple (vertical ou horizontal)
    
    Args:
        df: DataFrame contenant les données
        x_col: nom de la colonne pour l'axe X
        y_col: nom de la colonne pour l'axe Y
        titre: titre du graphique
        horizontal: True pour horizontal, False pour vertical
        couleur: couleur des barres
    """
    
    # Préparer les données
    x_data = df[x_col].tolist()
    y_data = df[y_col].tolist()
    
    if horizontal:
        option = {
            "title": {"text": titre, "left": "center"},
            "tooltip": {"trigger": "axis"},
            "xAxis": {"type": "value"},
            "yAxis": {"type": "category", "data": x_data},
            "series": [{
                "type": "bar",
                "data": y_data,
                "itemStyle": {"color": couleur}
            }]
        }
    else:
        option = {
            "title": {"text": titre, "left": "center"},
            "tooltip": {"trigger": "axis"},
            "xAxis": {"type": "category", "data": x_data},
            "yAxis": {"type": "value"},
            "series": [{
                "type": "bar",
                "data": y_data,
                "itemStyle": {"color": couleur}
            }]
        }
    
    st_echarts(options=option, height="400px")



def format_number(value):
    """
    Formate les nombres avec séparateur de milliers (espace)
    """
    if isinstance(value, (int, float)):
        if isinstance(value, float) and not value.is_integer():
            return f"{value:,.2f}".replace(",", " ").replace(".", ",")
        return f"{int(value):,}".replace(",", " ")
    return str(value)


def display_metric(
    label,
    value,
    unit=None,
    delta=None,
    delta_unit=None,
    delta_label=None,
    border_color="#3b82f6"
):

    # Formatage valeur principale
    value_str = format_number(value)
    if unit:
        value_str = f"{value_str} {unit}"

    # Delta
    delta_html = ""
    if delta is not None:
        is_positive = (isinstance(delta, (int, float)) and delta > 0) or str(delta).startswith("+")
        delta_color = "#10b981" if is_positive else "#ef4444"
        delta_prefix = "" if isinstance(delta, (int, float)) and delta > 0 else ""

        delta_value = format_number(delta)
        delta_text = f"{delta_prefix}{delta_value}"
        if delta_unit:
            delta_text = f"{delta_text} {delta_unit}"

        delta_html = f"""
        <div style="margin-top:8px;font-size:14px;">
            <span style="color:{delta_color};font-weight:600;">
                {delta_text}
            </span>
            {f"<span style='color:#6b7280;margin-left:4px;'>{delta_label}</span>" if delta_label else ""}
        </div>
        """

    # HTML final
    html = f"""
    <div style="
        background:#f9fafb;
        border-left:5px solid {border_color};
        border-radius:10px;
        padding:18px;
        box-shadow:0 2px 6px rgba(0,0,0,0.08);
        font-family:Inter, sans-serif;
    ">
        <div style="
            color:#6b7280;
            font-size:12px;
            font-weight:600;
            text-transform:uppercase;
            letter-spacing:0.05em;
            margin-bottom:6px;
        ">
            {label}
        </div>

        <div style="
            color:#111827;
            font-size:36px;
            font-weight:700;
            line-height:1.1;
        ">
            {value_str}
        </div>

        {delta_html}
    </div>
    """

    components.html(html, height=140)


def display_dataframe(
    df,
    header_color="#e8f5e9",
    text_color="#2d3748",
    height=400
):

    styled_df = df.style.hide(axis="index")

    # -------- FORMATAGE DES NOMBRES --------
    num_cols = df.select_dtypes(include=["number"]).columns

    def format_number(x):
        if pd.isna(x):
            return ""
        if isinstance(x, float):
            return f"{x:,.2f}".replace(",", " ").replace(".", ",")
        return f"{int(x):,}".replace(",", " ")

    styled_df = styled_df.format({col: format_number for col in num_cols})

    # -------- STYLES GLOBAUX --------
    styles = [
        {
            "selector": "thead th",
            "props": [
                ("background-color", header_color),
                ("color", text_color),
                ("font-weight", "700"),
                ("text-transform", "uppercase"),
                ("font-size", "11px"),
                ("letter-spacing", "0.05em"),
                ("padding", "12px 16px"),
                ("position", "sticky"),
                ("top", "0"),
                ("z-index", "2"),
            ],
        },
        {
            "selector": "tbody td",
            "props": [
                ("padding", "14px 16px"),
                ("border-bottom", "1px solid #e5e7eb"),
                ("font-size", "14px"),
                ("color", text_color),
                ("white-space", "nowrap"),
            ],
        },
        {
            "selector": "tbody tr:hover",
            "props": [("background-color", "#e25a0b")],
        },
        {
            "selector": "table",
            "props": [
                ("width", "100%"),
                ("border-collapse", "collapse"),
            ],
        },
    ]

    styled_df = styled_df.set_table_styles(styles)

    # -------- RENDU HTML AVEC SCROLL --------
    html = styled_df.to_html()

    st.markdown(
        f"""
        <div style="
            max-height:{height}px;
            overflow-y:auto;
            border-radius:8px;
            box-shadow:0 1px 3px rgba(0,0,0,0.1);
        "> {html}</div>
        """,
        unsafe_allow_html=True,
    )



def graphique_barre_croise_effectifs(df: pd.DataFrame,
                                   x_col: str,
                                   group_col: str,
                                   y_col: str,
                                   titre: str = "Graphique à barres croisées",
                                   empile: bool = False) -> None:
    """
    Crée un graphique à barres croisées des effectifs
    
    Args:
        df: DataFrame contenant les données
        x_col: nom de la colonne pour l'axe X
        group_col: nom de la colonne pour le regroupement
        y_col: nom de la colonne des valeurs
        titre: titre du graphique
        empile: True pour empilé, False pour juxtaposé
    """
    #
    # Pivoter les données
    pivot_df = df.pivot_table(values=y_col, index=x_col, columns=group_col, fill_value=0)
    
    x_data = pivot_df.index.tolist()
    series_data = []
    
    for col in pivot_df.columns:
        series_data.append({
            "name": str(col),
            "type": "bar",
            "data": pivot_df[col].tolist(),
            "stack": "total" if empile else None
        })
    
    option = {
        "title": {"text": titre, "left": "center"},
        "tooltip": {"trigger": "axis"},
        "legend": {"data": [str(col) for col in pivot_df.columns]},
        "xAxis": {"type": "category", "data": x_data},
        "yAxis": {"type": "value"},
        "series": series_data
    }
    
    st_echarts(options=option, height="400px")


def graphique_barre_croise_frequences(df: pd.DataFrame,
                                    x_col: str,
                                    group_col: str,
                                    titre: str = "Graphique à barres croisées (fréquences)") -> None:
    """
    Crée un graphique à barres croisées des fréquences empilées
    
    Args:
        df: DataFrame contenant les données
        x_col: nom de la colonne pour l'axe X
        group_col: nom de la colonne pour le regroupement
        titre: titre du graphique
    """
    
    # Calculer les fréquences
    freq_df = pd.crosstab(df[x_col], df[group_col], normalize='index') * 100
    
    x_data = freq_df.index.tolist()
    series_data = []
    
    for col in freq_df.columns:
        series_data.append({
            "name": str(col),
            "type": "bar",
            "data": freq_df[col].round(2).tolist(),
            "stack": "total"
        })
    
    option = {
        "title": {"text": titre, "left": "center"},
        "tooltip": {
            "trigger": "axis",
            "formatter": "{b}<br/>{a}: {c}%"
        },
        "legend": {"data": [str(col) for col in freq_df.columns]},
        "xAxis": {"type": "category", "data": x_data},
        "yAxis": {"type": "value", "axisLabel": {"formatter": "{value}%"}},
        "series": series_data
    }
    
    st_echarts(options=option, height="400px")


def diagramme_secteur(df: pd.DataFrame,
                     label_col: str,
                     value_col: str,
                     titre: str = "Diagramme en secteur") -> None:
    """
    Crée un diagramme en secteur (camembert)
    
    Args:
        df: DataFrame contenant les données
        label_col: nom de la colonne des étiquettes
        value_col: nom de la colonne des valeurs
        titre: titre du graphique
    """
    
    data = [{"value": row[value_col], "name": row[label_col]} for _, row in df.iterrows()]
    
    option = {
        "title": {"text": titre, "left": "center"},
        "tooltip": {"trigger": "item"},
        "legend": {"orient": "vertical", "left": "left"},
        "series": [{
            "type": "pie",
            "radius": "50%",
            "data": data,
            "emphasis": {
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowOffsetX": 0,
                    "shadowColor": "rgba(0, 0, 0, 0.5)"
                }
            }
        }]
    }
    
    st_echarts(options=option, height="400px")


def diagramme_donut(df: pd.DataFrame,
                   label_col: str,
                   value_col: str,
                   titre: str = "Diagramme en donut") -> None:
    """
    Crée un diagramme en donut
    
    Args:
        df: DataFrame contenant les données
        label_col: nom de la colonne des étiquettes
        value_col: nom de la colonne des valeurs
        titre: titre du graphique
    """
    
    data = [{"value": row[value_col], "name": row[label_col]} for _, row in df.iterrows()]
    
    option = {
        "title": {"text": titre, "left": "center"},
        "tooltip": {"trigger": "item"},
        "legend": {"orient": "vertical", "left": "left"},
        "series": [{
            "type": "pie",
            "radius": ["40%", "70%"],
            "data": data,
            "emphasis": {
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowOffsetX": 0,
                    "shadowColor": "rgba(0, 0, 0, 0.5)"
                }
            }
        }]
    }
    
    st_echarts(options=option, height="400px")


def diagramme_progression(valeur_actuelle: float,
                         valeur_max: float,
                         titre: str = "Diagramme de progression") -> None:
    """
    Crée un diagramme de progression (jauge)
    
    Args:
        valeur_actuelle: valeur actuelle
        valeur_max: valeur maximale
        titre: titre du graphique
    """
    
    pourcentage = (valeur_actuelle / valeur_max) * 100
    
    option = {
        "title": {"text": titre, "left": "center"},
        "series": [{
            "type": "gauge",
            "data": [{"value": pourcentage, "name": "Progression"}],
            "progress": {"show": True},
            "detail": {"valueAnimation": True, "formatter": "{value}%"}
        }]
    }
    
    st_echarts(options=option, height="400px")


def barre_progression_multiple(df: pd.DataFrame,
                              label_col: str,
                              value_col: str,
                              max_col: str,
                              titre: str = "Barres de progression multiples") -> None:
    """
    Crée des barres de progression multiples
    
    Args:
        df: DataFrame contenant les données
        label_col: nom de la colonne des étiquettes
        value_col: nom de la colonne des valeurs actuelles
        max_col: nom de la colonne des valeurs maximales
        titre: titre du graphique
    """
    
    labels = df[label_col].tolist()
    values = df[value_col].tolist()
    max_values = df[max_col].tolist()
    
    # Calculer les pourcentages
    percentages = [(v/m)*100 for v, m in zip(values, max_values)]
    
    option = {
        "title": {"text": titre, "left": "center"},
        "tooltip": {"trigger": "axis"},
        "xAxis": {"type": "value", "max": 100},
        "yAxis": {"type": "category", "data": labels},
        "series": [{
            "type": "bar",
            "data": percentages,
            "itemStyle": {"color": "#91cc75"}
        }]
    }
    
    st_echarts(options=option, height="400px")


def heatmap(df: pd.DataFrame,
           x_col: str,
           y_col: str,
           value_col: str,
           titre: str = "Heatmap") -> None:
    """
    Crée une heatmap
    
    Args:
        df: DataFrame contenant les données
        x_col: nom de la colonne pour l'axe X
        y_col: nom de la colonne pour l'axe Y
        value_col: nom de la colonne des valeurs
        titre: titre du graphique
    """
    
    # Pivoter les données
    pivot_df = df.pivot_table(values=value_col, index=y_col, columns=x_col, fill_value=0)
    
    x_data = pivot_df.columns.tolist()
    y_data = pivot_df.index.tolist()
    
    # Préparer les données pour ECharts
    data = []
    for i, y in enumerate(y_data):
        for j, x in enumerate(x_data):
            data.append([j, i, pivot_df.loc[y, x]])
    
    option = {
        "title": {"text": titre, "left": "center"},
        "tooltip": {"position": "top"},
        "grid": {"height": "50%", "top": "10%"},
        "xAxis": {"type": "category", "data": x_data, "splitArea": {"show": True}},
        "yAxis": {"type": "category", "data": y_data, "splitArea": {"show": True}},
        "visualMap": {
            "min": 0,
            "max": pivot_df.values.max(),
            "calculable": True,
            "orient": "horizontal",
            "left": "center",
            "bottom": "15%"
        },
        "series": [{
            "type": "heatmap",
            "data": data,
            "label": {"show": True}
        }]
    }
    
    st_echarts(options=option, height="500px")


def boxplot(df: pd.DataFrame,
           category_col: str,
           value_col: str,
           titre: str = "Boxplot") -> None:
    """
    Crée un boxplot
    
    Args:
        df: DataFrame contenant les données
        category_col: nom de la colonne des catégories
        value_col: nom de la colonne des valeurs
        titre: titre du graphique
    """
    
    categories = df[category_col].unique()
    boxplot_data = []
    
    for cat in categories:
        values = df[df[category_col] == cat][value_col].values
        q1 = np.percentile(values, 25)
        q3 = np.percentile(values, 75)
        median = np.percentile(values, 50)
        min_val = np.min(values)
        max_val = np.max(values)
        
        boxplot_data.append([min_val, q1, median, q3, max_val])
    
    option = {
        "title": {"text": titre, "left": "center"},
        "tooltip": {"trigger": "item"},
        "xAxis": {"type": "category", "data": categories.tolist()},
        "yAxis": {"type": "value"},
        "series": [{
            "type": "boxplot",
            "data": boxplot_data
        }]
    }
    
    st_echarts(options=option, height="400px")


def graphique_ligne(df: pd.DataFrame,
                   x_col: str,
                   y_col: str,
                   titre: str = "Graphique linéaire",
                   group_col: Optional[str] = None) -> None:
    """
    Crée un graphique linéaire
    
    Args:
        df: DataFrame contenant les données
        x_col: nom de la colonne pour l'axe X
        y_col: nom de la colonne pour l'axe Y
        titre: titre du graphique
        group_col: nom de la colonne pour les groupes (optionnel)
    """
    
    if group_col is None:
        # Graphique simple
        x_data = df[x_col].tolist()
        y_data = df[y_col].tolist()
        
        option = {
            "title": {"text": titre, "left": "center"},
            "tooltip": {"trigger": "axis"},
            "xAxis": {"type": "category", "data": x_data},
            "yAxis": {"type": "value"},
            "series": [{
                "type": "line",
                "data": y_data,
                "smooth": True
            }]
        }
    else:
        # Graphique avec groupes
        groups = df[group_col].unique()
        x_data = df[x_col].unique()
        x_data = sorted(x_data)
        
        series_data = []
        for group in groups:
            group_df = df[df[group_col] == group]
            group_df = group_df.set_index(x_col).reindex(x_data, fill_value=0)
            
            series_data.append({
                "name": str(group),
                "type": "line",
                "data": group_df[y_col].tolist(),
                "smooth": True
            })
        
        option = {
            "title": {"text": titre, "left": "center"},
            "tooltip": {"trigger": "axis"},
            "legend": {"data": [str(g) for g in groups]},
            "xAxis": {"type": "category", "data": x_data.tolist()},
            "yAxis": {"type": "value"},
            "series": series_data
        }
    
    st_echarts(options=option, height="400px")



def create_bar_chart(df, variable, 
                    title="Diagramme à barres", 
                    color="#5470c6", 
                    width="100%", 
                    height="400px",
                    orientation="vertical",
                    show_values=True,
                    sort_data=False,
                    ascending=True):
    """
    Crée un diagramme à barres avec st_echarts
    
    Paramètres:
    -----------
    df : pd.DataFrame
        Le dataframe contenant les données
    variable : str
        Le nom de la colonne à représenter
    title : str, optional
        Le titre du graphique (défaut: "Diagramme à barres")
    color : str, optional
        La couleur des barres (défaut: "#5470c6")
    width : str, optional
        La largeur du graphique (défaut: "100%")
    height : str, optional
        La hauteur du graphique (défaut: "400px")
    orientation : str, optional
        "vertical" ou "horizontal" (défaut: "vertical")
    show_values : bool, optional
        Afficher les valeurs sur les barres (défaut: True)
    sort_data : bool, optional
        Trier les données par valeur (défaut: False)
    ascending : bool, optional
        Ordre croissant si sort_data=True (défaut: True)
    
    Returns:
    --------
    None (affiche le graphique directement)
    """
    
    # Vérifier que la variable existe dans le dataframe
    if variable not in df.columns:
        st.error(f"La variable '{variable}' n'existe pas dans le dataframe")
        return
    
    # Calculer les fréquences/valeurs
    if df[variable].dtype in ['object', 'category']:
        # Variable catégorielle : compter les occurrences
        data_counts = df[variable].value_counts()
        x_data = data_counts.index.tolist()
        y_data = data_counts.values.tolist()
        y_axis_name = "Fréquence"
    else:
        # Variable numérique : utiliser les valeurs directement
        # On suppose qu'il y a une colonne index ou qu'on veut afficher les valeurs
        if len(df) > 50:
            st.warning("Trop de valeurs pour un diagramme à barres. Affichage des 50 premières.")
            df_plot = df.head(50)
        else:
            df_plot = df
        
        x_data = df_plot.index.tolist()
        y_data = df_plot[variable].tolist()
        y_axis_name = variable
    
    # Trier les données si demandé
    if sort_data:
        sorted_data = sorted(zip(x_data, y_data), key=lambda x: x[1], reverse=not ascending)
        x_data, y_data = zip(*sorted_data)
        x_data, y_data = list(x_data), list(y_data)
    
    # Configuration du graphique
    if orientation == "horizontal":
        option = {
            "title": {
                "text": title,
                "left": "center",
                "textStyle": {"fontSize": 16}
            },
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"}
            },
            "grid": {
                "left": "10%",
                "right": "4%",
                "bottom": "3%",
                "containLabel": True
            },
            "xAxis": {
                "type": "value",
                "name": y_axis_name,
                "nameLocation": "middle",
                "nameGap": 30
            },
            "yAxis": {
                "type": "category",
                "data": x_data,
                "name": variable,
                "nameLocation": "middle",
                "nameGap": 50
            },
            "series": [{
                "name": y_axis_name,
                "type": "bar",
                "data": y_data,
                "itemStyle": {"color": color},
                "label": {
                    "show": show_values,
                    "position": "right"
                }
            }]
        }
    else:  # vertical
        option = {
            "title": {
                "text": title,
                "left": "center",
                "textStyle": {"fontSize": 16}
            },
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"}
            },
            "grid": {
                "left": "3%",
                "right": "4%",
                "bottom": "10%",
                "containLabel": True
            },
            "xAxis": {
                "type": "category",
                "data": x_data,
                "name": variable,
                "nameLocation": "middle",
                "nameGap": 30,
                "axisLabel": {"rotate": 45 if len(x_data) > 10 else 0}
            },
            "yAxis": {
                "type": "value",
                "name": y_axis_name,
                "nameLocation": "middle",
                "nameGap": 50
            },
            "series": [{
                "name": y_axis_name,
                "type": "bar",
                "data": y_data,
                "itemStyle": {"color": color},
                "label": {
                    "show": show_values,
                    "position": "top"
                }
            }]
        }
    
    # Afficher le graphique
    st_echarts(options=option, width=width, height=height)


def create_bar_chart_from_contingency(contingency_table, 
                                    title="Diagramme à barres croisées",
                                    colors=None,
                                    width="100%", 
                                    height="400px",
                                    orientation="vertical",
                                    show_values=True,
                                    stacked=False,
                                    var1_name="Variable 1",
                                    var2_name="Variable 2",
                                    is_percentage=False,
                                    cle="vnlkgvgvh"
                                    ):
    """
    Crée un diagramme à barres croisées à partir d'un tableau de contingence
    
    Paramètres:
    -----------
    contingency_table : pd.DataFrame
        Tableau de contingence (crosstab)
    title : str, optional
        Le titre du graphique
    colors : list, optional
        Liste des couleurs pour chaque colonne
    width : str, optional
        La largeur du graphique
    height : str, optional
        La hauteur du graphique
    orientation : str, optional
        "vertical" ou "horizontal"
    show_values : bool, optional
        Afficher les valeurs sur les barres
    stacked : bool, optional
        Barres empilées ou côte à côte
    var1_name : str, optional
        Nom de la première variable (pour les labels)
    var2_name : str, optional
        Nom de la deuxième variable (pour la légende)
    is_percentage : bool, optional
        Indique si les valeurs sont en pourcentage
    """
    
    # Préparer les données
    categories = contingency_table.index.tolist()
    series_names = contingency_table.columns.tolist()
    
    # Couleurs par défaut
    if colors is None:
        default_colors = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc']
        colors = default_colors[:len(series_names)]
    
    # Créer les séries de données
    series = []
    for i, col in enumerate(series_names):
        series_data = contingency_table[col].tolist()
        series.append({
            "name": str(col),
            "type": "bar",
            "data": series_data,
            "itemStyle": {"color": colors[i % len(colors)]},
            "label": {
                "show": show_values,
                "position": "inside" if stacked else ("top" if orientation == "vertical" else "right"),
                "formatter": "{c}%" if is_percentage else "{c}"
            }
        })
        
        # Pour les barres empilées, ajuster la position des labels
        if stacked:
            series[i]["stack"] = "total"
    
    # Configuration du graphique
    if orientation == "horizontal":
        option = {
            "title": {
                "text": title,
                "left": "center",
                "textStyle": {"fontSize": 16}
            },
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"},
                "formatter": "{b}<br/>{a}: {c}" + ("%" if is_percentage else "")
            },
            "legend": {
                "data": series_names,
                "top": "bottom",
                "left": "center"
            },
            "grid": {
                "left": "15%",
                "right": "4%",
                "bottom": "15%",
                "containLabel": True
            },
            "xAxis": [{
                "type": "value",
                "name": "Effectifs" + (" (%)" if is_percentage else ""),
                "nameLocation": "middle",
                "nameGap": 30,
                "axisLabel": {"rotate": 30 if len(categories) > 6 else 0, "interval": 0}
            }],
            "yAxis": {
                "type": "category",
                "data": categories,
                "name": var1_name,
                "nameLocation": "middle",
                "nameGap": 60
            },
            "series": series
        }
    else:  # vertical
        option = {
            "title": {
                "text": title,
                "left": "center",
                "textStyle": {"fontSize": 16}
            },
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"},
                "formatter": "{b}<br/>{a}: {c}" + ("%" if is_percentage else "")
            },
            "legend": {
                "data": series_names,
                "top": "bottom",
                "left": "center"
            },
            "grid": {
                "left": "3%",
                "right": "4%",
                "bottom": "20%",
                "containLabel": True
            },
            
            "xAxis": [{"type": "category", 
                       "data": categories, 
                       "nameLocation": "middle",
                       "nameGap": 30,
                       "axisLabel": {"rotate": 45 if len(categories) > 6 else 0,
                                     "interval": 0,
                                     }
                       }
                      ],
            
            "yAxis": {
                "type": "value",
                "name": "Effectifs" + (" (%)" if is_percentage else ""),
                "nameLocation": "middle",
                "nameGap": 50
            },
            "series": series
        }
    
    # Afficher le graphique
    st_echarts(options=option, width=width, height=height, key=cle)




def create_crossed_bar_chart(df, var1, var2, 
                           title="Diagramme à barres croisées", 
                           colors=None,
                           width="100%", 
                           height="400px",
                           orientation="vertical",
                           show_values=True,
                           stacked=False,
                           normalize=False, 
                           keys="jnskfnkjnkn"):
    """
    Crée un diagramme à barres croisées à partir d'un dataframe
    
    Paramètres:
    -----------
    df : pd.DataFrame
        Le dataframe contenant les données
    var1 : str
        Première variable (axe principal)
    var2 : str
        Deuxième variable (groupement des barres)
    title : str, optional
        Le titre du graphique
    colors : list, optional
        Liste des couleurs pour chaque modalité de var2
    width : str, optional
        La largeur du graphique
    height : str, optional
        La hauteur du graphique
    orientation : str, optional
        "vertical" ou "horizontal"
    show_values : bool, optional
        Afficher les valeurs sur les barres
    stacked : bool, optional
        Barres empilées ou côte à côte
    normalize : bool, optional
        Normaliser en pourcentages
    """
    
    # Vérifier que les variables existent
    if var1 not in df.columns or var2 not in df.columns:
        st.error(f"Une ou plusieurs variables n'existent pas dans le dataframe")
        return
    
    # Créer le tableau de contingence
    contingency_table = pd.crosstab(df[var1], df[var2])
    
    # Normaliser si demandé
    if normalize:
        contingency_table = contingency_table.div(contingency_table.sum(axis=1), axis=0) * 100
    
    # Appeler la fonction avec le tableau de contingence
    create_bar_chart_from_contingency(
        contingency_table, 
        title=title, 
        colors=colors,
        width=width, 
        height=height,
        orientation=orientation,
        show_values=show_values,
        stacked=stacked,
        var1_name=var1,
        var2_name=var2,
        is_percentage=normalize,
        cle=keys
        
    )


def create_categorical_map(gdf, lat_col, lon_col, category_col, 
                          center_lat=None, center_lon=None, zoom_start=10,
                          popup_cols=None, tooltip_cols=None, style="OpenStreetMap"):
    """
    Crée une carte interactive avec des marqueurs colorés selon une variable catégorielle
    
    Paramètres:
    -----------
    gdf : GeoDataFrame ou DataFrame
        Les données à afficher
    lat_col : str
        Nom de la colonne contenant les latitudes
    lon_col : str
        Nom de la colonne contenant les longitudes
    category_col : str
        Nom de la colonne catégorielle pour la coloration
    center_lat : float, optional
        Latitude du centre de la carte (par défaut: moyenne des points)
    center_lon : float, optional
        Longitude du centre de la carte (par défaut: moyenne des points)
    zoom_start : int, optional
        Niveau de zoom initial (défaut: 10)
    popup_cols : list, optional
        Colonnes à afficher dans le popup
    tooltip_cols : list, optional
        Colonnes à afficher dans le tooltip
    
    Returns:
    --------
    folium.Map : La carte créée
    """
    
    # Vérifier les colonnes requises
    required_cols = [lat_col, lon_col, category_col]
    missing_cols = [col for col in required_cols if col not in gdf.columns]
    if missing_cols:
        st.error(f"Colonnes manquantes dans le DataFrame: {missing_cols}")
        return None
    
    # Supprimer les lignes avec des valeurs manquantes
    gdf_clean = gdf.dropna(subset=[lat_col, lon_col, category_col])
    
    if len(gdf_clean) == 0:
        st.error("Aucune donnée valide trouvée après nettoyage")
        return None
    
    # Calculer le centre si non spécifié
    if center_lat is None:
        center_lat = gdf_clean[lat_col].mean()
    if center_lon is None:
        center_lon = gdf_clean[lon_col].mean()
    
    # Créer la carte
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        tiles=style
    )
    
    # Définir les couleurs pour chaque catégorie
    categories = sorted(gdf_clean[category_col].unique())
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred',
              'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white',
              'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
    
    # Créer un dictionnaire couleur-catégorie
    color_map = {cat: colors[i % len(colors)] for i, cat in enumerate(categories)}
    
    # Ajouter les marqueurs
    for idx, row in gdf_clean.iterrows():
        # Préparer le popup
        if popup_cols:
            popup_text = "<br>".join([f"<b>{col}:</b> {row[col]}" for col in popup_cols if col in gdf_clean.columns]) + "<br>" + f"<b>ID Ménage:</b> {row['id_menage']}"
        else:
            popup_text = f"<b>{category_col}:</b> {row[category_col]}"+ "<br>" + f"<b>ID Ménage:</b> {row['id_menage']}"
        
        # Préparer le tooltip
        if tooltip_cols:
            tooltip_text = " | ".join([f"{col}: {row[col]}" for col in tooltip_cols if col in gdf_clean.columns]) + "<br>" + f"<b>ID Ménage:</b> {row['id_menage']}"
        else:
            tooltip_text = str(row[category_col])+ "<br>" + str(row['id_menage'])
        
        # Ajouter le marqueur
        folium.Marker(
            location=[row[lat_col], row[lon_col]],
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=tooltip_text,
            icon=folium.Icon(
                color=color_map[row[category_col]],
                icon='info-sign'
            )
        ).add_to(m)
    
    # Ajouter une légende
    legend_html = f"""
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 200px; height: auto; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
    <h4>Légende - {category_col}-{row["id_menage"]}</h4>
    """
    
    for category, color in color_map.items():
        legend_html += f'<p><i class="fa fa-circle" style="color:{color}"></i> {category}</p>'
    
    legend_html += "</div>"
    folium_static(m)
    
    return m


def calculate_boxplot_stats(data):
    """
    Calcule les statistiques nécessaires pour un boxplot
    
    Returns:
    --------
    dict : Contient min, Q1, médiane, Q3, max, outliers
    """
    if len(data) == 0:
        return None
    
    # Supprimer les valeurs manquantes
    clean_data = data.dropna()
    
    if len(clean_data) == 0:
        return None
    
    # Calculer les quartiles
    Q1 = clean_data.quantile(0.25)
    Q3 = clean_data.quantile(0.75)
    median = clean_data.median()
    
    # Calculer les limites des moustaches (whiskers)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Valeurs min et max dans les limites
    whisker_min = clean_data[clean_data >= lower_bound].min()
    whisker_max = clean_data[clean_data <= upper_bound].max()
    
    # Outliers
    outliers = clean_data[(clean_data < lower_bound) | (clean_data > upper_bound)].tolist()
    
    return {
        'min': whisker_min,
        'Q1': Q1,
        'median': median,
        'Q3': Q3,
        'max': whisker_max,
        'outliers': outliers
    }

def create_boxplot(df, quantitative_col, categorical_col=None, 
                   title="Boxplot", y_axis_label=None, 
                   colors=None, width=800, height=500,
                   show_outliers=True):
    """
    Crée un boxplot interactif avec streamlit_echarts
    
    Paramètres:
    -----------
    df : DataFrame
        Les données à visualiser
    quantitative_col : str
        Nom de la colonne quantitative à représenter
    categorical_col : str, optional
        Nom de la colonne catégorielle pour grouper les données
    title : str
        Titre du graphique
    y_axis_label : str, optional
        Label de l'axe Y (par défaut: nom de la colonne quantitative)
    colors : list, optional
        Liste des couleurs pour chaque catégorie
    width : int
        Largeur du graphique
    height : int
        Hauteur du graphique
    show_outliers : bool
        Afficher ou non les outliers
    
    Returns:
    --------
    dict : Configuration ECharts pour le boxplot
    """
    
    # Vérifications
    if quantitative_col not in df.columns:
        st.error(f"Colonne '{quantitative_col}' non trouvée dans le DataFrame")
        return None
    
    if categorical_col and categorical_col not in df.columns:
        st.error(f"Colonne '{categorical_col}' non trouvée dans le DataFrame")
        return None
    
    # Supprimer les lignes avec des valeurs manquantes
    cols_to_check = [quantitative_col]
    if categorical_col:
        cols_to_check.append(categorical_col)
    
    df_clean = df.dropna(subset=cols_to_check)
    
    if len(df_clean) == 0:
        st.error("Aucune donnée valide après nettoyage")
        return None
    
    # Couleurs par défaut
    if colors is None:
        colors = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', 
                  '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc']
    
    # Label de l'axe Y
    if y_axis_label is None:
        y_axis_label = quantitative_col
    
    # Préparer les données
    if categorical_col:
        # Boxplot par catégorie
        categories = sorted(df_clean[categorical_col].unique())
        boxplot_data = []
        scatter_data = []
        
        for i, category in enumerate(categories):
            category_data = df_clean[df_clean[categorical_col] == category][quantitative_col]
            stats = calculate_boxplot_stats(category_data)
            
            if stats:
                # Données pour le boxplot [min, Q1, median, Q3, max]
                boxplot_data.append([stats['min'], stats['Q1'], stats['median'], 
                                   stats['Q3'], stats['max']])
                
                # Données pour les outliers
                if show_outliers:
                    for outlier in stats['outliers']:
                        scatter_data.append([i, outlier])
        
        # Configuration ECharts
        option = {
            "title": {
                "text": title,
                "left": "center",
                "textStyle": {"fontSize": 16, "fontWeight": "bold"}
            },
            "tooltip": {
                "trigger": "item",
                "axisPointer": {"type": "shadow"}
            },
            "grid": {
                "left": "10%",
                "right": "10%",
                "bottom": "15%",
                "top": "15%"
            },
            "xAxis": {
                "type": "category",
                "data": categories,
                "boundaryGap": True,
                "nameGap": 30,
                "splitArea": {"show": False},
                "splitLine": {"show": False}
            },
            "yAxis": {
                "type": "value",
                "name": y_axis_label,
                "splitArea": {"show": True}
            },
            "series": [
                {
                    "name": "Boxplot",
                    "type": "boxplot",
                    "data": boxplot_data,
                    "itemStyle": {
                        "color": colors[0],
                        "borderColor": "#000"
                    },
                    "tooltip": {
                        "formatter": """"""
                                }
                }
            ]
        }
            
        
        
        # Ajouter les outliers si demandé
        if show_outliers and scatter_data:
            option["series"].append({
                "name": "Outliers",
                "type": "scatter",
                "data": scatter_data,
                "itemStyle": {
                    "color": colors[1] if len(colors) > 1 else "#ee6666",
                    "opacity": 0.6
                },
                "symbolSize": 6
            })
    
    else:
        # Boxplot simple (une seule série)
        stats = calculate_boxplot_stats(df_clean[quantitative_col])
        
        if not stats:
            st.error("Impossible de calculer les statistiques")
            return None
        
        boxplot_data = [[stats['min'], stats['Q1'], stats['median'], 
                        stats['Q3'], stats['max']]]
        
        scatter_data = [[0, outlier] for outlier in stats['outliers']] if show_outliers else []
        
        option = {
            "title": {
                "text": title,
                "left": "center",
                "textStyle": {"fontSize": 16, "fontWeight": "bold"}
            },
            "tooltip": {
                "trigger": "item",
                "axisPointer": {"type": "shadow"}
            },
            "grid": {
                "left": "10%",
                "right": "10%",
                "bottom": "15%",
                "top": "15%"
            },
            "xAxis": {
                "type": "category",
                "data": [quantitative_col],
                "boundaryGap": True,
                "nameGap": 30,
                "splitArea": {"show": False},
                "splitLine": {"show": False}
            },
            "yAxis": {
                "type": "value",
                "name": y_axis_label,
                "splitArea": {"show": True}
            },
            "series": [
                {
                    "name": "Boxplot",
                    "type": "boxplot",
                    "data": boxplot_data,
                    "itemStyle": {
                        "color": colors[0],
                        "borderColor": "#000"
                    },
                    "tooltip": {
                        "formatter": """function(param) {
                            return [
                                'Variable: ' + param.name,
                                'Maximum: ' + param.data[5],
                                'Q3: ' + param.data[4],
                                'Médiane: ' + param.data[3],
                                'Q1: ' + param.data[2],
                                'Minimum: ' + param.data[1]
                            ].join('<br/>');
                        }"""
                    }
                }
            ]
        }
        
        # Ajouter les outliers si demandé
        if show_outliers and scatter_data:
            option["series"].append({
                "name": "Outliers",
                "type": "scatter",
                "data": scatter_data,
                "itemStyle": {
                    "color": colors[1] if len(colors) > 1 else "#ee6666",
                    "opacity": 0.6
                },
                "symbolSize": 6
            })
    
    st_echarts(options=option, width=width, height=height)



def create_choropleth_map(gdf, geometry_col='geometry', value_col='nombre_questionnaire', 
                         label_col='arrondissement', zoom_start=10, colormap='YlOrRd', 
                         num_classes=5, title="Carte choroplèthe", 
                         legend_name="Nombre de questionnaires", popup_cols=None, 
                         tooltip_format=None, width=800, height=600):
    """
    Crée une carte choroplèthe avec labels personnalisés
    """

    # Vérification des colonnes
    required_cols = [geometry_col, value_col, label_col]
    missing_cols = [col for col in required_cols if col not in gdf.columns]
    if missing_cols:
        st.error(f"Colonnes manquantes : {missing_cols}")
        return None

    # Nettoyage des données
    gdf_clean = gdf.dropna(subset=required_cols)

    if gdf_clean.empty:
        st.error("Aucune donnée valide après nettoyage.")
        return None

    # Conversion en GeoDataFrame
    try:
        gdf_clean = gpd.GeoDataFrame(gdf_clean, geometry=geometry_col)
    except Exception as e:
        st.error(f"Erreur lors de la conversion en GeoDataFrame : {e}")
        return None

    # Vérification et définition du CRS
    if gdf_clean.crs is None:
        st.warning("CRS non défini. Utilisation de EPSG:4326 par défaut.")
        gdf_clean.set_crs(epsg=4326, inplace=True)
    else:
        gdf_clean = gdf_clean.to_crs(epsg=4326)

    # Création de la carte de base
    m = folium.Map(zoom_start=zoom_start, tiles='OpenStreetMap')

    # Palette de couleurs
    color_palettes = {
        'YlOrRd': ['#ffffcc', '#ffeda0', '#fed976', '#feb24c', '#fd8d3c', '#fc4e2a', '#e31a1c', '#bd0026', '#800026'],
        'Blues': ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#08519c', '#08306b'],
        'Greens': ["#eb2315", "#e63e0b", "#dd9308", "#bfe005", "#4fd810", '#41ab5d', '#238b45', '#006d2c', '#00441b'],
        'Reds': ['#fff5f0', '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a', '#ef3b2c', '#cb181d', '#a50f15', '#67000d'],
        'Purples': ['#fcfbfd', '#efedf5', '#dadaeb', '#bcbddc', '#9e9ac8', '#807dba', '#6a51a3', '#54278f', '#3f007d'],
        'Oranges': ['#fff5eb', '#fee6ce', '#fdd0a2', '#fdae6b', '#fd8d3c', '#f16913', '#d94801', '#a63603', '#7f2704']
    }

    colors = color_palettes.get(colormap, color_palettes['Greens'])

    # Création de la colormap
    min_val = gdf_clean[value_col].min()
    max_val = gdf_clean[value_col].max()
    colormap_obj = cm.LinearColormap(colors=colors[:num_classes], vmin=min_val, vmax=max_val, caption=legend_name)

    # Fonction couleur
    def get_color(value):
        if pd.isna(value):
            return '#808080'  # gris pour valeurs manquantes
        return colormap_obj(value)

    all_bounds = []

    # Ajout des polygones
    for idx, row in gdf_clean.iterrows():
        geom = row[geometry_col]

        # Préparation du popup
        if popup_cols:
            popup_text = "<br>".join([f"<b>{col}:</b> {row[col]}" for col in popup_cols if col in gdf_clean.columns])
        else:
            popup_text = f"<b>{label_col}:</b> {row[label_col]}<br><b>{legend_name}:</b> {row[value_col]}"
        
        # Tooltip
        tooltip_text = tooltip_format.format(**row) if tooltip_format else f"{row[label_col]}"

        # Bounds
        if hasattr(geom, 'bounds'):
            bounds = geom.bounds
            all_bounds.append([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

        # Ajout GeoJson
        folium.GeoJson(
            geom,
            style_function=lambda x, color=get_color(row[value_col]): {
                'fillColor': color,
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7,
                'dashArray': '3, 3'
            },
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=folium.Tooltip(tooltip_text)
        ).add_to(m)

        # Ajout du label au centroïde
        try:
            centroid = geom.centroid
            folium.Marker(
                location=[centroid.y, centroid.x],
                icon=folium.DivIcon(
                    html=f'<div style="font-size: 19px; color: black; font-weight: bold; text-align: left; text-shadow: 1px 1px 1px white;">{row[label_col]}</div>',
                    icon_size=(40, 20),
                    icon_anchor=(20, 10)
                )
            ).add_to(m)
        except Exception as e:
            st.warning(f"Impossible d’ajouter le label pour {row[label_col]} : {e}")

    # Ajustement de la vue
    if all_bounds:
        try:
            min_lat = min([b[0][0] for b in all_bounds])
            min_lon = min([b[0][1] for b in all_bounds])
            max_lat = max([b[1][0] for b in all_bounds])
            max_lon = max([b[1][1] for b in all_bounds])
            m.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]])
        except Exception as e:
            st.warning(f"Erreur lors de l'ajustement de la vue : {e}")

    # Ajout de la légende et du titre
    colormap_obj.add_to(m)
    title_html = f'''
    <h3 align="center" style="font-size:20px; margin-top:0px;"><b>{title}</b></h3>
    '''
    m.get_root().html.add_child(folium.Element(title_html))

    folium_static(m, width=width, height=height)
    return m

#12. Fonction pour tracer des graphiques type barre de progression
def make_multi_progress_bar(labels,values,colors,titre="",width=500,height=400):
    # Configuration
    max_blocks = 100  # Nombre total de segments
    block_size = 1  # Chaque bloc représente 1%
    space_factor = 0.1  # Espace entre les blocs (réduit à 20% de la largeur d'un bloc)

    fig = go.Figure()

    # Création des barres segmentées
    for i, (label, value, color) in enumerate(zip(labels, values, colors)):
        num_filled_blocks = int(value*100) // block_size  # Nombre de blocs colorés
        num_empty_blocks = max_blocks - num_filled_blocks  # Blocs restants

        # Blocs colorés (progression) avec espacement
        fig.add_trace(go.Bar(
            x=[block_size - space_factor] * num_filled_blocks,  # Réduction pour l'espacement
            y=[label] * num_filled_blocks,
            orientation='h',
            hoverinfo="skip",
            marker=dict(color=color),
            showlegend=False,
            width=0.5  # Réduction de la largeur des blocs
        ))

        # Blocs vides (fond) avec le même espacement
        fig.add_trace(go.Bar(
            x=[block_size - space_factor] * num_empty_blocks,
            y=[label] * num_empty_blocks,
            orientation='h',
            hoverinfo="skip",
            marker=dict(color="rgba(0, 0, 0, 0.2)"),
            showlegend=False,
            width=0.5  # Même largeur que les blocs colorés
        ))

    # Personnalisation du layout
    fig.update_layout(
        title=titre,
        barmode="stack",
        width=width,height=height,
        annotations=[dict(text= str(round(100*values[i],2))+'%', x=100*values[i], y=i,
            font_size=160/len(values) if len(values) > 5 else 30, showarrow=False,xanchor='left',font=dict(color=colors[i], family="Berlin Sans FB")) for i in range(len(values))] + 
        [dict(text= labels[i], x=-1, y=i+0.5,
            font_size=160/len(values) if len(values) > 5 else 30, showarrow=False,xanchor='left',font=dict(color=colors[i], family="Berlin Sans FB")) for i in range(len(values))],
        xaxis=dict(visible=False), 
        yaxis=dict(visible=False),
        margin=dict(l=50, r=20, t=20, b=20),
        paper_bgcolor='rgba(248,248,250,0)',
        plot_bgcolor='rgba(248,248,250,0)',
    )

    st.plotly_chart(fig)


def create_questionnaire_time_gauge(temps_remplissage, ecart_type, temps_cible=None, titre="Temps de Remplissage du Questionnaire",cle="gauge_questionnaire"):
    """
    Crée un graphique de jauge pour visualiser le temps de remplissage d'un questionnaire
    avec indication de l'écart-type en utilisant streamlit-echarts.
    
    Parameters:
    -----------
    temps_remplissage : float
        Temps moyen de remplissage en minutes
    ecart_type : float
        Écart-type du temps de remplissage en minutes
    temps_cible : float, optional
        Temps cible souhaité en minutes (défaut: None)
    titre : str
        Titre du graphique
    
    Returns:
    --------
    Affiche directement le graphique dans Streamlit
    """
    
    # Calcul des limites basées sur les données
    temps_min = max(0, temps_remplissage - 2 * ecart_type)
    temps_max = temps_remplissage + 2 * ecart_type
    
    # Si un temps cible est défini, ajuster les limites
    if temps_cible:
        temps_max = max(temps_max, temps_cible * 1.2)
    
    # Définition des seuils de couleur
    seuil_excellent = temps_max * 0.3
    seuil_bon = temps_max * 0.6
    seuil_moyen = temps_max * 0.8
    
    # Configuration de la jauge ECharts
    option = {
        "title": {
            "text": titre,
            "left": "center",
            "top": "10%",
            "textStyle": {
                "fontSize": 18,
                "fontWeight": "bold",
                "color": "#333"
            }
        },
        "series": [
            {
                "name": "Temps de remplissage",
                "type": "gauge",
                "center": ["50%", "60%"],
                "radius": "75%",
                "min": 0,
                "max": temps_max,
                "splitNumber": 5,
                "startAngle": 225,
                "endAngle": -45,
                "itemStyle": {
                    "color": "#1f77b4"
                },
                "progress": {
                    "show": True,
                    "width": 15
                },
                "pointer": {
                    "show": True,
                    "length": "75%",
                    "width": 8,
                    "itemStyle": {
                        "color": "#1f77b4"
                    }
                },
                "axisLine": {
                    "lineStyle": {
                        "width": 20,
                        "color": [
                            [seuil_excellent/temps_max, "#90EE90"],  # vert clair
                            [seuil_bon/temps_max, "#FFD700"],       # jaune
                            [seuil_moyen/temps_max, "#FFA500"],     # orange
                            [1, "#F08080"]                          # rouge clair
                        ]
                    }
                },
                "axisTick": {
                    "distance": -30,
                    "length": 8,
                    "lineStyle": {
                        "color": "#fff",
                        "width": 2
                    }
                },
                "splitLine": {
                    "distance": -30,
                    "length": 30,
                    "lineStyle": {
                        "color": "#fff",
                        "width": 4
                    }
                },
                "axisLabel": {
                    "color": "#333",
                    "distance": 40,
                    "fontSize": 12,
                    "formatter": "{value} min"
                },
                "detail": {
                    "valueAnimation": True,
                    "formatter": "{value} min",
                    "color": "#1f77b4",
                    "fontSize": 20,
                    "fontWeight": "bold",
                    "offsetCenter": [0, "35%"]
                },
                "data": [
                    {
                        "value": temps_remplissage,
                        "name": "Temps moyen"
                    }
                ]
            }
        ],
        "graphic": [
            {
                "type": "text",
                "left": "center",
                "top": "85%",
                "style": {
                    "text": f"Écart-type: ±{ecart_type:.1f} min",
                    "fontSize": 14,
                    "fontWeight": "bold",
                    "fill": "#666"
                }
            },
            {
                "type": "text",
                "left": "center",
                "top": "90%",
                "style": {
                    "text": f"Plage: {temps_remplissage-ecart_type:.1f} - {temps_remplissage+ecart_type:.1f} min",
                    "fontSize": 12,
                    "fill": "#888"
                }
            }
        ]
    }
    
    # Ajouter l'indication du temps cible si fourni
    if temps_cible:
        option["graphic"].append({
            "type": "text",
            "left": "center",
            "top": "95%",
            "style": {
                "text": f"Objectif: {temps_cible:.1f} min",
                "fontSize": 12,
                "fontWeight": "bold",
                "fill": "#d62728" if temps_remplissage > temps_cible else "#2ca02c"
            }
        })
        
        # Ajouter une ligne de référence pour le temps cible
        option["series"][0]["markLine"] = {
            "data": [
                {
                    "type": "average",
                    "name": "Objectif",
                    "yAxis": temps_cible,
                    "lineStyle": {
                        "color": "#d62728",
                        "width": 3,
                        "type": "dashed"
                    }
                }
            ]
        }
    
    # Afficher la jauge
    st_echarts(options=option, height="400px", key=cle)


def make_cross_echart(df, var1, var2, title="", x_label_rotation=45, colors=None, 
                     height="400px", cle="cross_chart", normalize=False, 
                     show_percentages=True, chart_type="bar", stack_mode="total"):
    """
    Generate a grouped/stacked bar chart using st_echarts from two variables in a dataframe.

    Parameters:
    -----------
    df : pd.DataFrame
        The input dataframe containing the data
    var1 : str
        Name of the first variable (will be used for x-axis categories)
    var2 : str
        Name of the second variable (will be used for series/colors)
    title : str, optional
        Title of the chart (default: "")
    x_label_rotation : int, optional
        Rotation angle for x-axis labels (default: 45)
    colors : list, optional
        List of colors for the series (default: predefined colors)
    height : str, optional
        Height of the chart (default: "400px")
    cle : str, optional
        Unique key for the chart (default: "cross_chart")
    normalize : bool, optional
        If True, show percentages instead of counts (default: False)
    show_percentages : bool, optional
        If True, show percentage labels on bars (default: True)
    chart_type : str, optional
        Type of chart: "bar" or "line" (default: "bar")
    stack_mode : str, optional
        Stacking mode: "total" for stacked, None for grouped (default: "total")

    Returns:
    --------
    pd.DataFrame
        The cross table used for the chart
    """
    
    # Vérifications des paramètres
    if var1 not in df.columns:
        st.error(f"La variable '{var1}' n'existe pas dans le dataframe")
        return None
        
    if var2 not in df.columns:
        st.error(f"La variable '{var2}' n'existe pas dans le dataframe")
        return None
    
    # Supprimer les valeurs manquantes
    df_clean = df[[var1, var2]].dropna()
    
    if df_clean.empty:
        st.warning("Aucune donnée valide trouvée après suppression des valeurs manquantes")
        return None
    
    # Créer la table de contingence
    if normalize:
        # Calcul des pourcentages en ligne (par rapport à var1)
        cross_table = pd.crosstab(df_clean[var1], df_clean[var2], normalize='index') * 100
        cross_table = cross_table.round(1)
    else:
        # Calcul des effectifs
        cross_table = pd.crosstab(df_clean[var1], df_clean[var2])
    
    # Couleurs par défaut
    if colors is None:
        colors = ["#10C92F", "#DBE917", "#E74219", "#490B07", "#0CA0B4", "#064C56", 
                 "#8B4513", "#FF69B4", "#32CD32", "#FF4500", "#9370DB", "#20B2AA"]
    
    # Préparer les données pour le graphique
    categories = cross_table.index.tolist()
    
    # Configuration des séries
    series_data = []
    for i, col in enumerate(cross_table.columns):
        series_config = {
            "name": str(col),
            "data": cross_table[col].tolist(),
            "type": chart_type,
            "itemStyle": {"color": colors[i % len(colors)]},
        }
        
        # Ajouter le mode stack si spécifié
        if stack_mode and chart_type == "bar":
            series_config["stack"] = stack_mode
            
        # Configuration des labels
        if show_percentages:
            if normalize:
                series_config["label"] = {
                    "show": True,
                    "formatter": "{c}%",
                    "position": "inside" if stack_mode else "top"
                }
            else:
                series_config["label"] = {
                    "show": True,
                    "formatter": "{c}",
                    "position": "inside" if stack_mode else "top"
                }
        
        series_data.append(series_config)
    
   
    
    # Configuration du graphique
    options = {
        "title": {
            "text": title,
            "left": "center",
            "textStyle": {
                "fontSize": 17,
                "fontWeight": "bold"
            }
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "shadow"
            },
            "formatter": "{b}<br/>{a}: {c}" + ("%" if normalize else "")
        },
        "legend": {
            "data": [str(col) for col in cross_table.columns],
            "top": "bottom",
            "left": "center"
        },
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "15%",
            "top": "20%",
            "containLabel": True
        },
        "xAxis": {
            "type": "category",
            "data": categories,
            "axisLabel": {
                "rotate": x_label_rotation,
                "interval": 0
            },
            #"name": var1,
            "nameLocation": "middle",
            "nameGap": 30
        },
        "yAxis": {
            "type": "value",
            "name": "Pourcentage (%)" if normalize else "Effectifs",
            "nameLocation": "middle",
            "nameGap": 50,
            "axisLabel": {
                "formatter": "{value}" + ("%" if normalize else "")
            }
        },
        "series": series_data
    }
    
    # Ajuster les options selon le type de graphique
    if chart_type == "line":
        options["tooltip"]["trigger"] = "item"
        for series in options["series"]:
            series["smooth"] = True
            series["symbol"] = "circle"
            series["symbolSize"] = 6
    
    # Afficher le graphique
    st_echarts(options=options, height=height, key=cle)
    

def create_missing_questions_gauge(questions_manquantes_moy, ecart_type, total_questions=None, 
                                 objectif_max=None, titre="Questions Sans Réponse par Questionnaire", cle="jhdskj"):
    """
    Crée un graphique de jauge pour visualiser le nombre moyen de questions sans réponse
    par questionnaire avec indication de l'écart-type.
    
    Parameters:
    -----------
    questions_manquantes_moy : float
        Nombre moyen de questions sans réponse par questionnaire
    ecart_type : float
        Écart-type du nombre de questions sans réponse
    total_questions : int, optional
        Nombre total de questions dans le questionnaire (pour calculer le %)
    objectif_max : float, optional
        Nombre maximum acceptable de questions sans réponse
    titre : str
        Titre du graphique
    
    Returns:
    --------
    Affiche directement le graphique dans Streamlit
    """
    
    # Calcul des limites de la jauge
    valeur_max = max(
        questions_manquantes_moy + 2 * ecart_type,
        objectif_max * 1.5 if objectif_max else questions_manquantes_moy * 2,
        5  # Minimum de 5 pour avoir une échelle visible
    )
    
    # Calcul du pourcentage si total_questions fourni
    if total_questions:
        pourcentage_moy = (questions_manquantes_moy / total_questions) * 100
        pourcentage_ecart = (ecart_type / total_questions) * 100
        show_percentage = True
    else:
        pourcentage_moy = 0
        pourcentage_ecart = 0
        show_percentage = False
    
    # Définition des seuils (inversés : bas = bon, haut = mauvais)
    seuil_excellent = valeur_max * 0.15  # Très peu de questions manquantes
    seuil_bon = valeur_max * 0.35        # Acceptable
    seuil_moyen = valeur_max * 0.65      # Préoccupant
    # Au-dessus = problématique
    col= "#d62728" if questions_manquantes_moy >15  else "#27d684"
    # Configuration de la jauge ECharts
    option = {
        "title": {
            "text": titre,
            "left": "center",
            "top": "5%",
            "textStyle": {
                "fontSize": 18,
                "fontWeight": "bold",
                "color": "#333"
            }
        },
        "series": [
            {
                "name": "Questions manquantes",
                "type": "gauge",
                "center": ["50%", "55%"],
                "radius": "80%",
                "min": 0,
                "max": valeur_max,
                "splitNumber": 5,
                "startAngle": 225,
                "endAngle": -45,
                "itemStyle": {
                    "color": "#9027d6"  # Rouge pour indiquer un problème
                },
                "progress": {
                    "show": True,
                    "width": 18
                },
                "pointer": {
                    "show": True,
                    "length": "75%",
                    "width": 8,
                    "itemStyle": {
                        "color": "#7819e4"
                    }
                },
                "axisLine": {
                    "lineStyle": {
                        "width": 25,
                        "color": [
                            [seuil_excellent/valeur_max, "#2ca02c"],   # Vert - Excellent
                            [seuil_bon/valeur_max, "#90EE90"],        # Vert clair - Bon  
                            [seuil_moyen/valeur_max, "#FFD700"],      # Jaune - Moyen
                            [0.85, "#FFA500"],                        # Orange - Préoccupant
                            [1, "#d62728"]                            # Rouge - Problématique
                        ]
                    }
                },
                "axisTick": {
                    "distance": -35,
                    "length": 8,
                    "lineStyle": {
                        "color": "#fff",
                        "width": 2
                    }
                },
                "splitLine": {
                    "distance": -35,
                    "length": 25,
                    "lineStyle": {
                        "color": "#fff",
                        "width": 4
                    }
                },
                "axisLabel": {
                    "color": "#333",
                    "distance": 45,
                    "fontSize": 12,
                    "formatter": "{value}"
                },
                "detail": {
                    "valueAnimation": True,
                    "formatter": "{value}",
                    "color": col ,
                    "fontSize": 24,
                    "fontWeight": "bold",
                    "offsetCenter": [0, "45%"]
                },
                "data": [
                    {
                        "value": questions_manquantes_moy,
                        "name": "Question sans reponse"
                    }
                ]
            }
        ],
        "graphic": []
    }
    
    # Ajout des annotations
    graphic_elements = [
        # Écart-type
        {
            "type": "text",
            "left": "center",
            "top": "83%",
            "style": {
                "text": f"Écart-type: ±{ecart_type:.1f}",
                "fontSize": 14,
                "fontWeight": "bold",
                "fill": "#666"
            }
        },
        # Plage normale
        {
            "type": "text", 
            "left": "center",
            "top": "88%",
            "style": {
                "text": f"Plage : {max(0, questions_manquantes_moy-ecart_type):.1f} - {questions_manquantes_moy+ecart_type:.1f}",
                "fontSize": 12,
                "fill": "#888"
            }
        }
    ]
    
    # Ajouter le pourcentage si disponible
    if show_percentage:
        graphic_elements.insert(1, {
            "type": "text",
            "left": "center", 
            "top": "93%",
            "style": {
                "text": f"Pourcentage moyen: {pourcentage_moy:.1f}% (±{pourcentage_ecart:.1f}%)",
                "fontSize": 12,
                "fontWeight": "bold",
                "fill": "#333"
            }
        })
    
    # Ajouter l'objectif si fourni
    if objectif_max:
        graphic_elements.append({
            "type": "text",
            "left": "center",
            "top": "98%" if show_percentage else "93%",
            "style": {
                "text": f"Objectif: ≤ {objectif_max}",
                "fontSize": 12,
                "fontWeight": "bold", 
                "fill": "#2ca02c" if questions_manquantes_moy <= objectif_max else "#d62728"
            }
        })
        
        # Ajouter une ligne de seuil pour l'objectif
        option["series"][0]["markLine"] = {
            "silent": True,
            "data": [{
                "yAxis": objectif_max,
                "lineStyle": {
                    "color": "#2ca02c",
                    "width": 3,
                    "type": "dashed"
                },
                "label": {
                    "formatter": "Objectif",
                    "position": "insideEndTop"
                }
            }]
        }
    
    option["graphic"] = graphic_elements
    
    # Afficher la jauge
    st_echarts(options=option, height="450px", key=cle)
    

def create_pie_chart_from_df(df, column, style="donut", title="", colors=None, 
                            show_legend=True, show_labels=True, show_percentages=True,
                            donut_radius="35%", height="400px", cle=str(random.randint(1, 9999)),
                            sort_values=True, top_n=None, other_threshold=None):
    """
    Crée un graphique en secteur (camembert) à partir d'un DataFrame et d'une colonne.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame contenant les données
    column : str
        Nom de la colonne à analyser
    style : str
        Style du graphique: "donut" ou "disque" (default: "donut")
    title : str
        Titre du graphique (si vide, utilise le nom de la colonne)
    colors : list, optional
        Liste de couleurs personnalisées
    show_legend : bool
        Afficher la légende (default: True)
    show_labels : bool
        Afficher les étiquettes sur les secteurs (default: True)
    show_percentages : bool
        Afficher les pourcentages (default: True)
    donut_radius : str
        Rayon intérieur pour le style donut (default: "50%")
    height : str
        Hauteur du graphique (default: "400px")
    cle : str
        Clé unique pour le graphique
    sort_values : bool
        Trier les valeurs par ordre décroissant (default: True)
    top_n : int, optional
        Limiter aux N premières catégories
    other_threshold : float, optional
        Regrouper les catégories < seuil% dans "Autres"
    
    Returns:
    --------
    dict : Statistiques et données utilisées pour le graphique
    """
    
    # Vérifications
    if column not in df.columns:
        st.error(f"La colonne '{column}' n'existe pas dans le DataFrame")
        return None
    
    # Supprimer les valeurs manquantes
    df_clean = df[column].dropna()
    
    if df_clean.empty:
        st.warning("Aucune donnée valide trouvée après suppression des valeurs manquantes")
        return None
    
    # Compter les occurrences
    value_counts = df_clean.value_counts()
    
    if sort_values:
        value_counts = value_counts.sort_values(ascending=False)
    
    # Limiter aux top N si spécifié
    if top_n and top_n < len(value_counts):
        top_values = value_counts.head(top_n)
        others_count = value_counts.tail(len(value_counts) - top_n).sum()
        if others_count > 0:
            top_values['Autres'] = others_count
        value_counts = top_values
    
    # Regrouper les petites catégories si seuil spécifié
    if other_threshold:
        total = value_counts.sum()
        threshold_count = (other_threshold / 100) * total
        
        main_categories = value_counts[value_counts >= threshold_count]
        small_categories = value_counts[value_counts < threshold_count]
        
        if len(small_categories) > 0:
            others_sum = small_categories.sum()
            main_categories['Autres'] = others_sum
            value_counts = main_categories
    
    # Préparer les données
    labels = value_counts.index.tolist()
    values = value_counts.values.tolist()
    
    # Couleurs par défaut
    if colors is None:
        colors = [
            "#0DB329", "#E4E917", "#E79D19", "#E32B1D", "#0CA0B4", "#064C56",
            "#8B4513", "#FF69B4", "#32CD32", "#FF4500", "#9370DB", "#20B2AA",
            "#FFD700", "#FF6347", "#40E0D0", "#EE82EE", "#98FB98", "#F0E68C"
        ]
    
    # Étendre les couleurs si nécessaire
    while len(colors) < len(values):
        colors.extend(colors)
    
    # Préparation des données pour ECharts
    chart_data = []
    for i, (label, value) in enumerate(zip(labels, values)):
        chart_data.append({
            "name": str(label),
            "value": value,
            "itemStyle": {"color": colors[i % len(colors)]}
        })
    
    # Configuration du rayon selon le style
    if style.lower() == "donut":
        radius = [donut_radius, "80%"]
    else:  # style == "disque"
        radius = ["0%", "80%"]
    
    # Configuration des labels
    label_config = {
        "show": show_labels,
        "position": "outside" if style.lower() == "disque" else "inside",
        "fontSize": 12,
        "fontWeight": "bold"
    }
    
    if show_percentages:
        label_config["formatter"] = "{b}\n{c} ({d}%)"
    else:
        label_config["formatter"] = "{b}\n{c}"
    
    
    # Configuration du graphique
    option = {
        "title": {
            "text": title,
            "left": "center",
            "top": "0%",
            "textStyle": {
                "fontSize": 18,
                "fontWeight": "bold",
                "color": "#333"
            }
        },
        "tooltip": {
            "trigger": "item",
            "formatter": "{b}: {c} ({d}%)<br/>Sur {total} observations".replace("{total}", str(value_counts.sum()))
        },
        "legend": {
            "show": show_legend,
            "type": "scroll",
            "orient": "horizontal",
            "bottom": 2,
            "left": "center",
            "data": labels
        },
        "series": [
            {
                "name": column,
                "type": "pie",
                "radius": radius,
                "center": ["40%", "50%"],
                "data": chart_data,
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)"
                    }
                },
                "label": label_config,
                "labelLine": {
                    "show": show_labels and style.lower() == "disque",
                    "length": 15,
                    "length2": 10
                }
            }
        ]
    }
    
    # Ajustements pour le style donut
    if style.lower() == "donut":
        total = sum(values)
        option["graphic"] = [
            {
                "type": "text",
                "left": "20%",
                "top": "28%",
                "style": {
                    "text": "",
                    "textAlign": "center",
                    "fontSize": 16,
                    "fontWeight": "bold",
                    "fill": "#333"
                }
            }
        ]
        
        option["series"][0]["label"]["position"] = "center"
        option["series"][0]["label"]["formatter"] = "{d}%"
        option["series"][0]["emphasis"]["label"] = {
            "show": True,
            "fontSize": 20,
            "fontWeight": "bold"
        }
    
    # Afficher le graphique
    st_echarts(options=option, height=height, key=cle,renderer="svg")
    


def get_image_as_base64_optimized(image_path: str, max_size: tuple = (400, 400)) -> Optional[str]:
    """
    Convertit et optimise une image en base64 pour éviter les problèmes de performance.
    """
    try:
        if not os.path.exists(image_path):
            return None
        
        # Ouvrir et redimensionner l'image si nécessaire
        with Image.open(image_path) as img:
            # Convertir en RGB si nécessaire
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Redimensionner si trop grande
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Sauvegarder en bytes
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=85, optimize=True)
            buffer.seek(0)
            
            return base64.b64encode(buffer.getvalue()).decode()
            
    except Exception as e:
        st.warning(f"Erreur lors du traitement de l'image {image_path}: {e}")
        return None

def create_simple_background_profile(name: str, title: str, about_text: str,
                                   image_path: Optional[str] = None,
                                   email: Optional[str] = None,
                                   phone: Optional[str] = None,
                                   skills: Optional[List[str]] = None,
                                   theme_color: str = "#4e8df5",
                                   height: int = 400):
    """
    Version simplifiée et plus stable de la carte profil avec background.
    """
    
    # Validation
    if not name or not title or not about_text:
        st.error("Les paramètres name, title et about_text sont obligatoires")
        return
    
    # Container principal avec style de base
    with st.container():
        # ID unique pour éviter les conflits
        card_id = f"simple-bg-{abs(hash(name + title)) % 10000}"
        
        # Gestion de l'image optimisée
        background_css = ""
        if image_path and os.path.exists(image_path):
            img_base64 = get_image_as_base64_optimized(image_path)
            if img_base64:
                background_css = f"""
                background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                                 url('data:image/jpeg;base64,{img_base64}');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                """
        
        # Si pas d'image, utiliser un gradient
        if not background_css:
            background_css = f"""
            background: linear-gradient(135deg, {theme_color}cc, {theme_color}88, {theme_color}44);
            """
        
        # CSS simplifié et robuste
        st.markdown(f"""
        <style>
        .{card_id} {{
            {background_css}
            border-radius: 15px;
            padding: 30px;
            margin: 20px 0;
            min-height: {height}px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            align-items: flex-start;
            text-align: left;
            color: white;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            position: relative;
        }}

        .{card_id} .profile-content {{
            z-index: 2;
            position: relative;
            width: 100%;
        }}

        .{card_id} .profile-name {{
            font-size: 58px;
            font-weight: bold;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            text-align: right;
        }}

        .{card_id} .profile-title {{
            font-size: 18px;
            background: rgba(255,255,255,0.1);
            color: #ffffff;
            padding: 8px 20px;
            border-radius: 20px;
            display: inline-block;
            margin-bottom: 15px;
            font-weight: 500;
            text-align: right;
        }}

        .{card_id} .profile-about {{
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 20px;
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 10px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
            text-align: left;
        }}

        .{card_id} .profile-contacts {{
            margin-bottom: 15px;
            text-align: left;
        }}

        .{card_id} .contact-item {{
            background: rgba(255,255,255,0.2);
            padding: 8px 15px;
            margin: 5px;
            border-radius: 15px;
            display: inline-block;
            font-size: 14px;
        }}

        .{card_id} .contact-item a {{
            color: white;
            text-decoration: none;
            font-weight: 500;
        }}

        .{card_id} .skills-section {{
            display: flex;
            flex-wrap: wrap;
            justify-content: flex-start;
            gap: 8px;
            text-align: left;
        }}

        .{card_id} .skill-tag {{
            background: rgba(255,255,255,0.2);
            padding: 6px 12px;
            border-radius: 12px;
            font-size: 13px;
            font-weight: 500;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # Construction du contenu avec validation
        contacts_html = ""
        if email or phone:
            contact_items = []
            if email:
                contact_items.append(f'<span class="contact-item">📧 <a href="mailto:{email}">{email}</a></span>')
            if phone:
                contact_items.append(f'<span class="contact-item">📞 {phone}</span>')
            contacts_html = f'<div class="profile-contacts">{"".join(contact_items)}</div>'
        
        skills_html = ""
        if skills:
            skill_tags = [f'<span class="skill-tag">{skill}</span>' for skill in skills if skill]
            if skill_tags:
                skills_html = f'<div class="skills-section">{"".join(skill_tags)}</div>'
        
        # Affichage de la carte
        card_html = f"""
        <div class="{card_id}">
            <div class="profile-content">
            <div class="profile-name" style="font-size: 88px;">{name}</div>
            <div class="profile-title">{title}</div>
            {contacts_html}
            {skills_html}
            <div class="profile-about">{about_text}</div>
            </div>
        </div>
        """
        
        st.markdown(card_html, unsafe_allow_html=True)

def create_overlay_profile_card(name: str, title: str, about_text: str,
                               image_path: Optional[str] = None,
                               email: Optional[str] = None,
                               phone: Optional[str] = None,
                               skills: Optional[List[str]] = None,
                               theme_color: str = "#4e8df5"):
    """
    Version alternative avec overlay en utilisant les colonnes Streamlit.
    """
    
    if image_path and os.path.exists(image_path):
        # Afficher l'image comme background avec Streamlit natif
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Afficher l'image
            try:
                st.image(image_path, use_container_width=True)
            except Exception as e:
                st.error(f"Impossible d'afficher l'image: {e}")
        
        with col2:
            # Informations avec style
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {theme_color}ee, {theme_color}cc);
                padding: 30px;
                border-radius: 15px;
                color: white;
                height: 100%;
                min-height: 300px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <h2 style="margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">{name}</h2>
                <h4 style="color: #FFD700; margin-bottom: 15px;">{title}</h4>
                <p style="line-height: 1.6; margin-bottom: 15px;">{about_text}</p>
                
                {"<p><strong>📧</strong> " + email + "</p>" if email else ""}
                {"<p><strong>📞</strong> " + phone + "</p>" if phone else ""}
                
                {'<div style="margin-top: 15px;">' + "".join([f'<span style="background: rgba(255,255,255,0.2); padding: 4px 8px; margin: 2px; border-radius: 8px; font-size: 12px;">{skill}</span>' for skill in (skills or [])]) + '</div>' if skills else ""}
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # Version sans image
        create_simple_background_profile(name, title, about_text, None, email, phone, skills, theme_color)

def create_streamlit_native_profile(name: str, title: str, about_text: str,
                                  image_path: Optional[str] = None,
                                  email: Optional[str] = None,
                                  phone: Optional[str] = None,
                                  skills: Optional[List[str]] = None,
                                  theme_color: str = "#4e8df5"):
    """
    Version 100% Streamlit natif - la plus stable.
    """
    
    # Container avec bordure colorée
    with st.container():
        st.markdown(f"""
        <div style="
            border-left: 5px solid {theme_color};
            background: linear-gradient(90deg, {theme_color}10, transparent);
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        ">
        """, unsafe_allow_html=True)
        
        # Layout en colonnes si image présente
        if image_path and os.path.exists(image_path):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                try:
                    st.image(image_path, width=200)
                except:
                    st.error("Image non trouvée")
            
            with col2:
                st.markdown(f"### {name}")
                st.markdown(f"**{title}**")
                st.write(about_text)
                
                if email:
                    st.write(f"📧 {email}")
                if phone:
                    st.write(f"📞 {phone}")
                
                if skills:
                    st.write("**Compétences:**")
                    st.write(" • ".join(skills))
        
        else:
            # Sans image
            st.markdown(f"### {name}")
            st.markdown(f"**{title}**")
            st.write(about_text)
            
            if email or phone:
                st.write("**Contact:**")
                if email:
                    st.write(f"📧 {email}")
                if phone:
                    st.write(f"📞 {phone}")
            
            if skills:
                st.write("**Compétences:**")
                st.write(" • ".join(skills))
        
        st.markdown("</div>", unsafe_allow_html=True)

# Interface de test et diagnostic
def test_background_profiles():
    """
    Interface de test avec plusieurs versions pour identifier les problèmes.
    """
    
    st.title("🔧 Test Profils Background - Versions Corrigées")
    
    # Données d'exemple
    sample_data = {
        'name': 'Landry KENGNE',
        'title': 'ISE',
        'about': 'STATISTICIEN',
        'email': 'landry.kengne99@gmail.com',
        'phone': '+237 6 98 28 05 37',
        'skills': ['Statistiques', 'Data Analysis', 'Python', 'R']
    }
    
    # Sélection de la version
    version = st.selectbox(
        "Choisir la version à tester:",
        ["Version Simplifiée", "Version Overlay", "Version Native Streamlit", "Diagnostic"]
    )
    
    # Upload d'image pour test
    uploaded_file = st.file_uploader("Choisir une image", type=['png', 'jpg', 'jpeg'])
    
    image_path = None
    if uploaded_file is not None:
        # Sauvegarder temporairement
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        image_path = temp_path
    
    # Options de personnalisation
    with st.sidebar:
        st.header("Personnalisation")
        theme_color = st.color_picker("Couleur thème", "#4e8df5")
        height = st.slider("Hauteur (px)", 300, 600, 400)
    
    # Test selon la version sélectionnée
    if version == "Version Simplifiée":
        st.subheader("🛠️ Version Simplifiée (Recommandée)")
        st.info("Version optimisée avec CSS simplifié et images redimensionnées")
        
        create_simple_background_profile(
            name=sample_data['name'],
            title=sample_data['title'],
            about_text=sample_data['about'],
            image_path=image_path,
            email=sample_data['email'],
            phone=sample_data['phone'],
            skills=sample_data['skills'],
            theme_color=theme_color,
            height=height
        )
    
    elif version == "Version Overlay":
        st.subheader("🎨 Version Overlay")
        st.info("Version avec colonnes Streamlit et overlay CSS")
        
        create_overlay_profile_card(
            name=sample_data['name'],
            title=sample_data['title'],
            about_text=sample_data['about'],
            image_path=image_path,
            email=sample_data['email'],
            phone=sample_data['phone'],
            skills=sample_data['skills'],
            theme_color=theme_color
        )
    
    elif version == "Version Native Streamlit":
        st.subheader("🏠 Version Native (Plus Stable)")
        st.info("Version 100% composants Streamlit natifs")
        
        create_streamlit_native_profile(
            name=sample_data['name'],
            title=sample_data['title'],
            about_text=sample_data['about'],
            image_path=image_path,
            email=sample_data['email'],
            phone=sample_data['phone'],
            skills=sample_data['skills'],
            theme_color=theme_color
        )
    
    else:  # Diagnostic
        st.subheader("🩺 Diagnostic")
        
        st.write("**Informations système:**")
        st.write(f"- Version Streamlit: {st.__version__}")
        
        if image_path:
            st.write("**Test image:**")
            try:
                img = Image.open(image_path)
                st.write(f"- Format: {img.format}")
                st.write(f"- Mode: {img.mode}")
                st.write(f"- Taille: {img.size}")
                
                # Test de la conversion base64
                img_b64 = get_image_as_base64_optimized(image_path)
                if img_b64:
                    st.success("✅ Conversion base64 réussie")
                    st.write(f"- Taille base64: {len(img_b64)} caractères")
                else:
                    st.error("❌ Échec conversion base64")
                    
            except Exception as e:
                st.error(f"Erreur lors de l'analyse: {e}")
        
        # Test CSS simple
        st.write("**Test CSS:**")
        st.markdown("""
        <div style="background: linear-gradient(45deg, #ff6b6b, #4ecdc4); 
                    padding: 20px; 
                    border-radius: 10px; 
                    color: white; 
                    text-align: center;">
            Si vous voyez ce texte stylisé, le CSS fonctionne ✅
        </div>
        """, unsafe_allow_html=True)
    
    # Nettoyage
    if uploaded_file and image_path and os.path.exists(image_path):
        try:
            os.remove(image_path)
        except:
            pass

# Pour lancer: streamlit run nom_du_fichier.py


def make_multi_progress_bar_echart(labels, values, colors, titre="", width="100%", height="400px",cle="jdflkdfkjn"):
    """
    Crée un graphique de barres de progression multiples avec ECharts
    """
    
    # Préparer les données pour chaque série
    filled_series = []
    empty_series = []
    labels=labels.tolist()
    values=values.tolist()
    # Créer les données pour les barres pleines et vides
    for i, (label, value, color) in enumerate(zip(labels, values, colors)):
        filled_value = value * 100
        empty_value = 100 - filled_value
        
        filled_series.append(filled_value)
        empty_series.append(empty_value)
    
    # Configuration du graphique
    option = {
        'title': {
            'text': titre,
            'left': 'center',
            'textStyle': {'fontSize': 16}
        },
        'grid': {
            'left': '5%',
            'right': '15%',
            'top': '10%',
            'bottom': '1%',
            'containLabel': True
        },
        'xAxis': {
            'type': 'value',
            'max': 100,
            'show': False,
            'splitLine': {'show': False}
        },
        'yAxis': {
            'type': 'category',
            'data': labels,
            'show': False,
            'axisLine': {'show': False},
            'axisTick': {'show': False}
        },
        'series': [
            {
                'name': 'Progression',
                'type': 'bar',
                'stack': 'total',
                'data': [
                    {
                        'value': filled_series[i],
                        'itemStyle': {
                            'color': colors[i],
                            'borderRadius': [2, 0, 0, 2]
                        }
                    } for i in range(len(labels))
                ],
                'barHeight': '60%',
                'showBackground': False
            },
            {
                'name': 'Restant',
                'type': 'bar',
                'stack': 'total',
                'data': [
                    {
                        'value': empty_series[i],
                        'itemStyle': {
                            'color': 'rgba(0, 0, 0, 0.1)',
                            'borderRadius': [0, 2, 2, 0]
                        }
                    } for i in range(len(labels))
                ],
                'barHeight': '60%',
                'showBackground': False
            }
        ],
        'animation': False,
        'backgroundColor': 'transparent'
    }
    
    # Ajouter les annotations avec graphic
    graphics = []
    
    for i, (label, value, color) in enumerate(zip(labels, values, colors)):
        # Calculer les positions
        # Calculer la position verticale pour aligner le label avec la barre
        #y_pos = (len(labels)+1)*10-(i*(len(labels)+1)*10/ len(labels))
        y_pos = (len(labels)+1)*10*len(labels)-(i*10*len(labels)*(len(labels)+1)/ len(labels))
        # Label à gauche
        graphics.append({
            'type': 'text',
            'left': '2%',
            'top': f'{y_pos}%',
            'style': {
                'text': label,
                'font': 'bold 15px Arial',
                'fill': color,
                'textAlign': 'left',
                'textVerticalAlign': 'middle'
            }
        })
        
        # Pourcentage à droite de la barre
        percentage_x = 36 + (value * 50)  # Position basée sur la valeur
        val_y_pos=y_pos+1.5
        graphics.append({
            'type': 'text',
            'left': f'{percentage_x}%',
            'top': f'{val_y_pos}%',
            'style': {
                'text': f'{round(100 * value, 1)}%',
                'font': 'bold 20px Arial',
                'fill': color,
                'textAlign': 'left',
                'textVerticalAlign': 'middle'
            }
        })
    
    option['graphic'] = graphics
    
    # Afficher le graphique
    st_echarts(
        options=option,
        width=width,
        height=height,
        key=cle  # Clé unique pour éviter les conflits
    )



def display_confusion_matrix(df, var1, var2, value=None, title="Matrice de Confusion", 
                             color_scheme="Blues", height="300px", icon="🔥", unit="", keys="matrix" + str(random.randint(1, 999))):
    """
    Affiche une matrice de confusion/heatmap avec ECharts.
    
    Parameters:
    -----------
    df : DataFrame
        Le dataframe source
    var1 : str
        Variable qualitative pour l'axe Y (lignes)
    var2 : str
        Variable qualitative pour l'axe X (colonnes)
    value : str, optional
        Variable quantitative à sommer. Si None, fait un count
    title : str
        Titre du graphique
    color_scheme : str
        Schéma de couleurs ('Blues', 'Reds', 'Greens', 'Purples', 'Oranges')
    height : str
        Hauteur du graphique
    icon : str
        Icône du titre
    """
    
    # Créer le tableau croisé
    if value is None:
        matrix = pd.crosstab(df[var1], df[var2])
    else:
        matrix = df.pivot_table(
            values=value, 
            index=var1, 
            columns=var2, 
            aggfunc='sum', 
            fill_value=0
        )
    
    # Préparer les données pour ECharts
    y_labels = [str(label) for label in matrix.index.tolist()]
    x_labels = [str(label) for label in matrix.columns.tolist()]
    
    # Convertir la matrice en format [x, y, value]
    data = []
    min_val = float(matrix.min().min())
    
    # Add axis titles
    x_title = var2 # Nom de la variable des colonnes
    y_title = var1 # Nom de la variable des lignes
    
    # Mise à jour des axes avec les titres
    if unit:
        x_title = f"{x_title}"
        y_title = f"{y_title}"
    max_val = float(matrix.max().max())
    
    for i, row_label in enumerate(matrix.index):
        for j, col_label in enumerate(matrix.columns):
            val = matrix.loc[row_label, col_label]
            data.append([int(j), int(i), float(val)])
    
    # Schémas de couleurs
    color_maps = {
        "Blues": ["#f7fbff", "#deebf7", "#c6dbef", "#9ecae1", "#6baed6", "#4292c6", "#2171b5", "#08519c", "#08306b"],
        "Reds": ["#fff5f0", "#fee0d2", "#fcbba1", "#fc9272", "#fb6a4a", "#ef3b2c", "#cb181d", "#a50f15", "#67000d"],
        "Greens": ["#f7fcf5", "#e5f5e0", "#c7e9c0", "#a1d99b", "#74c476", "#41ab5d", "#238b45", "#006d2c", "#00441b"],
        "Purples": ["#fcfbfd", "#efedf5", "#dadaeb", "#bcbddc", "#9e9ac8", "#807dba", "#6a51a3", "#54278f", "#3f007d"],
        "Oranges": ["#fff5eb", "#fee6ce", "#fdd0a2", "#fdae6b", "#fd8d3c", "#f16913", "#d94801", "#a63603", "#7f2704"]
    }
    
    colors = color_maps.get(color_scheme, color_maps["Blues"])
    
    # Configuration ECharts
    # Ajuster ici les marges (modifier les valeurs selon besoin : "10%", "50", etc.)
    margin_left = "1%"    # espace gauche
    margin_right = "20%"    # espace droite
    margin_top = "0%"      # espace haut
    margin_bottom = "10%"  # espace bas

    # Marges pour les labels d'axe (en pixels)
    x_label_margin = 8
    y_label_margin = 8

    options = {
        "tooltip": {
            "position": "top",
            "formatter": "{b}: {c}",
            # confine garde les tooltips à l'intérieur du conteneur
                        },
                        "grid": {
                                "left": margin_left,
                                "right": margin_right,
                                "top": margin_top,
                                "bottom": margin_bottom,
                                "containLabel": True
                        },
                        "xAxis": {
                                "type": "category",
                                "data": x_labels,
                                "splitArea": {"show": True},
                                "axisLabel": {
                                        "rotate": 0,
                                        "fontSize": 12,
                                        "margin": x_label_margin
                                },
                                # Titre axe X
                                "name": x_title,
                                "nameLocation": "middle",
                                "nameGap": 30,
                                "nameTextStyle": {"fontSize": 13, "fontWeight": "bold"}
                        },
                        "yAxis": {
                                "type": "category",
                                "data": y_labels,
                                "splitArea": {"show": True},
                                "axisLabel": {
                                        "fontSize": 12,
                                        "margin": y_label_margin
                                },
                                # Titre axe Y
                                "name": y_title,
                                "nameLocation": "middle",
                                "nameGap": 50,
                                "nameTextStyle": {"fontSize": 13, "fontWeight": "bold"}
                        },
                        "visualMap": {
                                "min": min_val,
                                "max": max_val,
                                "calculable": True,
                                "orient": "vertical",
                                "right": "3%",   # placer la légende de couleurs à droite (adapter si nécessaire)
            "top": "center",
            "inRange": {
                "color": colors
            },
            "text": ["Max", "Min"],
            "textStyle": {
                "fontSize": 11
            }
        },
        "series": [{
            "name": "Matrice",
            "type": "heatmap",
            "data": data,
            "label": {
                "show": True,
                "fontSize": 11,
                "fontWeight": "bold"
            },
            "emphasis": {
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowColor": "rgba(0, 0, 0, 0.5)"
                }
            }
        }]
    }
    
    
    
    st_echarts(options=options, height=height, key=keys)
      
def display_confusion_from_crosstab(
        matrix, 
        x_title="Axe X", 
        y_title="Axe Y", 
        title="Matrice de Confusion",
        color_scheme="Blues",
        height="300px",
        icon="🔥",
        unit="",
        keys="matrix" + str(random.randint(1, 999))
    ):
    """
    Affiche une matrice de confusion/heatmap à partir d'un tableau croisé déjà préparé.

    Parameters
    ----------
    matrix : DataFrame
        Tableau croisé (index = lignes, colonnes = colonnes).
    x_title : str
        Nom de l'axe X.
    y_title : str
        Nom de l'axe Y.
    title : str
        Titre du graphique.
    color_scheme : str
        Schéma de couleurs.
    height : str
        Hauteur.
    icon : str
        Icône dans le titre.
    unit : str
        Unité.
    keys : str
        Clé unique Streamlit.
    """

    # Préparer les labels
    y_labels = [str(label) for label in matrix.index.tolist()]
    x_labels = [str(label) for label in matrix.columns.tolist()]

    # Convertir la matrice en format [x, y, value]
    data = []
    min_val = float(matrix.min().min())
    max_val = float(matrix.max().max())

    for i, row_label in enumerate(matrix.index):
        for j, col_label in enumerate(matrix.columns):
            val = matrix.loc[row_label, col_label]
            data.append([int(j), int(i), float(val)])

    # Schémas de couleurs
    color_maps = {
        "Blues": ["#f7fbff", "#deebf7", "#c6dbef", "#9ecae1", "#6baed6", "#4292c6", "#2171b5", "#08519c", "#08306b"],
        "Reds": ["#fff5f0", "#fee0d2", "#fcbba1", "#fc9272", "#fb6a4a", "#ef3b2c", "#cb181d", "#a50f15", "#67000d"],
        "Greens": ["#f7fcf5", "#e5f5e0", "#c7e9c0", "#a1d99b", "#74c476", "#41ab5d", "#238b45", "#006d2c", "#00441b"],
        "Purples": ["#fcfbfd", "#efedf5", "#dadaeb", "#bcbddc", "#9e9ac8", "#807dba", "#6a51a3", "#54278f", "#3f007d"],
        "Oranges": ["#fff5eb", "#fee6ce", "#fdd0a2", "#fdae6b", "#fd8d3c", "#f16913", "#d94801", "#a63603", "#7f2704"]
    }

    colors = color_maps.get(color_scheme, color_maps["Blues"])

    # Marges
    margin_left = "1%"
    margin_right = "20%"
    margin_top = "10%"
    margin_bottom = "10%"
    x_label_margin = 8
    y_label_margin = 8

    # Options ECharts
    options = {
        "tooltip": {
            "position": "bottom",
            
        },
        "grid": {
            "left": margin_left,
            "right": margin_right,
            "top": margin_top,
            "bottom": margin_bottom,
            "containLabel": True
        },
        "xAxis": {
            "type": "category",
            "data": x_labels,
            "splitArea": {"show": True},
            "axisLabel": {
                "rotate": 15,
                "fontSize": 12,
                "margin": x_label_margin
            },
            "name": x_title,
            "nameLocation": "middle",
            "nameGap": 30,
            "nameTextStyle": {"fontSize": 13, "fontWeight": "bold"}
        },
        "yAxis": {
            "type": "category",
            "data": y_labels,
            "splitArea": {"show": True},
            "axisLabel": {
                "fontSize": 12,
                "margin": y_label_margin
            },
            "name": y_title,
            "nameLocation": "middle",
            "nameGap": 50,
            "nameTextStyle": {"fontSize": 13, "fontWeight": "bold"}
        },
        "title": {
            "text": title,
            "left": "center",   # options: 'left', 'center', 'right' or pixel/% value
            "top": "0%",        # options: pixel or '%' (ex: '10px', '5%')
            "textStyle": {
                "fontSize": 16,
                "fontWeight": "bold",
                "color": "#333"
            }
        },
        "visualMap": {
            "min": min_val,
            "max": max_val,
            "calculable": True,
            "orient": "vertical",
            "right": "3%",
            "top": "center",
            "inRange": {"color": colors},
            "text": ["Max", "Min"],
            "textStyle": {"fontSize": 11}
        },
        "series": [{
            "name": "Matrice",
            "type": "heatmap",
            "data": data,
            "label": {
                "show": True,
                "fontSize": 11,
                "fontWeight": "bold"
            },
            "emphasis": {
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowColor": "rgba(0, 0, 0, 0.5)"
                }
            }
        }]
    }

    st_echarts(options=options, height=height, key=keys)
   


def mapping(agg_data, data_marquer=None, aggregation="Region", contenu="Dwelling", 
            marquer=False, selected_region=None, marker_var="str_landmark_hab"):
    """
    Crée une carte choroplèthe avec des marqueurs optionnels
    
    Parameters:
    -----------
    agg_data : DataFrame contenant les données agrégées avec une colonne 'geometry'
    data_marquer : DataFrame contenant les données des marqueurs (str_id, dwl_latitude, dwl_longitude, str_landmark_hab)
    aggregation : str, niveau d'agrégation ("Region" ou "District")
    contenu : str, type de contenu ("Dwelling" ou "Structure")
    marquer : bool, afficher les marqueurs ou non
    selected_region : str, région sélectionnée pour filtrer les marqueurs
    marker_var : str, variable pour définir la couleur des marqueurs
    """
    
    # Définir la colonne de valeur selon le contenu
    value_col = "Total_dwelling" if contenu == "Dwelling" else "Total_structure"
    name_col = "dwl_region" if aggregation == "Region" else "dwl_district"
    
    # Calculer le centre de la carte
    bounds = agg_data.geometry.total_bounds  # [minx, miny, maxx, maxy]
    center_lat = data_marquer["dwl_latitude"].mean() if marquer and data_marquer is not None else (bounds[1] + bounds[3]) / 2
    center_lon = data_marquer["dwl_longitude"].mean() if marquer and data_marquer is not None else (bounds[0] + bounds[2]) / 2
    
    # Créer la carte de base
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=6.49,
        tiles='CartoDB positron'
    )
    
    # Ajouter la carte choroplèthe
    choropleth = Choropleth(
        geo_data=agg_data.__geo_interface__,  # Convertir GeoDataFrame en GeoJSON
        data=agg_data,
        columns=[name_col, value_col],
        key_on=f'feature.properties.{name_col}',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.3,
        legend_name=f'{contenu} par {aggregation}',
        highlight=True
    ).add_to(m)
    
    # Ajouter les tooltips
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(
            fields=[name_col, value_col],
            aliases=[aggregation, f'Total {contenu}'],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
        )
    )
    
    # Ajouter les marqueurs si activé
    if marquer and data_marquer is not None:
        # Filtrer les données des marqueurs selon la région sélectionnée si nécessaire
        if selected_region:
            # Vous devrez peut-être joindre avec geo_data pour obtenir la région
            data_marquer_filtered = data_marquer.copy()
        else:
            data_marquer_filtered = data_marquer.copy()
        
        # Définir une palette de couleurs pour les modalités
        modalites = data_marquer_filtered[marker_var].unique()
        couleurs = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 
                   'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 
                   'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 
                   'gray', 'black', 'lightgray']
        
        # Créer un dictionnaire de couleurs pour chaque modalité
        color_map = {modalite: couleurs[i % len(couleurs)] 
                    for i, modalite in enumerate(modalites)}
        
        # Ajouter les marqueurs
        for idx, row in data_marquer_filtered.iterrows():
            if pd.notna(row['dwl_latitude']) and pd.notna(row['dwl_longitude']):
                # Déterminer la couleur selon la modalité
                color = color_map.get(row[marker_var], 'gray')
                points = data_marquer_filtered[["dwl_latitude", "dwl_longitude"]]
                callback = """
                function (row) {
                    return L.marker(
                        new L.LatLng(row[0], row[1]),
                        {
                            icon: L.AwesomeMarkers.icon({
                                icon: 'home',
                                markerColor: 'blue',
                                prefix: 'fa'
                            })
                        }
                    );
                }
                """
                FastMarkerCluster(points, callback=callback).add_to(m)
                # Créer le marqueur
                #folium.Marker(
                    #location=[row['dwl_latitude'], row['dwl_longitude']],
                    #popup=f"Structure ID: {row['str_id']}<br>{marker_var}: {row[marker_var]}",
                    #tooltip=f"{row[marker_var]}",
                    #icon=folium.Icon(color=color, icon='home', prefix='fa')
                #).add_to(m)
        
        # Ajouter une légende pour les marqueurs
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; right: 50px; width: 200px; height: auto; 
                    background-color: white; z-index:9999; font-size:14px;
                    border:2px solid grey; border-radius: 5px; padding: 10px">
        <p style="margin-bottom: 5px;"><strong>Légende Marqueurs:</strong></p>
        '''
        for modalite, color in color_map.items():
            legend_html += f'<p style="margin: 3px 0;"><i class="fa fa-map-marker" style="color:{color}"></i> {modalite}</p>'
        legend_html += '</div>'
        
        m.get_root().html.add_child(folium.Element(legend_html))
    
    return m

