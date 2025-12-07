# remove.py - Application complète d'analyse démographique
# Installation : pip install streamlit numpy plotly scipy pandas xlsxwriter
# Exécution : streamlit run remove.py

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import pandas as pd
from io import BytesIO

# ==============================================
# CONFIGURATION DE LA PAGE
# ==============================================

st.set_page_config(
    page_title="Analyse Démographique Avancée",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================
# CSS PERSONNALISÉ
# ==============================================

st.markdown("""
<style>
    /* Style général */
    .main {
        padding: 2rem;
    }
    
    /* Titres */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #1E3A8A, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #1E3A8A;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3B82F6;
    }
    
    /* Cartes */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    .metric-title {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .metric-delta {
        font-size: 0.85rem;
        opacity: 0.8;
    }
    
    /* Formules mathématiques */
    .formula-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #3B82F6;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .formula-title {
        font-size: 1rem;
        font-weight: 600;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    
    .formula-equation {
        font-family: "Cambria Math", serif;
        font-size: 1.1rem;
        color: #374151;
        text-align: center;
        padding: 0.5rem;
        background: white;
        border-radius: 5px;
        border: 1px solid #e5e7eb;
    }
    
    .formula-explanation {
        font-size: 0.9rem;
        color: #6B7280;
        margin-top: 0.5rem;
        line-height: 1.5;
    }
    
    /* Boutons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Onglets */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #F0F2F6;
        border-radius: 10px 10px 0 0;
        padding: 1rem 2rem;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Badges */
    .badge-excellent {
        background-color: #10B981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .badge-good {
        background-color: #3B82F6;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .badge-acceptable {
        background-color: #F59E0B;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .badge-poor {
        background-color: #EF4444;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================
# DONNÉES DÉMOGRAPHIQUES
# ==============================================

Age = np.array([
    0.00, 1.00, 2.00, 3.00, 4.00, 5.00, 6.00, 7.00, 8.00, 9.00,
    10.00, 11.00, 12.00, 13.00, 14.00, 15.00, 16.00, 17.00, 18.00, 19.00,
    20.00, 21.00, 22.00, 23.00, 24.00, 25.00, 26.00, 27.00, 28.00, 29.00,
    30.00, 31.00, 32.00, 33.00, 34.00, 35.00, 36.00, 37.00, 38.00, 39.00,
    40.00, 41.00, 42.00, 43.00, 44.00, 45.00, 46.00, 47.00, 48.00, 49.00,
    50.00, 51.00, 52.00, 53.00, 54.00, 55.00, 56.00, 57.00, 58.00, 59.00,
    60.00, 61.00, 62.00, 63.00, 64.00, 65.00, 66.00, 67.00, 68.00, 69.00,
    70.00, 71.00, 72.00, 73.00, 74.00, 75.00, 76.00, 77.00, 78.00, 79.00,
    80.00, 81.00, 82.00, 83.00, 84.00, 85.00, 86.00, 87.00, 88.00, 89.00,
    90.00, 91.00, 92.00, 93.00, 94.00, 95.00, 96.00, 97.00, 98.00, 99.00,
    100.00, 101.00, 102.00, 103.00, 107.00, 108.00, 109.00, 110.00
])

Homme = np.array([
    2637, 2258, 2575, 2830, 2884, 2856, 2940, 3028, 3199, 2582,
    3323, 2474, 3064, 2955, 2650, 3020, 2395, 2408, 2631, 2047,
    2793, 1552, 2106, 1821, 1690, 2174, 1509, 1402, 1534, 1097,
    2276, 923, 1455, 1208, 1129, 1691, 1135, 1119, 1129, 825,
    1532, 717, 1073, 747, 662, 1131, 681, 674, 690, 520,
    1066, 439, 626, 512, 473, 568, 431, 443, 410, 344,
    709, 303, 475, 394, 300, 403, 281, 272, 242, 195,
    445, 183, 254, 163, 135, 171, 100, 120, 98, 49,
    151, 52, 85, 55, 40, 38, 33, 29, 19, 19,
    34, 8, 18, 12, 9, 12, 10, 5, 3, 43,
    6, 1, 1, 0, 1, 1, 1, 1
])

Femme = np.array([
    2552, 2136, 2381, 2735, 2651, 2674, 2692, 2802, 2707, 2234,
    2984, 2083, 2727, 2518, 2432, 2604, 2372, 2257, 2575, 2106,
    2908, 1629, 2275, 1911, 1842, 2422, 1602, 1514, 1604, 1158,
    2441, 965, 1372, 1316, 1090, 1863, 1181, 1125, 1042, 914,
    1579, 653, 999, 734, 636, 1009, 618, 685, 681, 591,
    1125, 535, 656, 533, 465, 641, 450, 434, 406, 323,
    817, 376, 506, 370, 290, 423, 271, 252, 251, 212,
    512, 205, 267, 149, 98, 189, 101, 129, 88, 65,
    200, 73, 89, 56, 42, 59, 19, 25, 24, 27,
    54, 11, 26, 10, 8, 10, 4, 5, 6, 23,
    7, 0, 3, 2, 1, 0, 0, 1
])

Total = Homme + Femme

# ==============================================
# FONCTIONS D'ANALYSE
# ==============================================

def get_first_digit(number):
    """Extrait le premier chiffre significatif."""
    if np.isnan(number) or number == 0:
        return None
    num_str = str(abs(number))
    num_str = num_str.lstrip('-0.')
    return int(num_str[0]) if num_str else None

def calculate_whipple(ages, populations, age_min=23, age_max=62):
    """Calcule l'indice de Whipple."""
    mask = (ages >= age_min) & (ages <= age_max)
    age_subset = ages[mask]
    pop_subset = populations[mask]
    pop_0_5 = pop_subset[(age_subset % 10 == 0) | (age_subset % 10 == 5)].sum()
    pop_total = pop_subset.sum()
    return (pop_0_5 / pop_total) * 100 if pop_total > 0 else np.nan

def calculate_myers(ages, populations):
    """Calcule l'indice de Myers."""
    mask = (ages >= 10) & (ages <= 89)
    age_subset = ages[mask]
    pop_subset = populations[mask]
    sum_digit = np.zeros(10)
    for i in range(10):
        sum_digit[i] = pop_subset[age_subset % 10 == i].sum()
    myers_index = 0
    for i in range(10):
        j = (i + 1) % 10
        weight = sum_digit[i] + sum_digit[j]
        myers_index += abs(weight - sum(sum_digit) / 10)
    return myers_index / (2 * sum(sum_digit)) * 100

def calculate_bachi(ages, populations):
    """Calcule l'indice de Bachi."""
    mask = (ages >= 20) & (ages <= 89)
    age_subset = ages[mask]
    pop_subset = populations[mask]
    digit_counts = np.zeros(10)
    for i in range(10):
        digit_counts[i] = pop_subset[age_subset % 10 == i].sum()
    digit_percent = (digit_counts / digit_counts.sum()) * 100
    bachi_index = 0
    for i in range(10):
        deviation = (digit_percent[i] - 10) / 10
        bachi_index += deviation ** 2
    return np.sqrt(bachi_index) * 100

def calculate_un_index(whipple, myers, bachi):
    """Calcule l'indice combiné des Nations Unies."""
    if np.isnan(whipple) or np.isnan(myers) or np.isnan(bachi):
        return np.nan
    # Normalisation des indices
    whipple_norm = min(whipple / 100, 2.0)  # Limité à 2.0
    myers_norm = min(myers / 100, 2.0)
    bachi_norm = min(bachi / 100, 2.0)
    return (whipple_norm + myers_norm + bachi_norm) / 3 * 100

def moving_average_2(data):
    """Calcule la moyenne mobile à deux termes."""
    if len(data) < 2:
        return data
    ma = np.zeros(len(data))
    ma[0] = data[0]
    for i in range(1, len(data)):
        ma[i] = (data[i-1] + data[i]) / 2
    return ma

def test_moving_average_diff(original, smoothed, alpha=0.05):
    """Test si la moyenne mobile diffère significativement des données brutes."""
    if len(original) != len(smoothed):
        return {"statistic": np.nan, "p_value": np.nan, "significant": False}
    
    # Test de Wilcoxon pour données appariées (non paramétrique)
    try:
        # Supprimer les valeurs NaN
        mask = ~np.isnan(original) & ~np.isnan(smoothed)
        if np.sum(mask) < 3:
            return {"statistic": np.nan, "p_value": np.nan, "significant": False}
        
        statistic, p_value = stats.wilcoxon(original[mask], smoothed[mask])
        return {
            "statistic": statistic,
            "p_value": p_value,
            "significant": p_value < alpha
        }
    except:
        return {"statistic": np.nan, "p_value": np.nan, "significant": False}

def evaluate_quality(value, method, seuil_bon):
    """Évalue la qualité selon la méthode."""
    if method == "whipple":
        if value < seuil_bon:
            return "Excellent", "#10B981"  # Vert
        elif value < 110:
            return "Bon", "#3B82F6"  # Bleu
        elif value < 125:
            return "Acceptable", "#F59E0B"  # Orange
        elif value < 175:
            return "Médiocre", "#EF4444"  # Rouge
        else:
            return "Très médiocre", "#7F1D1D"  # Rouge foncé
    elif method == "un_index":
        if value < 1.5:
            return "Très haute qualité", "#10B981"
        elif value < 2.5:
            return "Bonne qualité", "#3B82F6"
        elif value < 5.0:
            return "Qualité acceptable", "#F59E0B"
        else:
            return "Mauvaise qualité", "#EF4444"
    else:  # myers ou bachi
        if value < seuil_bon:
            return "Excellent", "#10B981"
        elif value < 2 * seuil_bon:
            return "Bon", "#3B82F6"
        elif value < 3 * seuil_bon:
            return "Acceptable", "#F59E0B"
        else:
            return "Mauvais", "#EF4444"

# ==============================================
# EN-TÊTE PRINCIPALE
# ==============================================

col_logo, col_title = st.columns([1, 5])

with col_logo:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)

with col_title:
    st.markdown('<h1 class="main-header">📊 Analyse Démographique Avancée</h1>', unsafe_allow_html=True)
    st.markdown("""
    <p style='font-size: 1.1rem; color: #6B7280;'>
    Application complète d'analyse de la qualité des données démographiques
    </p>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==============================================
# SIDEBAR - PARAMÈTRES AVANCÉS
# ==============================================

with st.sidebar:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">🔧 PARAMÈTRES AVANCÉS</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### 📏 Plages d'analyse")
    
    with st.expander("🔢 Indice de Whipple", expanded=True):
        age_min_whipple = st.slider("Âge minimum", 20, 30, 23, key="whipple_min")
        age_max_whipple = st.slider("Âge maximum", 55, 70, 62, key="whipple_max")
    
    st.markdown("### 🎯 Seuils de qualité")
    
    with st.expander("📊 Loi de Benford", expanded=True):
        seuil_benford = st.slider("Seuil α", 0.01, 0.10, 0.05, 0.01, key="benford")
    
    with st.expander("📈 Indices démographiques", expanded=True):
        col_seuil1, col_seuil2 = st.columns(2)
        with col_seuil1:
            seuil_whipple_bon = st.number_input("Whipple bon", 90, 120, 105, key="whipple_seuil")
        with col_seuil2:
            seuil_myers_bon = st.number_input("Myers bon", 1.0, 10.0, 2.0, 0.5, key="myers_seuil")
        
        col_seuil3, col_seuil4 = st.columns(2)
        with col_seuil3:
            seuil_bachi_bon = st.number_input("Bachi bon", 1.0, 10.0, 3.0, 0.5, key="bachi_seuil")
        with col_seuil4:
            seuil_test_ma = st.number_input("Test MA (α)", 0.01, 0.10, 0.05, 0.01, key="test_ma")
    
    st.markdown("### 📊 Visualisation")
    
    with st.expander("🎨 Options graphiques", expanded=True):
        theme = st.selectbox("Thème graphique", ["plotly_white", "plotly_dark", "ggplot2", "seaborn"])
        show_grid = st.checkbox("Afficher la grille", True)
        show_legend = st.checkbox("Afficher la légende", True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1.5rem; 
                border-radius: 15px; 
                color: white;'>
        <h4 style='margin: 0;'>📚 Guide rapide</h4>
        <p style='font-size: 0.9rem; opacity: 0.9;'>
        • <b>Benford</b>: Vérifie l'authenticité<br>
        • <b>Whipple</b>: Préférence âges 0/5<br>
        • <b>Myers</b>: Distribution chiffres<br>
        • <b>Bachi</b>: Qualité globale<br>
        • <b>ONU</b>: Indice combiné
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================
# SECTION 1: VUE D'ENSEMBLE
# ==============================================

st.markdown('<h2 class="section-header">👥 Vue d\'ensemble de la population</h2>', unsafe_allow_html=True)

# Calcul des indicateurs de base
total_pop = Total.sum()
pourcentage_h = Homme.sum() / total_pop * 100
pourcentage_f = Femme.sum() / total_pop * 100
rapport_global = Homme.sum() / Femme.sum() * 100

# Affichage des cartes métriques
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Population Totale</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{total_pop:,}</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-delta">personnes</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Hommes</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{Homme.sum():,}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-delta">{pourcentage_h:.1f}% de la population</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Femmes</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{Femme.sum():,}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-delta">{pourcentage_f:.1f}% de la population</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Rapport H/F</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{rapport_global:.1f}</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-delta">hommes pour 100 femmes</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ==============================================
# CALCULS PRINCIPAUX
# ==============================================

# Calcul des indices démographiques
whipple_h = calculate_whipple(Age, Homme, age_min_whipple, age_max_whipple)
whipple_f = calculate_whipple(Age, Femme, age_min_whipple, age_max_whipple)
whipple_t = calculate_whipple(Age, Total, age_min_whipple, age_max_whipple)

myers_h = calculate_myers(Age, Homme)
myers_f = calculate_myers(Age, Femme)
myers_t = calculate_myers(Age, Total)

bachi_h = calculate_bachi(Age, Homme)
bachi_f = calculate_bachi(Age, Femme)
bachi_t = calculate_bachi(Age, Total)

# Indice combiné des Nations Unies
un_h = calculate_un_index(whipple_h, myers_h, bachi_h)
un_f = calculate_un_index(whipple_f, myers_f, bachi_f)
un_t = calculate_un_index(whipple_t, myers_t, bachi_t)

# Loi de Benford
first_digits = []
for value in np.concatenate([Homme, Femme, Total]):
    digit = get_first_digit(value)
    if digit and 1 <= digit <= 9:
        first_digits.append(digit)

observed_counts = np.bincount(first_digits, minlength=10)[1:10]
observed_freq = observed_counts / observed_counts.sum()
benford_law = np.array([np.log10(1 + 1/d) for d in range(1, 10)])
chi2_stat, p_value_benford = stats.chisquare(observed_counts, f_exp=benford_law * observed_counts.sum())

# Rapport de masculinité
rapport_masculinite = np.zeros_like(Homme, dtype=float)
for i in range(len(Homme)):
    rapport_masculinite[i] = (Homme[i] / Femme[i] * 100) if Femme[i] > 0 else np.nan

# ==============================================
# SECTION 2: INDICATEURS DE QUALITÉ
# ==============================================

st.markdown('<h2 class="section-header">📈 Indicateurs de Qualité des Données</h2>', unsafe_allow_html=True)

# Évaluations
eval_benford, color_benford = ("Conforme", "#10B981") if p_value_benford >= seuil_benford else ("Non conforme", "#EF4444")
eval_whipple, color_whipple = evaluate_quality(whipple_t, "whipple", seuil_whipple_bon)
eval_myers, color_myers = evaluate_quality(myers_t, "myers", seuil_myers_bon)
eval_bachi, color_bachi = evaluate_quality(bachi_t, "bachi", seuil_bachi_bon)
eval_un, color_un = evaluate_quality(un_t, "un_index", 2.5)

# Affichage des indicateurs avec badges
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Loi de Benford</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">p={p_value_benford:.4f}</div>', unsafe_allow_html=True)
    st.markdown(f'<span class="badge-{eval_benford.lower().replace(" ", "-") if "conforme" in eval_benford.lower() else "poor"}" style="background-color: {color_benford}">{eval_benford}</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Indice Whipple</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{whipple_t:.1f}</div>', unsafe_allow_html=True)
    st.markdown(f'<span class="badge-{eval_whipple.lower()}" style="background-color: {color_whipple}">{eval_whipple}</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Indice Myers</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{myers_t:.1f}</div>', unsafe_allow_html=True)
    st.markdown(f'<span class="badge-{eval_myers.lower()}" style="background-color: {color_myers}">{eval_myers}</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Indice Bachi</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{bachi_t:.1f}</div>', unsafe_allow_html=True)
    st.markdown(f'<span class="badge-{eval_bachi.lower()}" style="background-color: {color_bachi}">{eval_bachi}</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Indice ONU</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{un_t:.2f}</div>', unsafe_allow_html=True)
    st.markdown(f'<span class="badge-{eval_un.lower().replace(" ", "-")}" style="background-color: {color_un}">{eval_un}</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Tableau détaillé des indices
st.markdown("### 📊 Détail des indices par groupe")

tab_indices = st.tabs(["🏃 Hommes", "👩 Femmes", "👥 Total"])

with tab_indices[0]:
    col_h1, col_h2, col_h3, col_h4 = st.columns(4)
    with col_h1:
        eval_w_h, _ = evaluate_quality(whipple_h, "whipple", seuil_whipple_bon)
        st.metric("Whipple", f"{whipple_h:.1f}", delta=eval_w_h)
    with col_h2:
        eval_m_h, _ = evaluate_quality(myers_h, "myers", seuil_myers_bon)
        st.metric("Myers", f"{myers_h:.1f}", delta=eval_m_h)
    with col_h3:
        eval_b_h, _ = evaluate_quality(bachi_h, "bachi", seuil_bachi_bon)
        st.metric("Bachi", f"{bachi_h:.1f}", delta=eval_b_h)
    with col_h4:
        eval_u_h, _ = evaluate_quality(un_h, "un_index", 2.5)
        st.metric("Indice ONU", f"{un_h:.2f}", delta=eval_u_h)

with tab_indices[1]:
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        eval_w_f, _ = evaluate_quality(whipple_f, "whipple", seuil_whipple_bon)
        st.metric("Whipple", f"{whipple_f:.1f}", delta=eval_w_f)
    with col_f2:
        eval_m_f, _ = evaluate_quality(myers_f, "myers", seuil_myers_bon)
        st.metric("Myers", f"{myers_f:.1f}", delta=eval_m_f)
    with col_f3:
        eval_b_f, _ = evaluate_quality(bachi_f, "bachi", seuil_bachi_bon)
        st.metric("Bachi", f"{bachi_f:.1f}", delta=eval_b_f)
    with col_f4:
        eval_u_f, _ = evaluate_quality(un_f, "un_index", 2.5)
        st.metric("Indice ONU", f"{un_f:.2f}", delta=eval_u_f)

with tab_indices[2]:
    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    with col_t1:
        st.metric("Whipple", f"{whipple_t:.1f}", delta=eval_whipple)
    with col_t2:
        st.metric("Myers", f"{myers_t:.1f}", delta=eval_myers)
    with col_t3:
        st.metric("Bachi", f"{bachi_t:.1f}", delta=eval_bachi)
    with col_t4:
        st.metric("Indice ONU", f"{un_t:.2f}", delta=eval_un)

st.markdown("---")

# ==============================================
# SECTION 3: VISUALISATIONS INTERACTIVES
# ==============================================

st.markdown('<h2 class="section-header">📊 Visualisations Interactives</h2>', unsafe_allow_html=True)

# Onglets principaux
tab_main1, tab_main2, tab_main3, tab_main4, tab_main5, tab_main6 = st.tabs([
    "📈 Loi de Benford", 
    "📊 Indices Démographiques", 
    "👨‍👩‍👧‍👦 Rapport de Masculinité", 
    "📉 Moyenne Mobile & Tests",
    "🏛️ Pyramide des Âges",
    "📚 Annexes Mathématiques"
])

# Tab 1: Loi de Benford
with tab_main1:
    col_ben1, col_ben2 = st.columns([2, 1])
    
    with col_ben1:
        fig_benford = go.Figure()
        
        # Courbe observée
        fig_benford.add_trace(go.Scatter(
            x=list(range(1, 10)),
            y=observed_freq * 100,
            mode='lines+markers',
            name='Observé',
            line=dict(color='#3B82F6', width=3),
            marker=dict(size=10, symbol='circle'),
            hovertemplate='Chiffre: %{x}<br>Observé: %{y:.2f}%<extra></extra>'
        ))
        
        # Courbe théorique
        fig_benford.add_trace(go.Scatter(
            x=list(range(1, 10)),
            y=benford_law * 100,
            mode='lines+markers',
            name='Théorique (Benford)',
            line=dict(color='#EF4444', width=3, dash='dash'),
            marker=dict(size=10, symbol='diamond'),
            hovertemplate='Chiffre: %{x}<br>Théorique: %{y:.2f}%<extra></extra>'
        ))
        
        fig_benford.update_layout(
            title=dict(
                text=f"Loi de Benford - Test d'adéquation (p-value = {p_value_benford:.4f})",
                font=dict(size=18, color='#1E3A8A')
            ),
            height=500,
            template=theme,
            showlegend=show_legend,
            xaxis=dict(
                title="Premier chiffre significatif",
                tickmode='linear',
                gridcolor='lightgray' if show_grid else 'rgba(0,0,0,0)'
            ),
            yaxis=dict(
                title="Proportion (%)",
                gridcolor='lightgray' if show_grid else 'rgba(0,0,0,0)'
            ),
            hovermode='x unified',
            plot_bgcolor='white'
        )
        
        st.plotly_chart(fig_benford, use_container_width=True)
    
    with col_ben2:
        st.markdown("### 📋 Résultats du test")
        
        if p_value_benford < seuil_benford:
            st.error("""
            **❌ Résultat significatif**
            
            Les données **ne suivent pas** la loi de Benford.
            
            **Interprétation :**
            - Possibilité de données artificielles
            - Erreurs systématiques potentielles
            - Regroupements excessifs détectés
            """)
        else:
            st.success("""
            **✅ Non significatif**
            
            Les données **suivent** la loi de Benford.
            
            **Interprétation :**
            - Données naturelles et cohérentes
            - Bon indicateur d'authenticité
            - Distribution conforme aux attentes
            """)
        
        st.metric("Statistique du χ²", f"{chi2_stat:.2f}")
        st.metric("Degrés de liberté", "8")
        st.metric("Seuil α", f"{seuil_benford}")

# Tab 2: Indices démographiques
with tab_main2:
    # Préparation des données
    groupes = ['Hommes', 'Femmes', 'Total']
    indices = ['Whipple', 'Myers', 'Bachi', 'Indice ONU']
    
    valeurs = {
        'Hommes': [whipple_h, myers_h, bachi_h, un_h],
        'Femmes': [whipple_f, myers_f, bachi_f, un_f],
        'Total': [whipple_t, myers_t, bachi_t, un_t]
    }
    
    # Graphique radar pour comparer les indices
    fig_radar = go.Figure()
    
    colors = ['#3B82F6', '#EF4444', '#10B981']
    
    for idx, groupe in enumerate(groupes):
        # Normalisation pour le radar
        vals_norm = []
        for i, val in enumerate(valeurs[groupe]):
            if i == 0:  # Whipple - normalisé sur 200
                vals_norm.append(min(val / 200 * 100, 100))
            elif i == 3:  # Indice ONU - normalisé sur 10
                vals_norm.append(min(val / 10 * 100, 100))
            else:  # Myers et Bachi - normalisés sur 20
                vals_norm.append(min(val / 20 * 100, 100))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=vals_norm + [vals_norm[0]],  # Fermer le polygone
            theta=indices + [indices[0]],
            name=groupe,
            line_color=colors[idx],
            fill='toself',
            opacity=0.3
        ))
    
    fig_radar.update_layout(
        title=dict(
            text="Comparaison des indices démographiques (normalisés)",
            font=dict(size=18, color='#1E3A8A')
        ),
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='lightgray' if show_grid else 'rgba(0,0,0,0)'
            ),
            angularaxis=dict(
                gridcolor='lightgray' if show_grid else 'rgba(0,0,0,0)'
            ),
            bgcolor='white'
        ),
        height=500,
        template=theme,
        showlegend=show_legend
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # Graphique à barres groupées
    fig_bar_grouped = go.Figure()
    
    for idx, groupe in enumerate(groupes):
        fig_bar_grouped.add_trace(go.Bar(
            name=groupe,
            x=indices,
            y=valeurs[groupe],
            marker_color=colors[idx],
            text=[f'{val:.1f}' for val in valeurs[groupe]],
            textposition='auto',
            hovertemplate=f'<b>{groupe}</b><br>%{{x}}: %{{y:.1f}}<extra></extra>'
        ))
    
    # Ajout des lignes de référence
    fig_bar_grouped.add_hline(
        y=100,
        line_dash="dash",
        line_color="gray",
        annotation_text="Référence Whipple (100)",
        annotation_position="top right"
    )
    
    fig_bar_grouped.add_hline(
        y=2.5,
        line_dash="dot",
        line_color="orange",
        annotation_text="Seuil ONU (2.5)",
        annotation_position="top right"
    )
    
    fig_bar_grouped.update_layout(
        title="Indices démographiques par groupe",
        barmode='group',
        height=400,
        template=theme,
        showlegend=show_legend,
        xaxis_title="Indices",
        yaxis_title="Valeur",
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig_bar_grouped, use_container_width=True)

# Tab 3: Rapport de masculinité
with tab_main3:
    st.markdown("### 👨‍👩‍👧‍👦 Rapport de masculinité par âge")
    
    # Contrôles interactifs
    col_control1, col_control2, col_control3 = st.columns(3)
    
    with col_control1:
        window_size = st.slider("Fenêtre de lissage", 1, 10, 3)
    
    with col_control2:
        show_confidence = st.checkbox("Intervalle de confiance", True)
    
    with col_control3:
        log_scale = st.checkbox("Échelle logarithmique", False)
    
    # Préparation des données
    rapport_valide = rapport_masculinite[~np.isnan(rapport_masculinite)]
    ages_valides = Age[~np.isnan(rapport_masculinite)]
    
    # Calcul du lissage
    if window_size > 1:
        rapport_lisse = np.convolve(rapport_valide, np.ones(window_size)/window_size, mode='valid')
        ages_lisse = ages_valides[window_size//2:len(ages_valides)-window_size//2]
    else:
        rapport_lisse = rapport_valide
        ages_lisse = ages_valides
    
    # Calcul de l'intervalle de confiance (95%)
    if show_confidence and len(rapport_valide) > 1:
        std_error = np.std(rapport_valide) / np.sqrt(len(rapport_valide))
        conf_lower = rapport_valide - 1.96 * std_error
        conf_upper = rapport_valide + 1.96 * std_error
    else:
        conf_lower = conf_upper = None
    
    # Création du graphique
    fig_rapport = go.Figure()
    
    # Intervalle de confiance
    if show_confidence and conf_lower is not None and conf_upper is not None:
        fig_rapport.add_trace(go.Scatter(
            x=np.concatenate([ages_valides, ages_valides[::-1]]),
            y=np.concatenate([conf_upper, conf_lower[::-1]]),
            fill='toself',
            fillcolor='rgba(59, 130, 246, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Intervalle 95%',
            showlegend=True,
            hoverinfo='skip'
        ))
    
    # Données brutes
    fig_rapport.add_trace(go.Scatter(
        x=ages_valides,
        y=rapport_valide,
        mode='markers',
        name='Données brutes',
        marker=dict(
            color='#6B7280',
            size=6,
            opacity=0.6,
            symbol='circle'
        ),
        hovertemplate='Âge: %{x} ans<br>Rapport: %{y:.1f} H/100F<extra></extra>'
    ))
    
    # Courbe lissée
    fig_rapport.add_trace(go.Scatter(
        x=ages_lisse,
        y=rapport_lisse,
        mode='lines',
        name=f'Lissé (fenêtre={window_size})',
        line=dict(
            color='#10B981',
            width=3,
            shape='spline'
        ),
        hovertemplate='Âge: %{x} ans<br>Rapport lissé: %{y:.1f} H/100F<extra></extra>'
    ))
    
    # Lignes de référence
    fig_rapport.add_hline(
        y=100,
        line_dash="dash",
        line_color="#EF4444",
        annotation_text="Parité (100)",
        annotation_position="top right",
        annotation_font=dict(color="#EF4444")
    )
    
    fig_rapport.add_hline(
        y=rapport_global,
        line_dash="dot",
        line_color="#8B5CF6",
        annotation_text=f"Moyenne globale ({rapport_global:.1f})",
        annotation_position="top right",
        annotation_font=dict(color="#8B5CF6")
    )
    
    fig_rapport.update_layout(
        title="Évolution du rapport de masculinité avec l'âge",
        height=500,
        template=theme,
        showlegend=show_legend,
        xaxis_title="Âge (années)",
        yaxis_title="Rapport de masculinité (hommes pour 100 femmes)",
        hovermode='x unified',
        plot_bgcolor='white',
        yaxis_type="log" if log_scale else "linear"
    )
    
    st.plotly_chart(fig_rapport, use_container_width=True)
    
    # Statistiques
    col_stats1, col_stats2, col_stats3, col_stats4, col_stats5 = st.columns(5)
    
    with col_stats1:
        st.metric("Moyenne", f"{np.mean(rapport_valide):.1f}")
    with col_stats2:
        st.metric("Médiane", f"{np.median(rapport_valide):.1f}")
    with col_stats3:
        st.metric("Minimum", f"{np.min(rapport_valide):.1f}")
    with col_stats4:
        st.metric("Maximum", f"{np.max(rapport_valide):.1f}")
    with col_stats5:
        st.metric("Écart-type", f"{np.std(rapport_valide):.1f}")

# Tab 4: Moyenne Mobile et Tests
with tab_main4:
    # Calcul des moyennes mobiles
    ma_homme = moving_average_2(Homme)
    ma_femme = moving_average_2(Femme)
    ma_total = moving_average_2(Total)
    
    # Tests statistiques
    test_homme = test_moving_average_diff(Homme, ma_homme, seuil_test_ma)
    test_femme = test_moving_average_diff(Femme, ma_femme, seuil_test_ma)
    test_total = test_moving_average_diff(Total, ma_total, seuil_test_ma)
    
    st.markdown("### 📊 Tests statistiques des moyennes mobiles")
    
    # Affichage des résultats des tests
    col_test1, col_test2, col_test3 = st.columns(3)
    
    with col_test1:
        st.markdown("#### 🏃 Hommes")
        if not np.isnan(test_homme["p_value"]):
            if test_homme["significant"]:
                st.error(f"""
                **❌ Différence significative**
                
                **p-value:** {test_homme['p_value']:.4f}
                **Statistique W:** {test_homme['statistic']:.2f}
                
                **Interprétation:** 
                La moyenne mobile MA(2) diffère significativement 
                des données brutes pour les hommes.
                """)
            else:
                st.success(f"""
                **✅ Pas de différence significative**
                
                **p-value:** {test_homme['p_value']:.4f}
                **Statistique W:** {test_homme['statistic']:.2f}
                
                **Interprétation:** 
                Pas de différence significative entre les données 
                brutes et la moyenne mobile pour les hommes.
                """)
        else:
            st.warning("Test non applicable - données insuffisantes")
    
    with col_test2:
        st.markdown("#### 👩 Femmes")
        if not np.isnan(test_femme["p_value"]):
            if test_femme["significant"]:
                st.error(f"""
                **❌ Différence significative**
                
                **p-value:** {test_femme['p_value']:.4f}
                **Statistique W:** {test_femme['statistic']:.2f}
                
                **Interprétation:** 
                La moyenne mobile MA(2) diffère significativement 
                des données brutes pour les femmes.
                """)
            else:
                st.success(f"""
                **✅ Pas de différence significative**
                
                **p-value:** {test_femme['p_value']:.4f}
                **Statistique W:** {test_femme['statistic']:.2f}
                
                **Interprétation:** 
                Pas de différence significative entre les données 
                brutes et la moyenne mobile pour les femmes.
                """)
        else:
            st.warning("Test non applicable - données insuffisantes")
    
    with col_test3:
        st.markdown("#### 👥 Total")
        if not np.isnan(test_total["p_value"]):
            if test_total["significant"]:
                st.error(f"""
                **❌ Différence significative**
                
                **p-value:** {test_total['p_value']:.4f}
                **Statistique W:** {test_total['statistic']:.2f}
                
                **Interprétation:** 
                La moyenne mobile MA(2) diffère significativement 
                des données brutes pour la population totale.
                """)
            else:
                st.success(f"""
                **✅ Pas de différence significative**
                
                **p-value:** {test_total['p_value']:.4f}
                **Statistique W:** {test_total['statistic']:.2f}
                
                **Interprétation:** 
                Pas de différence significative entre les données 
                brutes et la moyenne mobile pour la population totale.
                """)
        else:
            st.warning("Test non applicable - données insuffisantes")
    
    # Graphiques comparatifs
    fig_ma_comparison = make_subplots(
        rows=3, cols=1,
        subplot_titles=("Hommes", "Femmes", "Total"),
        vertical_spacing=0.1
    )
    
    # Hommes
    fig_ma_comparison.add_trace(
        go.Scatter(x=Age, y=Homme, mode='lines', name='Brut', line=dict(color='#3B82F6', width=2)),
        row=1, col=1
    )
    fig_ma_comparison.add_trace(
        go.Scatter(x=Age, y=ma_homme, mode='lines', name='MA(2)', line=dict(color='#10B981', width=2, dash='dash')),
        row=1, col=1
    )
    
    # Femmes
    fig_ma_comparison.add_trace(
        go.Scatter(x=Age, y=Femme, mode='lines', name='Brut', line=dict(color='#EF4444', width=2), showlegend=False),
        row=2, col=1
    )
    fig_ma_comparison.add_trace(
        go.Scatter(x=Age, y=ma_femme, mode='lines', name='MA(2)', line=dict(color='#10B981', width=2, dash='dash'), showlegend=False),
        row=2, col=1
    )
    
    # Total
    fig_ma_comparison.add_trace(
        go.Scatter(x=Age, y=Total, mode='lines', name='Brut', line=dict(color='#8B5CF6', width=2), showlegend=False),
        row=3, col=1
    )
    fig_ma_comparison.add_trace(
        go.Scatter(x=Age, y=ma_total, mode='lines', name='MA(2)', line=dict(color='#10B981', width=2, dash='dash'), showlegend=False),
        row=3, col=1
    )
    
    fig_ma_comparison.update_layout(
        title="Comparaison données brutes vs moyenne mobile à 2 termes",
        height=700,
        template=theme,
        showlegend=True,
        hovermode='x unified'
    )
    
    fig_ma_comparison.update_xaxes(title_text="Âge", row=3, col=1)
    fig_ma_comparison.update_yaxes(title_text="Population", row=2, col=1)
    
    st.plotly_chart(fig_ma_comparison, use_container_width=True)

# Tab 5: Pyramide des âges
with tab_main5:
    st.markdown("### 🏛️ Pyramide des âges interactive")
    
    # Contrôles
    col_pyr_control1, col_pyr_control2, col_pyr_control3 = st.columns(3)
    
    with col_pyr_control1:
        age_group = st.selectbox("Regroupement par", [1, 5, 10], index=1, key="age_group")
    
    with col_pyr_control2:
        max_age = st.slider("Âge maximum", 50, 110, 100, key="max_age")
    
    with col_pyr_control3:
        display_mode = st.radio("Mode d'affichage", ["Nombre", "Pourcentage"], key="display_mode")
    
    # Préparation des données
    bins = list(range(0, max_age + age_group, age_group))
    labels = []
    homme_counts = []
    femme_counts = []
    
    for i in range(len(bins) - 1):
        start = bins[i]
        end = bins[i + 1]
        mask = (Age >= start) & (Age < end)
        
        labels.append(f"{start}-{end-1}")
        homme_counts.append(Homme[mask].sum())
        femme_counts.append(Femme[mask].sum())
    
    # Conversion en pourcentage si nécessaire
    if display_mode == "Pourcentage":
        total_h = sum(homme_counts)
        total_f = sum(femme_counts)
        if total_h > 0:
            homme_counts = [h/total_h*100 for h in homme_counts]
        if total_f > 0:
            femme_counts = [f/total_f*100 for f in femme_counts]
    
    # Création de la pyramide
    fig_pyramid = go.Figure()
    
    # Hommes (gauche, valeurs négatives)
    fig_pyramid.add_trace(go.Bar(
        y=labels,
        x=[-h for h in homme_counts],
        name='Hommes',
        orientation='h',
        marker_color='#3B82F6',
        text=[f'{h:,.0f}' if display_mode == "Nombre" else f'{h:.1f}%' for h in homme_counts],
        textposition='outside',
        textfont=dict(color='white'),
        hovertemplate='Hommes: %{text}<extra></extra>'
    ))
    
    # Femmes (droite, valeurs positives)
    fig_pyramid.add_trace(go.Bar(
        y=labels,
        x=femme_counts,
        name='Femmes',
        orientation='h',
        marker_color='#EF4444',
        text=[f'{f:,.0f}' if display_mode == "Nombre" else f'{f:.1f}%' for f in femme_counts],
        textposition='outside',
        textfont=dict(color='white'),
        hovertemplate='Femmes: %{text}<extra></extra>'
    ))
    
    # Configuration
    fig_pyramid.update_layout(
        title=f"Pyramide des âges (regroupement: {age_group} ans)",
        barmode='overlay',
        height=600,
        template=theme,
        showlegend=show_legend,
        xaxis=dict(
            title='Population' + (' (%)' if display_mode == "Pourcentage" else ''),
            tickmode='array',
            tickvals=list(range(-int(max(max(homme_counts), max(femme_counts))), 
                             int(max(max(homme_counts), max(femme_counts))) + 1,
                             max(1, int(max(max(homme_counts), max(femme_counts))/5)))),
            ticktext=[str(abs(x)) for x in list(range(-int(max(max(homme_counts), max(femme_counts))), 
                                                     int(max(max(homme_counts), max(femme_counts))) + 1,
                                                     max(1, int(max(max(homme_counts), max(femme_counts))/5))))]
        ),
        yaxis=dict(title='Tranche d\'âge'),
        hovermode='y unified',
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig_pyramid, use_container_width=True)

# Tab 6: Annexes Mathématiques
with tab_main6:
    st.markdown('<h2 class="section-header">📚 Annexes Mathématiques</h2>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    Cette section présente les formules mathématiques et les concepts théoriques 
    utilisés dans les analyses démographiques présentées dans cette application.
    """)
    
    # 1. Loi de Benford
    with st.expander("📊 Loi de Benford", expanded=True):
        col_benford1, col_benford2 = st.columns([2, 1])
        
        with col_benford1:
            st.markdown("""
            <div class="formula-card">
                <div class="formula-title">Formule de la loi de Benford</div>
                <div class="formula-equation">
                    P(d) = log₁₀(1 + 1/d)
                </div>
                <div class="formula-explanation">
                où:<br>
                • P(d) est la probabilité que le premier chiffre significatif soit d<br>
                • d ∈ {1, 2, 3, 4, 5, 6, 7, 8, 9}<br>
                • log₁₀ est le logarithme décimal
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="formula-card">
                <div class="formula-title">Test du chi-deux d'adéquation</div>
                <div class="formula-equation">
                    χ² = Σ[(Oᵢ - Eᵢ)² / Eᵢ]
                </div>
                <div class="formula-explanation">
                où:<br>
                • Oᵢ = fréquence observée pour le chiffre i<br>
                • Eᵢ = fréquence théorique selon Benford pour le chiffre i<br>
                • Σ = somme sur i = 1 à 9<br>
                • Degrés de liberté = 8
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_benford2:
            st.markdown("### Distribution théorique")
            benford_table = pd.DataFrame({
                'Chiffre': range(1, 10),
                'Probabilité (%)': [round(np.log10(1 + 1/d) * 100, 2) for d in range(1, 10)]
            })
            st.dataframe(benford_table, hide_index=True)
    
    # 2. Indice de Whipple
    with st.expander("🔢 Indice de Whipple", expanded=True):
        st.markdown("""
        <div class="formula-card">
            <div class="formula-title">Formule de l'indice de Whipple</div>
            <div class="formula-equation">
                W = (P₂₃₋₆₂(0,5) / P₂₃₋₆₂) × 100
            </div>
            <div class="formula-explanation">
            où:<br>
            • P₂₃₋₆₂(0,5) = population âgée de 23 à 62 ans dont l'âge se termine par 0 ou 5<br>
            • P₂₃₋₆₂ = population totale âgée de 23 à 62 ans<br>
            • × 100 = conversion en pourcentage
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="formula-card">
            <div class="formula-title">Interprétation de l'indice de Whipple</div>
            <div class="formula-equation">
                W ≈ 100 ⇒ qualité parfaite<br>
                W < 100 ⇒ sous-déclaration des âges 0/5<br>
                W > 100 ⇒ sur-déclaration des âges 0/5
            </div>
            <div class="formula-explanation">
            Échelle de qualité (OMS):<br>
            • < 105 : Très précis<br>
            • 105-110 : Précis<br>
            • 110-125 : Acceptable<br>
            • > 125 : Médiocre
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 3. Indice de Myers
    with st.expander("📈 Indice de Myers", expanded=True):
        st.markdown("""
        <div class="formula-card">
            <div class="formula-title">Formule de l'indice de Myers</div>
            <div class="formula-equation">
                M = [Σ|(Sᵢ + Sᵢ₊₁) - N/5|] / (2N) × 100
            </div>
            <div class="formula-explanation">
            où:<br>
            • Sᵢ = population dont l'âge se termine par le chiffre i<br>
            • N = population totale (âges 10-89 ans)<br>
            • Σ = somme sur i = 0 à 9 (avec S₁₀ = S₀)<br>
            • i+1 est pris modulo 10
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="formula-card">
            <div class="formula-title">Étapes de calcul</div>
            <div class="formula-equation">
                1. Calculer Sᵢ = Σ population avec âge ≡ i mod 10<br>
                2. Calculer Tᵢ = Sᵢ + Sᵢ₊₁<br>
                3. Calculer D = Σ|Tᵢ - N/5|<br>
                4. M = D / (2N) × 100
            </div>
            <div class="formula-explanation">
            Interprétation:<br>
            • M → 0 : qualité excellente<br>
            • M < 2 : très bonne qualité<br>
            • 2 ≤ M < 4 : bonne qualité<br>
            • 4 ≤ M < 6 : qualité acceptable<br>
            • M ≥ 6 : mauvaise qualité
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 4. Indice de Bachi
    with st.expander("📊 Indice de Bachi", expanded=True):
        st.markdown("""
        <div class="formula-card">
            <div class="formula-title">Formule de l'indice de Bachi</div>
            <div class="formula-equation">
                B = √[Σ((pᵢ - 10)/10)²] × 100
            </div>
            <div class="formula-explanation">
            où:<br>
            • pᵢ = pourcentage de la population dont l'âge se termine par le chiffre i<br>
            • 10 = pourcentage théorique attendu pour chaque chiffre<br>
            • Σ = somme sur i = 0 à 9<br>
            • √ = racine carrée
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="formula-card">
            <div class="formula-title">Calcul détaillé</div>
            <div class="formula-equation">
                pᵢ = (Sᵢ / N) × 100<br>
                dᵢ = (pᵢ - 10) / 10<br>
                B = √(Σdᵢ²) × 100
            </div>
            <div class="formula-explanation">
            où:<br>
            • Sᵢ = population avec chiffre terminal i<br>
            • N = population totale (âges 20-89 ans)<br>
            • dᵢ = écart normalisé<br>
            Interprétation:<br>
            • B < 3 : très bonne qualité<br>
            • 3 ≤ B < 5 : bonne qualité<br>
            • 5 ≤ B < 10 : qualité acceptable<br>
            • B ≥ 10 : mauvaise qualité
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 5. Indice combiné des Nations Unies
    with st.expander("🌍 Indice combiné des Nations Unies", expanded=True):
        st.markdown("""
        <div class="formula-card">
            <div class="formula-title">Formule de l'indice combiné ONU</div>
            <div class="formula-equation">
                U = (Wₙ + Mₙ + Bₙ) / 3 × 100
            </div>
            <div class="formula-explanation">
            où:<br>
            • Wₙ = indice de Whipple normalisé (W/100, limité à 2.0)<br>
            • Mₙ = indice de Myers normalisé (M/100, limité à 2.0)<br>
            • Bₙ = indice de Bachi normalisé (B/100, limité à 2.0)<br>
            • × 100 = conversion en pourcentage
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="formula-card">
            <div class="formula-title">Normalisation des indices</div>
            <div class="formula-equation">
                Wₙ = min(W/100, 2.0)<br>
                Mₙ = min(M/100, 2.0)<br>
                Bₙ = min(B/100, 2.0)
            </div>
            <div class="formula-explanation">
            Interprétation selon les standards ONU:<br>
            • U < 1.5 : données de très haute qualité<br>
            • 1.5 ≤ U < 2.5 : données de bonne qualité<br>
            • 2.5 ≤ U < 5.0 : données de qualité acceptable<br>
            • U ≥ 5.0 : données de mauvaise qualité
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 6. Moyenne mobile
    with st.expander("📉 Moyenne Mobile à 2 termes", expanded=True):
        st.markdown("""
        <div class="formula-card">
            <div class="formula-title">Formule de la moyenne mobile MA(2)</div>
            <div class="formula-equation">
                MA(t) = (xₜ₋₁ + xₜ) / 2
            </div>
            <div class="formula-explanation">
            où:<br>
            • xₜ = valeur à l'instant t<br>
            • xₜ₋₁ = valeur à l'instant t-1<br>
            • MA(t) = moyenne mobile à l'instant t<br>
            Pour t = 1 : MA(1) = x₁ (pas de valeur précédente)
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="formula-card">
            <div class="formula-title">Propriétés de la moyenne mobile</div>
            <div class="formula-equation">
                1. Réduction du bruit aléatoire<br>
                2. Lissage des fluctuations<br>
                3. Conservation de la tendance<br>
                4. Décalage temporel (lag) d'un demi-période
            </div>
            <div class="formula-explanation">
            Application aux données démographiques:<br>
            • Réduction des erreurs de déclaration<br>
            • Atténuation des effets de cohorte<br>
            • Meilleure visualisation des tendances<br>
            • Préparation des données pour l'analyse
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 7. Test de Wilcoxon
    with st.expander("🔬 Test de Wilcoxon pour données appariées", expanded=True):
        st.markdown("""
        <div class="formula-card">
            <div class="formula-title">Hypothèses du test</div>
            <div class="formula-equation">
                H₀ : Médiane(Différences) = 0<br>
                H₁ : Médiane(Différences) ≠ 0
            </div>
            <div class="formula-explanation">
            où:<br>
            • H₀ : hypothèse nulle (pas de différence)<br>
            • H₁ : hypothèse alternative (différence significative)<br>
            • Différences = données brutes - données lissées<br>
            Test non-paramétrique pour données appariées
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="formula-card">
            <div class="formula-title">Calcul de la statistique W</div>
            <div class="formula-equation">
                1. dᵢ = xᵢ - yᵢ<br>
                2. |dᵢ| = valeur absolue de dᵢ<br>
                3. rᵢ = rang de |dᵢ|<br>
                4. W⁺ = Σ rᵢ pour dᵢ > 0<br>
                5. W⁻ = Σ rᵢ pour dᵢ < 0<br>
                6. W = min(W⁺, W⁻)
            </div>
            <div class="formula-explanation">
            où:<br>
            • xᵢ = donnée brute i<br>
            • yᵢ = donnée lissée i<br>
            • dᵢ = différence appariée<br>
            • W = statistique du test de Wilcoxon<br>
            • n = nombre de paires non-nulles
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="formula-card">
            <div class="formula-title">Interprétation du test</div>
            <div class="formula-equation">
                Si p-value < α : rejet de H₀<br>
                Si p-value ≥ α : non rejet de H₀
            </div>
            <div class="formula-explanation">
            où:<br>
            • α = seuil de significativité (généralement 0.05)<br>
            • p-value = probabilité d'observer les données si H₀ est vraie<br>
            • Rejet de H₀ : différence statistiquement significative<br>
            • Non rejet de H₀ : pas de preuve de différence significative
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 8. Rapport de masculinité
    with st.expander("👨‍👩‍👧‍👦 Rapport de masculinité", expanded=True):
        st.markdown("""
        <div class="formula-card">
            <div class="formula-title">Formule du rapport de masculinité</div>
            <div class="formula-equation">
                R = (H / F) × 100
            </div>
            <div class="formula-explanation">
            où:<br>
            • H = nombre d'hommes<br>
            • F = nombre de femmes<br>
            • × 100 = conversion en "hommes pour 100 femmes"<br>
            • R = 100 : parité parfaite<br>
            • R > 100 : excédent masculin<br>
            • R < 100 : excédent féminin
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="formula-card">
            <div class="formula-title">Évolution avec l'âge</div>
            <div class="formula-equation">
                R(a) = (H(a) / F(a)) × 100
            </div>
            <div class="formula-explanation">
            où:<br>
            • R(a) = rapport de masculinité à l'âge a<br>
            • H(a) = nombre d'hommes d'âge a<br>
            • F(a) = nombre de femmes d'âge a<br>
            Tendance générale:<br>
            • Naissance : R ≈ 105 (plus de garçons)<br>
            • Vieillesse : R < 100 (plus de femmes)
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 9. Pyramide des âges
    with st.expander("🏛️ Pyramide des âges", expanded=True):
        st.markdown("""
        <div class="formula-card">
            <div class="formula-title">Construction de la pyramide</div>
            <div class="formula-equation">
                Pour chaque tranche d'âge [a, a+Δ]:<br>
                Hₐ = Σ H(i) pour i ∈ [a, a+Δ)<br>
                Fₐ = Σ F(i) pour i ∈ [a, a+Δ)
            </div>
            <div class="formula-explanation">
            où:<br>
            • Δ = largeur de la tranche d'âge (1, 5, ou 10 ans)<br>
            • H(i) = nombre d'hommes d'âge i<br>
            • F(i) = nombre de femmes d'âge i<br>
            • Hₐ = hommes dans la tranche [a, a+Δ)<br>
            • Fₐ = femmes dans la tranche [a, a+Δ)
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="formula-card">
            <div class="formula-title">Indicateurs démographiques dérivés</div>
            <div class="formula-equation">
                • Taux de dépendance = (jeunes + âgés) / actifs<br>
                • Âge médian = âge qui divise la population en deux<br>
                • Espérance de vie = moyenne des âges au décès<br>
                • Taux de croissance = (naissances - décès) / population
            </div>
            <div class="formula-explanation">
            Types de pyramides:<br>
            • Expansive : base large (pays jeunes)<br>
            • Constrictive : base étroite (pays vieillissants)<br>
            • Stationnaire : forme régulière (population stable)<br>
            • Irrégulière : effets de guerre/migration
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 10. Références bibliographiques
    with st.expander("📖 Références bibliographiques", expanded=False):
        st.markdown("""
        ### Ouvrages de référence
        
        1. **Shryock, H. S., & Siegel, J. S. (1976).** *The Methods and Materials of Demography.*
           - Chapitre 5 : Évaluation de la qualité des données
           - Chapitre 6 : Techniques de lissage
        
        2. **Preston, S., Heuveline, P., & Guillot, M. (2001).** *Demography: Measuring and Modeling Population Processes.*
           - Analyse des structures par âge
           - Indices de qualité démographique
        
        3. **Newcomb, S. (1881).** "Note on the Frequency of Use of the Different Digits in Natural Numbers."
           - Publication originale sur la loi de Benford
        
        4. **United Nations (2019).** *Handbook on Training in Civil Registration and Vital Statistics Systems.*
           - Standards internationaux de qualité
           - Méthodes d'évaluation des données
        
        ### Articles scientifiques
        
        5. **Whipple, G. C. (1919).** "Vital Statistics: An Introduction to the Science of Demography."
           - Définition originale de l'indice de Whipple
        
        6. **Myers, R. J. (1940).** "Errors and Bias in the Reporting of Ages in Census Data."
           - Développement de l'indice de Myers
        
        7. **Bachi, R. (1951).** "The Tendency to Round Off Age Returns: Measurement and Correction."
           - Méthodologie de l'indice de Bachi
        
        8. **Nigrini, M. J. (2012).** *Benford's Law: Applications for Forensic Accounting, Auditing, and Fraud Detection.*
           - Applications modernes de la loi de Benford
        """)

# ==============================================
# SECTION 4: ANALYSE AVANCÉE
# ==============================================

st.markdown("---")
st.markdown('<h2 class="section-header">🔍 Analyse Avancée</h2>', unsafe_allow_html=True)

col_adv1, col_adv2 = st.columns(2)

with col_adv1:
    st.markdown("### 🔢 Analyse des chiffres terminaux")
    
    # Calcul des distributions
    digit_counts_h = np.zeros(10)
    digit_counts_f = np.zeros(10)
    for i in range(10):
        digit_counts_h[i] = Homme[Age % 10 == i].sum()
        digit_counts_f[i] = Femme[Age % 10 == i].sum()
    
    digit_percent_h = (digit_counts_h / digit_counts_h.sum()) * 100 if digit_counts_h.sum() > 0 else np.zeros(10)
    digit_percent_f = (digit_counts_f / digit_counts_f.sum()) * 100 if digit_counts_f.sum() > 0 else np.zeros(10)
    digit_percent_t = ((digit_counts_h + digit_counts_f) / 
                       (digit_counts_h.sum() + digit_counts_f.sum())) * 100 if (digit_counts_h.sum() + digit_counts_f.sum()) > 0 else np.zeros(10)
    
    # Graphique
    fig_digits = go.Figure()
    
    fig_digits.add_trace(go.Bar(
        x=list(range(10)),
        y=digit_percent_t,
        name='Observé',
        marker_color='#8B5CF6',
        text=[f'{val:.1f}%' for val in digit_percent_t],
        textposition='auto'
    ))
    
    fig_digits.add_hline(
        y=10,
        line_dash="dash",
        line_color="#10B981",
        annotation_text="Attendu (10%)",
        annotation_position="top right"
    )
    
    fig_digits.update_layout(
        title="Distribution des chiffres terminaux d'âge",
        height=400,
        template=theme,
        showlegend=False,
        xaxis_title="Chiffre terminal",
        yaxis_title="Pourcentage (%)",
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig_digits, use_container_width=True)

with col_adv2:
    st.markdown("### 📊 Qualité globale des données")
    
    # Score global
    score_components = []
    
    # Benford
    score_components.append(1 if p_value_benford >= seuil_benford else 0)
    
    # Whipple
    if whipple_t < seuil_whipple_bon:
        score_components.append(2)
    elif whipple_t < 110:
        score_components.append(1)
    else:
        score_components.append(0)
    
    # Myers
    if myers_t < seuil_myers_bon:
        score_components.append(2)
    elif myers_t < 2 * seuil_myers_bon:
        score_components.append(1)
    else:
        score_components.append(0)
    
    # Bachi
    if bachi_t < seuil_bachi_bon:
        score_components.append(2)
    elif bachi_t < 2 * seuil_bachi_bon:
        score_components.append(1)
    else:
        score_components.append(0)
    
    total_score = sum(score_components)
    max_score = 7
    
    # Graphique radar pour le score
    fig_score_radar = go.Figure()
    
    categories = ['Benford', 'Whipple', 'Myers', 'Bachi']
    
    fig_score_radar.add_trace(go.Scatterpolar(
        r=score_components + [score_components[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(59, 130, 246, 0.5)',
        line_color='#3B82F6',
        name='Score qualité'
    ))
    
    fig_score_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 2],
                tickvals=[0, 1, 2],
                ticktext=['0', '1', '2']
            )
        ),
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig_score_radar, use_container_width=True)
    
    # Évaluation
    if total_score >= 6:
        st.success(f"**Score: {total_score}/{max_score}** - Qualité EXCELLENTE")
    elif total_score >= 4:
        st.info(f"**Score: {total_score}/{max_score}** - Qualité BONNE")
    elif total_score >= 2:
        st.warning(f"**Score: {total_score}/{max_score}** - Qualité ACCEPTABLE")
    else:
        st.error(f"**Score: {total_score}/{max_score}** - Qualité INSUFFISANTE")

# ==============================================
# SECTION 5: EXPORT ET RAPPORT
# ==============================================

st.markdown("---")
st.markdown('<h2 class="section-header">📤 Export des Résultats</h2>', unsafe_allow_html=True)

col_exp1, col_exp2 = st.columns([2, 1])

with col_exp1:
    with st.expander("📋 Générer un rapport complet", expanded=True):
        st.markdown("""
        **Le rapport inclura :**
        
        1. **Synthèse** des indicateurs clés
        2. **Données brutes** complètes
        3. **Indices détaillés** par sexe
        4. **Tests statistiques** (Benford, moyennes mobiles)
        5. **Recommandations** personnalisées
        6. **Graphiques** en haute résolution
        7. **Annexes mathématiques**
        """)
        
        if st.button("🚀 Générer le rapport Excel", type="primary"):
            # Création du rapport
            output = BytesIO()
            
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                # Feuille 1: Synthèse
                synthèse_df = pd.DataFrame({
                    'Indicateur': [
                        'Population totale', 'Hommes', 'Femmes',
                        'Pourcentage hommes', 'Pourcentage femmes',
                        'Rapport H/F global', 'Indice Whipple', 'Indice Myers',
                        'Indice Bachi', 'Indice ONU', 'p-value Benford',
                        'Score qualité'
                    ],
                    'Valeur': [
                        total_pop, Homme.sum(), Femme.sum(),
                        f"{pourcentage_h:.1f}%", f"{pourcentage_f:.1f}%",
                        f"{rapport_global:.1f}", f"{whipple_t:.1f}",
                        f"{myers_t:.1f}", f"{bachi_t:.1f}", f"{un_t:.2f}",
                        f"{p_value_benford:.4f}", f"{total_score}/{max_score}"
                    ]
                })
                synthèse_df.to_excel(writer, sheet_name='Synthèse', index=False)
                
                # Feuille 2: Données brutes
                donnees_df = pd.DataFrame({
                    'Age': Age,
                    'Hommes': Homme,
                    'Femmes': Femme,
                    'Total': Total,
                    'Rapport_HF': rapport_masculinite,
                    'MA_Hommes': ma_homme,
                    'MA_Femmes': ma_femme,
                    'MA_Total': ma_total
                })
                donnees_df.to_excel(writer, sheet_name='Données', index=False)
                
                # Feuille 3: Indices
                indices_df = pd.DataFrame({
                    'Groupe': ['Hommes', 'Femmes', 'Total'],
                    'Whipple': [whipple_h, whipple_f, whipple_t],
                    'Myers': [myers_h, myers_f, myers_t],
                    'Bachi': [bachi_h, bachi_f, bachi_t],
                    'Indice_ONU': [un_h, un_f, un_t]
                })
                indices_df.to_excel(writer, sheet_name='Indices', index=False)
                
                # Feuille 4: Tests
                tests_df = pd.DataFrame({
                    'Test': ['Hommes', 'Femmes', 'Total'],
                    'Statistique': [test_homme.get('statistic', np.nan), 
                                   test_femme.get('statistic', np.nan), 
                                   test_total.get('statistic', np.nan)],
                    'p_value': [test_homme.get('p_value', np.nan), 
                               test_femme.get('p_value', np.nan), 
                               test_total.get('p_value', np.nan)],
                    'Significatif': [test_homme.get('significant', False), 
                                    test_femme.get('significant', False), 
                                    test_total.get('significant', False)]
                })
                tests_df.to_excel(writer, sheet_name='Tests', index=False)
                
                # Feuille 5: Chiffres terminaux
                chiffres_df = pd.DataFrame({
                    'Chiffre': range(10),
                    'Hommes_Nombre': digit_counts_h,
                    'Femmes_Nombre': digit_counts_f,
                    'Total_Nombre': digit_counts_h + digit_counts_f,
                    'Hommes_%': digit_percent_h,
                    'Femmes_%': digit_percent_f,
                    'Total_%': digit_percent_t
                })
                chiffres_df.to_excel(writer, sheet_name='Chiffres terminaux', index=False)
                
                # Feuille 6: Formules
                formules_df = pd.DataFrame({
                    'Concept': ['Loi de Benford', 'Indice Whipple', 'Indice Myers', 
                               'Indice Bachi', 'Indice ONU', 'Moyenne Mobile', 'Test Wilcoxon'],
                    'Formule': ['P(d) = log₁₀(1 + 1/d)', 'W = (P(0,5)/P) × 100', 
                               'M = [Σ|(Sᵢ+Sᵢ₊₁)-N/5|]/(2N)×100', 
                               'B = √[Σ((pᵢ-10)/10)²] × 100',
                               'U = (Wₙ+Mₙ+Bₙ)/3 × 100', 'MA(t) = (xₜ₋₁+xₜ)/2',
                               'W = min(Σrᵢ⁺, Σrᵢ⁻)']
                })
                formules_df.to_excel(writer, sheet_name='Formules', index=False)
            
            output.seek(0)
            
            # Bouton de téléchargement
            st.download_button(
                label="📥 Télécharger le rapport",
                data=output,
                file_name="rapport_analyse_demographique.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            st.success("✅ Rapport généré avec succès !")

with col_exp2:
    st.markdown("### 📊 Options d'export")
    
    export_format = st.selectbox("Format", ["Excel", "CSV", "JSON"])
    
    if st.button("📄 Exporter les données brutes"):
        if export_format == "Excel":
            # Export Excel
            pass
        elif export_format == "CSV":
            # Export CSV
            csv_data = pd.DataFrame({
                'Age': Age,
                'Hommes': Homme,
                'Femmes': Femme,
                'Total': Total
            }).to_csv(index=False)
            
            st.download_button(
                label="📥 Télécharger CSV",
                data=csv_data,
                file_name="donnees_demographiques.csv",
                mime="text/csv"
            )
        else:  # JSON
            # Export JSON
            import json
            json_data = json.dumps({
                'Age': Age.tolist(),
                'Hommes': Homme.tolist(),
                'Femmes': Femme.tolist(),
                'Total': Total.tolist()
            })
            
            st.download_button(
                label="📥 Télécharger JSON",
                data=json_data,
                file_name="donnees_demographiques.json",
                mime="application/json"
            )

# ==============================================
# PIED DE PAGE
# ==============================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            border-radius: 15px; color: white;'>
    <h3 style='margin: 0;'>📊 Application d'Analyse Démographique Avancée</h3>
    <p style='margin: 0.5rem 0; opacity: 0.9;'>
    • Auteur: Statisticien et Théoricien des Sciences et de l'Ingéniérie • Moussa DIAKITE
    </p>
    <div style='display: flex; justify-content: center; gap: 2rem; margin-top: 1rem;'>
        <div>
            <div style='font-size: 1.5rem;'>📚</div>
            <div style='font-size: 0.9rem;'>Formules</div>
        </div>
        <div>
            <div style='font-size: 1.5rem;'>📈</div>
            <div style='font-size: 0.9rem;'>Indices</div>
        </div>
        <div>
            <div style='font-size: 1.5rem;'>🔍</div>
            <div style='font-size: 0.9rem;'>Tests</div>
        </div>
        <div>
            <div style='font-size: 1.5rem;'>📊</div>
            <div style='font-size: 0.9rem;'>Graphiques</div>
        </div>
        <div>
            <div style='font-size: 1.5rem;'>🌍</div>
            <div style='font-size: 0.9rem;'>ONU</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)