"""
📊 DASHBOARD DE ANÁLISIS - REDES SOCIALES
Análisis histórico de rendimiento para @miguemontes1
Desarrollado por: Walter - Enero 2026
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ============================================
# CONFIGURACIÓN DE PÁGINA
# ============================================
st.set_page_config(
    page_title="📊 Análisis de Redes Sociales",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# ESTILOS CSS PERSONALIZADOS
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
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .semaforo-verde { color: #38a169; font-weight: bold; }
    .semaforo-amarillo { color: #d69e2e; font-weight: bold; }
    .semaforo-rojo { color: #e53e3e; font-weight: bold; }
    .semaforo-viral { color: #805ad5; font-weight: bold; }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNCIONES DE CARGA Y PROCESAMIENTO
# ============================================
@st.cache_data
def cargar_datos():
    """Carga y procesa los datos del Excel"""
    df = pd.read_excel('datos.xlsx', sheet_name='instagram', header=0)
    ig_df = df[df['Link Publicación'] == 'Instagram'].copy()
    
    # Calcular métricas
    ig_df['Sends_per_Reach'] = ((ig_df['Compartidos'] + ig_df['Reposteados']) / ig_df['Reproducciones']) * 100
    ig_df['Likes_per_Reach'] = (ig_df['Likes'] / ig_df['Reproducciones']) * 100
    
    # Normalizar para Quality Score
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

def semaforo_sends(val):
    if val > 1.0: return "🚀", "Explosivo"
    elif val > 0.4: return "🟢", "Alto"
    elif val > 0.1: return "🟡", "Promedio"
    else: return "🔴", "Bajo"

def semaforo_likes(val):
    if val > 6.0: return "🚀", "Viral"
    elif val > 3.0: return "🟢", "Excelente"
    elif val > 1.5: return "🟡", "Promedio"
    else: return "🔴", "Bajo"

def semaforo_qs(val):
    if val >= 8: return "🚀", "Excelente"
    elif val >= 6: return "🟢", "Bueno"
    elif val >= 4: return "🟡", "Promedio"
    else: return "🔴", "Bajo"

# ============================================
# CARGAR DATOS
# ============================================
try:
    df = cargar_datos()
except Exception as e:
    st.error(f"Error al cargar datos: {e}")
    st.stop()

# ============================================
# HEADER PRINCIPAL
# ============================================
st.markdown('<h1 class="main-header">📊 Dashboard de Análisis</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Análisis histórico de rendimiento en redes sociales</p>', unsafe_allow_html=True)

# ============================================
# SIDEBAR - INFORMACIÓN DEL PERFIL
# ============================================
with st.sidebar:
    st.image("https://via.placeholder.com/150x150.png?text=@miguemontes1", width=150)
    st.markdown("### 👤 Perfil Analizado")
    st.markdown("**@miguemontes1**")
    st.markdown("Miguel A. Montes Curi")
    st.divider()
    st.markdown("### 📈 Datos del Perfil")
    st.metric("Seguidores", "5,244")
    st.metric("Categoría", "Nano Influencer")
    st.metric("Videos Analizados", len(df))
    st.divider()
    st.markdown("### 📅 Período")
    st.markdown("Agosto 2025 - Enero 2026")
    st.divider()
    st.markdown("### ℹ️ Fuente")
    st.markdown("Algoritmo Instagram 2025")
    st.markdown("*Adam Mosseri, CEO Instagram*")

# ============================================
# MÉTRICAS PRINCIPALES (KPIs)
# ============================================
st.markdown("## 🎯 Métricas Globales")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="👁️ Total Vistas",
        value=f"{df['Reproducciones'].sum():,.0f}",
        delta=f"Prom: {df['Reproducciones'].mean():,.0f}/video"
    )

with col2:
    st.metric(
        label="❤️ Total Likes",
        value=f"{df['Likes'].sum():,.0f}",
        delta=f"Prom: {df['Likes'].mean():,.0f}/video"
    )

with col3:
    st.metric(
        label="💬 Total Comentarios",
        value=f"{df['Conteo Comentarios'].sum():,.0f}",
        delta=f"Prom: {df['Conteo Comentarios'].mean():,.0f}/video"
    )

with col4:
    st.metric(
        label="🔄 Total Compartidos",
        value=f"{df['Compartidos'].sum():,.0f}",
        delta=f"Prom: {df['Compartidos'].mean():,.0f}/video"
    )

with col5:
    st.metric(
        label="📤 Total Reposteados",
        value=f"{df['Reposteados'].sum():,.0f}",
        delta=f"Prom: {df['Reposteados'].mean():,.0f}/video"
    )

# Sección de Promedios por Video
st.markdown("### 📊 Promedios por Video")
col_p1, col_p2, col_p3, col_p4 = st.columns(4)

with col_p1:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 0.5rem; text-align: center; color: white;">
        <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">👁️ Prom. Views</p>
        <h3 style="margin: 0.3rem 0 0 0;">{df['Reproducciones'].mean():,.0f}</h3>
    </div>
    """, unsafe_allow_html=True)

with col_p2:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 1rem; border-radius: 0.5rem; text-align: center; color: white;">
        <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">❤️ Prom. Likes</p>
        <h3 style="margin: 0.3rem 0 0 0;">{df['Likes'].mean():,.0f}</h3>
    </div>
    """, unsafe_allow_html=True)

with col_p3:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 1rem; border-radius: 0.5rem; text-align: center; color: white;">
        <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">💬 Prom. Comentarios</p>
        <h3 style="margin: 0.3rem 0 0 0;">{df['Conteo Comentarios'].mean():,.0f}</h3>
    </div>
    """, unsafe_allow_html=True)

with col_p4:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 1rem; border-radius: 0.5rem; text-align: center; color: white;">
        <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">🔄 Prom. Compartidos</p>
        <h3 style="margin: 0.3rem 0 0 0;">{df['Compartidos'].mean():,.0f}</h3>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ============================================
# SEMÁFOROS DE RENDIMIENTO
# ============================================
st.markdown("## 🚦 Evaluación según Benchmarks (Mosseri 2025)")

col1, col2, col3 = st.columns(3)

sends_avg = df['Sends_per_Reach'].mean()
likes_avg = df['Likes_per_Reach'].mean()
qs_avg = df['Quality_Score'].mean()

with col1:
    emoji, estado = semaforo_sends(sends_avg)
    st.markdown(f"""
    <div style="background: #f7fafc; padding: 1.5rem; border-radius: 1rem; text-align: center; border-left: 5px solid {'#38a169' if emoji in ['🟢','🚀'] else '#d69e2e' if emoji == '🟡' else '#e53e3e'};">
        <h1 style="margin: 0;">{emoji}</h1>
        <h3 style="margin: 0.5rem 0; color: #1a365d; font-weight: 700;">📤 Sends per Reach</h3>
        <h2 style="margin: 0; color: #2d3748;">{sends_avg:.2f}%</h2>
        <p style="margin: 0.5rem 0 0 0; color: #4a5568; font-weight: 600;">{estado}</p>
        <p style="margin: 0.5rem 0 0 0; color: #718096; font-size: 0.8rem;">(Compartidos + Reposteados) / Vistas</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    emoji, estado = semaforo_likes(likes_avg)
    st.markdown(f"""
    <div style="background: #f7fafc; padding: 1.5rem; border-radius: 1rem; text-align: center; border-left: 5px solid {'#38a169' if emoji in ['🟢','🚀'] else '#d69e2e' if emoji == '🟡' else '#e53e3e'};">
        <h1 style="margin: 0;">{emoji}</h1>
        <h3 style="margin: 0.5rem 0; color: #1a365d; font-weight: 700;">❤️ Likes per Reach</h3>
        <h2 style="margin: 0; color: #2d3748;">{likes_avg:.2f}%</h2>
        <p style="margin: 0.5rem 0 0 0; color: #4a5568; font-weight: 600;">{estado}</p>
        <p style="margin: 0.5rem 0 0 0; color: #718096; font-size: 0.8rem;">Likes / Vistas</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    emoji, estado = semaforo_qs(qs_avg)
    st.markdown(f"""
    <div style="background: #f7fafc; padding: 1.5rem; border-radius: 1rem; text-align: center; border-left: 5px solid {'#38a169' if emoji in ['🟢','🚀'] else '#d69e2e' if emoji == '🟡' else '#e53e3e'};">
        <h1 style="margin: 0;">{emoji}</h1>
        <h3 style="margin: 0.5rem 0; color: #1a365d; font-weight: 700;">⭐ Quality Score</h3>
        <h2 style="margin: 0; color: #2d3748;">{qs_avg:.1f}/10</h2>
        <p style="margin: 0.5rem 0 0 0; color: #4a5568; font-weight: 600;">{estado}</p>
        <p style="margin: 0.5rem 0 0 0; color: #718096; font-size: 0.8rem;">Índice combinado de engagement</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ============================================
# TABS DE CONTENIDO
# ============================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Rankings", 
    "📊 Correlaciones", 
    "🎭 Sentimiento",
    "📉 Tendencias",
    "🔍 Detalle Videos"
])

# ============================================
# TAB 1: RANKINGS
# ============================================
with tab1:
    st.markdown("### 🏆 TOP 10 Videos por Métrica")
    
    metrica_seleccionada = st.selectbox(
        "Selecciona la métrica:",
        ["Reproducciones", "Likes", "Conteo Comentarios", "Compartidos", "Reposteados"],
        format_func=lambda x: {
            "Reproducciones": "👁️ Vistas",
            "Likes": "❤️ Likes",
            "Conteo Comentarios": "💬 Comentarios",
            "Compartidos": "🔄 Compartidos",
            "Reposteados": "📤 Reposteados"
        }.get(x, x)
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🥇 TOP 10 - Mejores")
        top_df = df.nlargest(10, metrica_seleccionada)[['#', 'Fecha', metrica_seleccionada, 'Sends_per_Reach', 'Likes_per_Reach', 'Quality_Score']].copy()
        top_df['Fecha'] = pd.to_datetime(top_df['Fecha']).dt.strftime('%Y-%m-%d')
        top_df['Sends_per_Reach'] = top_df['Sends_per_Reach'].apply(lambda x: f"{x:.2f}%")
        top_df['Likes_per_Reach'] = top_df['Likes_per_Reach'].apply(lambda x: f"{x:.2f}%")
        top_df['Quality_Score'] = top_df['Quality_Score'].fillna(0).apply(lambda x: f"{x:.1f}")
        st.dataframe(top_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### 📉 TOP 10 - Peores")
        bottom_df = df.nsmallest(10, metrica_seleccionada)[['#', 'Fecha', metrica_seleccionada, 'Sends_per_Reach', 'Likes_per_Reach', 'Quality_Score']].copy()
        bottom_df['Fecha'] = pd.to_datetime(bottom_df['Fecha']).dt.strftime('%Y-%m-%d')
        bottom_df['Sends_per_Reach'] = bottom_df['Sends_per_Reach'].apply(lambda x: f"{x:.2f}%")
        bottom_df['Likes_per_Reach'] = bottom_df['Likes_per_Reach'].apply(lambda x: f"{x:.2f}%")
        bottom_df['Quality_Score'] = bottom_df['Quality_Score'].fillna(0).apply(lambda x: f"{x:.1f}")
        st.dataframe(bottom_df, use_container_width=True, hide_index=True)
    
    # Gráfico de barras
    st.markdown("#### 📊 Visualización TOP 10")
    top_chart = df.nlargest(10, metrica_seleccionada)
    fig = px.bar(
        top_chart, 
        x='#', 
        y=metrica_seleccionada,
        color='Quality_Score',
        color_continuous_scale='RdYlGn',
        title=f'TOP 10 Videos por {metrica_seleccionada}',
        labels={'#': 'Video #', metrica_seleccionada: metrica_seleccionada}
    )
    fig.update_layout(xaxis_type='category')
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# TAB 2: CORRELACIONES
# ============================================
with tab2:
    st.markdown("### 🔗 Análisis de Correlaciones")
    st.markdown("*¿Qué métricas predicen la viralidad (vistas)?*")
    
    # Calcular correlaciones
    from scipy import stats
    
    correlaciones = {
        'Compartidos': stats.pearsonr(df['Compartidos'], df['Reproducciones']),
        'Likes': stats.pearsonr(df['Likes'], df['Reproducciones']),
        'Comentarios': stats.pearsonr(df['Conteo Comentarios'], df['Reproducciones']),
    }
    
    # Mostrar tabla de correlaciones
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### 📋 Tabla de Correlaciones")
        corr_data = []
        for metrica, (corr, pval) in correlaciones.items():
            r2 = corr**2 * 100
            if abs(corr) < 0.3:
                fuerza = "🔴 Débil"
            elif abs(corr) < 0.7:
                fuerza = "🟡 Moderada"
            else:
                fuerza = "🟢 Fuerte"
            corr_data.append({
                'Métrica': metrica,
                'Correlación': f"{corr:.3f}",
                'R²': f"{r2:.1f}%",
                'Fuerza': fuerza
            })
        
        st.dataframe(pd.DataFrame(corr_data), use_container_width=True, hide_index=True)
        
        st.markdown("""
        **Interpretación:**
        - **R² = 73%** de las vistas se explica por Likes
        - **27% restante** depende de **Watch Time** (no medible)
        """)
    
    with col2:
        st.markdown("#### 📈 Scatter Plots")
        scatter_metrica = st.selectbox(
            "Ver correlación con Vistas:",
            ["Likes", "Compartidos", "Conteo Comentarios"]
        )
        
        fig = px.scatter(
            df,
            x=scatter_metrica,
            y='Reproducciones',
            color='Quality_Score',
            color_continuous_scale='RdYlGn',
            hover_data=['#', 'Fecha'],
            title=f'{scatter_metrica} vs Vistas'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Conclusión importante
    st.info("""
    💡 **Hallazgo Clave:** Los compartidos tienen correlación DÉBIL (0.255) con las vistas. 
    Un video muy compartido NO garantiza viralidad. La clave está en el **Watch Time** 
    (retención del público frío), según Adam Mosseri, CEO de Instagram (Enero 2025).
    """)

# ============================================
# TAB 3: SENTIMIENTO
# ============================================
with tab3:
    st.markdown("### 🎭 Análisis de Sentimiento")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Distribución de Sentimiento")
        sentimiento_data = {
            'Categoría': ['Positivos', 'Neutrales', 'Negativos'],
            'Cantidad': [1131, 331, 182],
            'Porcentaje': [68.8, 20.1, 11.1]
        }
        sent_df = pd.DataFrame(sentimiento_data)
        
        fig = px.pie(
            sent_df, 
            values='Cantidad', 
            names='Categoría',
            color='Categoría',
            color_discrete_map={
                'Positivos': '#38a169',
                'Neutrales': '#718096',
                'Negativos': '#e53e3e'
            },
            title='Distribución de 1,644 Comentarios'
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 😀 Emojis Más Usados")
        emoji_data = {
            'Emoji': ['👏 Aplausos', '🙌 Celebración', '🔥 Fuego', '❤️ Corazón', '😍 Admiración'],
            'Cantidad': [1761, 330, 278, 222, 169]
        }
        emoji_df = pd.DataFrame(emoji_data)
        
        fig = px.bar(
            emoji_df, 
            x='Cantidad', 
            y='Emoji',
            orientation='h',
            color='Cantidad',
            color_continuous_scale='Oranges',
            title='TOP 5 Emojis en Comentarios'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Alertas de críticas
    st.markdown("#### ⚠️ Alertas Identificadas")
    col1, col2 = st.columns(2)
    
    with col1:
        st.warning("""
        **21 críticas reales identificadas:**
        - Referencias a William Montes
        - Menciones del Pacto de Ralito
        - Videos afectados: #5, #9, #17, #23
        """)
    
    with col2:
        st.error("""
        **⚠️ Spam/Bot detectado:**
        - 1 comentario repetido 7+ veces
        - Texto promocional estructurado
        - Videos: #20, #22, #23, #24, #26, #27, #29, #31
        """)

# ============================================
# TAB 4: TENDENCIAS
# ============================================
with tab4:
    st.markdown("### 📉 Tendencias Temporales")
    
    # Preparar datos temporales
    df_temp = df.copy()
    df_temp['Fecha'] = pd.to_datetime(df_temp['Fecha'])
    df_temp = df_temp.sort_values('Fecha')
    
    # Gráfico de línea - Vistas en el tiempo
    st.markdown("#### 👁️ Evolución de Vistas")
    fig = px.line(
        df_temp, 
        x='Fecha', 
        y='Reproducciones',
        markers=True,
        title='Reproducciones por Video (Cronológico)'
    )
    fig.add_hline(y=df['Reproducciones'].mean(), line_dash="dash", line_color="red", 
                  annotation_text=f"Promedio: {df['Reproducciones'].mean():,.0f}")
    st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico de Quality Score en el tiempo
    st.markdown("#### ⭐ Evolución de Quality Score")
    fig = px.line(
        df_temp, 
        x='Fecha', 
        y='Quality_Score',
        markers=True,
        color_discrete_sequence=['#805ad5'],
        title='Quality Score por Video (Cronológico)'
    )
    fig.add_hline(y=df['Quality_Score'].mean(), line_dash="dash", line_color="orange",
                  annotation_text=f"Promedio: {df['Quality_Score'].mean():.1f}")
    st.plotly_chart(fig, use_container_width=True)
    
    # Días sin publicar
    st.markdown("#### 📅 Frecuencia de Publicación")
    if 'Días sin publicar' in df.columns:
        fig = px.histogram(
            df, 
            x='Días sin publicar',
            nbins=20,
            title='Distribución de Días entre Publicaciones',
            color_discrete_sequence=['#667eea']
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# TAB 5: DETALLE VIDEOS
# ============================================
with tab5:
    st.markdown("### 🔍 Explorador de Videos")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_views = st.number_input("Mínimo de Vistas", min_value=0, value=0)
    
    with col2:
        min_qs = st.slider("Mínimo Quality Score", 1.0, 10.0, 1.0)
    
    with col3:
        orden = st.selectbox("Ordenar por", ["Reproducciones", "Quality_Score", "Likes", "Fecha"])
    
    # Filtrar datos
    df_filtrado = df[
        (df['Reproducciones'] >= min_views) & 
        (df['Quality_Score'] >= min_qs)
    ].sort_values(orden, ascending=False)
    
    st.markdown(f"**{len(df_filtrado)} videos encontrados**")
    
    # Mostrar tabla interactiva
    columnas_mostrar = ['#', 'Fecha', 'Reproducciones', 'Likes', 'Conteo Comentarios', 
                        'Compartidos', 'Sends_per_Reach', 'Likes_per_Reach', 'Quality_Score']
    
    df_mostrar = df_filtrado[columnas_mostrar].copy()
    df_mostrar['Fecha'] = pd.to_datetime(df_mostrar['Fecha']).dt.strftime('%Y-%m-%d')
    df_mostrar['Sends_per_Reach'] = df_mostrar['Sends_per_Reach'].apply(lambda x: f"{x:.2f}%")
    df_mostrar['Likes_per_Reach'] = df_mostrar['Likes_per_Reach'].apply(lambda x: f"{x:.2f}%")
    df_mostrar['Quality_Score'] = df_mostrar['Quality_Score'].fillna(0).apply(lambda x: f"{x:.1f}")
    
    st.dataframe(df_mostrar, use_container_width=True, hide_index=True)

# ============================================
# FOOTER
# ============================================
st.divider()

# Cargar logo como base64 para incrustar en HTML
import base64
with open("logo_ryan.png", "rb") as img_file:
    logo_base64 = base64.b64encode(img_file.read()).decode()

st.markdown(f"""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 1rem; margin-top: 0.5rem;">
    <img src="data:image/png;base64,{logo_base64}" style="width: 150px; margin-bottom: 1rem; display: block; margin-left: auto; margin-right: auto;">
    <p style="margin: 0.5rem 0; color: #4a5568; font-size: 1rem;">Análisis y Dashboard desarrollado por <strong>Ryan Deivis</strong></p>
    <p style="margin: 0.5rem 0; color: #718096; font-size: 0.9rem;">📊 Dashboard de Análisis de Redes Sociales</p>
    <p style="margin: 0.5rem 0; color: #718096; font-size: 0.9rem;">Basado en metodología de Adam Mosseri (CEO Instagram) - Enero 2025</p>
    <p style="margin: 1rem 0 0 0; color: #a0aec0; font-size: 0.8rem;">© 2026 - Desarrollado con Streamlit + Plotly</p>
</div>
""", unsafe_allow_html=True)
