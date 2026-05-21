#==========IMPORTATION DES BIBLIOTHEQUES NECESSAIRES===================================
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import geopandas as gpd
import streamlit as st
from scipy.stats import chi2_contingency
from scipy.stats import ttest_ind
from scipy.stats import levene
import random
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io
import os
import json
import branca.colormap as cm
import folium
from folium.plugins import MarkerCluster
from branca.colormap import linear
from streamlit_folium import folium_static
import datetime
from datetime import datetime, timedelta
from st_aggrid.grid_options_builder import GridOptionsBuilder
from deep_translator import GoogleTranslator
from requests.exceptions import ConnectionError, Timeout
from st_aggrid import AgGrid
from streamlit_echarts import st_echarts
import base64
import hashlib
import time
import requests
import json



    

#==================================================================================================

#============Variables Globales====================================================================
police=dict(size=25,family="Berlin Sans FB",)
police_label=dict(size=15,family="Berlin Sans FB",)
police_annot=dict(size=15,family="Berlin Sans FB",)
palette = ['#FDB5B5', '#F90B0B', '#830303','#B5B5FD', '#0808F8','#050595', '#ABEEFB', '#15CEF3', '#06687C', '#A3FBA7', '#09E513', '#046809', '#FCF1B2', '#F5D61B', '#755D05', '#FDD2B1', '#F87614', '#8A3D04', '#F46D43', '#FEE090', '#D73027']
val_couleur=[['#FDB5B5'],['#F90B0B'], ['#830303'],['#B5B5FD'], ['#0808F8'],['#050595'], ['#ABEEFB'], ['#15CEF3'], ['#06687C'], ['#A3FBA7'], ['#09E513'], ['#046809'], ['#FCF1B2'], ['#F5D61B'], ['#755D05'], ['#FDD2B1'], ['#F87614'], ['#8A3D04'], ['#F46D43'], ['#FEE090'], ['#D73027']]
sequence_couleur=["blues",'reds', 'agsunset', 'algae', 'amp', 'armyrose', 'balance',
             'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
             'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',
             'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',
             'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
             'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',
             'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
             'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl',
             'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn',
             'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu',
             'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'aggrnyl', 'solar',
             'spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn',
             'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid',
             'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr',
             'ylorrd']

useless_style="""
<style>
.sidebar-link {
    display: block;
    margin-bottom: 15px;
    padding: 10px 15px;
    text-decoration: none;
    color: #333;
    background-color: #f8f9fa;
    border-radius: 8px;
    transition: all 0.3s ease;
    font-weight: 500;
}

.sidebar-link-right {
    display: block;
    margin-bottom: 15px;
    padding: 10px 15px;
    text-decoration: none;
    color: #333;
    background-color: #f8f9fa;
    border-radius: 8px;
    transition: all 0.3s ease;
    font-weight: 500;
    text-align: right;
}

.sidebar-link-center {
    display: block;
    margin-bottom: 15px;
    padding: 10px 15px;
    text-decoration: none;
    color: #333;
    background-color: #f8f9fa;
    border-radius: 8px;
    transition: all 0.3s ease;
    font-weight: 500;
    text-align: center;
}
</style>
"""

echart_style="""
        <style>
        /* Styles de base pour tous les thèmes */
        .stContainer {
            border-radius: 10px;  /* Coins arrondis */
            border: 2px solid transparent;  /* Bordure transparente par défaut */
            padding: 20px;  /* Espacement intérieur */
            margin-bottom: 20px;  /* Espace entre les conteneurs */
            transition: all 0.3s ease;  /* Animation douce */
        }

        /* Mode Clair (par défaut) */
        body:not(.dark) .stContainer {
            background-color: rgba(255, 255, 255, 0.9);  /* Fond blanc légèrement transparent */
            border-color: rgba(224, 224, 224, 0.7);  /* Bordure grise légère */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.08);  /* Ombre douce */
        }

        /* Mode Sombre */
        body.dark .stContainer {
            background-color: rgba(30, 30, 40, 0.9);  /* Fond sombre légèrement transparent */
            border-color: rgba(60, 60, 70, 0.7);  /* Bordure sombre légère */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);  /* Ombre plus marquée */
        }

        /* Effet de survol - Mode Clair */
        body:not(.dark) .stContainer:hover {
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.5);  /* Ombre plus prononcée */
            transform: translateY(-5px);  /* Léger soulèvement */
            border-color: rgba(200, 200, 200, 0.9);  /* Bordure plus visible */
        }

        /* Effet de survol - Mode Sombre */
        body.dark .stContainer:hover {
            box-shadow: 0 8px 12px rgba(255, 255, 255, 0.5);  /* Ombre claire */
            transform: translateY(-5px);  /* Léger soulèvement */
            border-color: rgba(100, 100, 110, 0.9);  /* Bordure plus visible */
        }

        /* Style spécifique pour les graphiques - Mode Clair */
        body:not(.dark) .stPlotlyChart {
            background-color: rgba(250, 250, 250, 0.95);  /* Fond très légèrement gris */
            border-radius: 8px;  /* Coins légèrement arrondis */
            padding: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);  /* Ombre très légère */
        }

        /* Style spécifique pour les graphiques - Mode Sombre */
        body.dark .stPlotlyChart {
            background-color: rgba(40, 40, 50, 0.95);  /* Fond sombre légèrement transparent */
            border-radius: 8px;  /* Coins légèrement arrondis */
            padding: 10px;
            box-shadow: 0 2px 4px rgba(255, 255, 255, 0.05);  /* Ombre très légère */
        }

        /* Style spécifique pour les graphiques ECharts */
        .echarts-container {
            border-radius: 10px;
            padding: 5px;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }

        body:not(.dark) .echarts-container {
            background-color: rgba(255, 255, 255, 0.9);
            border: 2px solid rgba(224, 224, 224, 0.7);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.08);
        }

        body.dark .echarts-container {
            background-color: rgba(30, 30, 40, 0.9);
            border: 2px solid rgba(60, 60, 70, 0.7);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }

        body:not(.dark) .echarts-container:hover {
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
            transform: translateY(-3px);
        }

        body.dark .echarts-container:hover {
            box-shadow: 0 8px 12px rgba(255, 255, 255, 0.1);
            transform: translateY(-3px);
        }
        </style>
    """

#st.set_page_config(layout="wide")
#==================================================================================================

#==================================================================================================
# FONCTIONS
#==================================================================================================
#1. Fonction pour faire les regroupement de classe d'âge
def class_age(age):
    if age < 20:
        return "- 20 ans"
    elif age < 30:
        return "20-30 ans"
    elif age < 40:
        return "30-40 ans"
    elif age < 50:
        return "40-50 ans"
    elif age < 60:
        return "50-60 ans"
    else:
        return "+60 ans"

#2. Fonction de tranduction 

# Créer des traducteurs à l'avance pour les langues fréquemment utilisées
traducteur_en = GoogleTranslator(source='auto', target='en')
traducteur_fr = GoogleTranslator(source='auto', target='fr')

def traduire_texte(texte, langue='English'):
    """
    Traduit le texte donné vers la langue cible en utilisant Google Translate.

    :param texte: Le texte à traduire.
    :param langue: La langue cible pour la traduction (par défaut 'English').
    :return: Le texte traduit.
    """
    if langue == "" or not texte:
        return texte
    
    try:
        # Utiliser le traducteur préinitialisé approprié
        if langue == "Français":
            traduction = traducteur_fr.translate(texte)
        else:  # Par défaut, traduire vers l'anglais
            traduction = traducteur_en.translate(texte)
            
        return traduction
        
    except Exception as e:
        # print(f"Erreur lors de la traduction: {e}")
        return texte  # En cas d'erreur, retourner le texte original
    
#3. Fonction d'affichage des métriques version 1
def display_single_metric_advanced(label, value, delta, unit="", caption="", color_scheme="blue"):
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
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            text-align: top;
            font-size: 20px;
            transition: all 0.3s ease;
        "
        onmouseover="this.style.transform='scale(1.1)'; this.style.boxShadow='0 6px 12px rgba(0,0,0,0.3)'; this.style.backgroundColor='rgba(255,255,255,0.9)';"
        onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.2)'; this.style.backgroundColor='rgba(255,255,255,0.8)';">
            <h4 style="color: {color['text']}; margin-bottom: 5px; font-family: Arial, sans-serif; font-weight: bold;">
                {label}
            </h4>
            <div style="font-size: 19px; font-weight: bold; color: {color['text']};">
                <h2 class="dashboard-main-title", margin-bottom: 1px; style="font-family: Arial, sans-serif; font-weight: bold; position: relative; top: 0px;"> 
                Nombre: {value} {unit}
                </h2>
            </div>
            <div style="font-size: 15.5em; color: {color['text'] if delta >= 0 else color['delta_neg']};">
                <h3>Progress: {'▲' if delta >= 0 else '▼'} {abs(delta)} % </h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

#4. Fonction pour tracer l'histogramme croisé de deux variables  version 1
def make_cross_hist(df,var1,var2,titre="",typ_bar=1,width=500, height=400,sens="v"):
    bar_mode= "relative" if typ_bar==1 else "group"
    cross_df=pd.crosstab(df[var1],df[var2])
    table_cross = cross_df.reset_index().melt(id_vars=var1, var_name=var2, value_name='Effectif')
    table_cross=table_cross.sort_values("Effectif",ascending=False)
    fig = px.bar(table_cross, x=var2 if sens=="v" else 'Effectif' , y=var2 if sens=="h" else 'Effectif', color=var1, text_auto='.2s', 
                            title=titre, barmode=bar_mode,orientation=sens,)
    fig.update_layout(margin=dict(l=5, r=1, t=30, b=10),width=width, height=height,
                    title=dict(
        text=titre,
        x=0.0,  
        y=0.95, 
        xanchor='left', 
        yanchor='top'),
            legend=dict(
            x=0.8,  # Position horizontale (à droite)
            y=1,  # Position verticale (en haut)
            traceorder='normal',
            xanchor='center',  # Alignement horizontal de la légende
            yanchor='top',  # Alignement vertical de la légende
            bgcolor='rgba(255,255,255,0.1)',  # Fond semi-transparent de la légende
        ))
    
    st.plotly_chart(fig)
 
#5. Fonction pour tracer l'histogramme croisé de deux variables  version 2   
def make_cross_hist_2(df,var1,var2,titre="",typ_bar=2,width=500, height=400,sens="v"):
    bar_mode= "stack" if typ_bar==1 else "group"
    cross_df=pd.crosstab(df[var1],df[var2])
    table_cross = cross_df.reset_index().melt(id_vars=var1, var_name=var2, value_name='Effectif')
    table_cross=table_cross.sort_values("Effectif",ascending=False)
    fig = go.Figure()
    y_var=list(df[var1].unique())
    x_var=list(df[var2].unique())
    for i in range(len(y_var)):
        y_data = list(table_cross[table_cross[var1] == y_var[i]]["Effectif"])
        fig.add_trace(go.Bar(name=y_var[i],x=x_var if sens=='v' else y_data, y=x_var if sens=='h' else y_data,
                             text=y_data,  # Ajouter les valeurs sur les barres
            textposition='auto' ,
            orientation=sens,# Positionner les étiquettes automatiquement
            ))
    fig.update_layout(width=width, height=height, barmode=bar_mode,
                    title=dict(
        text=titre,
        x=0.0,  # Centre horizontalement
        y=0.95,  # Légèrement en dessous du bord supérieur
        xanchor='left', 
        yanchor='top'),)
    fig.update_layout(
        barmode=bar_mode,
        title=titre,
        margin=dict(l=5, r=1, t=30, b=10),
        legend=dict(
            x=0.8,  # Position horizontale (à droite)
            y=1,  # Position verticale (en haut)
            traceorder='normal',
            xanchor='center',  # Alignement horizontal de la légende
            yanchor='top',  # Alignement vertical de la légende
            bgcolor='rgba(255,255,255,0.1)',  # Fond semi-transparent de la légende
        )
    )
    st.plotly_chart(fig)
 
 #4. Fonction pour tracer l'histogramme croisé de deux variables    

#6. Fonction pour tracer graphique type anneau de progression
def make_progress_char(value,couleur="",titre="",width=500, height=300,ecart=50):
    n=int(ecart*value)
    p=ecart-n
    values = [1 for i in range(n+p)]
    col2=["rgba(0, 0, 0, 0.2)" for i in range(p)]
    col1=[f"rgb({255*(1-value)}, {255*value}, 0)" for i in range(n)] if couleur=="" else [couleur for i in range(n)]
    colors = col2 + col1

    fig = go.Figure(data=[go.Pie( values=values,hole=.7, 
                                pull=[0.07 for i in range(n+p)],
                                hoverinfo="none",
                                marker=dict(colors=colors),
                                textinfo='none')],)
    fig.add_trace(go.Pie(
        labels=["labels2","ajcn"],
        values=[13,42],
        hoverinfo="none",
        textinfo='none',
        opacity=0.15,
        #hole=0.75, 
        marker=dict(colors=[couleur,couleur]),
        domain={'x': [0.2, 0.8], 'y': [0.2, 0.8]}
    ))
    fig.update_layout(width=width, height=height,
                        title=dict(
                                    text=titre,
                                    x=0.1,  # Centre horizontalement
                                    y=0.99,  # Légèrement en dessous du bord supérieur
                                    xanchor='left', 
                                    yanchor='top'),
                        showlegend=False,
                        margin=dict(l=0, r=0, t=30, b=10),
                        paper_bgcolor='rgba(248,248,250,0)',
                        plot_bgcolor='rgba(248,248,250,0)',
                        annotations=[dict(text=str(round(100*value,2))+'%', x=0.5, y=0.5,
                        font_size=40, showarrow=False, xanchor="center",font=dict(color="#4b8bff", family="Berlin Sans FB"))])
    st.plotly_chart(fig)
 
#7. Fonction pour tracer graphique type barre de progression version 3    
def make_cross_hist_3(df,var_alpha,var_num,titre,width=500,height=300,bar_mode=1,agregation="count",color="blue",sens='v'):
    bar_mode="relative" if bar_mode==1 else "group"
    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc=agregation, y=df[var_num], x=df[var_alpha], name=var_num,marker=dict(color=color),opacity=0.7))
    fig.update_layout(width=width, height=height, barmode=bar_mode,
                        title=dict(
            text=titre,
            x=0.0,  # Centre horizontalement
            y=0.95,  # Légèrement en dessous du bord supérieur
            xanchor='left', 
            yanchor='top'),)
    fig.update_layout(
            barmode=bar_mode,
            title=titre,
            margin=dict(l=5, r=1, t=30, b=10),
            legend=dict(
                x=0.8,  # Position horizontale (à droite)
                y=1,  # Position verticale (en haut)
                traceorder='normal',
                orientation=sens,  # Orientation verticale
                xanchor='center',  # Alignement horizontal de la légende
                yanchor='top',  # Alignement vertical de la légende
                bgcolor='rgba(255,255,255,0.1)',  # Fond semi-transparent de la légende
            )
        )

    st.plotly_chart(fig)
    
#7. Fonction de test d'indépendance de Khi 2
def test_independance_khi2(df, var1, var2):
    # Création de la table de contingence
    contingency_table = pd.crosstab(df[var1], df[var2])
    index_labels = list(df[var1].unique())
    table_cross = pd.DataFrame(contingency_table, index=index_labels)
    # Application du test Khi-2
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    
    # Conclusion
    if p < 0.05:
        conclusion = f"Le test du Khi-deux rejette/accepte l'hypothèse nulle d'indépendance (ou d'ajustement) à 5% (χ² = {chi2}, p-value = {p}). La statistique calculée excède la critique, indiquant une association significative entre les variables. Au seuil de 10%, la conclusion persiste, consolidant la significativité. L'analyse des résidus standardisés révèle les catégories contribuant majoritairement à la statistique. Les effectifs théoriques étant supérieurs à 5 (conditions de Cochran respectées), l'approximation par la loi χ² reste valide. Ainsi, l'hypothèse d'indépendance est infirmée avec une robustesse confirmée."
    else:
        conclusion = "Les variables sont indépendantes."
    
    
    
    # Retour des résultats
    return  conclusion, table_cross,chi2, p,dof
  
#8. Fonction de test de comparaison de la moyenne
def test_comparaison_moyenne(df, var1, var2):
    # Séparation des groupes
    groupe1 = df[df[var1] == 1]  
    groupe2 = df[df[var1] == 0]
    # Test de Student pour comparer les moyennes
    t_stat, p_value = ttest_ind(groupe1[var2], groupe2[var2])
    # Conclusion
    
    fig=px.histogram(df,x=var2,color=var1,marginal="box",color_discrete_sequence=palette,opacity=0.8)
    if p_value < 0.05:
        result=f"Au seuil de significativité de 5%, l'hypothèse nulle d'égalité des moyennes est rejetée / acceptée (p-value = {p_value}, t = {t_stat}). Cela indique une différence statistiquement significative entre les groupes comparés, avec un risque d'erreur de première espèce contrôlé à 5%. Toutefois, au seuil de 10%, la conclusion demeure robuste, renforçant l'évidence contre l'hypothèse nulle. "
    else:
        result="Les moyennes des deux groupes ne sont pas significativement différentes."
    return result, fig

#9. Fonction d'affichage des métriques version 2
def plot_metric(label, value, prefix="", suffix="", show_graph=False, color_graph=""):
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            value=value,
            gauge={"axis": {"visible": False}},
            number={
                "prefix": prefix,
                "suffix": suffix,
                "font.size": 30,
                "font": {"size": 30, 
                         "family":"Berlin Sans FB"}
            },
            title={
                "text": label,
                "font": {"size": 30, 
                         "family":"Berlin Sans FB"},
            },
        )
    )

    if show_graph:
        fig.add_trace(
            go.Scatter(
                y=random.sample(range(0, 101), 30),
                hoverinfo="skip",
                fill="tozeroy",
                fillcolor=color_graph,
                line={
                    "color": color_graph,
                },
            )
        )

    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        margin=dict(t=0, b=0),
        showlegend=False,
        #plot_bgcolor="white",
        height=100,
        paper_bgcolor='rgba(248,248,250,0)',
        plot_bgcolor='rgba(248,248,250,0)',
    )

    st.plotly_chart(fig, use_container_width=True)

#10. Fonction d'affichage des métriques version 3
def plot_metric_2(label,df,var, prefix="", suffix="", show_graph=False, color_graph="#330C73",val_bin=60):
    fig = go.Figure()
    value=df[var].mean()
    fig.add_trace(
        go.Indicator(
            value=value,
            gauge={"axis": {"visible": False}},
            number={
                "prefix": prefix,
                "suffix": suffix,
                "font.size": 30,
                "font": {"size": 30, 
                         "family":"Berlin Sans FB"}
            },
            title={
                "text": label,
                "font": {"size": 30, 
                         "family":"Berlin Sans FB"},
            },
        )
    )

    if show_graph:
        x_graph=df[var]
        n_bin=(max(x_graph) - min(x_graph)) / val_bin
        fig.add_trace(go.Histogram(x=x_graph,marker_color=color_graph,opacity=0.75, xbins=dict(
                    start=min(x_graph),  # Début des bins
                    end=max(x_graph),    # Fin des bins
                    size=n_bin))
                                )

    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        paper_bgcolor='rgba(248,248,250,0)',
        plot_bgcolor='rgba(248,248,250,0)',
        # paper_bgcolor="lightgrey",
        margin=dict(t=0, b=0),
        showlegend=False,
        #plot_bgcolor="white",
        height=100,
    )

    st.plotly_chart(fig, use_container_width=True)

#10. Fonction pour tracer un demi aneau de progression
def plot_gauge(
    indicator_number, indicator_color, indicator_suffix, indicator_title, max_bound
):
    fig = go.Figure(
        go.Indicator(
            value=indicator_number,
            mode="gauge+number",
            domain={"x": [0, 1], "y": [0, 1]},
            number={
                "suffix": indicator_suffix,
                "font.size": 26,
            },
            gauge={
                "axis": {"range": [0, max_bound], "tickwidth": 1},
                "bar": {"color": indicator_color},
            },
            title={
                "text": indicator_title,
                "font": {"size": 28},
            },
        )
    )
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        height=200,
        margin=dict(l=10, r=10, t=50, b=10, pad=8),
    )
    st.plotly_chart(fig, use_container_width=True)

#11. Fonction pour tracer un heatmap
def make_heat_map(df,vars,oder_var,label_var,titre="",width=500, height=300):
    data_mp = df.groupby(vars).agg({
        oder_var: 'size',
    }).reset_index()
    data_mp=data_mp.rename(columns={oder_var: 'Effectif'})
    path_vars=[px.Constant('All')]+ vars
    fig = px.icicle(data_mp, path=path_vars, values='Effectif',
                    color='Effectif', hover_data=[label_var],
                    color_continuous_scale="sunsetdark")
    fig.update_traces(
        textinfo="label+value",  # Affiche le nom du segment et sa valeur
        textposition="middle center",  # Position du texte au centre des segments
        insidetextfont=dict(color='white', size=12)  # Personnalisation du texte
    )
    fig.update_layout(
            title=titre,
            width=width, height=height,
            margin=dict(l=5, r=1, t=30, b=10),
        )
    st.plotly_chart(fig)

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
            font_size=50, showarrow=False,xanchor='left',font=dict(color=colors[i], family="Berlin Sans FB")) for i in range(len(values))] + 
        [dict(text= labels[i], x=-1, y=i+0.5,
            font_size=30, showarrow=False,xanchor='left',font=dict(color=colors[i], family="Berlin Sans FB")) for i in range(len(values))],
        xaxis=dict(visible=False), 
        yaxis=dict(visible=False),
        margin=dict(l=50, r=20, t=20, b=20),
        paper_bgcolor='rgba(248,248,250,0)',
        plot_bgcolor='rgba(248,248,250,0)',
    )

    st.plotly_chart(fig)

#13. Fonction pour afficher un dataframe personalisé
def make_dataframe(df,col_alpha,col_num,hide_index=False):
    st.dataframe(df,
                 column_order=(col_alpha, col_num),
                 hide_index=hide_index,
                 width=None,
                 column_config={
                    col_alpha: st.column_config.TextColumn(
                        col_alpha,
                    ),
                    col_num: st.column_config.ProgressColumn(
                        col_num,
                        format="%f",
                        min_value=0,
                        max_value=float(df[col_num].max()),
                     )})

#14. Fonction pour tracer la distribution d'un variable quantitative version 1
def make_distribution(df,var_alpha,var_num,add_vline,add_vline2,titre="",width=500, height=300):
    fig = go.Figure()
    valeur=[]
    for i in list(df[var_alpha].unique()):
        df_to_print=df[df[var_alpha]==i]
        moy=float(df_to_print[var_num].mean())
        ecart=float(df_to_print[var_num].std()/4)**(1/300)
        occurrences_mode = df_to_print[(df_to_print[var_num]<=moy+ecart) & (df_to_print[var_num]>=moy-ecart)].shape[0]
        valeur=valeur+[occurrences_mode]
        fig.add_trace(go.Histogram(x=df_to_print[var_num],name=i,opacity=0.7))
        #fig.add_trace(go.Histogram(x=x1))

    # The two histograms are drawn on top of another
    fig.add_shape(
        type="line",  # Type de forme: ligne
        x0=add_vline,        # Position de départ sur l'axe x
        x1=add_vline,        # Position de fin sur l'axe x (identique pour une droite verticale)
        y0=0,         # Position de départ sur l'axe y
        y1=40,         # Position de fin sur l'axe y (selon l'échelle de ton graphique)
        line=dict(color="green", width=2)  # Style de la ligne
    )
    
    fig.add_shape(
        type="line",  # Type de forme: ligne
        x0=add_vline2,        # Position de départ sur l'axe x
        x1=add_vline2,        # Position de fin sur l'axe x (identique pour une droite verticale)
        y0=0,         # Position de départ sur l'axe y
        y1=40,         # Position de fin sur l'axe y (selon l'échelle de ton graphique)
        line=dict(color="green", width=2))
    fig.update_layout(barmode='stack',xaxis=dict(visible=True), 
        yaxis=dict(visible=True),)
    fig.update_layout(margin=dict(l=5, r=1, t=30, b=10),
                      paper_bgcolor='rgba(248,248,250,0)',
                      plot_bgcolor='rgba(248,248,250,0)',
                      width=width, height=height,
                    title=dict(
        text=titre,
        x=0.0,  
        y=0.95, 
        xanchor='left', 
        yanchor='top'),
            legend=dict(
            x=0.8,  # Position horizontale (à droite)
            y=1,  # Position verticale (en haut)
            traceorder='normal',
            xanchor='center',  # Alignement horizontal de la légende
            yanchor='top',  # Alignement vertical de la légende
            bgcolor='rgba(255,255,255,0.1)',  # Fond semi-transparent de la légende
        ))
    fig.update_xaxes(title_text=var_num)  # Titre de l'axe X
    fig.update_yaxes(title_text="Effectif")
    st.plotly_chart(fig)

#16. Fonction pour afficher un nuage de mot 
def make_wordcloud(texte,titre="",width=800, height=400):
    mot=texte.split(" ")
    mots_exclus = ["de", "à", "et"," et", "et "," de","de "," et "," de ","NON"," ","pas", "les"]
    mot = [m for m in mot if m not in mots_exclus]
    # Génération du nuage de mots
    wordcloud = WordCloud(width=width, height=height, background_color="white", colormap="viridis").generate(texte)
    # Sauvegarde de l'image en mémoire
    img = io.BytesIO()
    wordcloud.to_image().save(img, format='PNG')
    img.seek(0)
    # Convertir en tableau numpy pour Plotly
    img_array = np.array(Image.open(img))
    # Affichage avec Plotly
    fig = px.imshow(img_array)
    fig.update_layout(
        title=titre,
        margin=dict(l=1, r=1, t=30, b=10),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    st.plotly_chart(fig)
 
 #13. Fonction pour afficher un dataframe personalisé   

#17. Fonction pour afficher un double anneau de progression 
def make_dbl_progress_char(labels,vars,colors,titre="",width=500, height=300,n_secteur=50):
    # Données pour l'anneau externe
    labels2 = ["a"+str(i) for i in range(n_secteur)]
    sizes_2 = [1 for i in range(n_secteur)]
    labels_1= ["b"+str(i) for i in range(n_secteur + 10)]
    sizes_1 = [1 for i in range(n_secteur + 10)] 
    lab1=labels[0]
    lab2=labels[1]
    val1=vars[0]
    val2=vars[1]
    col1=colors[0]
    col2=colors[1]
    fig = go.Figure()
    # Ajout de l'anneau externe
    fig.add_trace(go.Pie(
        labels=labels2,
        values=sizes_2,
        pull=[0.1 for i in range(n_secteur)],
        hoverinfo="none",
        textinfo='none',
        hole=0.75, 
        marker=dict(colors=["rgba(0, 0, 0, 0.2)" for i in range(n_secteur-(int(n_secteur*val2)))] + [col2 for i in range(int(n_secteur*val2))]),
        domain={'x': [0.1, 0.9], 'y': [0.1, 0.9]}
    ))

    # Ajout de l'anneau interne
    fig.add_trace(go.Pie(
        labels=labels_1,
        values=sizes_1,
        pull=[0.1 for i in range(n_secteur +10)],
        hoverinfo="none",
        textinfo='none',
        hole=0.8, 
        marker=dict(colors= ["rgba(0, 0, 0, 0.2)" for i in range(n_secteur-(int((n_secteur+10)*val1)) + 10)] + [col1 for i in range(int((n_secteur+10)*val1))]),
        domain={'x': [0, 1], 'y': [0, 1]}
    ))

    # Mise en forme
    fig.update_layout(
        title=dict(text=titre,
                        x=0.1,  # Centre horizontalement
                        y=0.99,  # Légèrement en dessous du bord supérieur
                        xanchor='left', 
                        yanchor='top'),
        width=width, 
        height=height,
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=10),
        paper_bgcolor='rgba(248,248,250,0)',
        plot_bgcolor='rgba(248,248,250,0)',
        annotations=[dict(text= str(round(100*val2,2))+'%', x=0.5, y=0.25,
        font_size=30, showarrow=False, xanchor="center",font=dict(color=col2, family="Berlin Sans FB")),
                    dict(text=str(round(100*val1,2))+'%', x=0.5, y=0.6,
        font_size=30, showarrow=False, xanchor="center",font=dict(color=col1, family="Berlin Sans FB")),
                    dict(text=lab1, x=0.5, y=0.75,
        font_size=25, showarrow=False, xanchor="center",font=dict(color=col1, family="Berlin Sans FB")),
                    dict(text=lab2, x=0.5, y=0.4,
        font_size=25, showarrow=False, xanchor="center",font=dict(color=col2, family="Berlin Sans FB"))]
    )

    # Affichage
    st.plotly_chart(fig)

#18. Fonction pour afficher une carte chlorophete version 1: avec plotly   
def make_chlorophet_map_2(df, style_carte="carto-positron", palet_color="Blues", opacity=0.8, width=700, height=600):
    """
    Fonction pour créer une carte choroplèthe interactive montrant la distribution des candidats
    par statut d'éligibilité à travers différents quartiers et arrondissements.
    
    Parameters:
    -----------
    df : GeoDataFrame
        DataFrame contenant les données géospatiales des candidats
    style_carte : str, default="carto-positron"
        Style de fond de carte Mapbox (options: "carto-positron", "carto-darkmatter", "open-street-map", etc.)
    palet_color : str, default="Blues"
        Palette de couleurs pour la choroplèthe (options: "Blues", "Reds", "Greens", "Viridis", etc.)
    opacity : float, default=0.8
        Opacité des polygones de la choroplèthe (0-1)
    width : int, default=900
        Largeur de la carte en pixels
    height : int, default=600
        Hauteur de la carte en pixels
    """
    # Définition des catégories d'éligibilité et des couleurs associées
    eligibility_categories = {
        "Eligible": {"color": "#0073E6", "size_factor": 27, "opacity": 0.75},
        "Temporairement Non-eligible": {"color": "#B3D9FF", "size_factor": 17, "opacity": 0.7},
        "Définitivement non-eligible": {"color": "#FF5733", "size_factor": 10, "opacity": 0.7}
    }
    
    # Préparation des données par statut d'éligibilité
    dfs_by_eligibility = {}
    for category in eligibility_categories.keys():
        geo_data = df[df["Eligibilite"] == category]
        
        if not geo_data.empty:
            dfs_by_eligibility[category] = geo_data.groupby("Quartier").agg({
                'Quartier': 'size',
                'Lat': 'first',
                'Long': 'first'
            }).rename(columns={'Quartier': 'nb_donateur'})
            dfs_by_eligibility[category]["Qrt"] = dfs_by_eligibility[category].index

    # Préparation des données pour la choroplèthe par arrondissement
    df_chlph = df.groupby("Arrondissement").agg({
        'Arrondissement': 'size',
        'geometry': 'first',
        'Long': 'first',
        'Lat': 'first'
    }).rename(columns={'Arrondissement': 'nb_donateur'})
    df_chlph["Arr"] = df_chlph.index
    df_chlph = gpd.GeoDataFrame(df_chlph, geometry='geometry')

    # Total des candidats par quartier
    df_pts = df.groupby("Quartier").agg({
        'Quartier': 'size',
        'Lat': 'first',
        'Long': 'first'
    }).rename(columns={'Quartier': 'nb_donateur'})
    df_pts["Qrt"] = df_pts.index
    
    # Création de la figure
    fig = go.Figure()
    
    # Ajout de la couche choroplèthe pour les arrondissements
    fig.add_trace(go.Choroplethmapbox(
        geojson=df_chlph.geometry.__geo_interface__,
        locations=df_chlph.index,
        z=df_chlph["nb_donateur"],
        colorscale=palet_color,
        marker_opacity=opacity,
        marker_line_width=0.5,
        marker_line_color='white',  # Bordure blanche pour meilleure délimitation
        colorbar=dict(
            title="Nombre de Candidats",
            thickness=15,
            len=0.7,
            x=0.95,
            y=0.5,
        ),
        hovertext=df_chlph['Arr'],
        hovertemplate="<b>%{hovertext}</b><br>Nombre de candidats: %{z}<extra></extra>",
        name="Arrondissements",
    ))
    
    # Ajout des étiquettes d'arrondissement
    fig.add_trace(go.Scattermapbox(
        lat=df_chlph["Lat"],
        lon=df_chlph["Long"],
        mode='text',
        text=df_chlph["Arr"],
        textfont=dict(
            size=12,
            color="black",
            family="Arial Bold"
        ),
        hoverinfo='none',
        name="Labels"
    ))

    # Ajout des marqueurs pour le total des candidats
    fig.add_trace(go.Scattermapbox(
        lat=df_pts["Lat"],
        lon=df_pts["Long"],
        mode='markers',
        name="Total candidats",
        marker=dict(
            size=df_pts["nb_donateur"],
            sizemode='area',
            sizeref=2. * max(df_pts["nb_donateur"]) / (45.**2),
            color='#003F80',
            opacity=0.8
            # Suppression de line=dict(width=1, color='white') qui n'est pas supporté
        ),
        hovertemplate=(
            "<b>%{text}</b><br>"
            "Total candidats: <b>%{marker.size}</b><extra></extra>"
        ),
        text=df_pts["Qrt"]
    ))
    
    # Ajout des marqueurs pour chaque catégorie d'éligibilité
    for category, df_pts_cat in dfs_by_eligibility.items():
        config = eligibility_categories[category]
        fig.add_trace(go.Scattermapbox(
            lat=df_pts_cat["Lat"],
            lon=df_pts_cat["Long"],
            mode='markers',
            name=category,
            marker=dict(
                size=df_pts_cat["nb_donateur"],
                sizemode='area',
                sizeref=2. * max(df_pts_cat["nb_donateur"]) / (config["size_factor"]**2),
                color=config["color"],
                opacity=config["opacity"]
                # Suppression de line=dict(width=1, color='white') qui n'est pas supporté
            ),
            hovertemplate=(
                "<b>%{text}</b><br>"
                f"Candidats {category}: <b>%{{marker.size}}</b><extra></extra>"
            ),
            text=df_pts_cat["Qrt"]
        ))
    
    # Optimisation de la mise en page
    fig.update_layout(
        title=dict(
            text="Distribution des Candidats par Éligibilité",
            font=dict(size=20, family="Arial", color="#333"),
            x=0.5,
            y=0.98
        ),
        showlegend=True,
        legend=dict(
            x=0.01,
            y=0.01,
            bgcolor="rgba(255, 255, 255, 0.2)",
            bordercolor="#ddd",
            borderwidth=1,
            orientation='v',
            itemsizing='constant',
            font=dict(family="Arial", size=12,color="black")
        ),
        mapbox=dict(
            style=style_carte,
            center=dict(lat=df_pts["Lat"].mean(), lon=df_pts["Long"].mean()),
            zoom=10.5,
            accesstoken=None  # À définir si vous utilisez un token Mapbox
        ),
        margin=dict(l=1, r=1, t=10, b=1),
        width=width,
        height=height,
        paper_bgcolor='white',
        autosize=True,
    )

    # Affichage avec Streamlit
    st.plotly_chart(fig, use_container_width=True)

#19. Fonction pour afficher une carte chlorophete version 2: avec folium
def make_chlorophet_map_folium_2(df, style_carte="OpenStreetMap", palet_color="blues", opacity=0.8, width=700, height=600):
    """
    Fonction pour créer une carte choroplèthe interactive montrant la distribution des candidats
    par statut d'éligibilité à travers différents quartiers et arrondissements, en utilisant Folium.
    
    Parameters:
    -----------
    df : GeoDataFrame
        DataFrame contenant les données géospatiales des candidats
    style_carte : str, default="OpenStreetMap"
        Style de fond de carte Folium (options: "OpenStreetMap", "cartodbpositron", "cartodbdark_matter", etc.)
    palet_color : str, default="Blues"
        Palette de couleurs pour la choroplèthe (options: "Blues", "Reds", "Greens", "YlOrRd", etc.)
    opacity : float, default=0.8
        Opacité des polygones de la choroplèthe (0-1)
    width : int, default=700
        Largeur de la carte en pixels
    height : int, default=600
        Hauteur de la carte en pixels
    """
    
    
    # Nettoyer les données en supprimant les lignes avec des coordonnées NaN
    df_clean = df.dropna(subset=['Lat', 'Long']).copy()
    
    # Définition des catégories d'éligibilité et des couleurs associées
    eligibility_categories = {
        "Eligible": {"color": "#0073E6", "size_factor": 12, "opacity": 0.75},
        "Temporairement Non-eligible": {"color": "#B3D9FF", "size_factor": 8, "opacity": 0.7},
        "Définitivement non-eligible": {"color": "#FF5733", "size_factor": 4, "opacity": 0.7}
    }
    
    # Préparation des données par statut d'éligibilité
    dfs_by_eligibility = {}
    for category in eligibility_categories.keys():
        geo_data = df_clean[df_clean["Eligibilite"] == category]
        
        if not geo_data.empty:
            dfs_by_eligibility[category] = geo_data.groupby("Quartier").agg({
                'Quartier': 'size',
                'Lat': 'first',
                'Long': 'first'
            }).rename(columns={'Quartier': 'nb_donateur'})
            dfs_by_eligibility[category]["Qrt"] = dfs_by_eligibility[category].index
            # S'assurer qu'il n'y a pas de NaN dans les coordonnées agrégées
            dfs_by_eligibility[category] = dfs_by_eligibility[category].dropna(subset=['Lat', 'Long'])

    # Préparation des données pour la choroplèthe par arrondissement
    df_chlph = df_clean.groupby("Arrondissement").agg({
        'Arrondissement': 'size',
        'geometry': 'first',
        'Long': 'first',
        'Lat': 'first'
    }).rename(columns={'Arrondissement': 'nb_donateur'})
    df_chlph["Arr"] = df_chlph.index
    # S'assurer qu'il n'y a pas de NaN dans les coordonnées agrégées
    df_chlph = df_chlph.dropna(subset=['Lat', 'Long'])
    df_chlph = gpd.GeoDataFrame(df_chlph, geometry='geometry')
    
    # S'assurer que le CRS est défini - Utiliser EPSG:4326 (WGS84) pour compatibilité avec Folium
    if df_chlph.crs is None:
        df_chlph.set_crs(epsg=4326, inplace=True)
    else:
        # Si un CRS est déjà défini mais différent de WGS84, le convertir
        if df_chlph.crs != 'EPSG:4326':
            df_chlph = df_chlph.to_crs(epsg=4326)

    # Total des candidats par quartier
    df_pts = df_clean.groupby("Quartier").agg({
        'Quartier': 'size',
        'Lat': 'first',
        'Long': 'first'
    }).rename(columns={'Quartier': 'nb_donateur'})
    df_pts["Qrt"] = df_pts.index
    # S'assurer qu'il n'y a pas de NaN dans les coordonnées agrégées
    df_pts = df_pts.dropna(subset=['Lat', 'Long'])
    
    # Vérifier si df_pts est vide après filtrage
    if df_pts.empty:
        st.error("Aucune coordonnée valide trouvée dans les données. Impossible de créer la carte.")
        return None
    
    # Création de la carte Folium
    center_lat = df_pts["Lat"].mean()
    center_lon = df_pts["Long"].mean()
    
    # Dictionnaire de correspondance entre les styles dans votre fonction originale et ceux de Folium
    tile_styles = {
        "carto-positron": "cartodbpositron",
        "carto-darkmatter": "cartodbdark_matter",
        "open-street-map": "OpenStreetMap",
        "CartoDB positron": "cartodbpositron", 
        "CartoDB dark_matter": "cartodbdark_matter"
    }
    
    # Utiliser le style approprié ou OpenStreetMap par défaut
    actual_style = tile_styles.get(style_carte, style_carte)
    
    # Création de la carte avec le style approprié
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles=actual_style,
        width=width,
        height=height
    )
    
    # Ajout de la couche choroplèthe pour les arrondissements
    # Création d'une échelle de couleur avec la bonne classe de branca.colormap
    if palet_color == "blues":
        color_range = ['#f7fbff', '#08519c']
    elif palet_color == "reds":
        color_range = ['#fee5d9', '#a50f15']
    elif palet_color == "greens":
        color_range = ['#edf8e9', '#006d2c']
    elif palet_color == "viridis":
        color_range = ['#fde725', '#440154']
    else:
        color_range = ['#f7fbff', '#08519c']  # Default to Blues
    
    # Création des clusters uniquement pour les arrondissements
    arrondissement_cluster = MarkerCluster(name="Arrondissements").add_to(m)
    
    if not df_chlph.empty:
        colormap = cm.LinearColormap(
            colors=color_range, 
            vmin=df_chlph["nb_donateur"].min(),
            vmax=df_chlph["nb_donateur"].max(),
            caption="Nombre de Candidats par Arrondissement"
        )
        
        # Convertir le GeoDataFrame en GeoJSON
        geo_json_data = df_chlph.__geo_interface__
        
        # Ajout des polygones des arrondissements en utilisant le GeoJSON préparé
        folium.GeoJson(
            geo_json_data,
            style_function=lambda feature: {
                'fillColor': colormap(feature['properties']['nb_donateur']),
                'color': 'white',
                'weight': 0.5,
                'fillOpacity': opacity
            },
            tooltip=folium.GeoJsonTooltip(
                fields=['Arr', 'nb_donateur'],
                aliases=['Arrondissement:', 'Nombre de candidats:'],
                style="background-color: white; color: #333333; font-family: arial; font-size: 14px; padding: 10px;"
            )
        ).add_to(m)
        
        # Ajout des étiquettes d'arrondissement et des marqueurs au cluster d'arrondissements
        for idx, row in df_chlph.iterrows():
            # Étiquettes d'arrondissement
            folium.Marker(
                location=[row['Lat'], row['Long']],
                icon=folium.DivIcon(
                    icon_size=(150, 40),
                    icon_anchor=(75, 28),
                    html=f'<div style="font-size: 12px; font-weight: bold; text-align: center">{row["Arr"]}</div>'
                )
            ).add_to(m)
            
            # Marqueurs d'arrondissement pour le cluster
            folium.Marker(
                location=[row['Lat'], row['Long']],
                popup=f"<b>Arrondissement {row['Arr']}</b><br>Total candidats: <b>{row['nb_donateur']}</b>",
                icon=folium.Icon(color='blue')
            ).add_to(arrondissement_cluster)
        
        # Ajout de la légende de couleur
        colormap.add_to(m)

    # Fonction pour calculer la taille du cercle en fonction du nombre de candidats
    def calculate_radius(count, max_count, base_size=5):
        return base_size * np.sqrt(count / max_count * 100)
    
    max_count = df_pts["nb_donateur"].max() if not df_pts.empty else 1
    
    # Création d'un groupe de features pour les cercles des quartiers
    quartier_feature_group = folium.FeatureGroup(name="Total candidats par quartier")
    
    # Ajout des marqueurs pour le total des candidats (directement à la carte, pas de cluster)
    for idx, row in df_pts.iterrows():
        radius = calculate_radius(row["nb_donateur"], max_count)
        popup_text = f"<b>{row['Qrt']}</b><br>Total candidats: <b>{row['nb_donateur']}</b>"
        
        folium.CircleMarker(
            location=[row['Lat'], row['Long']],
            radius=radius,
            color='#003F80',
            fill=True,
            fill_color='#003F80',
            fill_opacity=0.8,
            popup=folium.Popup(popup_text, max_width=300)
        ).add_to(quartier_feature_group)
    
    # Ajout du groupe de features à la carte
    quartier_feature_group.add_to(m)
        
    # Ajout des marqueurs pour chaque catégorie d'éligibilité (directement à la carte, pas de cluster)
    for category, df_pts_cat in dfs_by_eligibility.items():
        if df_pts_cat.empty:
            continue
            
        config = eligibility_categories[category]
        
        # Création d'un groupe de features pour cette catégorie
        category_feature_group = folium.FeatureGroup(name=category)
        
        max_count_cat = df_pts_cat["nb_donateur"].max() if not df_pts_cat.empty else 1
        
        for idx, row in df_pts_cat.iterrows():
            radius = calculate_radius(row["nb_donateur"], max_count_cat, base_size=config["size_factor"]/4)
            popup_text = f"<b>{row['Qrt']}</b><br>Candidats {category}: <b>{row['nb_donateur']}</b>"
            
            folium.CircleMarker(
                location=[row['Lat'], row['Long']],
                radius=radius,
                color=config["color"],
                fill=True,
                fill_color=config["color"],
                fill_opacity=config["opacity"],
                popup=folium.Popup(popup_text, max_width=300)
            ).add_to(category_feature_group)
        
        # Ajout du groupe de features à la carte
        category_feature_group.add_to(m)
            
    # Ajout du contrôle de couches
    folium.LayerControl(collapsed=False).add_to(m)
    
    # Ajout d'une légende pour les cercles des points
    legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; right: 50px; 
                    width: 220px;
                    background-color: white;
                    border: 2px solid grey;
                    border-radius: 5px;
                    z-index: 9999;
                    font-size: 14px;
                    padding: 10px;
                    opacity: 0.9;">
            <div style="text-align: center; margin-bottom: 5px;"><b>Légende des points</b></div>
    '''
    
    # Ajouter une entrée de légende pour les cercles totaux
    legend_html += f'''
        <div style="margin-bottom: 7px;">
            <div style="display: inline-block; 
                      width: 15px; 
                      height: 15px; 
                      border-radius: 50%; 
                      background-color: #003F80;
                      margin-right: 5px;
                      vertical-align: middle;"></div>
            <span style="vertical-align: middle;">Total candidats</span>
        </div>
    '''
    
    # Ajouter des entrées pour chaque catégorie d'éligibilité
    for category, config in eligibility_categories.items():
        if category in dfs_by_eligibility and not dfs_by_eligibility[category].empty:
            legend_html += f'''
                <div style="margin-bottom: 7px;">
                    <div style="display: inline-block; 
                              width: 15px; 
                              height: 15px; 
                              border-radius: 50%; 
                              background-color: {config['color']};
                              opacity: {config['opacity']};
                              margin-right: 5px;
                              vertical-align: middle;"></div>
                    <span style="vertical-align: middle;">{category}</span>
                </div>
            '''
    
    # Fermer la div de la légende
    legend_html += '</div>'
    
    # Ajouter la légende à la carte
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Ajout d'un titre 
    title_html = '''
        <div style="position: fixed; 
                    top: 10px; left: 50px; width: 600px; height: 45px; 
                    background-color: white; border-radius: 5px;
                    z-index: 9999; font-size: 20px; font-family: Arial;
                    padding: 10px; text-align: center; color: #333;">
            <b>Distribution des Candidats par Éligibilité</b>
        </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Affichage avec Streamlit
    folium_static(m, width=width, height=height)
    
    return m

#20. Fonction pour afficher histogramme croisé version 4
def make_cross_hist_b(df, var1, var2, titre="", typ_bar=1, width=800, height=500, sens="v", 
                    palette=None, show_legend=True,bordure=None):
    """
    Crée un histogramme croisé optimisé pour les données de campagne de don de sang.
    
    Args:
        df: DataFrame contenant les données
        var1: Variable pour grouper (apparaîtra dans la légende)
        var2: Variable pour l'axe des x/y selon l'orientation
        titre: Titre du graphique
        typ_bar: 1 pour empilé, 2 pour groupé
        width: Largeur du graphique
        height: Hauteur du graphique
        sens: Orientation - "v" (vertical) ou "h" (horizontal)
        palette: Liste de couleurs personnalisée (si None, utilise la palette de don de sang par défaut)
        show_legend: Afficher ou masquer la légende
        bordure: pour les bordure
        
    Returns:
        Affiche le graphique dans Streamlit
    """
    # Définition des couleurs pour le thème don de sang si non spécifiées
    if palette is None:
        # Palette de couleurs orientée sang (rouge) et médical (bleu) #FDC7D3,
        palette = ['#FDC7D3', '#F61A49', '#640419', '#49030D', '#4575B4', '#74ADD1', '#ABD9E9', '#E0F3F8']  # nuances de bleu
    
    bar_mode = "relative" if typ_bar == 1 else "group"
    
    # Création du tableau croisé et formatage
    cross_df = pd.crosstab(df[var1], df[var2])
    table_cross = cross_df.reset_index().melt(id_vars=var1, var_name=var2, value_name='Effectif')
    table_cross = table_cross.sort_values("Effectif", ascending=False)
    
    # Déterminer les axes selon l'orientation
    x_axis = var2 if sens == "v" else 'Effectif'
    y_axis = var1 if sens == "h" else 'Effectif'
    color_clust=var2 if sens=="h" else var1
    # Création du graphique avec une meilleure disposition
    fig = px.bar(table_cross, 
                 x=x_axis, 
                 y=y_axis, 
                 color=color_clust, 
                 text_auto=True,  # Affiche automatiquement les valeurs
                 barmode=bar_mode,
                 orientation=sens,
                 color_discrete_sequence=palette
                 )
                 
    # Améliorations stylistiques
    fig.update_layout(barcornerradius=bordure,
        width=width, 
        height=height,
        paper_bgcolor='rgba(248,248,250,0)',  # Fond légèrement grisé pour le graphique
        plot_bgcolor='rgba(248,248,250,0)',   # Fond légèrement grisé pour les axes
        title={
            'text': f"<b>{titre}</b>",
            'x': 0.5,  # Centrer le titre
            'y': 1,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 22, 'family': 'Arial, sans-serif'}
        },
        margin=dict(l=1, r=5, t=20, b=5),  # Marges plus généreuses
        legend={
            #'title': var1,
            'orientation': 'h',              # Légende horizontale
            'y': 0.9,                      # Position sous le graphique
            'x': 0.8,
            'xanchor': 'center',
            'yanchor': 'top',
            'bgcolor': 'rgba(255,255,255,0)',
            'bordercolor': 'rgba(0,0,0,0)',
            'borderwidth': 1,
            'font': police_label
        } if show_legend else None
    )
    
    # Amélioration des axes et des annotations
    fig.update_xaxes(
        showgrid=True,
        gridwidth=0.5,
        gridcolor='rgba(211,211,211,0)',
        title_font=police_label,
        tickfont=police_label
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=0.5,
        gridcolor='rgba(211,211,211,0)',
        title_font={'size': 14},
        tickfont=police_label
    )
    
    # Amélioration des barres et du texte
    fig.update_traces(
        textfont_size=20,
        textposition='auto',
        marker_line_width=0.5,
        marker_line_color='rgba(0,0,0,0.3)',
    )
    
    # Affichage dans Streamlit
    st.plotly_chart(fig, use_container_width=True)

#21. Fonction pour afficher un heatmap version 2
def make_heat_map_2(df, vars, order_var, label_var, titre="", width=500, height=300, 
                   color_scale=None, show_titles=True, text_size=12):
    """
    Crée un diagramme en cascade (icicle chart) optimisé pour visualiser les données
    hiérarchiques de campagne de don de sang.
    
    Args:
        df: DataFrame contenant les données
        vars: Liste des variables pour la hiérarchie
        order_var: Variable à utiliser pour calculer les effectifs
        label_var: Variable à afficher dans les info-bulles
        titre: Titre du graphique
        width: Largeur du graphique
        height: Hauteur du graphique
        color_scale: Échelle de couleurs personnalisée (si None, utilise une échelle du bleu au rouge)
        show_titles: Afficher les titres des axes
        text_size: Taille du texte dans les segments
        
    Returns:
        Affiche le graphique dans Streamlit
    """
    # Création du dataframe agrégé pour le graphique
    data_mp = df.groupby(vars).agg({
        order_var: 'size',
    }).reset_index()
    data_mp = data_mp.rename(columns={order_var: 'Effectif'})
    
    # Ajout d'une colonne de pourcentage pour l'affichage
    total = data_mp['Effectif'].sum()
    data_mp['Pourcentage'] = (data_mp['Effectif'] / total * 100).round(1)
    
    # Définir une échelle de couleurs allant du bleu au rouge foncé si non spécifiée
    if color_scale is None:
        # Du bleu clair au rouge foncé
        color_scale = ["#EFF3FF", "#C6DBEF", "#9ECAE1", "#6BAED6", "#4292C6", "#2171B5", 
                       "#FEE0D2", "#FCBBA1", "#FC9272", "#FB6A4A", "#EF3B2C", "#CB181D", "#A50F15", "#67000D"]
    
    # Créer le chemin hiérarchique avec 'All' comme racine
    path_vars = [px.Constant('Tous les donneurs')] + vars
    # Création du graphique avec des paramètres améliorés
    fig = px.icicle(
        data_mp, 
        path=path_vars, 
        values='Effectif',
        color='Effectif', 
        hover_data=['Pourcentage', label_var],
        color_continuous_scale=color_scale,
        branchvalues='total'  # S'assure que les valeurs sont correctement agrégées
    )
    
    # Amélioration de l'apparence des segments
    fig.update_traces(
        textinfo="label+value",         # Affiche le nom du segment et sa valeur
        texttemplate='%{label}<br>%{value} donneurs',  # Format personnalisé
        textposition="middle center",   # Position du texte au centre des segments
        insidetextfont=dict(
            color='black',              # Couleur de texte de base
            size=text_size,             # Taille du texte ajustable
            family="Arial, sans-serif"  # Police plus moderne
        ),
        outsidetextfont=dict(
            color='black',
            size=text_size,
            family="Arial, sans-serif"
        ),
        marker=dict(
            line=dict(width=1, color='rgba(255,255,255,0)')  # Bordure fine pour distinguer les segments
        ),
        hovertemplate='<b>%{label}</b><br>Effectif: %{value} donneurs<br>Pourcentage: %{customdata[0]}%<br>%{customdata[1]}<extra></extra>'
    )
    
    # Amélioration de la mise en page générale
    fig.update_layout(
        title={
            'text': f"<b>{titre}</b>" if titre else "",
            'x': 0.5,
            'y': 1,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20,  'family': 'Arial, sans-serif'}
        },
        width=width, 
        height=height,
        margin=dict(l=2, r=2, t=8, b=2),
        paper_bgcolor='rgba(248,248,250,0)',  # Fond légèrement grisé
        coloraxis_colorbar=dict(
            title={
                'text': "Nombre de<br>donneurs",
                'font': police_label
            },
            tickfont=police_label,
            len=0.6,                  # Longueur de la barre de couleur
            thickness=15,             # Épaisseur de la barre de couleur
            x=0.95                    # Position horizontale
        )
    )
    
    # Ajuster le texte en fonction des valeurs
    # Les petits segments auront un texte blanc pour contraster avec les couleurs foncées
    for i in range(len(fig.data)):
        # Vérification corrigée pour éviter l'erreur de valeur de vérité ambiguë
        has_values = hasattr(fig.data[i], 'values')
        has_labels = hasattr(fig.data[i], 'labels')
        
        if has_values and has_labels:
            values = fig.data[i].values
            
            # Assurez-vous que values est non vide avant de continuer
            if len(values) > 0:
                text_colors = []
                for val in values:
                    # Pour les segments plus petits, utiliser du blanc pour le contraste
                    if val < total * 0.05:  # Seuil de 5% du total
                        text_colors.append('white')
                    else:
                        text_colors.append('black')
                
                fig.data[i].insidetextfont.color = text_colors
    
    # Affichage dans Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    return fig  # Retourne le graphique pour référence ultérieure

#22. Fonction pour afficher un anneau
def make_donutchart(df, var, titre="", width=600, height=450, color_palette=None,part=True):
    """
    Crée un graphique en anneau (donut chart) avec des améliorations visuelles.
    
    Args:
        df: DataFrame contenant les données
        var: Variable à visualiser
        titre: Titre du graphique
        width: Largeur du graphique
        height: Hauteur du graphique
        color_palette: Liste de couleurs personnalisées pour le graphique
        
    Returns:
        Affiche le graphique dans Streamlit
    """
    # Agrégation des données
    data_grouped = df.groupby(var).size().reset_index(name='Effectif')
    
    # Calculer les pourcentages pour l'affichage dans les étiquettes
    total = data_grouped['Effectif'].sum()
    data_grouped['Pourcentage'] = (data_grouped['Effectif'] / total * 100).round(1)
    
    # Trier par effectif décroissant pour une meilleure présentation
    data_grouped = data_grouped.sort_values('Effectif', ascending=False)
    
    
    # Construction du graphique
    fig = go.Figure()
    
    # Ajout du graphique en anneau
    fig.add_trace(go.Pie(
        labels=data_grouped[var], 
        values=data_grouped['Effectif'],
        textinfo='label+percent',
        textposition='inside',
        texttemplate='%{label}<br>%{percent}',
        hovertemplate='<b>%{label}</b><br>Effectif: %{value} (%{percent})<extra></extra>',
        hole=0.5,
        pull=[0.03 if (i == 0) & (len(data_grouped)>2)  else 0 for i in range(len(data_grouped))],  # Léger détachement du plus grand segment
        marker=dict(
            colors=palette,
            #line=dict(color='white', width=2)
        ),
        rotation=0,  # Rotation pour un meilleur positionnement des étiquettes
        sort=False  ,  # Respecter l'ordre du tri effectué
        textfont=police_label
        
    ))
    
    # Ajout du nombre total au centre du donut
    fig.add_annotation(
        text=f"{total:,}<br>Total",
        x=0.5, y=0.5,
        font=police,
        showarrow=False
    )
    
    # Optimisation de la mise en page
    fig.update_layout(
        title={
            'text': f"<b>{titre}</b>" if titre else "",
            'x': 0.5,
            'y': 1,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=18)
        },
        width=width,
        height=height,
        margin=dict(l=3, r=3, t=12, b=2),
        paper_bgcolor='rgba(248,248,250,0)',  # Fond légèrement grisé
        legend=dict(
            orientation='h',           # Disposition horizontale
            yanchor='bottom',
            y=-0.15,                   # Position sous le graphique
            xanchor='center',
            x=0.5,                     # Centré
            font=dict(size=16),
            bgcolor='rgba(255,255,255,0)',
            bordercolor='rgba(0,0,0,0)',
            borderwidth=1
        ),
        uniformtext=dict(
            minsize=15,
            #mode='hide'                # Cache le texte s'il est trop petit pour s'adapter
        )
    )
    
    # Affichage dans Streamlit avec option de largeur adaptative
    st.plotly_chart(fig, use_container_width=True)
    
    return fig  # Retourne le graphique pour référence ultérieure

#23. Fonction pour afficher un diagpramme barre simple
def make_bar(df, var, color=1, titre="", titre_x="", titre_y="", width=500, height=300, ordre=2, sens='v',bordure=None):
    """
    Crée un graphique à barres amélioré avec un style professionnel.
    
    Args:
        df: DataFrame contenant les données
        var: Variable à regrouper
        color: Couleur(s) pour les barres
        titre: Titre du graphique
        titre_x: Titre de l'axe X
        titre_y: Titre de l'axe Y
        width: Largeur du graphique
        height: Hauteur du graphique
        ordre: Tri (1=ascendant, 2=aucun, autre=descendant)
        sens: Orientation - "v" (vertical) ou "h" (horizontal)
    """
    # Agrégation des données
    ID=df.columns[0] if "ID" not in df.columns else "ID"
    data_plot = df.groupby(var).agg({ID: "size"})
    # Tri selon le paramètre ordre
    data_plot=data_plot.rename(columns={ID:"Effectif"})
    if ordre != 2:
        data_plot = data_plot.sort_values("Effectif", ascending=(ordre == 1))
    # Définition des axes selon l'orientation
    x_axis = data_plot.index if sens == 'v' else "Effectif"
    y_axis = "Effectif" if sens == 'v' else data_plot.index
    
    # Création du graphique
    fig = px.bar(
        data_plot, 
        x=x_axis, 
        y=y_axis, 
        text="Effectif",
        color_discrete_sequence=val_couleur[color],
        orientation=sens,
        
    )
    # Configuration des étiquettes de texte
    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        textfont=police_label,
        marker_line_width=0.5,
        marker_line_color='rgba(0, 0, 0, 0)',
    )
    # Mise en page améliorée
    fig.update_layout(barcornerradius=bordure,
        title={
            'text': f"<b>{titre}</b>" if titre else "",
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': police_label
        },
        width=width,
        height=height,
        margin=dict(l=10, r=10, t=50, b=10 if sens == 'v' else 80),
        paper_bgcolor='rgba(248, 248, 250, 0)',
        plot_bgcolor='rgba(248, 248, 250, 0)',
        xaxis=dict(
            title=dict(
                text=titre_x,
                font=police_label
            ),
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(211, 211, 211, 0)',
            tickfont=police_label
        ),
        yaxis=dict(
            title=dict(
                text=titre_y,
                font=police_label
            ),
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(211, 211, 211, 0)',
            tickfont=police_label
        )
    )
    
    # Ajout d'une bordure légère et d'un effet d'ombre pour chaque barre
    if sens == 'v':
        fig.update_layout(
            bargap=0.15,  # Espacement entre les barres
            bargroupgap=0.1  # Espacement entre les groupes de barres
        )
    st.plotly_chart(fig, use_container_width=True)

#24. Fonction pour afficher une courbe de surface
def make_area_chart(df,var,titre="",color=1,width=500,height=300):
    df_rempl=df.groupby(var).agg({ "ID":'size'})
    df_rempl=df_rempl.rename(columns={"ID":"Effectif"})
    fig=px.area(df_rempl,x=df_rempl.index,y="Effectif",color_discrete_sequence=val_couleur[color])
    fig.update_layout(width=width, height=height,
                    title=dict(
        text=titre,
        x=0.0,  # Centre horizontalement
        y=0.95,  # Légèrement en dessous du bord supérieur
        xanchor='left', 
        yanchor='top'),)
    fig.update_layout(
        title=titre,
        paper_bgcolor='rgba(248,248,250,0)',
        plot_bgcolor='rgba(248,248,250,0)',
        margin=dict(l=5, r=1, t=30, b=10),
        legend=dict(
            x=0.8,  # Position horizontale (à droite)
            y=1,  # Position verticale (en haut)
            traceorder='normal',
            xanchor='center',  # Alignement horizontal de la légende
            yanchor='top',  # Alignement vertical de la légende
            bgcolor='rgba(255,255,255,0.1)',  # Fond semi-transparent de la légende
        )
    )
    st.plotly_chart(fig) 

#25. Fonction pour afficher une distribution d'une variable quantitative, version 2
def make_distribution_2(df, var_alpha, var_num, add_vline=None, add_vline2=None, vline_labels=None, 
                     titre="", width=700, height=400, palette=None, bin_size=None, opacity=0.75,
                     show_grid=True):
    """
    Crée un graphique de distribution avec histogrammes superposés et lignes verticales annotées.
    
    Args:
        df: DataFrame contenant les données
        var_alpha: Variable catégorielle pour segmenter les données
        var_num: Variable numérique à analyser
        add_vline: Position de la première ligne verticale (None pour ne pas l'afficher)
        add_vline2: Position de la deuxième ligne verticale (None pour ne pas l'afficher)
        vline_labels: Liste des étiquettes pour les lignes verticales
        titre: Titre du graphique
        width: Largeur du graphique
        height: Hauteur du graphique
        palette: Liste de couleurs personnalisée (si None, utilise une palette agréable par défaut)
        bin_size: Taille des bins pour l'histogramme (None pour auto)
        opacity: Opacité des barres (entre 0 et 1)
        show_mean: Afficher les lignes verticales des moyennes par catégorie
        show_grid: Afficher ou masquer la grille
    """
    # Définition de la police pour les textes
    police_annotation = {'size': 12, 'family': 'Arial, sans-serif', 'color': '#333333'}
    
    # Définition des couleurs si non spécifiées
    if palette is None:
        # Palette de couleurs harmonieuse
        palette = ['#FDC7D3', '#F61A49', '#2ca02c', '#d62728', '#9467bd', 
                  '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    # Créer la figure
    fig = go.Figure()
    
    # Variables pour stocker les informations pour les annotations
    categories = list(df[var_alpha].unique())
    means = []
    max_y_value = 25
    
    # Déterminer les limites des axes pour les définir correctement
    min_x = df[var_num].min()
    max_x = df[var_num].max()
    range_x = max_x - min_x
    
    # Ajouter des marges
    x_min = min_x - range_x * 0.05
    x_max = max_x + range_x * 0.05
    
    # Ajouter les histogrammes pour chaque catégorie
    for i, category in enumerate(categories):
        color_idx = i % len(palette)
        df_filtered = df[df[var_alpha] == category]
        
        # Calculer la moyenne pour cette catégorie
        mean_val = float(df_filtered[var_num].mean())
        means.append(mean_val)
        
        # Ajouter l'histogramme
        hist = go.Histogram(
            x=df_filtered[var_num],
            name=category,
            opacity=opacity,
            marker_color=palette[color_idx],
            nbinsx=40 if bin_size is None else None,
            xbins=dict(size=bin_size) if bin_size is not None else None,
            
        )
        fig.add_trace(hist)
        
    # Configuration par défaut des labels de ligne verticale si non fournis
    if vline_labels is None:
        vline_labels = ["Seuil femme", "Seuil homme"]
     
    # Ajouter la première ligne verticale
    if add_vline is not None:
        fig.add_shape(
            type="line",
            x0=add_vline,
            x1=add_vline,
            y0=0,
            y1=max_y_value,
            line=dict(color="green", width=2.5),
        )
        
        # Ajouter l'annotation pour la première ligne verticale
        fig.add_annotation(
            x=add_vline,
            y=max_y_value,
            text=vline_labels[0],
            showarrow=False,
            textangle=-90,
            font=dict(size=13, color="#8B0000", family="Arial, sans-serif"),
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="#228B22",
            borderwidth=1,
            borderpad=4
        )
    
    # Ajouter la deuxième ligne verticale
    if add_vline2 is not None:
        fig.add_shape(
            type="line",
            x0=add_vline2,
            x1=add_vline2,
            y0=0,
            y1=max_y_value,
            line=dict(color="green", width=1.5),
        )
        
        # Ajouter l'annotation pour la deuxième ligne verticale
        fig.add_annotation(
            x=add_vline2,
            y=max_y_value * 0.7,
            text=vline_labels[1] if len(vline_labels) > 1 else "Seuil homme",
            showarrow=False,
            textangle=-90,
            font=dict(size=13, color="#8B0000", family="Arial, sans-serif"),
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="#8B0000",
            borderwidth=1,
            borderpad=4
        )
    
    # Mise à jour de la mise en page
    fig.update_layout(
        title={
            'text': f"<b>{titre}</b>" if titre else "",
            'x': 0.5,
            'y': 1,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': police_label
        },
        barmode='overlay',  # 'overlay' pour superposer, 'stack' pour empiler
        bargap=0.05,  # Espace entre les barres
        bargroupgap=0.1,  # Espace entre les groupes de barres
        width=width,
        height=height,
        paper_bgcolor='rgba(248,248,250,0)',
        plot_bgcolor='rgba(248,248,250,0)',
        margin=dict(l=8, r=4, t=8, b=8),  # Marges ajustées
        legend={
            'title': var_alpha,
            'orientation': 'h',
            'yanchor': 'bottom',
            'y':0.7,
            'xanchor': 'center',
            'x': 0.9,
            'bgcolor': 'rgba(255,255,255,0)',
            'bordercolor': 'rgba(0,0,0,0)',
            'borderwidth': 1,
            'font': police_label
        },
        xaxis=dict(
            title=dict(text=var_num, font=police_label),
            showgrid=show_grid,
            gridcolor='rgba(211,211,211,0)',
            gridwidth=0.5,
            zeroline=False,
            range=[x_min, x_max],
            tickfont=police_label
        ),
        yaxis=dict(
            showgrid=show_grid,
            gridcolor='rgba(211,211,211,0)',
            gridwidth=0.5,
            zeroline=True,
            zerolinecolor='rgba(0,0,0,0)',
            zerolinewidth=1,
            tickfont=police_label
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Arial, sans-serif"
        )
    )
    
    # Afficher dans Streamlit
    st.plotly_chart(fig, use_container_width=True)

#26. Fonction pour définir le thème
def set_custom_theme():
    """
    Applique un thème personnalisé (dark ou light) à votre application Streamlit
    en utilisant les codes de couleurs spécifiques.
    
    Args:
        theme_mode (str): "light" ou "dark" pour choisir le thème
    """
    theme = st.sidebar.radio(
        "Choisir le thème:",
        options=["Light", "Dark"],
        #index=0  # 0 pour Light par défaut
    )
    
    if theme == "Light":
        # Thème clair avec les couleurs exactes de l'image 2
        primary_color = "#FF4B4B"
        background_color = "#FFFFFF"
        text_color = "#31333F"
        secondary_bg_color = "#F0F2F6"
        
        st.markdown(f"""
        <style>
        :root {{
            --primary-color: {primary_color};
            --background-color: {background_color};
            --secondary-background-color: {secondary_bg_color};
            --text-color: {text_color};
        }}
        .stApp {{
            background-color: var(--background-color);
            color: var(--text-color);
        }}
        .stButton>button {{
            background-color: var(--primary-color);
            color: white;
        }}
        .stTextInput>div>div>input, .stSelectbox>div>div>input {{
            color: var(--text-color);
        }}
        .sidebar .sidebar-content {{
            background-color: var(--secondary-background-color);
        }}
        </style>
        """, unsafe_allow_html=True)
    else:
        # Thème sombre avec les couleurs exactes de l'image 1
        primary_color = "#FF4B4B"
        background_color = "#0E1117"
        text_color = "#FAFAFA"
        secondary_bg_color = "#262730"
        
        st.markdown(f"""
        <style>
        :root {{
            --primary-color: {primary_color};
            --background-color: {background_color};
            --secondary-background-color: {secondary_bg_color};
            --text-color: {text_color};
        }}
        .stApp {{
            background-color: var(--background-color);
            color: var(--text-color);
        }}
        .stButton>button {{
            background-color: var(--primary-color);
            color: white;
        }}
        .stTextInput>div>div>input, .stSelectbox>div>div>input {{
            color: var(--text-color);
        }}
        .sidebar .sidebar-content {{
            background-color: var(--secondary-background-color);
        }}
        </style>
        """, unsafe_allow_html=True)

#26. Fonction pour afficher histogramme amplilé à barres relatif      
def make_relative_bar(df, var1, var2, titre="", colors=None, width=650, height=400, 
                     show_values=True, round_digits=1):
    """
    Crée un graphique à barres empilées représentant des proportions relatives.
    
    Args:
        df: DataFrame contenant les données
        var1: Variable pour l'axe X
        var2: Variable pour la couleur/catégorie
        titre: Titre du graphique
        colors: Liste de couleurs (utilise Plotly Vivid par défaut)
        width: Largeur du graphique
        height: Hauteur du graphique
        show_values: Afficher les valeurs sur les barres
        round_digits: Nombre de décimales pour les pourcentages
    """
    
    # Utiliser les couleurs Vivid de Plotly par défaut si aucune couleur n'est spécifiée
    if colors is None:
        colors = palette
    
    # Calculer les proportions relatives
    cross_tab = pd.crosstab(df[var1], df[var2])  
    cross_tab_pct = cross_tab.div(cross_tab.sum(axis=1), axis=0) * 100 
    data_long = cross_tab_pct.reset_index().melt(id_vars=var1, var_name=var2, value_name='Pourcentage')
    
    # Créer le graphique
    fig = px.bar(
        data_long,
        x=var1,
        y='Pourcentage',
        color=var2,
        title=titre,
        labels={'Pourcentage': 'Proportion (%)', var1: var1, var2: var2},
        barmode='stack',
        text='Pourcentage' if show_values else None,
        color_discrete_sequence=colors
    )
    
    # Optimiser l'apparence
    fig.update_traces(
        texttemplate=f'%{{text:.{round_digits}f}}%', 
        textposition='inside',
        textfont=dict(size=25)
    )
    
    fig.update_layout(
        width=width, 
        height=height,
        yaxis=dict(visible=False),
        title=dict(
            text=titre,
            x=0.5,  # Centrer le titre
            xanchor='center',
            font=dict(size=20)
        ),
        margin=dict(l=10, r=5, t=20, b=40),
        paper_bgcolor='rgba(248,248,250,0)',
        plot_bgcolor='rgba(248,248,250,0)',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.25,
            xanchor='center',
            x=0.1
        )
    )
    
    # Afficher le graphique
    st.plotly_chart(fig, use_container_width=True)
    
    return fig  # Retourner la figure pour utilisation possible ailleurs

#27. Fonction pour une distribution avec les box plot
def make_hist_box(df,var1,var2,titre="",width=500,height=300):
    fig=px.histogram(df,x=var1,color=var2,marginal="box",color_discrete_sequence=palette,opacity=0.8)
    fig.update_layout(
        width=width, 
        height=height,
        yaxis=dict(visible=False),
        title=dict(
            text=titre,
            x=0.5,  # Centrer le titre
            xanchor='center',
            font=dict(size=16)
        ),
        margin=dict(l=10, r=5, t=20, b=40),
        paper_bgcolor='rgba(248,248,250,0)',
        plot_bgcolor='rgba(248,248,250,0)',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.25,
            xanchor='center',
            x=0.1
        ))
    st.plotly_chart(fig)
    
#28. Fonction pour afficher une carte dynamiquer version 3
def make_map_folium(df, style_carte="OpenStreetMap", palet_color="blues", opacity=0.8, width=700, height=600):
    """
    Fonction pour créer une carte choroplèthe interactive montrant la distribution des candidats
    par statut d'éligibilité à travers différents quartiers et arrondissements, en utilisant Folium.
    
    Parameters:
    -----------
    df : GeoDataFrame
        DataFrame contenant les données géospatiales des candidats
    style_carte : str, default="OpenStreetMap"
        Style de fond de carte Folium (options: "OpenStreetMap", "cartodbpositron", "cartodbdark_matter", etc.)
    palet_color : str, default="Blues"
        Palette de couleurs pour la choroplèthe (options: "Blues", "Reds", "Greens", "YlOrRd", etc.)
    opacity : float, default=0.8
        Opacité des polygones de la choroplèthe (0-1)
    width : int, default=700
        Largeur de la carte en pixels
    height : int, default=600
        Hauteur de la carte en pixels
    """
    
    
    # Nettoyer les données en supprimant les lignes avec des coordonnées NaN
    df_clean = df.dropna(subset=['Lat', 'Long']).copy()
    
    # Définition des catégories d'éligibilité et des couleurs associées
    eligibility_categories = {
        "Temporairement éligible": {"color": "#0073E6", "size_factor": 12, "opacity": 0.75},
        "Temporairement non-éligible": {"color": "#B3D9FF", "size_factor": 8, "opacity": 0.7},
        "Non-éligible": {"color": "#FF5733", "size_factor": 4, "opacity": 0.7}
    }
    
    # Préparation des données par statut d'éligibilité
    dfs_by_eligibility = {}
    for category in eligibility_categories.keys():
        geo_data = df_clean[df_clean["Statut"] == category]
        
        if not geo_data.empty:
            dfs_by_eligibility[category] = geo_data.groupby("quartier").agg({
                'quartier': 'size',
                'Lat': 'first',
                'Long': 'first'
            }).rename(columns={'quartier': 'nb_donateur'})
            dfs_by_eligibility[category]["Qrt"] = dfs_by_eligibility[category].index
            # S'assurer qu'il n'y a pas de NaN dans les coordonnées agrégées
            dfs_by_eligibility[category] = dfs_by_eligibility[category].dropna(subset=['Lat', 'Long'])

    # Préparation des données pour la choroplèthe par arrondissement
    df_chlph = df_clean.groupby("Arrondissement").agg({
        'Arrondissement': 'size',
        'geometry': 'first',
        'Long': 'first',
        'Lat': 'first'
    }).rename(columns={'Arrondissement': 'nb_donateur'})
    df_chlph["Arr"] = df_chlph.index
    # S'assurer qu'il n'y a pas de NaN dans les coordonnées agrégées
    df_chlph = df_chlph.dropna(subset=['Lat', 'Long'])
    df_chlph = gpd.GeoDataFrame(df_chlph, geometry='geometry')
    
    # S'assurer que le CRS est défini - Utiliser EPSG:4326 (WGS84) pour compatibilité avec Folium
    if df_chlph.crs is None:
        df_chlph.set_crs(epsg=4326, inplace=True)
    else:
        # Si un CRS est déjà défini mais différent de WGS84, le convertir
        if df_chlph.crs != 'EPSG:4326':
            df_chlph = df_chlph.to_crs(epsg=4326)

    # Total des candidats par quartier
    df_pts = df_clean.groupby("quartier").agg({
        'quartier': 'size',
        'Lat': 'first',
        'Long': 'first'
    }).rename(columns={'quartier': 'nb_donateur'})
    df_pts["Qrt"] = df_pts.index
    # S'assurer qu'il n'y a pas de NaN dans les coordonnées agrégées
    df_pts = df_pts.dropna(subset=['Lat', 'Long'])
    
    # Vérifier si df_pts est vide après filtrage
    if df_pts.empty:
        st.error("Aucune coordonnée valide trouvée dans les données. Impossible de créer la carte.")
        return None
    
    # Création de la carte Folium
    center_lat = df_pts["Lat"].mean()
    center_lon = df_pts["Long"].mean()
    
    # Dictionnaire de correspondance entre les styles dans votre fonction originale et ceux de Folium
    tile_styles = {
        "carto-positron": "cartodbpositron",
        "carto-darkmatter": "cartodbdark_matter",
        "open-street-map": "OpenStreetMap",
        "CartoDB positron": "cartodbpositron", 
        "CartoDB dark_matter": "cartodbdark_matter"
    }
    
    # Utiliser le style approprié ou OpenStreetMap par défaut
    actual_style = tile_styles.get(style_carte, style_carte)
    
    # Création de la carte avec le style approprié
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles=actual_style,
        width=width,
        height=height
    )
    
    # Ajout de la couche choroplèthe pour les arrondissements
    # Création d'une échelle de couleur avec la bonne classe de branca.colormap
    if palet_color == "blues":
        color_range = ['#f7fbff', '#08519c']
    elif palet_color == "reds":
        color_range = ['#fee5d9', '#a50f15']
    elif palet_color == "greens":
        color_range = ['#edf8e9', '#006d2c']
    elif palet_color == "viridis":
        color_range = ['#fde725', '#440154']
    else:
        color_range = ['#f7fbff', '#08519c']  # Default to Blues
    
    # Création des clusters uniquement pour les arrondissements
    arrondissement_cluster = MarkerCluster(name="Arrondissements").add_to(m)
    
    if not df_chlph.empty:
        colormap = cm.LinearColormap(
            colors=color_range, 
            vmin=df_chlph["nb_donateur"].min(),
            vmax=df_chlph["nb_donateur"].max(),
            caption="Nombre de Candidats par Arrondissement"
        )
        
        # Convertir le GeoDataFrame en GeoJSON
        geo_json_data = df_chlph.__geo_interface__
        
        # Ajout des polygones des arrondissements en utilisant le GeoJSON préparé
        folium.GeoJson(
            geo_json_data,
            style_function=lambda feature: {
                'fillColor': colormap(feature['properties']['nb_donateur']),
                'color': 'white',
                'weight': 0.5,
                'fillOpacity': opacity
            },
            tooltip=folium.GeoJsonTooltip(
                fields=['Arr', 'nb_donateur'],
                aliases=['Arrondissement:', 'Nombre de candidats:'],
                style="background-color: white; color: #333333; font-family: arial; font-size: 14px; padding: 10px;"
            )
        ).add_to(m)
        
        # Ajout des étiquettes d'arrondissement et des marqueurs au cluster d'arrondissements
        for idx, row in df_chlph.iterrows():
            # Étiquettes d'arrondissement
            folium.Marker(
                location=[row['Lat'], row['Long']],
                icon=folium.DivIcon(
                    icon_size=(150, 40),
                    icon_anchor=(75, 28),
                    html=f'<div style="font-size: 12px; font-weight: bold; text-align: center">{row["Arr"]}</div>'
                )
            ).add_to(m)
            
            # Marqueurs d'arrondissement pour le cluster
            folium.Marker(
                location=[row['Lat'], row['Long']],
                popup=f"<b>Arrondissement {row['Arr']}</b><br>Total candidats: <b>{row['nb_donateur']}</b>",
                icon=folium.Icon(color='blue')
            ).add_to(arrondissement_cluster)
        
        # Ajout de la légende de couleur
        colormap.add_to(m)

    # Fonction pour calculer la taille du cercle en fonction du nombre de candidats
    def calculate_radius(count, max_count, base_size=5):
        return base_size * np.sqrt(count / max_count * 100)
    
    max_count = df_pts["nb_donateur"].max() if not df_pts.empty else 1
    
    # Création d'un groupe de features pour les cercles des quartiers
    quartier_feature_group = folium.FeatureGroup(name="Total candidats par quartier")
    
    # Ajout des marqueurs pour le total des candidats (directement à la carte, pas de cluster)
    for idx, row in df_pts.iterrows():
        radius = calculate_radius(row["nb_donateur"], max_count)
        popup_text = f"<b>{row['Qrt']}</b><br>Total candidats: <b>{row['nb_donateur']}</b>"
        
        folium.CircleMarker(
            location=[row['Lat'], row['Long']],
            radius=radius,
            color='#003F80',
            fill=True,
            fill_color='#003F80',
            fill_opacity=0.8,
            popup=folium.Popup(popup_text, max_width=300)
        ).add_to(quartier_feature_group)
    
    # Ajout du groupe de features à la carte
    quartier_feature_group.add_to(m)
        
    # Ajout des marqueurs pour chaque catégorie d'éligibilité (directement à la carte, pas de cluster)
    for category, df_pts_cat in dfs_by_eligibility.items():
        if df_pts_cat.empty:
            continue
            
        config = eligibility_categories[category]
        
        # Création d'un groupe de features pour cette catégorie
        category_feature_group = folium.FeatureGroup(name=category)
        
        max_count_cat = df_pts_cat["nb_donateur"].max() if not df_pts_cat.empty else 1
        
        for idx, row in df_pts_cat.iterrows():
            radius = calculate_radius(row["nb_donateur"], max_count_cat, base_size=config["size_factor"]/4)
            popup_text = f"<b>{row['Qrt']}</b><br>Candidats {category}: <b>{row['nb_donateur']}</b>"
            
            folium.CircleMarker(
                location=[row['Lat'], row['Long']],
                radius=radius,
                color=config["color"],
                fill=True,
                fill_color=config["color"],
                fill_opacity=config["opacity"],
                popup=folium.Popup(popup_text, max_width=300)
            ).add_to(category_feature_group)
        
        # Ajout du groupe de features à la carte
        category_feature_group.add_to(m)
            
    # Ajout du contrôle de couches
    folium.LayerControl(collapsed=False).add_to(m)
    
    # Ajout d'une légende pour les cercles des points
    legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; right: 50px; 
                    width: 220px;
                    background-color: white;
                    border: 2px solid grey;
                    border-radius: 5px;
                    z-index: 9999;
                    font-size: 14px;
                    padding: 10px;
                    opacity: 0.9;">
            <div style="text-align: center; margin-bottom: 5px;"><b>Légende des points</b></div>
    '''
    
    # Ajouter une entrée de légende pour les cercles totaux
    legend_html += f'''
        <div style="margin-bottom: 7px;">
            <div style="display: inline-block; 
                      width: 15px; 
                      height: 15px; 
                      border-radius: 50%; 
                      background-color: #003F80;
                      margin-right: 5px;
                      vertical-align: middle;"></div>
            <span style="vertical-align: middle;">Total candidats</span>
        </div>
    '''
    
    # Ajouter des entrées pour chaque catégorie d'éligibilité
    for category, config in eligibility_categories.items():
        if category in dfs_by_eligibility and not dfs_by_eligibility[category].empty:
            legend_html += f'''
                <div style="margin-bottom: 7px;">
                    <div style="display: inline-block; 
                              width: 15px; 
                              height: 15px; 
                              border-radius: 50%; 
                              background-color: {config['color']};
                              opacity: {config['opacity']};
                              margin-right: 5px;
                              vertical-align: middle;"></div>
                    <span style="vertical-align: middle;">{category}</span>
                </div>
            '''
    
    # Fermer la div de la légende
    legend_html += '</div>'
    
    # Ajouter la légende à la carte
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Ajout d'un titre 
    title_html = '''
        <div style="position: fixed; 
                    top: 10px; left: 50px; width: 600px; height: 45px; 
                    background-color: white; border-radius: 5px;
                    z-index: 9999; font-size: 20px; font-family: Arial;
                    padding: 10px; text-align: center; color: #333;">
            <b>Distribution des Candidats par Éligibilité</b>
        </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Affichage avec Streamlit
    folium_static(m, width=width, height=height)
    
    return m

#29. Fonction de production de carte
def make_chlorophet_map(df,style_carte="carto-positron",palet_color="Blues",opacity=0.8,width=500, height=300):
    geo_data_El=df[df["Eligibilite"]=="Eligible"]
    geo_data_TNE=df[df["Eligibilite"]=="Temporairement Non-eligible"]
    geo_data_NE=df[df["Eligibilite"]=="Définitivement non-eligible"]

    df_pts_El=geo_data_El.groupby("Quartier").agg({
    'Quartier': 'size',
    'Lat': 'first',
    'Long':'first'
    }).rename(columns={'Quartier': 'nb_donateur'})
    df_pts_El["Qrt"]=df_pts_El.index

    df_pts_TNE=geo_data_TNE.groupby("Quartier").agg({
        'Quartier': 'size',
        'Lat': 'first',
        'Long':'first'
    }).rename(columns={'Quartier': 'nb_donateur'})
    df_pts_TNE["Qrt"]=df_pts_TNE.index

    df_pts_NE=geo_data_NE.groupby("Quartier").agg({
        'Quartier': 'size',
        'Lat': 'first',
        'Long':'first'
    }).rename(columns={'Quartier': 'nb_donateur'})
    df_pts_NE["Qrt"]=df_pts_NE.index

    df_chlph=df.groupby("Arrondissement").agg({
        'Arrondissement': 'size',
        'geometry': 'first',
        'Long':'first',
        'Lat':'first'
    }).rename(columns={'Arrondissement': 'nb_donateur'})
    df_chlph["Arr"]=df_chlph.index
    df_chlph = gpd.GeoDataFrame(df_chlph, geometry='geometry')


    df_pts=df.groupby("Quartier").agg({
        'Quartier': 'size',
        'Lat': 'first',
        'Long':'first'
    }).rename(columns={'Quartier': 'nb_donateur'})
    df_pts["Qrt"]=df_pts.index
    
    fig = go.Figure(go.Choroplethmapbox(
        geojson=df_chlph.geometry.__geo_interface__,  # Géométries des arrondissements
        locations=df_chlph.index,  # Indices des polygones
        z=df_chlph["nb_donateur"],  # Variable à visualiser (nombre de donateurs)
        colorscale=palet_color,  # Échelle de couleurs
        marker_opacity=opacity,  # Opacité des polygones
        marker_line_width=0.5,  # Épaisseur des bordures
        colorbar_title="Nombre de Candidat",  # Titre de la barre de couleur
        hovertext=df_chlph['Arr'],
        hovertemplate=" %{hovertext}  <br>Nombre de candidat : %{z}<extra></extra>",
    ))
    
    fig.add_trace(go.Scattermapbox(
        lat=df_chlph["Lat"],
        lon=df_chlph["Long"],
        mode='text',
        text=df_chlph["Arr"],  # Nom des arrondissements
        textfont=dict(size=12, color="black"),
        hoverinfo='none'
    ))

    # Ajout des points pour représenter le nombre de donateurs
    fig.add_trace(go.Scattermapbox(
        lat=df_pts["Lat"],  # Colonne des latitudes des points
        lon=df_pts["Long"],  # Colonne des longitudes des points
        mode='markers',  # Mode de dispersion (points)
        name="Total candidat",
        marker=dict(
            size=df_pts["nb_donateur"],  # Taille des points basée sur 'nb_donateur'
            sizemode='area',  # La taille est proportionnelle à la surface
            sizeref=2. * max(df_pts["nb_donateur"]) / (45.**2),  # Ajustement de la taille
            color='#003F80',  # Couleur des points
            opacity=0.8  # Opacité des points
        ),
        hovertemplate=(
            "<b>Quartier :</b> %{text}<br>"
            "<b>Total candidat :</b> %{marker.size}<extra></extra>"
        ),  # Format de l'infobulle
        text=df_pts["Qrt"]
    ))
    # Ajout des points pour représenter le nombre de donateurs eligibles
    fig.add_trace(go.Scattermapbox(
        lat=df_pts_El["Lat"],  
        lon=df_pts_El["Long"],  
        mode='markers',  
        name="Eligibles",
        marker=dict(
            size=df_pts_El["nb_donateur"],  
            sizemode='area',  
            sizeref=2. * max(df_pts_El["nb_donateur"]) / (27.**2),  
            color='#0073E6',  
            opacity=0.75  
        ),
        hovertemplate=(
            "<b>Quartier :</b> %{text}<br>"
            "<b> candidat Eligibles :</b> %{marker.size}<extra></extra>"
        ),
        text=df_pts_El["Qrt"]
    ))
    # Ajout des points pour représenter le nombre de donateurs temporairement non-eligibles
    fig.add_trace(go.Scattermapbox(
        lat=df_pts_NE["Lat"],  
        lon=df_pts_NE["Long"],  
        mode='markers',  
        name="Temporairement Non-eligibles",
        marker=dict(
            size=df_pts_NE["nb_donateur"],  
            sizemode='area',  
            sizeref=2. * max(df_pts_NE["nb_donateur"]) / (17.**2),  
            color='#B3D9FF',  
            opacity=0.7  
        ),
        hovertemplate=(
            "<b>Quartier :</b> %{text}<br>"
            "<b>candidat Temporairement Non-eligibles :</b> %{marker.size}<extra></extra>"
        ), 
        text=df_pts_NE["Qrt"]
    ))
    # Ajout des points pour représenter le nombre de donateurs Non eligibles
    fig.add_trace(go.Scattermapbox(
        lat=df_pts_NE["Lat"],  
        lon=df_pts_NE["Long"],  
        mode='markers',  
        name="Non Eligible",
        marker=dict(
            size=df_pts_NE["nb_donateur"],  
            sizemode='area',  
            sizeref=2. * max(df_pts_NE["nb_donateur"]) / (10.**2),  
            color='white',  
            opacity=0.7  
        ),
        hovertemplate=(
            "<b>Quartier :</b> %{text}<br>"
            "<b> candidat Non-eligibles :</b> %{marker.size}<extra></extra>"
        ), 
        text=df_pts_NE["Qrt"]
    ))

    # Mise à jour de la mise en page de la carte
    fig.update_layout(
        showlegend=True,
        legend=dict(
            x=0.0,  # Centré horizontalement
            y=0.1,  # Sous la carte
            orientation='h',  # Légende horizontale
        ),
        mapbox=dict(
            #style="open-street-map",
            style=style_carte,  # Style de la carte
            #style="carto-darkmatter",
            center=dict(lat=df_pts["Lat"].mean(), lon=df_pts["Long"].mean()),  # Centrer la carte
            zoom=10  # Niveau de zoom
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        width=width, height=height,
    )

    st.plotly_chart(fig)

#30. Fonction de calibrage de la carte
def calculate_zoom(lon_diff, lat_diff, map_width=800, map_height=600):
            max_zoom = 18
            zoom_level = 0
            while (lon_diff * 2 ** zoom_level < map_width) and (lat_diff * 2 ** zoom_level < map_height):
                zoom_level += 1
                if zoom_level >= max_zoom:
                    break
            return min(zoom_level, max_zoom)

#31. Fonction de téléchargement de rapport
def telecharger_pdf(file_path, lang="Français"):
    with open(file_path, "rb") as f:
        pdf_bytes = f.read()
    
    st.download_button(
        label=traduire_texte("📥 Télécharger le rapport PDF",lang),
        data=pdf_bytes,
        file_name="Rapport_TDB.pdf",
        mime="application/pdf",
    )
#==========================================================

def make_blood_group(df, var):
    df1=df.groupby(var).agg({ "Horodateur":"size"})
    df1=df1.rename(columns={"Horodateur":"Effectif"})
    df1["Modal"]=df1.index
    df1["prop"]=df1["Effectif"]/df1["Effectif"].sum()
    mod=list(df1["Modal"])
    val=list(df1["Effectif"])
    prop=list(df1["prop"])
    p=len(mod)//4
    i=1
    k=0
    while i<=p:
        col=st.columns(4)
        for j in range(4):
            with col[j]:
                st.markdown(f"""
                    <h3 class="sidebar-link">{mod[k]}🩸
                    <br><center>{val[k]} </center>
                    <br> <center>{round(prop[k]*100, 2)}% </center>
                    </h3>
                """, unsafe_allow_html=True)
                k=k+1
        i=i+1
        
def make_donutchart_2(df, var, titre="", width=600, height=450, color_palette=None, part=True):
    """
    Crée un graphique en anneau (donut chart) avec des améliorations visuelles en utilisant ECharts.
    
    Args:
        df: DataFrame contenant les données
        var: Variable à visualiser
        titre: Titre du graphique
        width: Largeur du graphique
        height: Hauteur du graphique
        color_palette: Liste de couleurs personnalisées pour le graphique
        part: Afficher les pourcentages (True par défaut)
        
    Returns:
        Affiche le graphique dans Streamlit via ECharts
    """
    st.write(". ")
    # Agrégation des données
    data_grouped = df.groupby(var).size().reset_index(name='Effectif')
    
    # Calculer les pourcentages pour l'affichage dans les étiquettes
    total = data_grouped['Effectif'].sum()
    data_grouped['Pourcentage'] = (data_grouped['Effectif'] / total * 100).round(1)
    
    # Trier par effectif décroissant pour une meilleure présentation
    data_grouped = data_grouped.sort_values('Effectif', ascending=False)
    
    # Préparation des données pour ECharts
    categories = data_grouped[var].tolist()
    values = data_grouped['Effectif'].tolist()
    percentages = data_grouped['Pourcentage'].tolist()
    
    # Couleurs par défaut si non spécifiées
    if color_palette is None:
        color_palette = palette
    
    # Limiter les couleurs à la longueur des données
    colors = color_palette[:len(categories)]
    
    # Construction des données pour les séries
    series_data = []
    for i, (cat, val, pct) in enumerate(zip(categories, values, percentages)):
        # Déterminer si ce segment doit être légèrement détaché
        offset = 10 if (i == 0) and (len(data_grouped) > 2) else 0
        
        item = {
            "name": cat,
            "value": val,
            "itemStyle": {"color": colors[i % len(colors)]},
            "tooltip": {"formatter": f"<b>{cat}</b><br>Effectif: {val} ({pct}%)"},
        }
        
        # Ajouter l'offset pour le premier segment si nécessaire
        if offset > 0:
            item["offset"] = offset
            
        series_data.append(item)
    
    # Configuration du graphique
    options = {
        "title": {
            "text": titre,
            "left": "center",
            "textStyle": {
                "fontWeight": "bold",
                "fontSize": 18
            }
        },
        "tooltip": {
            "trigger": "item",
            "backgroundColor": "rgba(255, 255, 255, 0.9)",
            "borderColor": "#ccc",
            "borderWidth": 1,
            "textStyle": {
                "color": "#333"
            },
            "formatter": "{b}: {c} ({d}%)"
        },
        "legend": {
            "orient": "horizontal",
            "bottom": "bottom",
            "left": "center",
            "data": categories
        },
        "series": [
            {
                "name": var,
                "type": "pie",
                "radius": ["40%", "70%"],  # Effet donut
                "center": ["50%", "50%"],
                "avoidLabelOverlap": False,
                "itemStyle": {
                    "borderRadius": 4,
                    "borderColor": "#fff",
                    "borderWidth": 2
                },
                "label": {
                    "show": part,
                    "position": "inside",
                    "formatter": "{b}\n{d}%" if part else "{b}",
                    "fontSize": 10,
                    "fontWeight": "bold"
                },
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)"
                    },
                    "label": {
                        "show": True,
                        "fontSize": 12,
                        "fontWeight": "bold"
                    }
                },
                "labelLine": {
                    "show": False
                },
                "data": series_data
            }
        ]
    }
    
    # Ajout du nombre total au centre
    options["graphic"] = [{
        "type": "text",
        "left": "center",
        "top": "50%",
        "style": {
            "text": f"{total:,}\nTotal",
            "textAlign": "center",
            "fill": "#333",
            "fontSize": 16,
            "fontWeight": "bold"
        }
    }]
    
    # Affichage dans Streamlit
    st_echarts(
        options=options,
        height=f"{height}px",
        width="100%"  # Pour utiliser toute la largeur disponible
    )
    
def Make_Global_DataFrame(df, title="", height=None, pagination=True, filters=True, width="100%", search=True, sort=True, selection=False, hide_columns=None, column_config=None, download=False, download_filename="data.csv", cle="key1"):
    """
    Affiche un DataFrame de façon stylée avec des options de filtrage, tri, pagination et téléchargement.
    
    Args:
        df: DataFrame pandas à afficher
        title: Titre à afficher au-dessus du tableau (optionnel)
        height: Hauteur du tableau en pixels (None = automatique)
        pagination: Activer la pagination (True par défaut)
        filters: Activer les filtres par colonne (True par défaut)
        width: Largeur du tableau ("100%" par défaut)
        search: Activer la recherche globale (True par défaut)
        sort: Activer le tri des colonnes (True par défaut)
        selection: Activer la sélection de lignes (False par défaut)
        hide_columns: Liste des colonnes à masquer (None par défaut)
        column_config: Configuration personnalisée des colonnes (dictionnaire)
        download: Activer l'option de téléchargement (False par défaut)
        download_filename: Nom du fichier à télécharger ("data.csv" par défaut)
        
    Returns:
        En mode sélection, retourne les données sélectionnées, sinon None
    """

    # Vérifier si le DataFrame est vide
    if df.empty:
        st.warning("Le DataFrame est vide.")
        return None
    
    # Afficher le titre si fourni
    if title:
        st.subheader(title)
    
    # Créer une copie du DataFrame pour éviter de modifier l'original
    df_display = df.copy()
    
    # Masquer les colonnes spécifiées
    if hide_columns:
        df_display = df_display.drop(columns=[col for col in hide_columns if col in df_display.columns])
    
    # Section de filtrage manuel (avant le tableau)
    if filters:
        with st.expander("Filtres avancés", expanded=False):
            cols = st.columns(min(3, len(df_display.columns)))
            filter_conditions = []
            
            for i, column in enumerate(df_display.columns):
                col_idx = i % 3
                with cols[col_idx]:
                    # Adapter le type de filtre en fonction du type de données
                    if pd.api.types.is_numeric_dtype(df_display[column]):
                        min_val, max_val = float(df_display[column].min()), float(df_display[column].max())
                        if min_val != max_val:
                            filter_val = st.slider(f"Filtrer par {column}", min_val, max_val, (min_val, max_val),key=random.randint(1, 1000000))
                            if filter_val != (min_val, max_val):
                                filter_conditions.append(f"{filter_val[0]} <= `{column}` <= {filter_val[1]}")
                    elif pd.api.types.is_datetime64_any_dtype(df_display[column]):
                        min_date, max_date = df_display[column].min(), df_display[column].max()
                        if min_date != max_date:
                            filter_date = st.date_input(f"Filtrer par {column}", (min_date, max_date),key=random.randint(1, 1000000))
                            if len(filter_date) == 2 and (filter_date[0] != min_date or filter_date[1] != max_date):
                                filter_conditions.append(f"`{column}` >= '{filter_date[0]}' and `{column}` <= '{filter_date[1]}'")
                    else:
                        # Pour les colonnes textuelles ou catégorielles
                        unique_values = df_display[column].dropna().unique()
                        if len(unique_values) < 20:  # Utiliser une liste déroulante si peu de valeurs
                            selected_values = st.multiselect(f"Filtrer par {column}", unique_values, key=random.randint(1, 1000000))
                            if selected_values:
                                filter_conditions.append(f"`{column}` in {selected_values}")
                        else:  # Utiliser un champ texte pour beaucoup de valeurs
                            filter_text = st.text_input(f"Chercher dans {column}",key=random.randint(1, 1000000))
                            if filter_text:
                                filter_conditions.append(f"`{column}`.str.contains('{filter_text}', case=False, na=False)")
            
            # Appliquer les filtres
            if filter_conditions:
                combined_filter = " and ".join(filter_conditions)
                try:
                    df_display = df_display.query(combined_filter)
                    st.info(f"{len(df_display)} lignes après filtrage")
                except Exception as e:
                    st.error(f"Erreur de filtrage: {e}")
    
    # Configuration des options de st.dataframe
    df_kwargs = {
        "use_container_width": width == "100%",
        "hide_index": True,
    }
    
    # Ajout des options conditionnelles
    if height:
        df_kwargs["height"] = height
    
    # Configuration avancée des colonnes
    if column_config:
        df_kwargs["column_config"] = column_config
    
    # Configuration des options d'affichage
    config = {}
    if pagination:
        config["page_size"] = 10
    if not sort:
        config["sorting"] = False
    if search:
        config["search_bar"] = True
    if selection:
        config["selection"] = "multi"
    
    if config:
        df_kwargs["column_order"] = list(df_display.columns)
        if selection:  # Ajouter column_labels uniquement pour data_editor
            df_kwargs["column_labels"] = {col: col.replace("_", " ").title() for col in df_display.columns}
    
    # Option de téléchargement
    #if download:
        # Préparation des formats disponibles
    download_formats = {
            "CSV": ".csv",
            "Excel": ".xlsx",
            "JSON": ".json"
        }
        
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
            selected_format = st.selectbox("Format:", options=list(download_formats.keys()), index=0,key=random.randint(1, 1000000))
        
    with col2:  
            filename = st.text_input("Nom du fichier:", download_filename.split('.')[0], key=random.randint(1, 1000000))
        
    with col3:
            ext = download_formats[selected_format]
            download_filename = f"{filename}{ext}"
            
            buffer = io.BytesIO()
            
            if selected_format == "CSV":
                df_display.to_csv(buffer, index=False)
            elif selected_format == "Excel":
                df_display.to_excel(buffer, index=False)
            elif selected_format == "JSON":
                buffer.write(df_display.to_json(orient="records").encode())
            
            buffer.seek(0)
            
            st.download_button(
                label="Télécharger",
                data=buffer,
                file_name=download_filename,
                mime="application/octet-stream", key=random.randint(1, 1000000)
            )
    
    # Affichage du DataFrame avec les options configurées
    if selection:
        return st.data_editor(df_display, **df_kwargs,key=random.randint(1, 1000000))
    else:
        if "column_labels" in df_kwargs:
            # Retirer l'argument non supporté pour st.dataframe
            labels_dict = df_kwargs.pop("column_labels")
        st.dataframe(df_display,**df_kwargs, key=cle)
        
    # Information sur le nombre de lignes
    st.caption(f"Total: {len(df_display)} lignes affichées (sur {len(df)} au total)")
    
    return None

def get_image_as_base64(image_path):
        """Convertit une image en base64 pour l'affichage dans HTML"""
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        except Exception:
            # Image par défaut si l'image n'est pas trouvée
            return ""  # Retourner une chaîne vide si l'image n'est pas trouvée

def create_member_profile(name, title, image_path, about_text, email="", phone=""):
        # Créer une carte stylisée avec ombres et arrondis
        with st.container():
            # Appliquer un style CSS personnalisé à la carte
            st.markdown("""
            <style>
            .member-card {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                margin-bottom: 20px;
                transition: transform 0.3s;
                height: 100%;
            }
            .member-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            }
            .member-image {
                width: 120px;
                height: 120px;
                border-radius: 50%;
                object-fit: cover;
                margin: 0 auto;
                display: block;
                border: 3px solid #4e8df5;
            }
            .member-name {
                color: #1a1a1a;
                font-size: 18px;
                font-weight: bold;
                text-align: center;
                margin-top: 15px;
                margin-bottom: 5px;
            }
            .member-title {
                color: #4e8df5;
                font-size: 14px;
                font-style: italic;
                text-align: center;
                margin-bottom: 15px;
            }
            .member-about {
                color: #333;
                font-size: 14px;
                text-align: justify;
                line-height: 1.5;
                margin-bottom: 15px;
            }
            .contact-info {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 8px;
                margin-top: 15px;
                color: #555;
            }
            .contact-item {
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 13px;
            }
            .contact-icon {
                color: #4e8df5;
                display: flex;
                align-items: center;
                justify-content: center;
                width: 20px;
            }
            .contact-text {
                color: #555;
            }
            .contact-text:hover {
                color: #4e8df5;
                text-decoration: underline;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Obtenir l'image en base64
            img_base64 = get_image_as_base64(image_path)
            
            # Créer la structure HTML de la carte
            if img_base64:
                img_html = f'<img src="data:image/png;base64,{img_base64}" class="member-image">'
            else:
                # Si l'image n'est pas trouvée, utiliser une div colorée à la place
                img_html = f'<div style="width: 120px; height: 120px; border-radius: 50%; background-color: #4e8df5; margin: 0 auto; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">{name[0]}</div>'
            
            # Préparer la section des contacts
            contact_html = '<div class="contact-info">'
            
            # Ajouter l'email avec icône si fourni
            # Assembler la carte complète
            card_html = f"""
            <div class="member-card">
                {img_html}
                <div class="member-name">{name}</div>
                <div class="member-title">
                    <center> <a href="mailto:{email}" class="contact-text"> 📧 : {email} </center></a>
                </div>
                <div class="member-name">📞 : {phone}</div>
                <div class="member-title">{title}</div>
                <div class="member-about">{about_text}</div>
                {contact_html}
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
                
                # Obtenir l'image en base64
            img_base64 = get_image_as_base64(image_path)
            
            # Créer la structure HTML de la carte
            if img_base64:
                img_html = f'<img src="data:image/png;base64,{img_base64}" class="member-image">'
            else:
                # Si l'image n'est pas trouvée, utiliser une div colorée à la place
                img_html = f'<div style="width: 120px; height: 120px; border-radius: 50%; background-color: #4e8df5; margin: 0 auto; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">{name[0]}</div>'
            

# Fonction principale pour afficher les profils
def display_team_profiles2():
        st.markdown("""
        <style>
        .main-title {
            font-size: 32px;
            font-weight: bold;
            text-align: center;
            color: #2c3e50;
            margin-bottom: 30px;
            border-bottom: 2px solid #4e8df5;
            padding-bottom: 10px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="main-title">Notre Équipe</div>', unsafe_allow_html=True)
        
        # Description de l'équipe
        st.markdown("""
        <div style="text-align: center; margin-bottom: 40px; padding: 0 10%;">
            Notre équipe est composée de professionnels passionnés dans les domaines des statistiques, 
            de l'économie et de la data science, chacun apportant une expertise unique à nos projets.
        </div>
        """, unsafe_allow_html=True)
        
        # Arrangement des profils en 2 colonnes
        col1, col2, col3= st.columns([1,1,2])
        
        with col1:
            create_member_profile(
                name="KENGNE Landry",
                title="Mathématicien, Statisticien Economiste",
                image_path="Landry_Pro.jpg",
                about_text="Titulaire d'une licence en mathématique à l'Université de Yaoundé I. Actuellement en Master I en Statistiques et Economie appliquée à l'ISSEA.",
                email="landrykengne99@gmail.com",
                phone="+237 6 98 28 05 37")
            create_member_profile(
                name="ANABA Rodrigue",
                title="Economiste - Data Scientist",
                image_path="ANABA.jpg",
                email="student.rodrigue.anabaohandza@issea-cemac.org",
                phone="+237 6 96 26 90 77",
                about_text="Diplômé d'une Licence en Sciences Économiques, je suis actuellement en dernière année du cycle d'Ingénieur Statisticien Économiste à l'ISSEA. J'ai une solide maîtrise des méthodes statistiques avancées et des outils de modélisation économétrique.")
            
        with col2:
            create_member_profile(
                name="NOULAYE Merveille",
                title="Elève ingénieure statisticienne économiste",
                image_path="Merveille_pro.jpg",
                email="noulayemerveille@gmail.com",
                phone="+237 6 77 39 32 86",
                about_text="Jeune statisticienne en devenir dynamique et passionnée des métiers de la data. Je privilégie le travail en équipe dans la recherche des solutions efficaces et rapide face aux problèmes que je rencontre.")   
            create_member_profile(
                name="TCHINDA Rinel",
                title="Economiste - Data Scientist",
                image_path="Rinel.jpg",
                email="cezangue@gmail.com",
                phone="+237 6 73 83 11 57",
                about_text="Je suis un data scientist titulaire d'une licence en mathématiques, un master en économie quantitative et ingénierie statistique, alliant expertise analytique et foi évangélique fervente.")
        
        with col3:
            st.image("QR_code.jpg", use_container_width=False,width=700)    
            


def make_cross_hist_b_ech(df, var1, var2, titre="", typ_bar=1, width=800, height=500, sens="v", 
                    palette=None, show_legend=True, bordure=None):
    """
    Crée un histogramme croisé optimisé pour les données de campagne de don de sang.
    
    Args:
        df: DataFrame contenant les données
        var1: Variable pour grouper (apparaîtra dans la légende)
        var2: Variable pour l'axe des x/y selon l'orientation
        titre: Titre du graphique
        typ_bar: 1 pour empilé, 2 pour groupé
        width: Largeur du graphique
        height: Hauteur du graphique
        sens: Orientation - "v" (vertical) ou "h" (horizontal)
        palette: Liste de couleurs personnalisée (si None, utilise la palette de don de sang par défaut)
        show_legend: Afficher ou masquer la légende
        bordure: pour les bordure
        
    Returns:
        Affiche le graphique dans Streamlit
    """
    # Définition des couleurs pour le thème don de sang si non spécifiées
    if palette is None:
        # Palette de couleurs orientée sang (rouge) et médical (bleu) #FDC7D3,
        palette = ['#FDC7D3', '#F61A49', '#640419', '#49030D', '#4575B4', '#74ADD1', '#ABD9E9', '#E0F3F8']  # nuances de bleu
    
    bar_mode = "stack" if typ_bar == 1 else "cluster"
    
    # Création du tableau croisé et formatage
    cross_df = pd.crosstab(df[var1], df[var2])
    table_cross = cross_df.reset_index().melt(id_vars=var1, var_name=var2, value_name='Effectif')
    table_cross = table_cross.sort_values("Effectif", ascending=False)
    
    # Déterminer les axes selon l'orientation
    x_axis = var2 if sens == "v" else 'Effectif'
    y_axis = var1 if sens == "h" else 'Effectif'
    
    # Création du graphique avec Streamlit Echarts
    options = {
        "xAxis": {
            "type": "category",
            "data": list(table_cross[x_axis].unique()),
            "axisLabel": {
                "rotate": 45,
                "fontSize": 12,
                "fontFamily": "Arial, sans-serif"
            }
        },
        "yAxis": {
            "type": "value",
            "name": "Effectif",
            "nameLocation": "center",
            "nameGap": 30,
            "splitLine": {
                "lineStyle": {
                    "color": "rgba(211,211,211,0.5)"
                }
            },
            "axisLabel": {
                "fontSize": 14,
                "fontFamily": "Arial, sans-serif"
            }
        },
        "series": [
            {
                "name": cat,
                "type": "bar",
                "data": list(table_cross[table_cross[var1] == cat]["Effectif"]),
                "stack": bar_mode,
                "label": {
                    "show": True,
                    "position": "auto",
                    "fontSize": 14,
                    "fontFamily": "Arial, sans-serif"
                },
                "itemStyle": {
                    "color": palette[i]
                }
            } for i, cat in enumerate(table_cross[var1].unique())
        ],
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "shadow"
            }
        },
        "title": {
            "text": titre,
            "left": "center",
            "top": "4%",
            "textStyle": {
                "fontSize": 18,
                "fontWeight": "bold",
                "fontFamily": "Arial, sans-serif"
            }
        },
        "legend": {
            "type": "scroll",
            "orient": "horizontal",
            "right": "10%",
            "top": "10%",
            "itemWidth": 16,
            "itemHeight": 12,
            "itemGap": 8,
            "textStyle": {
                "fontSize": 12,
                "fontFamily": "Arial, sans-serif"
            }
        },
        "grid": {
            "left": "1%",
            "right": "1%",
            "bottom": "1%",
            "containLabel": True
        }
    }
    
    if sens == "h":
        options["xAxis"], options["yAxis"] = options["yAxis"], options["xAxis"]
        for serie in options["series"]:
            serie["type"] = "bar"
            serie["data"] = list(table_cross[table_cross[var1] == serie["name"]]["Effectif"])
    st.write(" ")        
    st_echarts(options, width=width, height=height)


def make_chlorophet_map_echarts(df, style_carte="light", palet_color="blues", opacity=0.8, width="700px", height="600px"):
    """
    Fonction pour créer une carte choroplèthe interactive montrant la distribution des candidats
    par statut d'éligibilité à travers différents quartiers et arrondissements, en utilisant ECharts.
    
    Parameters:
    -----------
    df : GeoDataFrame
        DataFrame contenant les données géospatiales des candidats
    style_carte : str, default="light"
        Style de fond de carte ECharts (options: "light", "dark")
    palet_color : str, default="blues"
        Palette de couleurs pour la choroplèthe (options: "blues", "reds", "greens", "yellows")
    opacity : float, default=0.8
        Opacité des polygones de la choroplèthe (0-1)
    width : str ou int, default="700px"
        Largeur de la carte (peut être int ou str)
    height : str ou int, default="600px"
        Hauteur de la carte (peut être int ou str)
    """
   
    # Convertir les dimensions en chaînes si elles sont des nombres
    if isinstance(width, int):
        width = f"{width}px"
    if isinstance(height, int):
        height = f"{height}px"
    
    # Nettoyer les données en supprimant les lignes avec des coordonnées NaN
    df_clean = df.dropna(subset=['Lat', 'Long']).copy()
    
    # Définition des catégories d'éligibilité et des couleurs associées
    eligibility_categories = {
        "Eligible": {"color": "#0073E6", "symbol_size": 12, "opacity": 0.75},
        "Temporairement Non-eligible": {"color": "#B3D9FF", "symbol_size": 8, "opacity": 0.7},
        "Définitivement non-eligible": {"color": "#FF5733", "symbol_size": 4, "opacity": 0.7}
    }
    
    # Préparation des données par statut d'éligibilité
    series_data = []
    all_category_data = []
    
    # Fonction pour calculer la taille du marqueur en fonction du nombre de candidats
    def calculate_size(count, max_count, base_size=10):
        return base_size * (1 + np.sqrt(count / max_count * 100) / 2)
    
    # Préparation des données par arrondissement
    arr_data = df_clean.groupby("Arrondissement").agg({
        'Arrondissement': 'size',
        'Long': 'mean',
        'Lat': 'mean'
    }).rename(columns={'Arrondissement': 'nb_donateur'})
    arr_data["name"] = arr_data.index
    arr_data = arr_data.reset_index(drop=True)
    
    # Convertir en format compatible pour ECharts
    arr_points = []
    max_arr_count = arr_data["nb_donateur"].max() if not arr_data.empty else 1
    
    for _, row in arr_data.iterrows():
        size = calculate_size(row["nb_donateur"], max_arr_count, base_size=15)
        arr_points.append({
            "name": str(row["name"]),
            "value": [float(row["Long"]), float(row["Lat"]), int(row["nb_donateur"])],
            "symbolSize": float(size),  # Convertir en float pour la sérialisation JSON
            "itemStyle": {"color": "#003366", "opacity": float(opacity)}
        })
    
    # Ajouter la série pour les arrondissements
    series_data.append({
        "name": "Arrondissements",
        "type": "scatter",
        "coordinateSystem": "geo",
        "data": arr_points,
        "encode": {
            "value": 2,
            "tooltip": [2]
        },
        "label": {
            "formatter": "{b}",
            "position": "right",
            "show": True,
            "color": "#000",
            "fontSize": 12
        },
        "emphasis": {
            "label": {
                "show": True
            }
        }
    })
    
    # Préparation des données pour le total des candidats par quartier
    qrt_data = df_clean.groupby("Quartier").agg({
        'Quartier': 'size',
        'Long': 'mean',
        'Lat': 'mean'
    }).rename(columns={'Quartier': 'nb_donateur'})
    qrt_data["name"] = qrt_data.index
    qrt_data = qrt_data.reset_index(drop=True)
    
    # Convertir en format compatible pour ECharts
    qrt_points = []
    max_qrt_count = qrt_data["nb_donateur"].max() if not qrt_data.empty else 1
    
    for _, row in qrt_data.iterrows():
        size = calculate_size(row["nb_donateur"], max_qrt_count)
        qrt_points.append({
            "name": str(row["name"]),
            "value": [float(row["Long"]), float(row["Lat"]), int(row["nb_donateur"])],
            "symbolSize": float(size),
            "itemStyle": {"color": "#003F80", "opacity": float(opacity)}
        })
    
    # Ajouter la série pour les quartiers
    series_data.append({
        "name": "Total candidats par quartier",
        "type": "effectScatter",
        "coordinateSystem": "geo",
        "data": qrt_points,
        "encode": {
            "value": 2,
            "tooltip": [2]
        },
        "rippleEffect": {
            "brushType": "stroke"
        },
        "showEffectOn": "render",
        "hoverAnimation": True
    })
    
    # Traiter chaque catégorie d'éligibilité
    for category, config in eligibility_categories.items():
        cat_data = df_clean[df_clean["Eligibilite"] == category]
        
        if not cat_data.empty:
            # Agréger par quartier
            grouped_cat = cat_data.groupby("Quartier").agg({
                'Quartier': 'size',
                'Long': 'mean',
                'Lat': 'mean'
            }).rename(columns={'Quartier': 'nb_donateur'})
            grouped_cat["name"] = grouped_cat.index
            grouped_cat = grouped_cat.reset_index(drop=True)
            
            # Convertir en format compatible pour ECharts
            cat_points = []
            max_cat_count = grouped_cat["nb_donateur"].max() if not grouped_cat.empty else 1
            
            for _, row in grouped_cat.iterrows():
                size = calculate_size(row["nb_donateur"], max_cat_count, base_size=config["symbol_size"])
                cat_points.append({
                    "name": f"{row['name']} ({category})",
                    "value": [float(row["Long"]), float(row["Lat"]), int(row["nb_donateur"])],
                    "symbolSize": float(size),
                    "itemStyle": {"color": config["color"], "opacity": float(config["opacity"])}
                })
                
                # Ajouter à la liste globale pour visualisation toggle
                all_category_data.append({
                    "category": category,
                    "quartier": row["name"],
                    "coords": [float(row["Long"]), float(row["Lat"])],
                    "count": int(row["nb_donateur"])
                })
            
            # Ajouter la série pour cette catégorie
            series_data.append({
                "name": category,
                "type": "scatter",
                "coordinateSystem": "geo",
                "data": cat_points,
                "encode": {
                    "value": 2,
                    "tooltip": [2]
                }
            })
    
    # Définir la palette de couleurs
    if palet_color == "blues":
        visual_range_color = ['#f7fbff', '#08519c']
    elif palet_color == "reds":
        visual_range_color = ['#fee5d9', '#a50f15']
    elif palet_color == "greens":
        visual_range_color = ['#edf8e9', '#006d2c']
    elif palet_color == "yellows":
        visual_range_color = ['#ffffd4', '#bd0026']
    else:
        visual_range_color = ['#f7fbff', '#08519c']  # Default to Blues
    
    # Définir le thème de la carte
    if style_carte == "dark":
        map_theme = "dark"
    else:
        map_theme = "light"
    
    # Calculer la position centrale pour la carte
    center_lat = df_clean["Lat"].mean()
    center_lon = df_clean["Long"].mean()
    
    # Configurer les options ECharts
    option = {
        "title": {
            "text": "Distribution des Candidats par Éligibilité",
            "left": "center",
            "top": "20px"
        },
        "backgroundColor": "#fff" if map_theme == "light" else "#333",
        "tooltip": {
            "trigger": "item",
            "formatter": """
            function(params) {
                if (params.seriesName === 'Arrondissements') {
                    return 'Arrondissement: ' + params.name + '<br/>Candidats: ' + params.value[2];
                } else if (params.seriesName === 'Total candidats par quartier') {
                    return 'Quartier: ' + params.name + '<br/>Total candidats: ' + params.value[2];
                } else {
                    return params.name + '<br/>Candidats: ' + params.value[2];
                }
            }
            """
        },
        "legend": {
            "orient": "vertical",
            "left": "left",
            "data": ["Arrondissements", "Total candidats par quartier"] + list(eligibility_categories.keys()),
            "textStyle": {
                "color": "black" if map_theme == "light" else "white"
            }
        },
        "geo": {
            "map": "world",  # ECharts utilise une carte du monde par défaut
            "roam": True,    # Permet de zoomer et déplacer la carte
            "center": [center_lon, center_lat],
            "zoom": 11,      # Zoom initial
            "scaleLimit": {
                "min": 8,
                "max": 18
            },
            "itemStyle": {
                "areaColor": "#f3f3f3" if map_theme == "light" else "#1a1a1a",
                "borderColor": "#ccc",
                "borderWidth": 0.5
            },
            "emphasis": {
                "itemStyle": {
                    "areaColor": "#e6e6e6" if map_theme == "light" else "#2a2a2a"
                },
                "label": {
                    "show": False
                }
            }
        },
        "series": series_data
    }
    
    # Convertir en JSON et revenir en dictionnaire pour s'assurer de la compatibilité
    option_json = json.dumps(option, default=lambda x: x if not hasattr(x, 'item') else x.item())
    option = json.loads(option_json)
    
    # Afficher la carte avec st_echarts
    # CORRECTION: ne pas utiliser le paramètre map avec une chaîne de caractères
    st_echarts(option, height=height, width=width)
    
    #return option


def make_donutchart_3(df, var, titre="", width=600, height=450, color_palette=None, part=True):
    """
    Crée un graphique en anneau (donut chart) avec des améliorations visuelles en utilisant ECharts.
    
    Args:
        df: DataFrame contenant les données
        var: Variable à visualiser
        titre: Titre du graphique
        width: Largeur du graphique
        height: Hauteur du graphique
        color_palette: Liste de couleurs personnalisées pour le graphique
        part: Afficher les pourcentages (True par défaut)
        
    Returns:
        Affiche le graphique dans Streamlit via ECharts
    """
    # Appliquer le style CSS personnalisé une seule fois (c'est mieux de le faire dans votre script principal)
    st.markdown("""
        <style>
        /* Vos styles CSS ici */
        .custom-echarts-container {
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
            transition: all 0.3s ease;
            border: 2px solid rgba(224, 224, 224, 0.7);
            background-color: rgba(255, 255, 255, 0.9);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.08);
        }
        
        .dark-mode .custom-echarts-container {
            background-color: rgba(30, 30, 40, 0.9);
            border-color: rgba(60, 60, 70, 0.7);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }
        
        .custom-echarts-container:hover {
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
            transform: translateY(-3px);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Créer un conteneur Streamlit avec une classe personnalisée
    container = st.container(height=400,key=25,border=True)
    
    # Agrégation des données
    data_grouped = df.groupby(var).size().reset_index(name='Effectif')
    
    # Calculer les pourcentages pour l'affichage dans les étiquettes
    total = data_grouped['Effectif'].sum()
    data_grouped['Pourcentage'] = (data_grouped['Effectif'] / total * 100).round(1)
    
    # Trier par effectif décroissant pour une meilleure présentation
    data_grouped = data_grouped.sort_values('Effectif', ascending=False)
    
    # Préparation des données pour ECharts
    categories = data_grouped[var].tolist()
    values = data_grouped['Effectif'].tolist()
    percentages = data_grouped['Pourcentage'].tolist()
    
    # Couleurs par défaut si non spécifiées
    if color_palette is None:
        # Assurez-vous que 'palette' est défini ou utilisez une palette par défaut
        try:
            color_palette = palette
        except NameError:
            color_palette = ["#5470c6", "#91cc75", "#fac858", "#ee6666", "#73c0de", "#3ba272", "#fc8452", "#9a60b4", "#ea7ccc"]
    
    # Limiter les couleurs à la longueur des données
    colors = color_palette[:len(categories)]
    
    # Construction des données pour les séries
    series_data = []
    for i, (cat, val, pct) in enumerate(zip(categories, values, percentages)):
        # Déterminer si ce segment doit être légèrement détaché
        offset = 10 if (i == 0) and (len(data_grouped) > 2) else 0
        
        item = {
            "name": cat,
            "value": val,
            "itemStyle": {"color": colors[i % len(colors)]},
            "tooltip": {"formatter": f"<b>{cat}</b><br>Effectif: {val} ({pct}%)"},
        }
        
        # Ajouter l'offset pour le premier segment si nécessaire
        if offset > 0:
            item["offset"] = offset
            
        series_data.append(item)
    
    # Configuration du graphique
    options = {
        "title": {
            "text": titre,
            "left": "center",
            "textStyle": {
                "fontWeight": "bold",
                "fontSize": 18
            }
        },
        "tooltip": {
            "trigger": "item",
            "backgroundColor": "rgba(255, 255, 255, 0.9)",
            "borderColor": "#ccc",
            "borderWidth": 1,
            "textStyle": {
                "color": "#333"
            },
            "formatter": "{b}: {c} ({d}%)"
        },
        "legend": {
            "orient": "horizontal",
            "bottom": "bottom",
            "left": "center",
            "data": categories
        },
        "series": [
            {
                "name": var,
                "type": "pie",
                "radius": ["40%", "70%"],  # Effet donut
                "center": ["50%", "50%"],
                "avoidLabelOverlap": False,
                "itemStyle": {
                    "borderRadius": 4,
                    "borderColor": "#fff",
                    "borderWidth": 2
                },
                "label": {
                    "show": part,
                    "position": "inside",
                    "formatter": "{b}\n{d}%" if part else "{b}",
                    "fontSize": 10,
                    "fontWeight": "bold"
                },
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)"
                    },
                    "label": {
                        "show": True,
                        "fontSize": 12,
                        "fontWeight": "bold"
                    }
                },
                "labelLine": {
                    "show": False
                },
                "data": series_data
            }
        ]
    }
    
    # Ajout du nombre total au centre
    options["graphic"] = [{
        "type": "text",
        "left": "center",
        "top": "50%",
        "style": {
            "text": f"{total:,}\nTotal",
            "textAlign": "center",
            "fill": "#333",
            "fontSize": 16,
            "fontWeight": "bold"
        }
    }]
    
    # Dans le conteneur Streamlit, créer une div personnalisée
    with container:
        #pass # Créer une div avec style personnalisé
        
        st_echarts(
                options=options,
                height=f"{height}px",
                width="100%",  # Pour utiliser toute la largeur disponible
            )
        #st.markdown(f'<div class="custom-echarts-container"> {a}</div>', unsafe_allow_html=True)
            
        # Affichage dans Streamlit
    
        
        # Fermer la div
    #st.markdown('</div>', unsafe_allow_html=True)
 
# Utilisation dans Streamlit

def make_school_map(df, style_carte="OpenStreetMap", palet_color="blues", opacity=0.8, width=700, height=600):
    """
    Fonction pour créer une carte choroplèthe interactive montrant la distribution des candidats
    par statut d'éligibilité à travers différents quartiers et arrondissements, en utilisant Folium.
    
    Parameters:
    -----------
    df : GeoDataFrame
        DataFrame contenant les données géospatiales des candidats
    style_carte : str, default="OpenStreetMap"
        Style de fond de carte Folium (options: "OpenStreetMap", "cartodbpositron", "cartodbdark_matter", etc.)
    palet_color : str, default="Blues"
        Palette de couleurs pour la choroplèthe (options: "Blues", "Reds", "Greens", "YlOrRd", etc.)
    opacity : float, default=0.8
        Opacité des polygones de la choroplèthe (0-1)
    width : int, default=700
        Largeur de la carte en pixels
    height : int, default=600
        Hauteur de la carte en pixels
    """
    
    
    # Nettoyer les données en supprimant les lignes avec des coordonnées NaN
    df_clean = df.dropna(subset=['Latitude', 'Longitude']).copy()
    
    # Définition des catégories d'éligibilité et des couleurs associées
    questionnaire_categories = {
        "Enseignant": {"color": ["#D6182A", "#EF7E5F", "#381FF5"], "size_factor": 3, "opacity": 0.75},
        "Elève": {"color": [f"rgb({255*(19-i)/19}, 0 , {255*i/19}" for i in range(18)], "size_factor": 7, "opacity": 0.7},
    }
    
    # Préparation des données par statut d'éligibilité
    dfs_by_questinaire = {}
    for category in questionnaire_categories.keys():
        geo_data = df_clean[df_clean["Type"] == category]
        
        if not geo_data.empty:
            dfs_by_questinaire[category] = geo_data.groupby("Etablissement").agg({
                'Type': 'size',
                'Latitude': 'first',
                'Longitude': 'first'
            }).rename(columns={'Type': 'nb_questionnaire'})
            dfs_by_questinaire[category]["Qrt"] = dfs_by_questinaire[category].index
            # S'assurer qu'il n'y a pas de NaN dans les coordonnées agrégées
            dfs_by_questinaire[category] = dfs_by_questinaire[category].dropna(subset=['Latitude', 'Longitude'])
            #École
    # Préparation des données pour la choroplèthe par arrondissement
    df_chlph = df_clean.groupby("Région").agg({
        'Région': 'size',
        'geometry': 'first',
        'Latitude': 'first',
        'Longitude': 'first'
    }).rename(columns={'Région': 'nb_questionnaire'})
    df_chlph["reg"] = df_chlph.index
    # S'assurer qu'il n'y a pas de NaN dans les coordonnées agrégées
    df_chlph = df_chlph.dropna(subset=['Latitude', 'Longitude'])
    df_chlph = gpd.GeoDataFrame(df_chlph, geometry='geometry')
    
    # S'assurer que le CRS est défini - Utiliser EPSG:4326 (WGS84) pour compatibilité avec Folium
    if df_chlph.crs is None:
        df_chlph.set_crs(epsg=4326, inplace=True)
    else:
        # Si un CRS est déjà défini mais différent de WGS84, le convertir
        if df_chlph.crs != 'EPSG:4326':
            df_chlph = df_chlph.to_crs(epsg=4326)

    # Total des candidats par quartier
    df_pts = df_clean.groupby("Etablissement").agg({
        'Etablissement': 'size',
        'Latitude': 'first',
        'Longitude': 'first'
    }).rename(columns={'Etablissement': 'nb_questionnaire'})
    df_pts["ecole"] = df_pts.index
    # S'assurer qu'il n'y a pas de NaN dans les coordonnées agrégées
    df_pts = df_pts.dropna(subset=['Latitude', 'Longitude'])
    
    # Vérifier si df_pts est vide après filtrage
    if df_pts.empty:
        st.error("Aucune coordonnée valide trouvée dans les données. Impossible de créer la carte.")
        return None
    
    # Création de la carte Folium
    center_lat = df_pts["Latitude"].mean()
    center_lon = df_pts["Longitude"].mean()
    
    # Dictionnaire de correspondance entre les styles dans votre fonction originale et ceux de Folium
    tile_styles = {
        "carto-positron": "cartodbpositron",
        "carto-darkmatter": "cartodbdark_matter",
        "open-street-map": "OpenStreetMap",
        "CartoDB positron": "cartodbpositron", 
        "CartoDB dark_matter": "cartodbdark_matter"
    }
    
    # Utiliser le style approprié ou OpenStreetMap par défaut
    actual_style = tile_styles.get(style_carte, style_carte)
    
    # Création de la carte avec le style approprié
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=6.5,
        tiles=actual_style,
        width=width,
        height=height
    )
    
    # Ajout de la couche choroplèthe pour les arrondissements
    # Création d'une échelle de couleur avec la bonne classe de branca.colormap
    if palet_color == "blues":
        color_range = ['#f7fbff', '#08519c']
    elif palet_color == "reds":
        color_range = ['#fee5d9', '#a50f15']
    elif palet_color == "greens":
        color_range = ['#a50f15', '#006d2c']
    elif palet_color == "viridis":
        color_range = ['#fde725', '#440154']
    else:
        color_range = ['#f7fbff', '#08519c']  # Default to Blues
    
    # Création des clusters uniquement pour les arrondissements
    region_cluster = MarkerCluster(name="Région").add_to(m)
    
    if not df_chlph.empty:
        colormap = cm.LinearColormap(
            colors=color_range, 
            vmin=df_chlph["nb_questionnaire"].min(),
            vmax=df_chlph["nb_questionnaire"].max(),
            caption="Nombre de Questionnaire par Région"
        )
        
        # Convertir le GeoDataFrame en GeoJSON
        geo_json_data = df_chlph.__geo_interface__
        
        # Ajout des polygones des arrondissements en utilisant le GeoJSON préparé
        folium.GeoJson(
            geo_json_data,
            style_function=lambda feature: {
                'fillColor': colormap(feature['properties']['nb_questionnaire']),
                'color': 'white',
                'weight': 0.5,
                'fillOpacity': opacity
            },
            tooltip=folium.GeoJsonTooltip(
                fields=['reg', 'nb_questionnaire'],
                aliases=['Région:', 'Nombre de Questionnaire:'],
                style="background-color: white; color: #333333; font-family: arial; font-size: 14px; padding: 10px;"
            )
        ).add_to(m)
        
        # Ajout des étiquettes d'arrondissement et des marqueurs au cluster d'arrondissements
        for idx, row in df_chlph.iterrows():
            # Étiquettes d'arrondissement
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                icon=folium.DivIcon(
                    icon_size=(150, 40),
                    icon_anchor=(75, 28),
                    html=f'<div style="font-size: 12px; font-weight: bold; text-align: center">{row["reg"]}</div>'
                )
            ).add_to(m)
            
            # Marqueurs d'arrondissement pour le cluster
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=f"<b>Région {row['reg']}</b><br>Total Questionnaire: <b>{row['nb_questionnaire']}</b>",
                icon=folium.Icon(color='blue')
            ).add_to(region_cluster)
        
        # Ajout de la légende de couleur
        colormap.add_to(m)

    # Fonction pour calculer la taille du cercle en fonction du nombre de candidats
    def calculate_radius(count, max_count, base_size=5):
        return base_size * np.sqrt(count / max_count * 100)
    
    max_count = df_pts["nb_questionnaire"].max() if not df_pts.empty else 1
    
    # Création d'un groupe de features pour les cercles des quartiers
    #ecole_feature_group = folium.FeatureGroup(name="Total Questinnaire par Ecole")
    
    # Ajout des marqueurs pour le total des candidats (directement à la carte, pas de cluster)
    """
    for idx, row in df_pts.iterrows():
        radius = calculate_radius(row["nb_questionnaire"], max_count)
        popup_text = f"<b>{row['ecole']}</b><br>Total Questionnaire: <b>{row['nb_questionnaire']}</b>"
        
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=radius,
            color='#003F80',
            fill=True,
            fill_color='#003F80',
            fill_opacity=0.8,
            popup=folium.Popup(popup_text, max_width=300)
        ).add_to(ecole_feature_group)
    """
    # Ajout du groupe de features à la carte
    #ecole_feature_group.add_to(m)
        
    # Ajout des marqueurs pour chaque catégorie d'éligibilité (directement à la carte, pas de cluster)
    for category, df_pts_cat in dfs_by_questinaire.items():
        if df_pts_cat.empty:
            continue
            
        config = questionnaire_categories[category]
        
        # Création d'un groupe de features pour cette catégorie
        category_feature_group = folium.FeatureGroup(name=category)
        
        max_count_cat = df_pts_cat["nb_questionnaire"].max() if not df_pts_cat.empty else 1
        
        for idx, row in df_pts_cat.iterrows():
            radius = calculate_radius(row["nb_questionnaire"], max_count_cat, base_size=config["size_factor"]/4)
            popup_text = f"<b>{row['Qrt']}</b><br>Questionnaire {category}: <b>{row['nb_questionnaire']}</b>"
            
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=radius,
                color=config["color"],
                fill=True,
                fill_color=config["color"],
                fill_opacity=config["opacity"],
                popup=folium.Popup(popup_text, max_width=300)
            ).add_to(category_feature_group)
        
        # Ajout du groupe de features à la carte
        category_feature_group.add_to(m)
            
    # Ajout du contrôle de couches
    folium.LayerControl(collapsed=False).add_to(m)
    # Déplacer la légende entièrement à droite
    legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; right: 20px; 
                    width: 220px;
                    background-color: white;
                    border: 2px solid grey;
                    border-radius: 5px;
                    z-index: 9999;
                    font-size: 14px;
                    padding: 10px;
                    opacity: 0.9;">
            <div style="text-align: center; margin-bottom: 5px;"><b>Légende des points</b></div>
    '''
    
    # Ajouter une entrée de légende pour les cercles totaux
    legend_html += f'''
        <div style="margin-bottom: 7px;">
            <div style="display: inline-block; 
                      width: 15px; 
                      height: 15px; 
                      border-radius: 50%; 
                      background-color: #003F80;
                      margin-right: 5px;
                      vertical-align: middle;"></div>
            <span style="vertical-align: middle;">Total Questionnaire</span>
        </div>
    '''
    
    # Ajouter des entrées pour chaque catégorie de questionnaire
    for category, config in questionnaire_categories.items():
        if category in dfs_by_questinaire and not dfs_by_questinaire[category].empty:
            legend_html += f'''
                <div style="margin-bottom: 7px;">
                    <div style="display: inline-block; 
                              width: 15px; 
                              height: 15px; 
                              border-radius: 50%; 
                              background-color: {config['color']};
                              opacity: {config['opacity']};
                              margin-right: 5px;
                              vertical-align: middle;"></div>
                    <span style="vertical-align: middle;">{category}</span>
                </div>
            '''
    
    # Fermer la div de la légende
    legend_html += '''
        </div>
    '''
    
    # Ajouter la légende à la carte
    m.get_root().html.add_child(folium.Element(legend_html))
    
    
    # Ajout d'un titre 
    title_html = '''
        <div style="position: fixed; 
                    top: 10px; left: 1px; width: 600px; height: 45px; 
                    background-color: white; border-radius: 5px;
                    z-index: 9999; font-size: 20px; font-family: Arial;
                    padding: 10px; text-align: center; color: #333;">
            <b>Distribution des questionnaire par Type</b>
        </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Affichage avec Streamlit
    folium_static(m, width=width, height=height)
    
    return m


def make_school_map2(df, style_carte="OpenStreetMap", palet_color="blues", opacity=0.8, width=700, height=600):
    """
    Fonction pour créer une carte choroplèthe interactive montrant la distribution des candidats
    par statut d'éligibilité à travers différents quartiers et arrondissements, en utilisant Folium.
    
    Parameters:
    -----------
    df : GeoDataFrame
        DataFrame contenant les données géospatiales des candidats
    style_carte : str, default="OpenStreetMap"
        Style de fond de carte Folium (options: "OpenStreetMap", "cartodbpositron", "cartodbdark_matter", etc.)
    palet_color : str, default="Blues"
        Palette de couleurs pour la choroplèthe (options: "Blues", "Reds", "Greens", "YlOrRd", etc.)
    opacity : float, default=0.8
        Opacité des polygones de la choroplèthe (0-1)
    width : int, default=700
        Largeur de la carte en pixels
    height : int, default=600
        Hauteur de la carte en pixels
    """
    
    
    # Nettoyer les données en supprimant les lignes avec des coordonnées NaN
    df_clean = df.dropna(subset=['Latitude', 'Longitude']).copy()
    
    # Définition des catégories d'éligibilité et des couleurs associées
    questionnaire_categories = {
        "Enseignant": {"color": "#0073E6", "size_factor": 3, "opacity": 0.75},
        "Elève": {"color": "#B3D9FF", "size_factor": 7, "opacity": 0.7},
    }
    #École
    # Préparation des données par Etablissement
    dfs_by_questinaire = {}
    for category in questionnaire_categories.keys():
        geo_df = df_clean[df_clean["Type"] == category]
        
        if not geo_df.empty:
            dfs_by_questinaire[category] = geo_df.groupby("Etablissement").agg({
                'Type': 'size',
                'Latitude': 'first',
                'Total_ense':'sum',
                'Total_enfa':'sum',
                'Longitude': 'first'
            }).rename(columns={'Type': 'nb_questionnaire'})
            dfs_by_questinaire[category]["Qrt"] = dfs_by_questinaire[category].index
            # S'assurer qu'il n'y a pas de NaN dans les coordonnées agrégées
            dfs_by_questinaire[category] = dfs_by_questinaire[category].dropna(subset=['Latitude', 'Longitude'])

    # Préparation des données pour la choroplèthe par arrondissement
    df_chlph = df_clean.groupby("Région").agg({
        'Région': 'size',
        'geometry': 'first',
        'Total_ense':'sum',
        'Total_enfa':'sum',
        'Reg_ens':'first',
        'Reg_enf':'first',
        'Latitude': 'first',
        'Longitude': 'first'
    }).rename(columns={'Région': 'nb_questionnaire'})
    df_chlph["reg"] = df_chlph.index
    df_chlph["Evolution"] = df_chlph["nb_questionnaire"]/ (df_chlph["Reg_ens"] + df_chlph["Reg_enf"])
    # S'assurer qu'il n'y a pas de NaN dans les coordonnées agrégées
    df_chlph = df_chlph.dropna(subset=['Latitude', 'Longitude'])
    df_chlph = gpd.GeoDataFrame(df_chlph, geometry='geometry')
    
    # S'assurer que le CRS est défini - Utiliser EPSG:4326 (WGS84) pour compatibilité avec Folium
    if df_chlph.crs is None:
        df_chlph.set_crs(epsg=4326, inplace=True)
    else:
        # Si un CRS est déjà défini mais différent de WGS84, le convertir
        if df_chlph.crs != 'EPSG:4326':
            df_chlph = df_chlph.to_crs(epsg=4326)

    # Total des candidats par quartier
    df_pts = df_clean.groupby("Etablissement").agg({
        'Etablissement': 'size',
        'Total_ense':'sum',
        'Total_enfa':'sum',
        'Latitude': 'first',
        'Longitude': 'first'
    }).rename(columns={'Etablissement': 'nb_questionnaire'})
    df_pts["ecole"] = df_pts.index
    # S'assurer qu'il n'y a pas de NaN dans les coordonnées agrégées
    df_pts = df_pts.dropna(subset=['Latitude', 'Longitude'])
    
    # Vérifier si df_pts est vide après filtrage
    if df_pts.empty:
        st.error("Aucune coordonnée valide trouvée dans les données. Impossible de créer la carte.")
        return None
    
    # Création de la carte Folium
    center_lat = df_pts["Latitude"].mean()+0.9
    center_lon = df_pts["Longitude"].mean()+0.5
    
    # Dictionnaire de correspondance entre les styles dans votre fonction originale et ceux de Folium
    tile_styles = {
        "carto-positron": "cartodbpositron",
        "carto-darkmatter": "cartodbdark_matter",
        "open-street-map": "OpenStreetMap",
        "CartoDB positron": "cartodbpositron", 
        "CartoDB dark_matter": "cartodbdark_matter"
    }
    
    # Utiliser le style approprié ou OpenStreetMap par défaut
    actual_style = tile_styles.get(style_carte, style_carte)
    
    # Création de la carte avec le style approprié
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=6.5,
        tiles=actual_style,
        width=width,
        height=height,
        max_lat=df_pts["Latitude"].max(),
        min_lat=df_pts["Latitude"].min(),
        max_lon=df_pts["Longitude"].max(),
        min_lon=df_pts["Longitude"].min()
        
        
    )
    
    # Ajout de la couche choroplèthe pour les Régions
    # Création d'une échelle de couleur avec la bonne classe de branca.colormap
    if palet_color == "blues":
        color_range = ['#f7fbff', '#08519c']
    elif palet_color == "reds":
        color_range = ['#fee5d9', '#a50f15']
    elif palet_color == "greens":
        color_range = ['#edf8e9', '#006d2c']
    elif palet_color == "viridis":
        color_range = ['#fde725', '#440154']
    elif palet_color == "orange":
        color_range = ['#fee8c8', '#e34a33']
    elif palet_color == "yellow":
        color_range = ['#ffffb2', '#bd0026']
    elif palet_color == "purple":
        color_range = ['#f7f4f9', '#756bb1']
    elif palet_color == "pink":
        color_range = ['#f7f3f8', '#762a83']
    elif palet_color == "brown":
        color_range = ['#f5f5f0', '#8c510a']
    else:
        color_range = ['#f7fbff', '#08519c']  # Default to Blues
    
    # Création des clusters uniquement pour les arrondissements
    region_cluster = MarkerCluster(name="Région").add_to(m)
    
    if not df_chlph.empty:
        colormap = cm.LinearColormap(
            colors=color_range, 
            vmin=0,
            #vmin=df_chlph["nb_questionnaire"].min(),
            #vmax=df_chlph["nb_questionnaire"].max(),
            vmax=1,
            caption="Taux d'évolution",
            max_labels=15
        )
        
        # Convertir le GeoDataFrame en GeoJSON
        geo_json_data = df_chlph.__geo_interface__
        # Ajout des polygones des arrondissements en utilisant le GeoJSON préparé
        """
        folium.GeoJson(
            geo_json_data,
            style_function=lambda feature: {
            'fillColor': colormap(feature['properties']['Evolution']),
            'color': 'white',
            'weight': 0.5,
            'fillOpacity': opacity
            },
            tooltip=folium.GeoJsonTooltip(
            fields=['reg', 'nb_questionnaire', 'Total_ense', 'Total_enfa'],
            aliases=['Région:', 'Nombre de Questionnaire:', 'Total Enseignants:', 'Total Enfants:'],
            style="background-color: white; color: #333333; font-family: arial; font-size: 14px; padding: 10px;",
            labels=True,
            sticky=True,
            localize=True,
            toLocaleString=True,
            formatters={
                'Total_enfa': lambda x: f"{x} / {df_chlph.loc[df_chlph['reg'] == x, 'Reg_enf'].values[0]}",
                'Total_ense': lambda x: f"{x} / {df_chlph.loc[df_chlph['reg'] == x, 'Reg_ens'].values[0]}"
            }
            )
        ).add_to(m)
        """
        folium.GeoJson(
            geo_json_data,
            style_function=lambda feature: {
            'fillColor': colormap(feature['properties']['Evolution']),
            'color': 'white',
            'weight': 0.5,
            'fillOpacity': opacity
            },
            tooltip=folium.GeoJsonTooltip(
            fields=['reg', 'nb_questionnaire', 'Total_ense', 'Total_enfa'],
            aliases=['Région:', 'Nombre de Questionnaire:', 'Total Enseignants:', 'Total Enfants:'],
            style="background-color: white; color: #333333; font-family: arial; font-size: 14px; padding: 10px;"
            )
        ).add_to(m)
        
        # Ajout des polygones des arrondissements en utilisant le GeoJSON préparé
       
        # Ajout des étiquettes d'arrondissement et des marqueurs au cluster d'arrondissements
        for idx, row in df_chlph.iterrows():
            # Étiquettes des pourcentages d'évolution
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                icon=folium.DivIcon(
                    icon_size=(150, 40),
                    icon_anchor=(75, 28),
                    html=f'<div style="font-size: 25px; font-weight: bold; text-align: center">{100*round(row["Evolution"],2)} %</div>'
                )
            ).add_to(m)
            
            # Marqueurs d'arrondissement pour le cluster
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=f"<b>Région {row['reg']}</b><br>Total Questionnaire: <b>{row['nb_questionnaire']}</b>",
                icon=folium.Icon(color='blue')
            ).add_to(region_cluster)
        
        # Ajout de la légende de couleur - Déplacée sur le côté gauche
        colormap.add_to(m)
        # Modifier la position de la légende de couleur à gauche via CSS
        colormap_css = """
        <style>
        .leaflet-right .leaflet-control {
            /* Cacher la légende à droite */
            display: none;
        }
        
        /* Repositionner la légende à gauche */
        .leaflet-left .info.legend {
            margin-left: 10px;
            margin-bottom: 10px;
        }
        </style>
        """
        # Ajout du CSS à la carte
        m.get_root().html.add_child(folium.Element(colormap_css))
        
        # Copier la légende à gauche
        

    # Fonction pour calculer la taille du cercle en fonction du nombre de candidats
    def calculate_radius(count, max_count, base_size=5):
        return base_size * np.sqrt(count / max_count * 100)
    
    max_count = df_pts["nb_questionnaire"].max() if not df_pts.empty else 1
    
        
    # Ajout des marqueurs pour chaque catégorie d'éligibilité (directement à la carte, pas de cluster)
    for category, df_pts_cat in dfs_by_questinaire.items():
        if df_pts_cat.empty:
            continue
            
        config = questionnaire_categories[category]
        
        # Création d'un groupe de features pour cette catégorie
        category_feature_group = folium.FeatureGroup(name=category)
        
        max_count_cat = df_pts_cat["nb_questionnaire"].max() if not df_pts_cat.empty else 1
        #couleur des points
        enfant_color=[f"rgb({255*(19-i)/19} , {255*i/19}, 0" for i in range(18)]
        enseignant_color=["#D6182A", "#EF7E5F", "#228A22"]
        
        for idx, row in df_pts_cat.iterrows():
            tval=18 if category=="Elève" else 3
            radius = calculate_radius(row["nb_questionnaire"], max_count_cat, base_size=config["size_factor"]/4)
            popup_text = f"<b>{row['Qrt']}</b><br>Questionnaire {category}: <b>{row['nb_questionnaire']} / {tval}</b>" 
            
            
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=radius,
                color=enfant_color[row['nb_questionnaire']-1] if category == "Elève" else enseignant_color[row['nb_questionnaire']-1],
                fill=True,
                fill_color=enfant_color[row['nb_questionnaire']-1] if category == "Elève" else enseignant_color[row['nb_questionnaire']-1],
                fill_opacity=0.8,
                popup=folium.Popup(popup_text, max_width=300)
            ).add_to(category_feature_group)
        
        # Ajout du groupe de features à la carte
        category_feature_group.add_to(m)
            
    # Ajout du contrôle de couches (déplacer en haut à gauche)
    layer_control = folium.LayerControl(collapsed=True, draggable=True, position='topleft')
    layer_control.add_to(m)
    
    # Déplacer la légende à gauche
    legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; left: 20px; 
                    width: 220px;
                    background-color: white;
                    border: 2px solid grey;
                    border-radius: 5px;
                    z-index: 9999;
                    font-size: 14px;
                    padding: 10px;
                    opacity: 0.9;">
            <div style="text-align: center; margin-bottom: 5px;"><b>Légende des points</b></div>
    '''
    
    # Ajouter une entrée de légende pour les cercles totaux
    legend_html += f'''
        <div style="margin-bottom: 7px;">
            <div style="display: inline-block; 
                      width: 15px; 
                      height: 15px; 
                      border-radius: 50%; 
                      background-color: #003F80;
                      margin-right: 5px;
                      vertical-align: middle;"></div>
            <span style="vertical-align: middle;">Total Questionnaire</span>
        </div>
    '''
    
    # Ajouter des entrées pour chaque catégorie de questionnaire
    for category, config in questionnaire_categories.items():
        if category in dfs_by_questinaire and not dfs_by_questinaire[category].empty:
            legend_html += f'''
                <div style="margin-bottom: 7px;">
                    <div style="display: inline-block; 
                              width: 15px; 
                              height: 15px; 
                              border-radius: 50%; 
                              background-color: {config['color']};
                              opacity: {config['opacity']};
                              margin-right: 5px;
                              vertical-align: middle;"></div>
                    <span style="vertical-align: middle;">{category}</span>
                </div>
            '''
    
    # Fermer la div de la légende
    legend_html += '''
        </div>
    '''
    
    # Ajouter la légende à la carte
    m.get_root().html.add_child(folium.Element(legend_html))
    
    
    # Ajout d'un titre - centré en haut
    title_html = '''
        <div style="position: fixed; 
                    top: 10px; left: 50%; transform: translateX(-50%); 
                    width: 600px; height: 45px; 
                    background-color: white; border-radius: 5px;
                    z-index: 9999; font-size: 20px; font-family: Arial;
                    padding: 10px; text-align: center; color: #333;">
            <b>Distribution des questionnaire par Type</b>
        </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Affichage avec Streamlit
    folium_static(m, width=width, height=height)

    return m


def make_st_heatmap_echat(df, title="", height="700px"):
            """
            Create an interactive heatmap using echarts
            
            Parameters:
            -----------
            df : pandas.DataFrame
                The crosstab or pivot table to visualize
            title : str
                Title of the heatmap
            height : str
                Height of the chart (default "600px")
            """
            # Get dimensions and prepare data
            x_labels = df.columns.tolist()
            y_labels = df.index.tolist()
            
            # Determine which axis should be longer
            if len(x_labels) < len(y_labels):
                x_labels, y_labels = y_labels, x_labels
                df = df.T
                
            data = []
            for i, y_val in enumerate(y_labels):
                for j, x_val in enumerate(x_labels):
                    data.append([j, i, float(df.iloc[i, j])])
            
            options = {
                "tooltip": {"position": 'top'},
                "grid": {
                    "height": '55%',
                    "top": '1%'
                },
                "xAxis": {
                    "type": 'category',
                    "data": x_labels,
                    "splitArea": {"show": True},
                    "axisLabel": {
                        "rotate": 90,
                        "interval": 0,
                        "fontSize": 8,
                        "width": 50,
                        "overflow": "truncate"
                    }
                },
                "yAxis": {
                    "type": 'category',
                    "data": y_labels,
                    "splitArea": {"show": True}
                },
                "visualMap": {
                    "min": 0,
                    "max": max([d[2] for d in data]),
                    "calculable": True,
                    "orient": 'vertical',
                    "right": '5%',
                    "bottom": '50%'
                },
                "series": [{
                    "name": "Charge accomplie" ,
                    "type": 'heatmap',
                    "data": data,
                    "label": {"show": True},
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowColor": 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }]
            }

            st.write(title)
            st_echarts(options=options, height=height)
            
            
def make_st_heatmap_echat2(df, title="", height="700px", cle="bdjbdc"):
    """
    Create an interactive heatmap using echarts
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The crosstab or pivot table to visualize
    title : str
        Title of the heatmap
    height : str
        Height of the chart (default "600px")
    """
    # Convert timestamps in index and columns to strings
    df.columns = [str(col) for col in df.columns]
    df.index = [str(idx) for idx in df.index]
    
    x_labels = df.columns.tolist()
    y_labels = df.index.tolist()
    
    # Determine which axis should be longer
    if len(x_labels) < len(y_labels):
        x_labels, y_labels = y_labels, x_labels
        df = df.T

    data = []
    for i, y_val in enumerate(y_labels):
        for j, x_val in enumerate(x_labels):
            value = df.iloc[i, j]
            try:
                value = float(value)
            except:
                value = 0  # ou np.nan si tu veux ignorer
            data.append([j, i, value])

    options = {
        "tooltip": {"position": 'top'},
        "grid": {
            "height": '87%',
            "top": '1%'
        },
        "xAxis": {
            "type": 'category',
            "data": x_labels,
            "splitArea": {"show": True},
            "axisLabel": {
                "rotate": 45 if len(x_labels)>5 else 0,
                "interval": 0,
                "fontSize": 14,
                "width": 50,
                "overflow": "truncate"
            }
        },
        "yAxis": {
            "type": 'category',
            "data": y_labels,
            "splitArea": {"show": True}
        },
        "visualMap": {
            "min": 0,
            "max": max([d[2] for d in data]),
            "calculable": True,
            "orient": 'vertical',
            "right": '3%',
            "bottom": '50%'
        },
        "series": [{
            "name": "Charge accomplie",
            "type": 'heatmap',
            "data": data,
            "label": {"show": True},
            "emphasis": {
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowColor": 'rgba(0, 0, 0, 0.5)'
                }
            }
        }]
    }

    st.write(title)
    st_echarts(options=options, height=height, key=cle)
