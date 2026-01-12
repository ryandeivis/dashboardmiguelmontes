"""
🏠 PÁGINA PRINCIPAL - DASHBOARDS DE REDES SOCIALES
Sistema de análisis y estrategia para @miguemontes1
"""

import streamlit as st

st.set_page_config(
    page_title="📊 Social Media Analytics",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.3rem;
        text-align: center;
        color: #718096;
        margin-bottom: 3rem;
    }
    .card {
        background: white;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s;
    }
    .card:hover {
        transform: translateY(-5px);
    }
    .card-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    .card-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1a365d;
        margin-bottom: 0.5rem;
    }
    .card-desc {
        color: #718096;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">📊 Social Media Analytics</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Sistema de análisis y estrategia para redes sociales</p>', unsafe_allow_html=True)

# Información del perfil
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 1rem; color: white; text-align: center;">
        <h2>@miguemontes1</h2>
        <p>Miguel A. Montes Curi</p>
        <p>📊 57 Videos Analizados | 👥 5,244 Seguidores</p>
        <p>📅 Agosto 2025 - Enero 2026</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Cards de navegación
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-icon">📊</div>
        <div class="card-title">Dashboard de Análisis</div>
        <div class="card-desc">
            Métricas históricas, correlaciones, semáforos de rendimiento, 
            análisis de sentimiento y tendencias temporales.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔍 Ir al Análisis", use_container_width=True, type="primary"):
        st.switch_page("pages/01_Dashboard_Analisis.py")

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🎯</div>
        <div class="card-title">Dashboard de Estrategia</div>
        <div class="card-desc">
            Selector de contenido para TikTok/FB/Instagram, 
            recomendación de pauta y calendario de publicación.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Ir a Estrategia", use_container_width=True, type="primary"):
        st.switch_page("pages/02_Dashboard_Estrategia.py")

st.divider()

# Resumen rápido
st.markdown("## 📈 Resumen Rápido")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👁️ Total Vistas", "1,106,629", "19,415/video")

with col2:
    st.metric("❤️ Total Likes", "21,552", "378/video")

with col3:
    st.metric("🔄 Sends/Reach", "0.44%", "🟢 Alto")

with col4:
    st.metric("⭐ Quality Score", "4.5/10", "🟡 Promedio")

st.divider()

# Metodología
st.markdown("## 📚 Metodología")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🔬 Basado en Algoritmo Instagram 2025
    
    Según **Adam Mosseri** (CEO Instagram, Enero 2025):
    
    1. **Watch Time** - Retención de audiencia (no medible externamente)
    2. **Sends per Reach** - Compartidos / Vistas (medible ✅)
    3. **Likes per Reach** - Likes / Vistas (medible ✅)
    
    > *"Para descubrimiento viral, los shares importan más que los likes"*
    """)

with col2:
    st.markdown("""
    ### 🎯 Estrategia de Funnel
    
    ```
    TikTok/FB (5-10 clips/día)
           ↓
    Instagram (2 mejores)
           ↓
    Pauta (1 video/semana)
    ```
    
    **Objetivo:** Maximizar alcance con inversión optimizada.
    """)

# Footer
st.markdown("""
<div style="text-align: center; color: #718096; padding: 2rem; margin-top: 2rem;">
    <p>📊 Social Media Analytics Dashboard</p>
    <p>Desarrollado con Streamlit + Plotly | Enero 2026</p>
</div>
""", unsafe_allow_html=True)
