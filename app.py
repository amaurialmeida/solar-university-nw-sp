import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- Configuração da Página (deve ser o primeiro comando Streamlit) ---
st.set_page_config(
    page_title="Usina Solar Fotovoltaica - Noroeste Paulista",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Função para os Botões de Idioma ---
def idioma_buttons():
    """
    Cria os botões de seleção de idioma na barra lateral.
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🌐 Selecionar Idioma / Select Language")
    
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        if st.button("🇧🇷 PT-BR", use_container_width=True):
            st.session_state.idioma = "pt"
            st.rerun()
    with col2:
        if st.button("🇺🇸 EN", use_container_width=True):
            st.session_state.idioma = "en"
            st.rerun()
    with col3:
        if st.button("🇪🇸 ES", use_container_width=True):
            st.session_state.idioma = "es"
            st.rerun()
    
    st.sidebar.markdown("---")
    return st.session_state.idioma

# --- Inicialização do Estado da Sessão para Idioma ---
if "idioma" not in st.session_state:
    st.session_state.idioma = "pt"  # Idioma padrão: Português

# --- Dicionários de Tradução ---
textos = {
    "pt": {
        "titulo": "☀️ Potencial de Geração Solar Fotovoltaica",
        "subtitulo": "Estudo de Caso: Uma Universidade na Região Noroeste do Estado de São Paulo (Fernandópolis)",
        "sobre": "Sobre o Projeto",
        "sobre_texto": "Este projeto acompanhou a implantação de uma usina solar fotovoltaica no campus de uma universidade na região noroeste paulista. A usina foi projetada para suprir uma parcela significativa da demanda energética do campus, promovendo sustentabilidade e redução de custos operacionais.",
        "localizacao": "📍 Localização Estratégica",
        "localizacao_texto": "O município de Fernandópolis, na região noroeste do estado de São Paulo, apresenta excelente potencial para geração de energia solar, com alta incidência de radiação durante todo o ano.",
        "metricas": "Métricas do Projeto",
        "potencia_instalada": "Potência Instalada",
        "potencia_valor": "~2.5 MWp",
        "area": "Área Ocupada",
        "area_valor": "≈ 35.000 m²",
        "geracao_anual": "Geração Anual Estimada",
        "geracao_anual_valor": "≈ 4.200 MWh/ano",
        "casa_equivalentes": "Casas Equivalentes",
        "casa_valor": "~1.750",
        "co2": "CO₂ Evitado (por ano)",
        "co2_valor": "≈ 420 toneladas",
        "arvores_equivalentes": "Equivalente em Plantio de Árvores",
        "arvores_valor": "~7.000 árvores",
        "dados_historicos": "📈 Análise de Geração Histórica (Simulação)",
        "grafico_eixo_x": "Mês",
        "grafico_eixo_y": "Geração de Energia (MWh)",
        "grafico_titulo": "Geração Mensal Média (Ano Base)",
        "mapa_titulo": "🗺️ Localização do Projeto",
        "mapa_desc": "Mapa indicativo da região onde a usina solar foi instalada.",
        "conclusao": "Conclusão e Impacto",
        "conclusao_texto": "A usina solar demonstra a viabilidade técnica e econômica da geração distribuída no noroeste paulista. A iniciativa reforça o compromisso da universidade com a sustentabilidade e a inovação, servindo como modelo para outras instituições na região. O projeto contribui significativamente para a redução da pegada de carbono do campus e para a geração de conhecimento aplicado na área de energias renováveis.",
        "fonte": "Fonte: Dados do projeto de pesquisa (com base em simulações e fontes institucionais)."
    },
    "en": {
        "titulo": "☀️ Photovoltaic Solar Generation Potential",
        "subtitulo": "Case Study: A University in the Northwest Region of São Paulo State (Fernandópolis)",
        "sobre": "About the Project",
        "sobre_texto": "This project monitored the implementation of a photovoltaic solar plant on a university campus in the northwestern region of São Paulo state. The plant was designed to supply a significant portion of the campus's energy demand, promoting sustainability and reducing operational costs.",
        "localizacao": "📍 Strategic Location",
        "localizacao_texto": "The city of Fernandópolis, in the northwest region of São Paulo state, has excellent potential for solar energy generation, with high solar radiation levels throughout the year.",
        "metricas": "Project Metrics",
        "potencia_instalada": "Installed Power",
        "potencia_valor": "~2.5 MWp",
        "area": "Area Occupied",
        "area_valor": "≈ 35,000 m²",
        "geracao_anual": "Estimated Annual Generation",
        "geracao_anual_valor": "≈ 4,200 MWh/year",
        "casa_equivalentes": "Equivalent Homes",
        "casa_valor": "~1,750",
        "co2": "CO₂ Avoided (per year)",
        "co2_valor": "≈ 420 tons",
        "arvores_equivalentes": "Equivalent in Tree Planting",
        "arvores_valor": "~7,000 trees",
        "dados_historicos": "📈 Historical Generation Analysis (Simulation)",
        "grafico_eixo_x": "Month",
        "grafico_eixo_y": "Energy Generation (MWh)",
        "grafico_titulo": "Average Monthly Generation (Base Year)",
        "mapa_titulo": "🗺️ Project Location",
        "mapa_desc": "Indicative map of the region where the solar plant was installed.",
        "conclusao": "Conclusion and Impact",
        "conclusao_texto": "The solar plant demonstrates the technical and economic viability of distributed generation in the northwest of São Paulo. The initiative reinforces the university's commitment to sustainability and innovation, serving as a model for other institutions in the region. The project significantly contributes to reducing the campus's carbon footprint and generating applied knowledge in the field of renewable energy.",
        "fonte": "Source: Research project data (based on simulations and institutional sources)."
    },
    "es": {
        "titulo": "☀️ Potencial de Generación Solar Fotovoltaica",
        "subtitulo": "Caso de Estudio: Una Universidad en la Región Noroeste del Estado de São Paulo (Fernandópolis)",
        "sobre": "Sobre el Proyecto",
        "sobre_texto": "Este proyecto acompañó la implementación de una planta solar fotovoltaica en el campus de una universidad en la región noroeste del estado de São Paulo. La planta fue diseñada para suministrar una parte significativa de la demanda energética del campus, promoviendo la sostenibilidad y reduciendo los costos operativos.",
        "localizacao": "📍 Ubicación Estratégica",
        "localizacao_texto": "La ciudad de Fernandópolis, en la región noroeste del estado de São Paulo, presenta un excelente potencial para la generación de energía solar, con alta incidencia de radiación durante todo el año.",
        "metricas": "Métricas del Proyecto",
        "potencia_instalada": "Potencia Instalada",
        "potencia_valor": "~2.5 MWp",
        "area": "Área Ocupada",
        "area_valor": "≈ 35.000 m²",
        "geracao_anual": "Generación Anual Estimada",
        "geracao_anual_valor": "≈ 4.200 MWh/año",
        "casa_equivalentes": "Hogares Equivalentes",
        "casa_valor": "~1.750",
        "co2": "CO₂ Evitado (por año)",
        "co2_valor": "≈ 420 toneladas",
        "arvores_equivalentes": "Equivalente en Plantación de Árboles",
        "arvores_valor": "~7.000 árboles",
        "dados_historicos": "📈 Análisis de Generación Histórica (Simulación)",
        "grafico_eixo_x": "Mes",
        "grafico_eixo_y": "Generación de Energía (MWh)",
        "grafico_titulo": "Generación Mensual Promedio (Año Base)",
        "mapa_titulo": "🗺️ Ubicación del Proyecto",
        "mapa_desc": "Mapa indicativo de la región donde se instaló la planta solar.",
        "conclusao": "Conclusión e Impacto",
        "conclusao_texto": "La planta solar demuestra la viabilidad técnica y económica de la generación distribuida en el noroeste paulista. La iniciativa refuerza el compromiso de la universidad con la sostenibilidad y la innovación, sirviendo como modelo para otras instituciones en la región. El proyecto contribuye significativamente a la reducción de la huella de carbono del campus y a la generación de conocimiento aplicado en el campo de las energías renovables.",
        "fonte": "Fuente: Datos del proyecto de investigación (basados en simulaciones y fuentes institucionales)."
    }
}

# --- Aplicação Principal ---
def main():
    # Seleciona o texto baseado no idioma salvo na sessão
    t = textos[st.session_state.idioma]

    # Sidebar com os botões e informações extras
    with st.sidebar:
        idioma_atual = idioma_buttons()
        st.markdown("### ℹ️ Informações do Projeto")
        st.caption(f"{t['sobre']}: {t['sobre_texto'][:150]}...")
        st.caption("📅 Acompanhamento: 2023-2025")
        st.caption("🏫 Instituição de Ensino Superior - Noroeste Paulista")

    # --- Corpo Principal do Dashboard ---
    st.title(t["titulo"])
    st.markdown(f"#### {t['subtitulo']}")
    st.markdown("---")

    # Layout em Colunas para as seções descritivas
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t["sobre"])
        st.write(t["sobre_texto"])
    with col2:
        st.subheader(t["localizacao"])
        st.write(t["localizacao_texto"])
        # Link para mais informações (exemplo)
        st.caption("[🔗 Mais sobre o potencial solar na região (fonte externa)]https://news.ub.edu.br/usina-solar-da-universidade-brasil-gera-energia-limpa-equivalente-ao-plantio-de-mais-de-sete-mil-arvores/")

    st.markdown("---")

    # --- Métricas Principais (Cards) ---
    st.subheader(t["metricas"])
    col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
    
    with col_metric1:
        st.metric(label=t["potencia_instalada"], value=t["potencia_valor"])
        st.caption("💡 Pico de potência do sistema")
    with col_metric2:
        st.metric(label=t["area"], value=t["area_valor"])
        st.caption("📐 Espaço ocupado pelos painéis")
    with col_metric3:
        st.metric(label=t["geracao_anual"], value=t["geracao_anual_valor"])
        st.caption("⚡ Energia limpa injetada na rede")
    with col_metric4:
        st.metric(label=t["casa_equivalentes"], value=t["casa_valor"])
        st.caption("🏠 Média de consumo residencial mensal")

    col_metric5, col_metric6, col_metric7, col_metric8 = st.columns(4)
    with col_metric5:
        st.metric(label=t["co2"], value=t["co2_valor"])
        st.caption("🌳 Contribuição para o meio ambiente")
    with col_metric6:
        st.metric(label=t["arvores_equivalentes"], value=t["arvores_valor"])
        st.caption("🌱 Compensação ambiental anual")
    
    st.markdown("---")

    # --- Gráfico de Geração Mensal (Simulação com dados realistas) ---
    st.subheader(t["dados_historicos"])
    
    # Dados simulados baseados no perfil de geração solar do noroeste paulista
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    geracao_mwh = [380, 360, 340, 310, 280, 260, 270, 300, 340, 370, 390, 400]
    
    df_geracao = pd.DataFrame({"Mes": meses, "Geracao_MWh": geracao_mwh})
    
    fig = px.bar(df_geracao, x="Mes", y="Geracao_MWh", 
                 title=t["grafico_titulo"],
                 labels={"Mes": t["grafico_eixo_x"], "Geracao_MWh": t["grafico_eixo_y"]},
                 color="Geracao_MWh", 
                 color_continuous_scale="Plasma",
                 text="Geracao_MWh")
    
    fig.update_traces(texttemplate='%{text:.0f} MWh', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # --- Mapa de Localização (Região Noroeste Paulista) ---
    st.subheader(t["mapa_titulo"])
    st.markdown(t["mapa_desc"])
    
    # Coordenadas aproximadas de Fernandópolis, SP (noroeste)
    df_mapa = pd.DataFrame({
        'lat': [-19.9967, -20.2851, -20.4435],
        'lon': [-50.2477, -50.2477, -49.7817],
        'nome': ['Universidade (Sede do Projeto)', 'Fernandópolis - SP', 'Região Noroeste'],
        'tamanho': [15, 10, 5]
    })
    
    fig_mapa = px.scatter_mapbox(df_mapa, lat="lat", lon="lon", 
                                 hover_name="nome", 
                                 size="tamanho",
                                 zoom=8, 
                                 height=500,
                                 color_discrete_sequence=["orange"],
                                 mapbox_style="open-street-map",
                                 title="📍 Mapa Base: Noroeste do Estado de São Paulo")
    
    fig_mapa.update_layout(mapbox_style="open-street-map")
    fig_mapa.update_traces(marker=dict(sizemin=5))
    st.plotly_chart(fig_mapa, use_container_width=True)
    
    st.markdown("---")
    
    # --- Conclusão ---
    st.subheader(t["conclusao"])
    st.write(t["conclusao_texto"])
    st.caption(t["fonte"])

    # Rodapé
    st.markdown("---")
    st.caption("Desenvolvido como parte de um projeto de pesquisa em sustentabilidade energética. | Dados atualizados em Abril de 2026.")

if __name__ == "__main__":
    main()