"""
🎯 DASHBOARD DE ESTRATEGIA - REDES SOCIALES
Herramienta operativa para publicación de contenido
Desarrollado por: Walter - Enero 2026
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# ============================================
# CONFIGURACIÓN DE PÁGINA
# ============================================
st.set_page_config(
    page_title="🎯 Estrategia de Contenido",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# ESTILOS CSS
# ============================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a365d;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #718096;
        text-align: center;
        margin-bottom: 2rem;
    }
    .platform-card {
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .tiktok-card {
        background: linear-gradient(135deg, #000000 0%, #25F4EE 50%, #FE2C55 100%);
        color: white;
    }
    .instagram-card {
        background: linear-gradient(135deg, #833AB4 0%, #FD1D1D 50%, #FCAF45 100%);
        color: white;
    }
    .facebook-card {
        background: linear-gradient(135deg, #1877F2 0%, #3B5998 100%);
        color: white;
    }
    .recomendacion-box {
        background: #f0fff4;
        border-left: 5px solid #38a169;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .alerta-box {
        background: #fffaf0;
        border-left: 5px solid #dd6b20;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .pauta-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNCIONES
# ============================================
@st.cache_data
def cargar_datos():
    """Carga y procesa los datos del Excel"""
    df = pd.read_excel('datos.xlsx', sheet_name='instagram', header=0)
    ig_df = df[df['Link Publicación'] == 'Instagram'].copy()
    
    # Calcular métricas
    ig_df['Sends_per_Reach'] = ((ig_df['Compartidos'] + ig_df['Reposteados']) / ig_df['Reproducciones']) * 100
    ig_df['Likes_per_Reach'] = (ig_df['Likes'] / ig_df['Reproducciones']) * 100
    
    def normalize_to_10(series):
        min_val = series.min()
        max_val = series.max()
        if max_val == min_val:
            return pd.Series([5.0] * len(series))
        return 1 + 9 * (series - min_val) / (max_val - min_val)
    
    ig_df['Sends_Score'] = normalize_to_10(ig_df['Sends_per_Reach'])
    ig_df['Likes_Score'] = normalize_to_10(ig_df['Likes_per_Reach'])
    ig_df['Quality_Score'] = (ig_df['Sends_Score'] * 0.6) + (ig_df['Likes_Score'] * 0.4)
    
    return ig_df

def obtener_mejor_formato():
    """Retorna el formato de video que mejor funciona"""
    return {
        'tipo': 'Preguntas en la Calle',
        'duracion': '0:30 - 1:00',
        'elementos': [
            '✅ Rostro visible hablando a cámara',
            '✅ Interacción con personas reales',
            '✅ Preguntas de interés general',
            '✅ Locación reconocible (Cartagena)'
        ],
        'evitar': [
            '❌ Contenido político tradicional',
            '❌ Videos muy editados',
            '❌ Contenido solo para círculo cercano'
        ]
    }

def calcular_presupuesto_pauta(views_objetivo, cpm=5):
    """Calcula presupuesto sugerido para pauta"""
    return (views_objetivo / 1000) * cpm

# ============================================
# CARGAR DATOS
# ============================================
try:
    df = cargar_datos()
except Exception as e:
    st.error(f"Error al cargar datos: {e}")
    st.stop()

# ============================================
# HEADER
# ============================================
st.markdown('<h1 class="main-header">🎯 Estrategia de Contenido</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Herramienta operativa para publicación en redes sociales</p>', unsafe_allow_html=True)

# ============================================
# SIDEBAR - CONFIGURACIÓN
# ============================================
with st.sidebar:
    st.markdown("### ⚙️ Configuración")
    
    st.markdown("#### 📅 Semana Actual")
    fecha_inicio = st.date_input("Fecha inicio semana", datetime.now())
    
    st.divider()
    
    st.markdown("#### 📊 Parámetros de Selección")
    clips_tiktok_fb = st.slider("Clips diarios TikTok/FB", 3, 15, 7)
    clips_instagram = st.slider("Clips diarios Instagram", 1, 5, 2)
    
    st.divider()
    
    st.markdown("#### 💰 Pauta Semanal")
    presupuesto_semanal = st.number_input("Presupuesto (COP)", min_value=0, value=100000, step=10000)
    cpm_estimado = st.number_input("CPM estimado ($)", min_value=1.0, value=5.0, step=0.5)
    
    views_estimados = int((presupuesto_semanal / cpm_estimado) * 1000 / 4500)  # Convertir COP a USD aprox
    st.metric("Views Estimados", f"{views_estimados:,}")

# ============================================
# ESTRATEGIA - FUNNEL DE CONTENIDO
# ============================================
st.markdown("## 📈 Estrategia: Funnel de Contenido")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="platform-card tiktok-card">
        <h2>📱 TikTok + Facebook</h2>
        <h1 style="font-size: 3rem;">5-10</h1>
        <p>clips diarios</p>
        <p><strong>Objetivo:</strong> Volumen + Descubrimiento</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="platform-card instagram-card">
        <h2>📸 Instagram</h2>
        <h1 style="font-size: 3rem;">2</h1>
        <p>mejores del día</p>
        <p><strong>Objetivo:</strong> Audiencia de Calidad</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="platform-card facebook-card">
        <h2>💰 Pauta Semanal</h2>
        <h1 style="font-size: 3rem;">1</h1>
        <p>video pautado</p>
        <p><strong>Objetivo:</strong> Amplificación</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ============================================
# TABS DE ESTRATEGIA
# ============================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📱 Selector TikTok/FB",
    "📸 Selector Instagram", 
    "💰 Recomendación Pauta",
    "📅 Calendario"
])

# ============================================
# TAB 1: SELECTOR TIKTOK/FB
# ============================================
with tab1:
    st.markdown("### 📱 Videos para TikTok y Facebook")
    st.markdown("*Selecciona 5-10 clips diarios basados en el formato que mejor funciona*")
    
    # Mostrar formato recomendado
    formato = obtener_mejor_formato()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ✅ Formato Recomendado")
        st.success(f"""
        **Tipo:** {formato['tipo']}
        
        **Duración:** {formato['duracion']}
        
        **Elementos clave:**
        """)
        for elem in formato['elementos']:
            st.markdown(f"- {elem}")
    
    with col2:
        st.markdown("#### ❌ Evitar")
        st.error("**No publicar:**")
        for elem in formato['evitar']:
            st.markdown(f"- {elem}")
    
    st.divider()
    
    # Videos disponibles ordenados por potencial viral
    st.markdown("#### 🎬 Videos Disponibles (ordenados por Quality Score)")
    
    # Filtrar por categoría si está disponible
    df_tiktok = df.sort_values('Quality_Score', ascending=False)
    
    # Mostrar tabla de selección
    df_seleccion = df_tiktok[['#', 'Fecha', 'Reproducciones', 'Likes', 'Quality_Score', 'Descripción/Caption']].head(20).copy()
    df_seleccion['Fecha'] = pd.to_datetime(df_seleccion['Fecha']).dt.strftime('%Y-%m-%d')
    df_seleccion['Quality_Score'] = df_seleccion['Quality_Score'].apply(lambda x: f"⭐ {x:.1f}")
    df_seleccion['Descripción/Caption'] = df_seleccion['Descripción/Caption'].apply(
        lambda x: str(x)[:50] + "..." if pd.notna(x) and len(str(x)) > 50 else x
    )
    
    st.dataframe(df_seleccion, use_container_width=True, hide_index=True)
    
    # Sugerencia automática
    st.markdown("#### 🤖 Sugerencia Automática para Hoy")
    top_videos = df_tiktok.head(clips_tiktok_fb)
    
    st.info(f"""
    **Videos sugeridos para publicar hoy en TikTok/FB:**
    
    {', '.join([f"Video #{int(v)}" for v in top_videos['#'].tolist()])}
    
    *Basado en Quality Score + Sends per Reach*
    """)

# ============================================
# TAB 2: SELECTOR INSTAGRAM
# ============================================
with tab2:
    st.markdown("### 📸 Videos para Instagram")
    st.markdown("*Selecciona los 2 mejores videos del día basados en rendimiento*")
    
    col1, col2 = st.columns(2)
    
    # Opción 1: Por más vistas
    with col1:
        st.markdown("#### 👁️ Opción A: Por Vistas")
        st.markdown("*Videos con mayor alcance*")
        
        top_views = df.nlargest(5, 'Reproducciones')[['#', 'Reproducciones', 'Likes', 'Quality_Score']]
        top_views['Quality_Score'] = top_views['Quality_Score'].apply(lambda x: f"⭐ {x:.1f}")
        st.dataframe(top_views, use_container_width=True, hide_index=True)
        
        mejor_views = df.nlargest(1, 'Reproducciones').iloc[0]
        st.success(f"""
        🥇 **Recomendado:** Video #{int(mejor_views['#'])}
        - Vistas: {mejor_views['Reproducciones']:,.0f}
        - Quality Score: {mejor_views['Quality_Score']:.1f}
        """)
    
    # Opción 2: Por más likes
    with col2:
        st.markdown("#### ❤️ Opción B: Por Likes")
        st.markdown("*Videos con mayor engagement*")
        
        top_likes = df.nlargest(5, 'Likes')[['#', 'Reproducciones', 'Likes', 'Quality_Score']]
        top_likes['Quality_Score'] = top_likes['Quality_Score'].apply(lambda x: f"⭐ {x:.1f}")
        st.dataframe(top_likes, use_container_width=True, hide_index=True)
        
        mejor_likes = df.nlargest(1, 'Likes').iloc[0]
        st.success(f"""
        🥇 **Recomendado:** Video #{int(mejor_likes['#'])}
        - Likes: {mejor_likes['Likes']:,.0f}
        - Quality Score: {mejor_likes['Quality_Score']:.1f}
        """)
    
    st.divider()
    
    # Recomendación final
    st.markdown("#### 🎯 Recomendación Final para Instagram Hoy")
    
    # Combinar mejores por vistas y por likes
    video1 = df.nlargest(1, 'Reproducciones').iloc[0]
    video2 = df.nlargest(2, 'Likes').iloc[1] if df.nlargest(1, 'Likes').iloc[0]['#'] == video1['#'] else df.nlargest(1, 'Likes').iloc[0]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #833AB4 0%, #FD1D1D 100%); 
                    color: white; padding: 1.5rem; border-radius: 1rem; text-align: center;">
            <h3>📸 Video #1</h3>
            <h1>#{int(video1['#'])}</h1>
            <p>👁️ {video1['Reproducciones']:,.0f} vistas</p>
            <p>❤️ {video1['Likes']:,.0f} likes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FCAF45 0%, #833AB4 100%); 
                    color: white; padding: 1.5rem; border-radius: 1rem; text-align: center;">
            <h3>📸 Video #2</h3>
            <h1>#{int(video2['#'])}</h1>
            <p>👁️ {video2['Reproducciones']:,.0f} vistas</p>
            <p>❤️ {video2['Likes']:,.0f} likes</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# TAB 3: RECOMENDACIÓN PAUTA
# ============================================
with tab3:
    st.markdown("### 💰 Recomendación de Pauta Semanal")
    st.markdown("*Selección automática del mejor video para invertir*")
    
    # Calcular el mejor video para pauta (combinación de métricas)
    df['Pauta_Score'] = (
        df['Quality_Score'] * 0.3 +
        (df['Reproducciones'] / df['Reproducciones'].max()) * 10 * 0.4 +
        (df['Likes'] / df['Likes'].max()) * 10 * 0.3
    )
    
    mejor_pauta = df.nlargest(1, 'Pauta_Score').iloc[0]
    
    st.markdown(f"""
    <div class="pauta-box">
        <h2>🏆 VIDEO RECOMENDADO PARA PAUTA</h2>
        <h1 style="font-size: 4rem;">Video #{int(mejor_pauta['#'])}</h1>
        <p style="font-size: 1.2rem;">
            👁️ {mejor_pauta['Reproducciones']:,.0f} vistas orgánicas | 
            ❤️ {mejor_pauta['Likes']:,.0f} likes |
            ⭐ QS: {mejor_pauta['Quality_Score']:.1f}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Detalles de la pauta
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Proyección de Resultados")
        
        # Calcular proyecciones
        views_organicas = mejor_pauta['Reproducciones']
        views_pauta = views_estimados
        views_total = views_organicas + views_pauta
        
        er_actual = (mejor_pauta['Likes'] / mejor_pauta['Reproducciones']) * 100
        likes_proyectados = int(views_pauta * (er_actual / 100) * 0.7)  # 70% de retención en pauta
        
        st.metric("Views Orgánicos", f"{views_organicas:,.0f}")
        st.metric("Views Estimados (Pauta)", f"{views_pauta:,}")
        st.metric("Views Total Proyectado", f"{views_total:,.0f}")
        st.metric("Likes Proyectados (Pauta)", f"{likes_proyectados:,}")
    
    with col2:
        st.markdown("#### 💵 Detalles de Inversión")
        
        st.metric("Presupuesto", f"${presupuesto_semanal:,.0f} COP")
        st.metric("CPM Estimado", f"${cpm_estimado:.2f} USD")
        st.metric("Costo por View", f"${cpm_estimado/1000:.4f} USD")
        
        # ROI estimado
        costo_por_like = presupuesto_semanal / likes_proyectados if likes_proyectados > 0 else 0
        st.metric("Costo por Like", f"${costo_por_like:.0f} COP")
    
    # Alternativas
    st.divider()
    st.markdown("#### 🔄 Videos Alternativos para Pauta")
    
    top_pauta = df.nlargest(5, 'Pauta_Score')[['#', 'Reproducciones', 'Likes', 'Quality_Score', 'Pauta_Score']]
    top_pauta['Quality_Score'] = top_pauta['Quality_Score'].apply(lambda x: f"⭐ {x:.1f}")
    top_pauta['Pauta_Score'] = top_pauta['Pauta_Score'].apply(lambda x: f"💰 {x:.1f}")
    
    st.dataframe(top_pauta, use_container_width=True, hide_index=True)

# ============================================
# TAB 4: CALENDARIO
# ============================================
with tab4:
    st.markdown("### 📅 Calendario de Publicación")
    
    # Generar calendario semanal
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    
    st.markdown("#### 📆 Plan Semanal")
    
    # Crear tabla de calendario
    calendario_data = []
    
    for i, dia in enumerate(dias):
        fecha = fecha_inicio + timedelta(days=i)
        
        # Sugerir videos basados en QS
        videos_dia = df.nlargest(clips_tiktok_fb + i, 'Quality_Score').tail(clips_tiktok_fb)
        videos_tiktok = ", ".join([f"#{int(v)}" for v in videos_dia['#'].head(clips_tiktok_fb).tolist()])
        
        videos_ig = df.nlargest(clips_instagram + i*2, 'Reproducciones').tail(clips_instagram)
        videos_instagram = ", ".join([f"#{int(v)}" for v in videos_ig['#'].tolist()])
        
        calendario_data.append({
            'Día': dia,
            'Fecha': fecha.strftime('%d/%m'),
            'TikTok/FB': videos_tiktok,
            'Instagram': videos_instagram,
            'Pauta': '💰' if i == 6 else ''  # Pauta el domingo
        })
    
    calendario_df = pd.DataFrame(calendario_data)
    st.dataframe(calendario_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Resumen semanal
    st.markdown("#### 📊 Resumen Semanal")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total TikTok/FB", f"{clips_tiktok_fb * 7} videos")
    
    with col2:
        st.metric("Total Instagram", f"{clips_instagram * 7} videos")
    
    with col3:
        st.metric("Pauta", "1 video")
    
    with col4:
        st.metric("Inversión", f"${presupuesto_semanal:,.0f} COP")
    
    # Checklist
    st.markdown("#### ✅ Checklist Semanal")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Preparar clips para TikTok/FB")
        st.checkbox("Seleccionar mejores para Instagram")
        st.checkbox("Revisar horarios óptimos de publicación")
        st.checkbox("Preparar copies/captions")
    
    with col2:
        st.checkbox("Configurar pauta en Meta Ads")
        st.checkbox("Definir audiencia de pauta")
        st.checkbox("Revisar métricas del día anterior")
        st.checkbox("Ajustar estrategia si es necesario")

# ============================================
# FOOTER
# ============================================
st.divider()
st.markdown("""
<div style="text-align: center; color: #718096; padding: 1rem;">
    <p>🎯 Dashboard de Estrategia de Contenido</p>
    <p>Metodología: Funnel de Contenido (TikTok/FB → Instagram → Pauta)</p>
    <p>Desarrollado con Streamlit + Plotly</p>
</div>
""", unsafe_allow_html=True)
