import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import os

from translations import TRANSLATIONS

st.set_page_config(
    page_title="Usina Solar · Noroeste Paulista",
    page_icon="⚡",
    layout="wide"
)

# ============================================================
# IDIOMAS (mesmos 10 do portfólio) — textos em translations.py
# ============================================================
LANGS = [
    ("pt", "🇧🇷", "PT"), ("en", "🇺🇸", "EN"), ("es", "🇪🇸", "ES"),
    ("it", "🇮🇹", "IT"), ("fr", "🇫🇷", "FR"), ("de", "🇩🇪", "DE"),
    ("zh", "🇨🇳", "ZH"), ("ar", "🇸🇦", "AR"), ("el", "🇬🇷", "EL"),
    ("af", "🇿🇦", "AF"),
]
CODES = [c for c, _, _ in LANGS]
FLAGS = {c: f"{flag} {label}" for c, flag, label in LANGS}

# separador decimal / de milhar usado nos textos e nos gráficos (Plotly: "decimal+milhar")
DECIMAL = {"pt": ",", "en": ".", "es": ",", "it": ",", "fr": ",", "de": ",",
           "zh": ".", "ar": ".", "el": ",", "af": ","}
THOUSANDS = {"pt": ".", "en": ",", "es": ".", "it": ".", "fr": "\u202f", "de": ".",
             "zh": ",", "ar": ",", "el": ".", "af": "\u00a0"}
PLOTLY_SEP = {"pt": ",.", "en": ".,", "es": ",.", "it": ",.", "fr": ", ",
              "de": ",.", "zh": ".,", "ar": ".,", "el": ",.", "af": ", "}


def _initial_lang():
    q = st.query_params.get("lang")
    if isinstance(q, list):
        q = q[0] if q else None
    return q if q in CODES else "pt"


if "lang" not in st.session_state:
    st.session_state.lang = _initial_lang()


def render_lang_selector():
    """Seletor com os 10 idiomas; guarda a escolha também na URL (?lang=xx)."""
    try:
        escolha = st.pills(
            "Language", CODES, selection_mode="single",
            default=st.session_state.lang, format_func=lambda c: FLAGS[c],
            key="lang_pick", label_visibility="collapsed",
        )
    except AttributeError:  # versões antigas do Streamlit sem st.pills
        escolha = st.radio(
            "Language", CODES, index=CODES.index(st.session_state.lang),
            format_func=lambda c: FLAGS[c], horizontal=True,
            key="lang_pick", label_visibility="collapsed",
        )
    if escolha and escolha != st.session_state.lang:
        st.session_state.lang = escolha
        st.query_params["lang"] = escolha
        st.rerun()


render_lang_selector()
LANG = st.session_state.lang
T = TRANSLATIONS[LANG]
RTL = LANG == "ar"


def fmt(x, nd=1):
    """Número com o separador decimal do idioma."""
    return f"{x:.{nd}f}".replace(".", DECIMAL[LANG])


def fmt_int(x):
    """Inteiro com o separador de milhar do idioma."""
    return f"{int(round(x)):,}".replace(",", THOUSANDS[LANG])


def plot(fig):
    """st.plotly_chart compatível com versões novas e antigas do Streamlit."""
    fig.update_layout(separators=PLOTLY_SEP[LANG])
    try:
        st.plotly_chart(fig, width="stretch")
    except TypeError:
        st.plotly_chart(fig, use_container_width=True)


def show_image(path):
    try:
        st.image(path, width="stretch")
    except TypeError:
        st.image(path, use_container_width=True)


# ============================================================
# ESTILOS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&family=DM+Mono&family=Noto+Serif:wght@700&family=Noto+Sans:wght@400;500&family=Noto+Sans+SC:wght@400;500;700&family=Noto+Naskh+Arabic:wght@400;700&display=swap');

:root{
  --solar:#F5A623;--solar-dark:#C47D0E;--solar-mid:#E8940F;
  --night:#0D1A2E;--night-mid:#142238;--night-light:#1A3050;
  --sky:#2C8FD9;--sky-light:#56B3F0;
  --green:#2D7A3A;--cream:#FDFAF4;--warm-gray:#8A7B6B;
  --danger:#C0392B;--black:#0D1117;
}
html,body,[class*="css"]{font-family:'DM Sans','Noto Sans','Noto Sans SC','Noto Naskh Arabic',sans-serif;background-color:var(--cream);color:var(--black);}

.hero-wrap{
  background:linear-gradient(135deg,var(--night) 0%,var(--night-mid) 55%,#1E3560 100%);
  border-radius:20px;padding:3rem 2.5rem 2rem;margin-bottom:2rem;
  position:relative;overflow:hidden;
}
.hero-wrap::before{content:"⚡";font-size:200px;position:absolute;right:-20px;top:-30px;opacity:0.05;}
.hero-tag{background:var(--solar);color:var(--night);font-family:'DM Mono','Noto Sans','Noto Sans SC','Noto Naskh Arabic',monospace;font-size:0.7rem;font-weight:bold;letter-spacing:2px;padding:4px 12px;border-radius:4px;display:inline-block;margin-bottom:1rem;text-transform:uppercase;}
.hero-title{font-family:'Playfair Display','Noto Serif','Noto Sans SC','Noto Naskh Arabic',serif;font-size:2.8rem;font-weight:900;color:#fff;line-height:1.15;margin-bottom:0.8rem;white-space:pre-line;}
.hero-subtitle{font-size:1rem;color:rgba(255,255,255,0.75);max-width:660px;line-height:1.6;margin-bottom:1.5rem;}
.hero-badges{display:flex;gap:10px;flex-wrap:wrap;}
.badge{background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.85);font-size:0.72rem;font-family:'DM Mono','Noto Sans','Noto Sans SC','Noto Naskh Arabic',monospace;padding:5px 12px;border-radius:20px;letter-spacing:0.5px;}
.badge-solar{background:rgba(245,166,35,0.2);border-color:var(--solar);color:var(--solar);}

.metric-box{background:white;border-radius:16px;padding:1.4rem 1.2rem;border-top:4px solid var(--solar);box-shadow:0 2px 12px rgba(0,0,0,0.06);text-align:center;}
.metric-box.green{border-top-color:var(--green);}
.metric-box.sky{border-top-color:var(--sky);}
.metric-box.night{border-top-color:var(--night-light);}
.metric-val{direction:ltr;font-family:'Playfair Display','Noto Serif','Noto Sans SC','Noto Naskh Arabic',serif;font-size:2.1rem;font-weight:900;color:var(--night);line-height:1;margin-bottom:0.3rem;}
.metric-label{font-size:0.75rem;color:var(--warm-gray);text-transform:uppercase;letter-spacing:1px;}

.section-label{font-family:'DM Mono','Noto Sans','Noto Sans SC','Noto Naskh Arabic',monospace;font-size:0.65rem;color:var(--solar-dark);text-transform:uppercase;letter-spacing:3px;margin-bottom:0.3rem;}
.section-title{font-family:'Playfair Display','Noto Serif','Noto Sans SC','Noto Naskh Arabic',serif;font-size:1.9rem;font-weight:700;color:var(--night);margin-bottom:1.2rem;line-height:1.2;}

.info-card{background:white;border-radius:16px;padding:1.5rem;box-shadow:0 2px 12px rgba(0,0,0,0.05);border-left:4px solid var(--solar);margin-bottom:1rem;}
.info-card.green{border-left-color:var(--green);}
.info-card.sky{border-left-color:var(--sky);}
.info-card.night{border-left-color:var(--night-light);}

.timeline-item{display:flex;gap:1rem;padding:1rem 0;border-bottom:1px solid #f0e8d8;}
.timeline-year{font-family:'Playfair Display','Noto Serif','Noto Sans SC','Noto Naskh Arabic',serif;font-size:1.1rem;font-weight:700;color:var(--solar-dark);min-width:80px;}
.timeline-content{flex:1;}
.timeline-title{font-weight:500;color:var(--night);margin-bottom:0.2rem;}
.timeline-desc{font-size:0.85rem;color:var(--warm-gray);}

.source-badges{display:flex;gap:8px;flex-wrap:wrap;margin-top:0.8rem;}
.source-badge{background:var(--night);color:white;font-family:'DM Mono','Noto Sans','Noto Sans SC','Noto Naskh Arabic',monospace;font-size:0.65rem;padding:4px 10px;border-radius:4px;letter-spacing:1px;text-transform:uppercase;}

.method-step{display:flex;align-items:flex-start;gap:1rem;padding:1rem;background:white;border-radius:12px;margin-bottom:0.8rem;box-shadow:0 1px 6px rgba(0,0,0,0.04);}
.step-num{background:var(--solar);color:var(--night);font-family:'Playfair Display','Noto Serif','Noto Sans SC','Noto Naskh Arabic',serif;font-size:1.1rem;font-weight:700;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.step-content{flex:1;}
.step-title{font-weight:500;color:var(--night);font-size:0.95rem;}
.step-desc{font-size:0.82rem;color:var(--warm-gray);margin-top:0.2rem;}

.discovery-box{background:linear-gradient(135deg,#FFF9EE 0%,#FFF3D0 100%);border:2px solid var(--solar);border-radius:16px;padding:1.8rem;margin:0.8rem 0;}
.discovery-title{font-family:'Playfair Display','Noto Serif','Noto Sans SC','Noto Naskh Arabic',serif;font-size:1.1rem;font-weight:700;color:var(--night);margin-bottom:0.5rem;}

.footer-wrap{background:var(--night);border-radius:20px;padding:2rem;color:rgba(255,255,255,0.8);text-align:center;margin-top:3rem;}
.footer-title{font-family:'Playfair Display','Noto Serif','Noto Sans SC','Noto Naskh Arabic',serif;color:var(--solar);font-size:1.2rem;margin-bottom:0.5rem;}

.photo-placeholder{background:#FFF8EC;border:2px dashed var(--solar-mid);border-radius:12px;padding:2rem;text-align:center;min-height:200px;display:flex;flex-direction:column;align-items:center;justify-content:center;}
.photo-emoji{font-size:2.5rem;}
.photo-title{font-weight:600;color:var(--night);margin:0.5rem 0 0.2rem;font-size:0.9rem;}
.photo-desc{font-size:0.78rem;color:var(--warm-gray);line-height:1.5;}
.photo-path{font-size:0.65rem;color:var(--solar-dark);font-family:'DM Mono','Noto Sans','Noto Sans SC','Noto Naskh Arabic',monospace;margin-top:0.5rem;background:#FFF3D0;padding:3px 8px;border-radius:4px;}
.photo-legenda{font-size:0.72rem;color:var(--warm-gray);font-style:italic;padding:0.5rem 0.8rem;background:#faf7f0;text-align:center;border-top:1px solid #f0e8d0;}
.photo-destaque{border:3px solid var(--solar);border-radius:14px;overflow:hidden;box-shadow:0 4px 20px rgba(245,166,35,0.2);}
</style>
""", unsafe_allow_html=True)


if RTL:
    # Árabe: texto da direita para a esquerda; mapa, gráficos e números continuam LTR
    st.markdown("""
<style>
[data-testid="stMain"], [data-testid="stAppViewContainer"] .main { direction: rtl; text-align: right; }
.hero-wrap, .info-card, .method-step, .discovery-box, .timeline-item { direction: rtl; text-align: right; }
.hero-wrap::before { right: auto; left: -20px; }
.info-card, .info-card.green, .info-card.sky, .info-card.night { border-left: none; border-right: 4px solid var(--solar); }
.js-plotly-plot, iframe { direction: ltr; }
body, html, [class*="css"] { font-family: 'Noto Naskh Arabic','DM Sans',sans-serif; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DADOS DE GERAÇÃO — baseados na notícia real
# ============================================================
# 1º semestre 2020: ~390.000 kWh → ~65.000 kWh/mês médio
# Distribuição mensal realista para região (irradiação Fernandópolis)
MES = T["months"]
meses_2020 = [f"{MES[i]}/20" for i in range(6)]
geracao_mwh = [72.0, 68.5, 65.0, 62.0, 58.5, 64.0]   # ~390 MWh total

# Acumulado desde fev/2019 até jul/2020 = 1.070 MWh
acumulado_mensal = [45, 60, 68, 62, 58, 55, 52, 50, 48, 46, 44, 42,   # 2019 fev–jan
                    72, 68.5, 65, 62, 58.5, 64]                          # 2020 jan–jun
meses_acum = [f"{MES[i]}/19" for i in range(1, 12)] + [f"{MES[i]}/20" for i in range(0, 6)]

co2_evitado_t = 953
nox_kg = 1568
so2_kg = 5.45
arvores_eq = 7250

# ============================================================
# HERO
# ============================================================
st.markdown(f"""
<div class="hero-wrap">
  <div class="hero-tag">{T['hero_tag']}</div>
  <div class="hero-title">{T['hero_title']}</div>
  <div class="hero-subtitle">{T['hero_subtitle']}</div>
  <div class="hero-badges">
    <span class="badge badge-solar">{T['badge1']}</span>
    <span class="badge badge-solar">{T['badge2']}</span>
    <span class="badge">{T['badge3']}</span>
    <span class="badge">{T['badge4']}</span>
    <span class="badge">{T['badge5']}</span>
  </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown(f'<div class="metric-box"><div class="metric-val">{fmt_int(390)} MWh</div><div class="metric-label">{T["m1"]}</div></div>', unsafe_allow_html=True)
with col2: st.markdown(f'<div class="metric-box green"><div class="metric-val">{fmt_int(953)} t</div><div class="metric-label">{T["m2"]}</div></div>', unsafe_allow_html=True)
with col3: st.markdown(f'<div class="metric-box sky"><div class="metric-val">{fmt_int(7250)}</div><div class="metric-label">{T["m3"]}</div></div>', unsafe_allow_html=True)
with col4: st.markdown(f'<div class="metric-box night"><div class="metric-val">{T["m4_value"]}</div><div class="metric-label">{T["m4"]}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# ABAS
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([T['tab1'], T['tab2'], T['tab3'], T['tab4'], T['tab5']])

# ── TAB 1: MAPA & ANÁLISE ────────────────────────────────────
with tab1:
    st.markdown(f'<div class="section-label">{T["map_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["map_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-card">{T["map_hint"]}</div>', unsafe_allow_html=True)

    # Mapa — UM único ponto com coordenadas fornecidas pelo usuário
    LAT_USINA = -20.298020
    LON_USINA = -50.282114

    # A chave fica no Streamlit Secrets, nunca no código público.
    try:
        carto_key = st.secrets.get("CARTO_API_KEY", "")
    except Exception:
        carto_key = ""

    # tiles=None impede o Folium de adicionar uma camada base automaticamente.
    mapa = folium.Map(
        location=[LAT_USINA, LON_USINA],
        zoom_start=16,
        tiles=None,
        control_scale=True,
    )

    if carto_key:
        folium.TileLayer(
            tiles=(
                "https://{s}.basemaps.cartocdn.com/rastertiles/voyager/"
                "{z}/{x}/{y}{r}.png?key=" + carto_key
            ),
            attr=(
                '&copy; <a href="https://www.openstreetmap.org/copyright">'
                "OpenStreetMap</a> contributors &copy; "
                '<a href="https://carto.com/attributions">CARTO</a>'
            ),
            name="CARTO Voyager",
            subdomains="abcd",
            max_zoom=20,
            overlay=False,
            control=True,
        ).add_to(mapa)
    else:
        # Fallback: o app continua funcional sem o Secret configurado.
        folium.TileLayer(
            "OpenStreetMap",
            name="OpenStreetMap",
            attr=(
                '&copy; <a href="https://www.openstreetmap.org/copyright">'
                "OpenStreetMap</a> contributors"
            ),
            control=True,
        ).add_to(mapa)

    popup_html = f"""
    <div style='font-family:sans-serif;min-width:240px;padding:12px;{"direction:rtl;text-align:right" if RTL else ""}'>
      <h4 style='color:#0D1A2E;margin:0 0 8px;font-size:14px'>{T['popup_title']}</h4>
      <p style='margin:3px 0;font-size:12px'>{T['popup_campus']}</p>
      <p style='margin:3px 0;font-size:12px'>{T['popup_inverter']}: <b>ABB TRIO-50.0-TL-OUTD · 50 kW</b></p>
      <p style='margin:3px 0;font-size:12px'>{T['popup_op']}: <b>{T['m4_value']}</b></p>
      <p style='margin:3px 0;font-size:12px'>{T['popup_gen']}: <b>{fmt(1.07, 2)} GWh</b> {T['popup_gen_until']}</p>
      <p style='margin:3px 0;font-size:12px'>{T['popup_co2']}: <b>{fmt_int(953)} t</b></p>
      <hr style='margin:8px 0;border-color:#eee'>
      <p style='margin:0;font-size:10px;color:#999;direction:ltr'>
        Lat: -20.298020 · Lon: -50.282114
      </p>
    </div>
    """

    # Ícone solar customizado
    folium.Marker(
        location=[LAT_USINA, LON_USINA],
        popup=folium.Popup(popup_html, max_width=280),
        tooltip=T["marker_tip"],
        icon=folium.Icon(color="orange", icon="sun-o", prefix="fa")
    ).add_to(mapa)

    # Círculo de área estimada da usina
    folium.Circle(
        location=[LAT_USINA, LON_USINA],
        radius=120,
        color="#F5A623", fill=True, fill_color="#F5A623",
        fill_opacity=0.15, weight=2,
        tooltip=T["area_tip"]
    ).add_to(mapa)

    folium_static(mapa, width=1100, height=480)

    # ── GRÁFICOS ──────────────────────────────────────────────
    st.markdown(f"<br><div class='section-label'>{T['chart_label']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>{T['chart_title']}</div>", unsafe_allow_html=True)

    # Gráfico 1 — barras de geração com raios / tema elétrico
    fig_gen = go.Figure()

    # Área preenchida para efeito visual
    fig_gen.add_trace(go.Bar(
        x=meses_2020, y=geracao_mwh,
        name=T["gen_name"],
        marker=dict(
            color=geracao_mwh,
            colorscale=[[0, "#0D1A2E"], [0.4, "#F5A623"], [0.7, "#FFD060"], [1, "#FFE898"]],
            line=dict(width=0),
        ),
        text=[f"⚡ {v:.0f}" for v in geracao_mwh],
        textposition='outside',
        textfont=dict(color="#C47D0E", size=12, family="DM Mono, Noto Sans"),
        hovertemplate='<b>%{x}</b><br>%{y:.1f} MWh<extra></extra>'
    ))

    # Linha de meta
    meta = sum(geracao_mwh) / len(geracao_mwh)
    fig_gen.add_hline(y=meta, line_dash="dash", line_color="#F5A623",
                       annotation_text="  " + T["avg_label"].format(v=fmt(meta, 0)),
                       annotation_font_color="#C47D0E")

    fig_gen.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(13,26,46,0.03)',
        font=dict(family='DM Sans, Noto Sans, Noto Sans SC, Noto Naskh Arabic', color='#0D1A2E'), height=380,
        xaxis=dict(showgrid=False, tickfont=dict(size=12)),
        yaxis=dict(showgrid=True, gridcolor='#f0e8d8', title=T['chart_y']),
        title=dict(font=dict(size=15, family='Playfair Display, Noto Serif, Noto Sans SC, Noto Naskh Arabic')),
        showlegend=False, margin=dict(t=30, b=20)
    )
    plot(fig_gen)

    col_a, col_b = st.columns(2)

    with col_a:
        # Gauge de CO₂ evitado — estilo voltímetro
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=co2_evitado_t,
            number={'suffix': " t CO₂", 'font': {'size': 28, 'family': 'Playfair Display', 'color': '#0D1A2E'}},
            delta={'reference': 500, 'increasing': {'color': "#2D7A3A"}},
            gauge={
                'axis': {'range': [0, 1200], 'tickwidth': 1, 'tickcolor': "#0D1A2E"},
                'bar': {'color': "#F5A623", 'thickness': 0.3},
                'bgcolor': "white",
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 400], 'color': '#FFF9EE'},
                    {'range': [400, 800], 'color': '#FFF3D0'},
                    {'range': [800, 1200], 'color': '#FFE898'},
                ],
                'threshold': {
                    'line': {'color': "#2D7A3A", 'width': 4},
                    'thickness': 0.75,
                    'value': co2_evitado_t
                }
            },
            title={'text': f"🌱 {T['chart2_title']}", 'font': {'size': 13, 'family': 'Playfair Display'}}
        ))
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', height=320,
            font=dict(family='DM Sans, Noto Sans, Noto Sans SC, Noto Naskh Arabic'), margin=dict(t=50, b=10)
        )
        plot(fig_gauge)

    with col_b:
        # Gráfico de impacto ambiental — barras horizontais com raios
        categorias = T["impact_cats"]
        valores_norm = [co2_evitado_t, nox_kg * 0.1, arvores_eq / 10]
        cores_bar = ["#F5A623", "#2D7A3A", "#2C8FD9"]

        fig_impact = go.Figure()
        for i, (cat, val, cor) in enumerate(zip(categorias, valores_norm, cores_bar)):
            fig_impact.add_trace(go.Bar(
                y=[cat], x=[val], orientation='h',
                marker_color=cor, opacity=0.85,
                name=cat,
                hovertemplate=f'<b>{cat}</b><br>{val:.0f}<extra></extra>'
            ))

        fig_impact.update_layout(
            title=dict(text=T['chart2_title'], font=dict(size=13, family='Playfair Display, Noto Serif, Noto Sans SC, Noto Naskh Arabic')),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=320, font=dict(family='DM Sans, Noto Sans, Noto Sans SC, Noto Naskh Arabic'),
            showlegend=False,
            xaxis=dict(showgrid=True, gridcolor='#f0e8d8'),
            yaxis=dict(showgrid=False),
            margin=dict(t=50, b=10, r=20)
        )
        plot(fig_impact)

    # Gráfico de linha acumulada
    acum_cumsum = np.cumsum(geracao_mwh).tolist()
    fig_acum = go.Figure()
    fig_acum.add_trace(go.Scatter(
        x=meses_2020, y=acum_cumsum,
        mode='lines+markers',
        line=dict(color='#F5A623', width=3),
        marker=dict(size=10, color='#F5A623', symbol='star',
                    line=dict(width=1, color='#C47D0E')),
        fill='tozeroy', fillcolor='rgba(245,166,35,0.08)',
        hovertemplate='<b>%{x}</b><br>' + T['cum_hover'] + ': %{y:.1f} MWh<extra></extra>',
        name=T['cum_name']
    ))
    # Linha de raio decorativa
    fig_acum.add_annotation(
        x=meses_2020[-1], y=acum_cumsum[-1],
        text=f"⚡ {fmt_int(390)} MWh", showarrow=False,
        font=dict(color="#C47D0E", size=12, family="DM Mono, Noto Sans"),
        xshift=5, yshift=15
    )
    fig_acum.update_layout(
        title=dict(text=T['chart3_title'], font=dict(size=13, family='Playfair Display, Noto Serif, Noto Sans SC, Noto Naskh Arabic')),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(13,26,46,0.02)',
        height=300, font=dict(family='DM Sans, Noto Sans, Noto Sans SC, Noto Naskh Arabic'),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#f0e8d8', title=T["cum_name"]),
        margin=dict(t=50, b=20)
    )
    plot(fig_acum)

# ── TAB 2: METODOLOGIA ────────────────────────────────────────
with tab2:
    st.markdown(f'<div class="section-label">{T["method_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["method_title"]}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="discovery-box">
      <div class="discovery-title">{T['sci_question_title']}</div>
      <p style="font-size:1.05rem;color:#1A2E50;line-height:1.7"><em>{T['sci_question']}</em></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="section-label" style="margin-top:1.5rem">{T["pipeline_label"]}</div>', unsafe_allow_html=True)

    for num, title, desc in T['steps']:
        st.markdown(f"""
        <div class="method-step">
          <div class="step-num">{num}</div>
          <div class="step-content">
            <div class="step-title">{title}</div>
            <div class="step-desc">{desc}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown(f"""
        <div class="info-card">
          <strong>{T['tech_specs_title']}</strong><br><br>
          <div style="font-size:0.88rem;line-height:2.1">{T['tech_specs']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
        <div class="info-card green">
          <strong>{T['env_title']}</strong><br><br>
          <div style="font-size:0.88rem;line-height:2.1">{T['env_text']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Fórmula ambiental
    formula_rows = "".join(f"<b>{k}:</b> {v}<br>" for k, v in T["formula_lines"])
    st.markdown(f"""
    <div class="info-card sky" style="margin-top:0.5rem;background:linear-gradient(135deg,#EFF7FF,#DCF0FF)">
      <strong style="color:#0D4E72">{T['formula_title']}</strong><br><br>
      <div style="font-family:'DM Mono','Noto Sans','Noto Sans SC','Noto Naskh Arabic',monospace;font-size:0.85rem;line-height:2.2;color:#1A4E72">
        {formula_rows}
      </div>
      <div style="font-size:0.75rem;color:#7A8A96;margin-top:0.5rem">
        {T['formula_source']}
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── TAB 3: DESCOBERTAS ────────────────────────────────────────
with tab3:
    st.markdown(f'<div class="section-label">{T["discovery_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["discovery_title"]}</div>', unsafe_allow_html=True)

    for emoji, titulo, texto in T['discoveries']:
        st.markdown(f"""
        <div class="discovery-box" style="margin-bottom:0.8rem">
          <div style="display:flex;align-items:flex-start;gap:1rem">
            <span style="font-size:1.5rem">{emoji}</span>
            <div>
              <div class="discovery-title">{titulo}</div>
              <p style="color:#2A1E0D;line-height:1.65;font-size:0.93rem;margin:0">{texto}</p>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f'<div class="section-label" style="margin-top:1.5rem">{T["conclusion_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="info-card" style="border-left-color:#0D1A2E;background:linear-gradient(135deg,#FFF9EE,#FFF0CC)">
      <strong style="color:#0D1A2E;font-size:1rem">{T['conclusion_title']}</strong><br><br>
      <p style="color:#3A2800;line-height:1.7;font-size:0.93rem">{T['conclusion_text']}</p>
      <p style="color:#C47D0E;font-size:0.82rem;margin-bottom:0"><em>{T['conclusion_author']}</em></p>
    </div>
    """, unsafe_allow_html=True)

    # Gráfico de raio — impacto por categoria
    fig_final = go.Figure()
    cats = T["final_cats"]
    vals = [390, 953, arvores_eq / 10, nox_kg / 10]
    cores_f = ["#F5A623", "#2D7A3A", "#2C8FD9", "#C47D0E"]

    for cat, val, cor in zip(cats, vals, cores_f):
        fig_final.add_trace(go.Bar(
            x=[cat], y=[val],
            marker=dict(color=cor, opacity=0.85, line=dict(width=0)),
            text=[f"⚡ {val:.0f}"],
            textposition='outside',
            textfont=dict(size=11, color=cor, family="DM Mono, Noto Sans"),
            showlegend=False,
            hovertemplate=f'<b>{cat}</b><br>{val:.0f}<extra></extra>'
        ))

    fig_final.update_layout(
        title=dict(text=T["final_title"], font=dict(size=14, family='Playfair Display, Noto Serif, Noto Sans SC, Noto Naskh Arabic')),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=360, font=dict(family='DM Sans, Noto Sans, Noto Sans SC, Noto Naskh Arabic'),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#f0e8d8'),
        margin=dict(t=50, b=20)
    )
    plot(fig_final)

# ── TAB 4: EM CAMPO ───────────────────────────────────────────
with tab4:
    st.markdown(f'<div class="section-label">{T["field_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["field_title"]}</div>', unsafe_allow_html=True)


    photos = T['photos']
    foto_destaque = next((f for f in photos if f.get("destaque")), None)
    fotos_normais = [f for f in photos if not f.get("destaque")]

    # Grade 3 colunas — fotos normais
    for row_start in range(0, len(fotos_normais), 3):
        row_photos = fotos_normais[row_start:row_start + 3]
        cols = st.columns(len(row_photos))
        for col, foto in zip(cols, row_photos):
            with col:
                exists = os.path.exists(foto['path'])
                if exists:
                    show_image(foto['path'])
                else:
                    st.markdown(f"""
                    <div class="photo-placeholder">
                      <div class="photo-emoji">{foto['emoji']}</div>
                      <div class="photo-title">{foto['titulo']}</div>
                      <div class="photo-desc">{foto['desc']}</div>
                      <div class="photo-path">{foto['path']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown(f'<div class="photo-legenda">{foto["legenda"]}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # Foto destaque — largura total
    if foto_destaque:
        st.markdown("---")
        st.markdown('<div class="section-label" style="color:#C47D0E">' + T["dest_label"] + '</div>', unsafe_allow_html=True)
        exists_dest = os.path.exists(foto_destaque['path'])
        if exists_dest:
            st.markdown('<div class="photo-destaque">', unsafe_allow_html=True)
            show_image(foto_destaque['path'])
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="photo-placeholder" style="min-height:300px">
              <div class="photo-emoji" style="font-size:3rem">{foto_destaque['emoji']}</div>
              <div class="photo-title" style="font-size:1.1rem">{foto_destaque['titulo']}</div>
              <div class="photo-desc" style="max-width:600px">{foto_destaque['desc']}</div>
              <div class="photo-path">{foto_destaque['path']}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(f'<div class="photo-legenda" style="font-size:0.82rem;padding:0.7rem 1.2rem">{foto_destaque["legenda"]}</div>', unsafe_allow_html=True)

    # Timeline
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div class="section-label">{T["timeline_field_label"]}</div>', unsafe_allow_html=True)
    for data, titulo, desc in T['timeline_field_items']:
        st.markdown(f"""
        <div class="timeline-item">
          <div class="timeline-year">{data}</div>
          <div class="timeline-content">
            <div class="timeline-title">{titulo}</div>
            <div class="timeline-desc">{desc}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ── TAB 5: FONTES ─────────────────────────────────────────────
with tab5:
    st.markdown(f'<div class="section-label">{T["sources_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["sources_title"]}</div>', unsafe_allow_html=True)

    SIGLAS = [("AURORAVISION ABB", "#F5A623"), ("ABB SOLAR", "#C47D0E"), ("TJPR", "#2D7A3A"),
              ("SEEG/MCTI", "#2C8FD9"), ("NEWS UB", "#0D1A2E"), ("ANEEL", "#F5A623"), ("ABNT NBR", "#C47D0E")]
    fontes = [(sg, nome, desc, cor) for (sg, cor), (nome, desc) in zip(SIGLAS, T["sources_items"])]

    for sigla, nome, desc, cor in fontes:
        st.markdown(f"""
        <div class="info-card" style="border-left-color:{cor}">
          <div style="display:flex;align-items:flex-start;gap:1rem">
            <div style="background:{cor};color:{'#0D1A2E' if cor == '#F5A623' else 'white'};
                 font-family:'DM Mono','Noto Sans','Noto Sans SC','Noto Naskh Arabic',monospace;font-size:0.6rem;padding:4px 7px;border-radius:4px;
                 white-space:nowrap;flex-shrink:0;margin-top:2px;letter-spacing:0.5px;font-weight:bold;
                 text-align:center;min-width:80px">{sigla}</div>
            <div>
              <div style="font-weight:500;font-size:0.9rem;color:#0D1A2E">{nome}</div>
              <div style="font-size:0.82rem;color:#8A7B6B;margin-top:0.2rem">{desc}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"<br><div class='section-label'>{T['tech_label']}</div>", unsafe_allow_html=True)
    techs = ["Python 3.11", "Streamlit", "Plotly", "Folium", "Pandas", "NumPy", "AuroraVision ABB"]
    badges_html = "".join([f'<span class="source-badge">{t}</span>' for t in techs])
    st.markdown(f'<div class="source-badges">{badges_html}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="footer-wrap" style="margin-top:2rem">
      <div class="footer-title">{T['footer_title']}</div>
      <p style="margin:0.5rem 0;font-size:0.9rem">{T['footer_desc']}</p>
      <p style="margin:1rem 0 0.5rem;font-size:0.85rem;opacity:0.7">
        {T['footer_links']} &nbsp;|&nbsp;
        🌐 <a href="https://amaurialmeida.github.io/environmental-portfolio/" style="color:var(--solar)">{T['portfolio_label']}</a> &nbsp;|&nbsp;
        🐙 <a href="https://github.com/amaurialmeida" style="color:var(--solar)">GitHub</a>
      </p>
      <p style="font-size:0.75rem;opacity:0.5;margin:0">{T['footer_copy']}</p>
    </div>
    """, unsafe_allow_html=True)
