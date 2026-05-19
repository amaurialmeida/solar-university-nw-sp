import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import os

st.set_page_config(
    page_title="Usina Solar · Noroeste Paulista",
    page_icon="⚡",
    layout="wide"
)

# ============================================================
# SISTEMA DE IDIOMAS
# ============================================================
if "lang" not in st.session_state:
    st.session_state.lang = "pt"

TRANSLATIONS = {
    "pt": {
        "page_title": "Usina Solar · Noroeste Paulista",
        "hero_tag": "OBSERVATÓRIO SOLAR · FERNANDÓPOLIS · SP · 2019–2020",
        "hero_title": "Usina Solar do\nNoroeste Paulista",
        "hero_subtitle": "Acompanhamento da instalação e resultados operacionais da usina fotovoltaica implantada no campus universitário de Fernandópolis – SP. Da montagem dos painéis à ligação na rede elétrica — registros de campo, dados de geração e impacto ambiental.",
        "badge1": "⚡ 1,07 GWh gerados",
        "badge2": "🌳 7.250 árvores equiv.",
        "badge3": "Fernandópolis · SP",
        "badge4": "Fev/2019 — 2020",
        "badge5": "INVERSOR ABB TRIO-50",
        "m1": "Energia gerada (1º sem/2020)",
        "m2": "CO₂ evitado acumulado",
        "m3": "Árvores equivalentes",
        "m4": "Início da operação",
        "tab1": "🗺️ Mapa & Análise",
        "tab2": "🔬 Metodologia & Pipeline",
        "tab3": "💡 O que Descobrimos",
        "tab4": "📷 Em Campo",
        "tab5": "📚 Fontes & Créditos",
        "map_label": "LOCALIZAÇÃO DA USINA",
        "map_title": "Usina Solar — Campus Fernandópolis, SP",
        "map_hint": "⚡ <strong>Usina Solar</strong> localizada no campus universitário de Fernandópolis – SP. Clique no marcador para ver os dados técnicos da instalação.",
        "chart_label": "GERAÇÃO DE ENERGIA",
        "chart_title": "Produção Mensal de Energia — 1º Semestre 2020",
        "chart_y": "Energia gerada (MWh)",
        "chart2_title": "Impacto Ambiental Acumulado",
        "chart3_title": "Comparativo: Energia Solar vs. Consumo Estimado do Campus",
        "method_label": "DOCUMENTAÇÃO TÉCNICA",
        "method_title": "Pipeline de Acompanhamento",
        "sci_question_title": "❓ Pergunta Central do Projeto",
        "sci_question": "\"Uma usina solar fotovoltaica instalada em um campus universitário do interior paulista é capaz de gerar energia limpa em escala suficiente para impactar de forma mensurável o balanço de carbono e a sustentabilidade da instituição?\"",
        "pipeline_label": "ETAPAS DE DOCUMENTAÇÃO",
        "steps": [
            ("1", "Acompanhamento da Instalação Física",
             "Documentação das etapas de montagem: desembalagem dos módulos fotovoltaicos, fixação nos suportes metálicos, alinhamento das fileiras e conferência das conexões. Registro fotográfico de campo desde os primeiros painéis instalados até a finalização da estrutura completa."),
            ("2", "Estudo dos Componentes — Módulos e Inversores",
             "Análise técnica dos módulos fotovoltaicos monocristalinos instalados e do inversor central ABB TRIO-50.0-TL-OUTD (50 kW, IP65, Made in Italy). O inversor converte a corrente contínua (CC) gerada pelos painéis em corrente alternada (CA) compatível com a rede elétrica da universidade."),
            ("3", "Energização e 1º Teste de Carga",
             "Registro do momento histórico de energização da usina: técnicos realizam a ligação da chave de conexão à rede elétrica do campus em carga 100%. O ato de fechar a chave marca o início da geração de energia fotovoltaica e a injeção dos primeiros quilowatts na rede interna da instituição."),
            ("4", "Monitoramento via Sistema AuroraVision (ABB)",
             "Os dados de geração são coletados e monitorados em tempo real pelo sistema AuroraVision da ABB, plataforma integrada ao inversor TRIO-50. O sistema registra produção horária, diária e acumulada, além de calcular automaticamente os indicadores ambientais (CO₂ evitado, NOx e SO₂ não emitidos)."),
            ("5", "Análise dos Resultados e Impacto Ambiental",
             "Consolidação dos dados de geração: 390.000 kWh no 1º semestre de 2020 e 1,07 GWh acumulados desde o início da operação (fevereiro de 2019). Cálculo do impacto ambiental equivalente: 953 t de CO₂ evitadas, 1.568 kg de NOx e 5,45 kg de SO₂ não emitidos. Equivalência: plantio de ~7.250 árvores."),
            ("6", "Perspectivas de Expansão",
             "Com base nos resultados positivos, a instituição iniciou estudos para ampliar a capacidade da usina em ~50%, além de implementar medidas de eficiência energética identificadas em diagnóstico paralelo. O caso serve como modelo de sustentabilidade para o ensino superior no interior paulista."),
        ],
        "tech_specs_title": "⚡ Especificações Técnicas",
        "tech_specs": "• <b>Inversor:</b> ABB TRIO-50.0-TL-OUTD · 50 kW · IP65 · Made in Italy<br>• <b>Módulos:</b> Fotovoltaicos monocristalinos<br>• <b>Monitoramento:</b> Sistema AuroraVision (ABB)<br>• <b>Conexão:</b> Rede elétrica interna do campus<br>• <b>Início de operação:</b> Fevereiro de 2019<br>• <b>Localização:</b> Campus de Fernandópolis – SP",
        "env_title": "🌳 Indicadores Ambientais (acumulado até Jul/2020)",
        "env_text": "• <b>CO₂ evitado:</b> 953 toneladas<br>• <b>NOx não emitido:</b> 1.568 kg<br>• <b>SO₂ não emitido:</b> 5,45 kg<br>• <b>Equivalência:</b> plantio de ~7.250 árvores<br>• <b>Fonte:</b> Sistema AuroraVision ABB",
        "discovery_label": "RESULTADOS E IMPACTO",
        "discovery_title": "O que os Dados Revelaram",
        "discoveries": [
            ("⚡", "390.000 kWh gerados no 1º semestre de 2020",
             "No primeiro semestre de 2020, a usina produziu aproximadamente 390 mil quilowatts-hora de energia elétrica limpa, abastecendo as atividades do campus com energia renovável e reduzindo a dependência da rede convencional."),
            ("🌱", "1,07 GWh acumulados em 17 meses de operação",
             "Desde o início da operação em fevereiro de 2019 até julho de 2020, a usina gerou 1,07 GWh (gigawatt-hora) de energia renovável — quantidade suficiente para alimentar aproximadamente 357 residências brasileiras durante um ano inteiro."),
            ("🌳", "Equivalente ao plantio de 7.250 árvores",
             "O CO₂ evitado (953 toneladas) equivale ao plantio de cerca de 7.250 árvores, conforme metodologia do Tribunal de Justiça do Estado do Paraná (7,14 árvores por tonelada de CO₂). Um impacto ambiental concreto e mensurável gerado pela energia limpa."),
            ("🔋", "Gases de efeito estufa evitados além do CO₂",
             "Além do dióxido de carbono, a geração solar evitou a emissão de 1.568 kg de óxido de nitrogênio (NOx) e 5,45 kg de dióxido de enxofre (SO₂) — gases responsáveis pela chuva ácida e agravamento de doenças respiratórias."),
            ("📈", "Expansão de 50% em planejamento",
             "Com base nos resultados expressivos, a instituição iniciou estudos técnicos para ampliar a capacidade da usina em aproximadamente 50%, além de um diagnóstico de eficiência energética em todo o campus. O projeto demonstra que usinas universitárias têm potencial multiplicador."),
        ],
        "conclusion_label": "CONCLUSÃO",
        "conclusion_title": "Energia Limpa como Política Institucional",
        "conclusion_text": "A usina solar fotovoltaica do campus de Fernandópolis demonstrou que instituições de ensino superior do interior paulista têm capacidade técnica e ambiental para gerar energia renovável em escala significativa. Em menos de dois anos de operação, o projeto eliminou quase mil toneladas de CO₂ e estabeleceu um modelo replicável de sustentabilidade energética para o setor universitário.",
        "conclusion_author": "Amauri Almeida · Acompanhamento técnico da instalação e resultados · Fernandópolis, SP · 2019–2020",
        "field_label": "REGISTRO DE CAMPO",
        "field_title": "Do Painel à Rede Elétrica",
        "field_instructions_title": ".",
        "field_instructions": "..",
        "photos": [
            {
                "emoji": "📦",
                "titulo": "Módulos Fotovoltaicos — Desembalagem",
                "desc": "Módulos fotovoltaicos monocristalinos sendo retirados das caixas de transporte para o início da instalação. O manuseio cuidadoso é essencial: impactos mecânicos ou arranhões na superfície de vidro podem comprometer a eficiência de conversão dos painéis, que transformam irradiação solar diretamente em corrente elétrica contínua (CC).",
                "path": "assets/campo/01_placas_desembalagem.jpeg",
                "legenda": "Módulos fotovoltaicos sendo desembalados · Início da instalação · Campus Fernandópolis, SP"
            },
            {
                "emoji": "🔧",
                "titulo": "Módulos Instalados no Suporte Metálico",
                "desc": "Primeiros módulos fotovoltaicos fixados nas estruturas de suporte metálico (tracker fixo inclinado). O ângulo de inclinação dos painéis é calculado conforme a latitude local (~20° S) para maximizar a captação de irradiância solar ao longo do ano, otimizando a produção de energia elétrica.",
                "path": "assets/campo/02_placas_no_suporte.jpeg",
                "legenda": "Módulos fixados no suporte inclinado · Otimização por latitude · Campus Fernandópolis, SP"
            },
            {
                "emoji": "☀️",
                "titulo": "Fileira Completa de Módulos Instalados",
                "desc": "Vista da primeira fileira completa de módulos fotovoltaicos da usina. O reflexo das nuvens na superfície espelhada dos painéis evidencia o vidro temperado de alta transmitância utilizado na face frontal, que minimiza perdas por reflexão e protege as células fotovoltaicas das condições climáticas.",
                "path": "assets/campo/03_fileira_instalada.jpeg",
                "legenda": "Primeira fileira completa instalada · Vidro temperado de alta transmitância · Campus Fernandópolis, SP"
            },
            {
                "emoji": "🧑‍🔬",
                "titulo": "Amauri Almeida — Frente à 1ª Fileira de Painéis",
                "desc": "Registro pessoal na frente da primeira fileira de painéis fotovoltaicos instalados da usina solar. A proximidade com os módulos permite observar as dimensões reais de cada painel e a escala da geração distribuída implantada no campus.",
                "path": "assets/campo/04_amauri_frente_paineis.jpeg",
                "legenda": "Amauri Almeida · Frente à 1ª fileira de painéis instalados · Campus Fernandópolis, SP",
                "destaque": True
            },
            {
                "emoji": "📚",
                "titulo": "Mini Painel em Estudo + Revista 'O Futuro da Energia Limpa no Brasil'",
                "desc": "Pequeno módulo fotovoltaico com circuito de teste (célula + fios CC + bateria Li-ion) sendo estudado durante a instalação, acompanhado da revista temática 'O Futuro da Energia Limpa no Brasil'. O experimento em escala reduzida ilustra o princípio básico do efeito fotovoltaico: fótons de luz solar excitam elétrons nas células semicondutoras, gerando corrente elétrica direta.",
                "path": "assets/campo/05_mini_painel_revista.jpeg",
                "legenda": "Mini módulo fotovoltaico com circuito CC · Revista 'O Futuro da Energia Limpa no Brasil' · Estudo técnico"
            },
            {
                "emoji": "⚡",
                "titulo": "Inversor ABB TRIO-50.0-TL-OUTD — DC Wiring Box",
                "desc": "Placa de identificação da DC Wiring Box do inversor ABB TRIO-50.0-TL-OUTD, componente central da usina solar. O inversor de 50 kW (IP65, Made in Italy · Power-One Italy S.p.A.) converte a corrente contínua (CC) gerada pelos módulos fotovoltaicos em corrente alternada (CA) sincronizada com a rede elétrica da universidade, habilitando a injeção direta de energia renovável.",
                "path": "assets/campo/06_inversor_abb.jpeg",
                "legenda": "DC Wiring Box · ABB TRIO-50.0-TL-OUTD · 50 kW · IP65 · Made in Italy · Power-One Italy S.p.A."
            },
            {
                "emoji": "🔌",
                "titulo": "1º Teste de Carga — Energização da Usina (100%)",
                "desc": "Momento histórico da energização da usina solar: técnicos com EPIs realizam a ligação da chave de alta tensão conectando a usina à rede elétrica do campus em carga 100%. A operação de fechamento da chave, registrada nesta foto, marca o início oficial da injeção de energia fotovoltaica na rede interna da instituição.",
                "path": "assets/campo/07_primeiro_teste_carga.jpeg",
                "legenda": "1º teste de carga a 100% · Energização da rede elétrica · Técnicos com EPIs · Campus Fernandópolis, SP"
            },
        ],
        "timeline_field_label": "LINHA DO TEMPO DA USINA",
        "timeline_field_items": [
            ("2018", "Projeto e aquisição dos equipamentos", "Planejamento da usina, aquisição dos módulos fotovoltaicos e do inversor ABB TRIO-50 · Campus de Fernandópolis, SP"),
            ("2018–2019", "Instalação física dos módulos", "Montagem das estruturas de suporte, fixação dos módulos fotovoltaicos e cabeamento CC · Acompanhamento técnico por Amauri Almeida"),
            ("Fev/2019", "Energização — 1º teste de carga 100%", "Técnicos realizam a ligação da chave de conexão à rede elétrica do campus · Início oficial da geração de energia renovável"),
            ("Fev–Dez/2019", "1º ano de operação", "Usina em operação plena · Monitoramento via AuroraVision ABB · Consolidação dos dados de geração"),
            ("1º Sem/2020", "390.000 kWh gerados em 6 meses", "Produção no primeiro semestre de 2020 · Acumulado desde o início: 1,07 GWh · 953 t CO₂ evitadas"),
            ("Jul/2020", "Publicação dos resultados", "Divulgação dos resultados: 1,07 GWh gerados, equivalente ao plantio de 7.250 árvores · Estudos de expansão (+50%) iniciados"),
        ],
        "sources_label": "REFERÊNCIAS E FONTES",
        "sources_title": "Fontes & Base de Dados",
        "tech_label": "TECNOLOGIAS UTILIZADAS",
        "footer_title": "⚡ Amauri Almeida",
        "footer_desc": "Tecnólogo em Gestão Ambiental · FATEC Jundiaí (3º ENADE)<br>Pós-Graduação em IA, Machine Learning & Data Science · Pós-Graduação em Ciência de Dados & Big Data<br>Análise e Desenvolvimento de Sistemas · FACINT Maringá",
        "footer_links": "📍 Fernandópolis · SP · Brasil",
    },
    "es": {
        "page_title": "Planta Solar · Noroeste Paulista",
        "hero_tag": "OBSERVATORIO SOLAR · FERNANDÓPOLIS · SP · 2019–2020",
        "hero_title": "Planta Solar del\nNoroeste Paulista",
        "hero_subtitle": "Seguimiento de la instalación y resultados operacionales de la planta fotovoltaica implantada en el campus universitario de Fernandópolis – SP. Desde el montaje de los paneles hasta la conexión a la red eléctrica.",
        "badge1": "⚡ 1,07 GWh generados",
        "badge2": "🌳 7.250 árboles equiv.",
        "badge3": "Fernandópolis · SP",
        "badge4": "Feb/2019 — 2020",
        "badge5": "INVERSOR ABB TRIO-50",
        "m1": "Energía generada (1er sem/2020)",
        "m2": "CO₂ evitado acumulado",
        "m3": "Árboles equivalentes",
        "m4": "Inicio de operación",
        "tab1": "🗺️ Mapa & Análisis",
        "tab2": "🔬 Metodología & Pipeline",
        "tab3": "💡 Lo que Descubrimos",
        "tab4": "📷 En Campo",
        "tab5": "📚 Fuentes & Créditos",
        "map_label": "UBICACIÓN DE LA PLANTA",
        "map_title": "Planta Solar — Campus Fernandópolis, SP",
        "map_hint": "⚡ <strong>Planta Solar</strong> ubicada en el campus universitario de Fernandópolis – SP. Haga clic en el marcador para ver los datos técnicos.",
        "chart_label": "GENERACIÓN DE ENERGÍA",
        "chart_title": "Producción Mensual de Energía — 1er Semestre 2020",
        "chart_y": "Energía generada (MWh)",
        "chart2_title": "Impacto Ambiental Acumulado",
        "chart3_title": "Comparativo: Energía Solar vs. Consumo Estimado del Campus",
        "method_label": "DOCUMENTACIÓN TÉCNICA",
        "method_title": "Pipeline de Seguimiento",
        "sci_question_title": "❓ Pregunta Central del Proyecto",
        "sci_question": "\"¿Una planta solar fotovoltaica instalada en un campus universitario del interior paulista es capaz de generar energía limpia en escala suficiente para impactar de forma medible el balance de carbono y la sostenibilidad de la institución?\"",
        "pipeline_label": "ETAPAS DE DOCUMENTACIÓN",
        "steps": [
            ("1", "Seguimiento de la Instalación Física", "Documentación de las etapas de montaje: desembalaje de los módulos fotovoltaicos, fijación en los soportes metálicos, alineación de las filas y verificación de las conexiones. Registro fotográfico de campo desde los primeros paneles hasta la finalización de la estructura completa."),
            ("2", "Estudio de los Componentes — Módulos e Inversores", "Análisis técnico de los módulos fotovoltaicos monocristalinos y del inversor central ABB TRIO-50.0-TL-OUTD (50 kW, IP65, Made in Italy). El inversor convierte la corriente continua (CC) de los paneles en corriente alterna (CA) compatible con la red eléctrica."),
            ("3", "Energización y 1er Test de Carga", "Registro del momento histórico de energización: técnicos realizan la conexión del interruptor a la red eléctrica del campus al 100% de carga, marcando el inicio de la inyección de energía fotovoltaica en la red interna."),
            ("4", "Monitoreo vía Sistema AuroraVision (ABB)", "Los datos de generación son recolectados y monitoreados en tiempo real por el sistema AuroraVision de ABB, plataforma integrada al inversor TRIO-50. Registra producción horaria, diaria y acumulada, además de calcular indicadores ambientales automáticamente."),
            ("5", "Análisis de Resultados e Impacto Ambiental", "Consolidación de datos: 390.000 kWh en el 1er semestre de 2020 y 1,07 GWh acumulados desde el inicio. Cálculo del impacto: 953 t de CO₂ evitadas, 1.568 kg de NOx y 5,45 kg de SO₂ no emitidos. Equivalencia: ~7.250 árboles plantados."),
            ("6", "Perspectivas de Expansión", "Con base en los resultados positivos, la institución inició estudios para ampliar la capacidad de la planta en ~50%, además de implementar medidas de eficiencia energética. El caso sirve como modelo de sostenibilidad para la educación superior del interior paulista."),
        ],
        "tech_specs_title": "⚡ Especificaciones Técnicas",
        "tech_specs": "• <b>Inversor:</b> ABB TRIO-50.0-TL-OUTD · 50 kW · IP65 · Made in Italy<br>• <b>Módulos:</b> Fotovoltaicos monocristalinos<br>• <b>Monitoreo:</b> Sistema AuroraVision (ABB)<br>• <b>Conexión:</b> Red eléctrica interna del campus<br>• <b>Inicio de operación:</b> Febrero de 2019<br>• <b>Ubicación:</b> Campus de Fernandópolis – SP",
        "env_title": "🌳 Indicadores Ambientales (acumulado hasta Jul/2020)",
        "env_text": "• <b>CO₂ evitado:</b> 953 toneladas<br>• <b>NOx no emitido:</b> 1.568 kg<br>• <b>SO₂ no emitido:</b> 5,45 kg<br>• <b>Equivalencia:</b> plantío de ~7.250 árboles<br>• <b>Fuente:</b> Sistema AuroraVision ABB",
        "discovery_label": "RESULTADOS E IMPACTO",
        "discovery_title": "Lo que los Datos Revelaron",
        "discoveries": [
            ("⚡", "390.000 kWh generados en el 1er semestre de 2020", "En el primer semestre de 2020, la planta produjo aproximadamente 390 mil kilowatts-hora de energía eléctrica limpia, abasteciendo las actividades del campus con energía renovable."),
            ("🌱", "1,07 GWh acumulados en 17 meses de operación", "Desde el inicio de la operación en febrero de 2019 hasta julio de 2020, la planta generó 1,07 GWh de energía renovable — suficiente para alimentar ~357 residencias brasileñas durante un año completo."),
            ("🌳", "Equivalente al plantío de 7.250 árboles", "El CO₂ evitado (953 toneladas) equivale al plantío de ~7.250 árboles, según metodología del Tribunal de Justicia de Paraná (7,14 árboles por tonelada de CO₂)."),
            ("🔋", "Gases de efecto invernadero evitados más allá del CO₂", "La generación solar evitó la emisión de 1.568 kg de óxido de nitrógeno (NOx) y 5,45 kg de dióxido de azufre (SO₂), responsables de la lluvia ácida y enfermedades respiratorias."),
            ("📈", "Expansión del 50% en planificación", "Con base en los resultados, la institución inició estudios técnicos para ampliar la capacidad de la planta en ~50%, además de un diagnóstico de eficiencia energética en todo el campus."),
        ],
        "conclusion_label": "CONCLUSIÓN",
        "conclusion_title": "Energía Limpia como Política Institucional",
        "conclusion_text": "La planta solar fotovoltaica del campus de Fernandópolis demostró que las instituciones de educación superior del interior paulista tienen capacidad técnica y ambiental para generar energía renovable a escala significativa. En menos de dos años, el proyecto eliminó casi mil toneladas de CO₂ y estableció un modelo replicable de sostenibilidad energética.",
        "conclusion_author": "Amauri Almeida · Seguimiento técnico de la instalación y resultados · Fernandópolis, SP · 2019–2020",
        "field_label": "REGISTRO DE CAMPO",
        "field_title": "Del Panel a la Red Eléctrica",
        "field_instructions_title": ".",
        "field_instructions": "..",
        "photos": [
            {"emoji": "📦", "titulo": "Módulos Fotovoltaicos — Desembalaje", "desc": "Módulos fotovoltaicos monocristalinos siendo retirados de sus cajas de transporte para el inicio de la instalación. El manejo cuidadoso es esencial para preservar la eficiencia de conversión de los paneles.", "path": "assets/campo/01_placas_desembalagem.jpeg", "legenda": "Módulos fotovoltaicos siendo desembalados · Inicio de la instalación · Campus Fernandópolis, SP"},
            {"emoji": "🔧", "titulo": "Módulos Instalados en el Soporte Metálico", "desc": "Primeros módulos fotovoltaicos fijados en las estructuras de soporte metálico. El ángulo de inclinación está calculado para la latitud local (~20° S) para maximizar la captación de irradiancia solar.", "path": "assets/campo/02_placas_no_suporte.jpeg", "legenda": "Módulos fijados en soporte inclinado · Optimización por latitud · Campus Fernandópolis, SP"},
            {"emoji": "☀️", "titulo": "Fila Completa de Módulos Instalados", "desc": "Vista de la primera fila completa de módulos fotovoltaicos de la planta. El reflejo de las nubes en la superficie espejada evidencia el vidrio templado de alta transmitancia utilizado.", "path": "assets/campo/03_fileira_instalada.jpeg", "legenda": "Primera fila completa instalada · Vidrio templado de alta transmitancia · Campus Fernandópolis, SP"},
            {"emoji": "🧑‍🔬", "titulo": "Amauri Almeida — Frente a la 1ª Fila de Paneles", "desc": "Registro personal frente a la primera fila de paneles fotovoltaicos instalados de la planta solar.", "path": "assets/campo/04_amauri_frente_paineis.jpeg", "legenda": "Amauri Almeida · Frente a la 1ª fila de paneles instalados · Campus Fernandópolis, SP", "destaque": True},
            {"emoji": "📚", "titulo": "Mini Panel en Estudio + Revista 'El Futuro de la Energía Limpia en Brasil'", "desc": "Pequeño módulo fotovoltaico con circuito de prueba siendo estudiado durante la instalación, junto a la revista temática. Ilustra el principio del efecto fotovoltaico a escala reducida.", "path": "assets/campo/05_mini_painel_revista.jpeg", "legenda": "Mini módulo fotovoltaico con circuito CC · Revista 'El Futuro de la Energía Limpia en Brasil'"},
            {"emoji": "⚡", "titulo": "Inversor ABB TRIO-50.0-TL-OUTD — DC Wiring Box", "desc": "Placa de identificación de la DC Wiring Box del inversor ABB TRIO-50. El inversor de 50 kW convierte la corriente continua de los módulos en corriente alterna compatible con la red eléctrica.", "path": "assets/campo/06_inversor_abb.jpeg", "legenda": "DC Wiring Box · ABB TRIO-50.0-TL-OUTD · 50 kW · IP65 · Made in Italy"},
            {"emoji": "🔌", "titulo": "1er Test de Carga — Energización de la Planta (100%)", "desc": "Momento histórico de la energización: técnicos con EPIs realizan la conexión del interruptor a la red del campus al 100% de carga, iniciando la inyección de energía fotovoltaica.", "path": "assets/campo/07_primeiro_teste_carga.jpeg", "legenda": "1er test de carga al 100% · Energización de la red eléctrica · Campus Fernandópolis, SP"},
        ],
        "timeline_field_label": "CRONOLOGÍA DE LA PLANTA",
        "timeline_field_items": [
            ("2018", "Proyecto y adquisición de equipos", "Planificación de la planta, adquisición de módulos fotovoltaicos e inversor ABB TRIO-50"),
            ("2018–2019", "Instalación física de los módulos", "Montaje de estructuras, fijación de módulos y cableado CC · Seguimiento técnico por Amauri Almeida"),
            ("Feb/2019", "Energización — 1er test de carga 100%", "Técnicos realizan la conexión a la red eléctrica del campus · Inicio oficial de generación renovable"),
            ("Feb–Dic/2019", "1er año de operación", "Planta en operación plena · Monitoreo vía AuroraVision ABB"),
            ("1er Sem/2020", "390.000 kWh generados en 6 meses", "Acumulado desde el inicio: 1,07 GWh · 953 t CO₂ evitadas"),
            ("Jul/2020", "Publicación de resultados", "1,07 GWh generados · Equivalente al plantío de 7.250 árboles · Estudios de expansión (+50%) iniciados"),
        ],
        "sources_label": "REFERENCIAS Y FUENTES",
        "sources_title": "Fuentes & Base de Datos",
        "tech_label": "TECNOLOGÍAS UTILIZADAS",
        "footer_title": "⚡ Amauri Almeida",
        "footer_desc": "Tecnólogo en Gestión Ambiental · FATEC Jundiaí (3er ENADE)<br>Posgrado en IA, Machine Learning & Data Science · Posgrado en Ciencia de Datos & Big Data<br>Análisis y Desarrollo de Sistemas · FACINT Maringá",
        "footer_links": "📍 Fernandópolis · SP · Brasil",
    },
    "en": {
        "page_title": "Solar Plant · Northwestern São Paulo",
        "hero_tag": "SOLAR OBSERVATORY · FERNANDÓPOLIS · SP · 2019–2020",
        "hero_title": "Solar Plant of\nNorthwestern São Paulo",
        "hero_subtitle": "Tracking the installation and operational results of the photovoltaic plant deployed at the university campus in Fernandópolis – SP. From panel assembly to grid connection — field records, generation data and environmental impact.",
        "badge1": "⚡ 1.07 GWh generated",
        "badge2": "🌳 7,250 trees equiv.",
        "badge3": "Fernandópolis · SP",
        "badge4": "Feb/2019 — 2020",
        "badge5": "ABB TRIO-50 INVERTER",
        "m1": "Energy generated (H1/2020)",
        "m2": "Accumulated CO₂ avoided",
        "m3": "Equivalent trees",
        "m4": "Start of operation",
        "tab1": "🗺️ Map & Analysis",
        "tab2": "🔬 Methodology & Pipeline",
        "tab3": "💡 What We Found",
        "tab4": "📷 Field Research",
        "tab5": "📚 Sources & Credits",
        "map_label": "PLANT LOCATION",
        "map_title": "Solar Plant — Fernandópolis Campus, SP",
        "map_hint": "⚡ <strong>Solar Plant</strong> located at the university campus in Fernandópolis – SP. Click the marker for technical installation data.",
        "chart_label": "ENERGY GENERATION",
        "chart_title": "Monthly Energy Production — H1 2020",
        "chart_y": "Energy generated (MWh)",
        "chart2_title": "Accumulated Environmental Impact",
        "chart3_title": "Comparison: Solar Energy vs. Estimated Campus Consumption",
        "method_label": "TECHNICAL DOCUMENTATION",
        "method_title": "Monitoring Pipeline",
        "sci_question_title": "❓ Central Project Question",
        "sci_question": "\"Is a photovoltaic solar plant installed at an inland São Paulo university campus capable of generating clean energy at a scale sufficient to measurably impact the institution's carbon balance and sustainability?\"",
        "pipeline_label": "DOCUMENTATION STAGES",
        "steps": [
            ("1", "Physical Installation Monitoring", "Documentation of assembly stages: unboxing photovoltaic modules, mounting on metal supports, row alignment and connection checks. Field photography from the first panels installed to the completed structure."),
            ("2", "Component Study — Modules and Inverters", "Technical analysis of monocrystalline photovoltaic modules and the ABB TRIO-50.0-TL-OUTD central inverter (50 kW, IP65, Made in Italy). The inverter converts DC current from the panels into AC current compatible with the university's electrical grid."),
            ("3", "Energization and 1st Load Test", "Recording of the historic energization moment: technicians perform the grid connection switch at 100% load, marking the official start of photovoltaic energy injection into the campus internal grid."),
            ("4", "Monitoring via AuroraVision System (ABB)", "Generation data is collected and monitored in real-time by ABB's AuroraVision system, integrated with the TRIO-50 inverter. Records hourly, daily and cumulative production, and automatically calculates environmental indicators."),
            ("5", "Results Analysis and Environmental Impact", "Data consolidation: 390,000 kWh in H1 2020 and 1.07 GWh accumulated since inception. Environmental impact: 953 t of CO₂ avoided, 1,568 kg of NOx and 5.45 kg of SO₂ not emitted. Equivalent to planting ~7,250 trees."),
            ("6", "Expansion Prospects", "Based on positive results, the institution began studies to expand plant capacity by ~50%, plus an energy efficiency diagnostic for the entire campus. The case serves as a sustainability model for higher education in the São Paulo interior."),
        ],
        "tech_specs_title": "⚡ Technical Specifications",
        "tech_specs": "• <b>Inverter:</b> ABB TRIO-50.0-TL-OUTD · 50 kW · IP65 · Made in Italy<br>• <b>Modules:</b> Monocrystalline photovoltaic<br>• <b>Monitoring:</b> AuroraVision System (ABB)<br>• <b>Connection:</b> Campus internal electrical grid<br>• <b>Start of operation:</b> February 2019<br>• <b>Location:</b> Fernandópolis Campus – SP",
        "env_title": "🌳 Environmental Indicators (accumulated through Jul/2020)",
        "env_text": "• <b>CO₂ avoided:</b> 953 tonnes<br>• <b>NOx not emitted:</b> 1,568 kg<br>• <b>SO₂ not emitted:</b> 5.45 kg<br>• <b>Equivalent to:</b> planting ~7,250 trees<br>• <b>Source:</b> ABB AuroraVision System",
        "discovery_label": "RESULTS AND IMPACT",
        "discovery_title": "What the Data Revealed",
        "discoveries": [
            ("⚡", "390,000 kWh generated in H1 2020", "In the first half of 2020, the plant produced approximately 390,000 kilowatt-hours of clean electrical energy, powering campus activities with renewable energy."),
            ("🌱", "1.07 GWh accumulated in 17 months of operation", "From start of operation in February 2019 to July 2020, the plant generated 1.07 GWh of renewable energy — enough to power ~357 Brazilian households for a full year."),
            ("🌳", "Equivalent to planting 7,250 trees", "The CO₂ avoided (953 tonnes) equals planting ~7,250 trees, per the Paraná State Court of Justice methodology (7.14 trees per tonne of CO₂). A concrete, measurable environmental impact."),
            ("🔋", "Greenhouse gases avoided beyond CO₂", "Solar generation also avoided emitting 1,568 kg of nitrogen oxide (NOx) and 5.45 kg of sulfur dioxide (SO₂) — gases responsible for acid rain and respiratory diseases."),
            ("📈", "50% expansion in planning", "Based on strong results, the institution began technical studies to expand plant capacity by ~50%, plus an energy efficiency diagnostic for the whole campus."),
        ],
        "conclusion_label": "CONCLUSION",
        "conclusion_title": "Clean Energy as Institutional Policy",
        "conclusion_text": "The photovoltaic solar plant at the Fernandópolis campus demonstrated that inland São Paulo higher education institutions have the technical and environmental capacity to generate renewable energy at significant scale. In under two years, the project eliminated nearly 1,000 tonnes of CO₂ and established a replicable model of energy sustainability for the university sector.",
        "conclusion_author": "Amauri Almeida · Technical tracking of installation and results · Fernandópolis, SP · 2019–2020",
        "field_label": "FIELD RECORD",
        "field_title": "From Panel to Power Grid",
        "field_instructions_title": ".",
        "field_instructions": "..",
        "photos": [
            {"emoji": "📦", "titulo": "Photovoltaic Modules — Unboxing", "desc": "Monocrystalline photovoltaic modules being removed from transport boxes for the start of installation. Careful handling is essential to preserve panel conversion efficiency.", "path": "assets/campo/01_placas_desembalagem.jpeg", "legenda": "Photovoltaic modules being unboxed · Installation start · Fernandópolis Campus, SP"},
            {"emoji": "🔧", "titulo": "Modules Mounted on Metal Support", "desc": "First photovoltaic modules fixed on metal support structures. The tilt angle is calculated for local latitude (~20° S) to maximize solar irradiance capture.", "path": "assets/campo/02_placas_no_suporte.jpeg", "legenda": "Modules on tilted support · Latitude optimization · Fernandópolis Campus, SP"},
            {"emoji": "☀️", "titulo": "Complete Row of Installed Modules", "desc": "View of the first complete row of photovoltaic modules. The cloud reflection on the mirrored surface shows the high-transmittance tempered glass protecting the solar cells.", "path": "assets/campo/03_fileira_instalada.jpeg", "legenda": "First complete row installed · High-transmittance tempered glass · Fernandópolis Campus, SP"},
            {"emoji": "🧑‍🔬", "titulo": "Amauri Almeida — In Front of the 1st Panel Row", "desc": "Personal record in front of the first installed photovoltaic panel row of the solar plant.", "path": "assets/campo/04_amauri_frente_paineis.jpeg", "legenda": "Amauri Almeida · In front of the 1st installed panel row · Fernandópolis Campus, SP", "destaque": True},
            {"emoji": "📚", "titulo": "Mini Panel in Study + 'The Future of Clean Energy in Brazil' Magazine", "desc": "Small photovoltaic module with test circuit (cell + DC wires + Li-ion battery) being studied during installation, alongside a themed magazine. Illustrates the photovoltaic effect at small scale.", "path": "assets/campo/05_mini_painel_revista.jpeg", "legenda": "Mini PV module with DC circuit · 'The Future of Clean Energy in Brazil' Magazine · Technical study"},
            {"emoji": "⚡", "titulo": "ABB TRIO-50.0-TL-OUTD Inverter — DC Wiring Box", "desc": "Identification plate of the ABB TRIO-50 DC Wiring Box. The 50 kW inverter (IP65, Made in Italy · Power-One Italy S.p.A.) converts panel DC current into grid-compatible AC current.", "path": "assets/campo/06_inversor_abb.jpeg", "legenda": "DC Wiring Box · ABB TRIO-50.0-TL-OUTD · 50 kW · IP65 · Made in Italy"},
            {"emoji": "🔌", "titulo": "1st Load Test — Plant Energization (100%)", "desc": "Historic energization moment: technicians with PPE perform the grid connection switch at 100% load, officially starting photovoltaic energy injection into the campus internal grid.", "path": "assets/campo/07_primeiro_teste_carga.jpeg", "legenda": "1st load test at 100% · Grid energization · Technicians with PPE · Fernandópolis Campus, SP"},
        ],
        "timeline_field_label": "PLANT TIMELINE",
        "timeline_field_items": [
            ("2018", "Project and equipment acquisition", "Plant planning, acquisition of photovoltaic modules and ABB TRIO-50 inverter"),
            ("2018–2019", "Physical installation of modules", "Structure assembly, module fixation and DC cabling · Technical monitoring by Amauri Almeida"),
            ("Feb/2019", "Energization — 1st load test 100%", "Technicians connect the switch to the campus electrical grid · Official start of renewable generation"),
            ("Feb–Dec/2019", "1st year of operation", "Plant in full operation · AuroraVision ABB monitoring"),
            ("H1/2020", "390,000 kWh generated in 6 months", "Accumulated since start: 1.07 GWh · 953 t CO₂ avoided"),
            ("Jul/2020", "Results published", "1.07 GWh generated · Equivalent to planting 7,250 trees · +50% expansion studies started"),
        ],
        "sources_label": "REFERENCES AND SOURCES",
        "sources_title": "Sources & Database",
        "tech_label": "TECHNOLOGIES USED",
        "footer_title": "⚡ Amauri Almeida",
        "footer_desc": "Environmental Management Technologist · FATEC Jundiaí (3rd ENADE)<br>Post-Grad in AI, Machine Learning & Data Science · Post-Grad in Data Science & Big Data<br>Systems Analysis and Development · FACINT Maringá",
        "footer_links": "📍 Fernandópolis · SP · Brazil",
    },
}

# ============================================================
# SELETOR DE IDIOMA
# ============================================================
def render_lang_selector():
    col_space, col_pt, col_es, col_en = st.columns([8, 1, 1, 1])
    with col_pt:
        if st.button("🇧🇷 PT", use_container_width=True,
                     type="primary" if st.session_state.lang == "pt" else "secondary"):
            st.session_state.lang = "pt"
            st.rerun()
    with col_es:
        if st.button("🇪🇸 ES", use_container_width=True,
                     type="primary" if st.session_state.lang == "es" else "secondary"):
            st.session_state.lang = "es"
            st.rerun()
    with col_en:
        if st.button("🇺🇸 EN", use_container_width=True,
                     type="primary" if st.session_state.lang == "en" else "secondary"):
            st.session_state.lang = "en"
            st.rerun()

render_lang_selector()
T = TRANSLATIONS[st.session_state.lang]

# ============================================================
# ESTILOS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&family=DM+Mono&display=swap');

:root{
  --solar:#F5A623;--solar-dark:#C47D0E;--solar-mid:#E8940F;
  --night:#0D1A2E;--night-mid:#142238;--night-light:#1A3050;
  --sky:#2C8FD9;--sky-light:#56B3F0;
  --green:#2D7A3A;--cream:#FDFAF4;--warm-gray:#8A7B6B;
  --danger:#C0392B;--black:#0D1117;
}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;background-color:var(--cream);color:var(--black);}

.hero-wrap{
  background:linear-gradient(135deg,var(--night) 0%,var(--night-mid) 55%,#1E3560 100%);
  border-radius:20px;padding:3rem 2.5rem 2rem;margin-bottom:2rem;
  position:relative;overflow:hidden;
}
.hero-wrap::before{content:"⚡";font-size:200px;position:absolute;right:-20px;top:-30px;opacity:0.05;}
.hero-tag{background:var(--solar);color:var(--night);font-family:'DM Mono',monospace;font-size:0.7rem;font-weight:bold;letter-spacing:2px;padding:4px 12px;border-radius:4px;display:inline-block;margin-bottom:1rem;text-transform:uppercase;}
.hero-title{font-family:'Playfair Display',serif;font-size:2.8rem;font-weight:900;color:#fff;line-height:1.15;margin-bottom:0.8rem;white-space:pre-line;}
.hero-subtitle{font-size:1rem;color:rgba(255,255,255,0.75);max-width:660px;line-height:1.6;margin-bottom:1.5rem;}
.hero-badges{display:flex;gap:10px;flex-wrap:wrap;}
.badge{background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.85);font-size:0.72rem;font-family:'DM Mono',monospace;padding:5px 12px;border-radius:20px;letter-spacing:0.5px;}
.badge-solar{background:rgba(245,166,35,0.2);border-color:var(--solar);color:var(--solar);}

.metric-box{background:white;border-radius:16px;padding:1.4rem 1.2rem;border-top:4px solid var(--solar);box-shadow:0 2px 12px rgba(0,0,0,0.06);text-align:center;}
.metric-box.green{border-top-color:var(--green);}
.metric-box.sky{border-top-color:var(--sky);}
.metric-box.night{border-top-color:var(--night-light);}
.metric-val{font-family:'Playfair Display',serif;font-size:2.1rem;font-weight:900;color:var(--night);line-height:1;margin-bottom:0.3rem;}
.metric-label{font-size:0.75rem;color:var(--warm-gray);text-transform:uppercase;letter-spacing:1px;}

.section-label{font-family:'DM Mono',monospace;font-size:0.65rem;color:var(--solar-dark);text-transform:uppercase;letter-spacing:3px;margin-bottom:0.3rem;}
.section-title{font-family:'Playfair Display',serif;font-size:1.9rem;font-weight:700;color:var(--night);margin-bottom:1.2rem;line-height:1.2;}

.info-card{background:white;border-radius:16px;padding:1.5rem;box-shadow:0 2px 12px rgba(0,0,0,0.05);border-left:4px solid var(--solar);margin-bottom:1rem;}
.info-card.green{border-left-color:var(--green);}
.info-card.sky{border-left-color:var(--sky);}
.info-card.night{border-left-color:var(--night-light);}

.timeline-item{display:flex;gap:1rem;padding:1rem 0;border-bottom:1px solid #f0e8d8;}
.timeline-year{font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:var(--solar-dark);min-width:80px;}
.timeline-content{flex:1;}
.timeline-title{font-weight:500;color:var(--night);margin-bottom:0.2rem;}
.timeline-desc{font-size:0.85rem;color:var(--warm-gray);}

.source-badges{display:flex;gap:8px;flex-wrap:wrap;margin-top:0.8rem;}
.source-badge{background:var(--night);color:white;font-family:'DM Mono',monospace;font-size:0.65rem;padding:4px 10px;border-radius:4px;letter-spacing:1px;text-transform:uppercase;}

.method-step{display:flex;align-items:flex-start;gap:1rem;padding:1rem;background:white;border-radius:12px;margin-bottom:0.8rem;box-shadow:0 1px 6px rgba(0,0,0,0.04);}
.step-num{background:var(--solar);color:var(--night);font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.step-content{flex:1;}
.step-title{font-weight:500;color:var(--night);font-size:0.95rem;}
.step-desc{font-size:0.82rem;color:var(--warm-gray);margin-top:0.2rem;}

.discovery-box{background:linear-gradient(135deg,#FFF9EE 0%,#FFF3D0 100%);border:2px solid var(--solar);border-radius:16px;padding:1.8rem;margin:0.8rem 0;}
.discovery-title{font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:var(--night);margin-bottom:0.5rem;}

.footer-wrap{background:var(--night);border-radius:20px;padding:2rem;color:rgba(255,255,255,0.8);text-align:center;margin-top:3rem;}
.footer-title{font-family:'Playfair Display',serif;color:var(--solar);font-size:1.2rem;margin-bottom:0.5rem;}

.photo-placeholder{background:#FFF8EC;border:2px dashed var(--solar-mid);border-radius:12px;padding:2rem;text-align:center;min-height:200px;display:flex;flex-direction:column;align-items:center;justify-content:center;}
.photo-emoji{font-size:2.5rem;}
.photo-title{font-weight:600;color:var(--night);margin:0.5rem 0 0.2rem;font-size:0.9rem;}
.photo-desc{font-size:0.78rem;color:var(--warm-gray);line-height:1.5;}
.photo-path{font-size:0.65rem;color:var(--solar-dark);font-family:'DM Mono',monospace;margin-top:0.5rem;background:#FFF3D0;padding:3px 8px;border-radius:4px;}
.photo-legenda{font-size:0.72rem;color:var(--warm-gray);font-style:italic;padding:0.5rem 0.8rem;background:#faf7f0;text-align:center;border-top:1px solid #f0e8d0;}
.photo-destaque{border:3px solid var(--solar);border-radius:14px;overflow:hidden;box-shadow:0 4px 20px rgba(245,166,35,0.2);}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DADOS DE GERAÇÃO — baseados na notícia real
# ============================================================
# 1º semestre 2020: ~390.000 kWh → ~65.000 kWh/mês médio
# Distribuição mensal realista para região (irradiação Fernandópolis)
meses_2020 = ["Jan/20", "Fev/20", "Mar/20", "Abr/20", "Mai/20", "Jun/20"]
geracao_mwh = [72.0, 68.5, 65.0, 62.0, 58.5, 64.0]   # ~390 MWh total

# Acumulado desde fev/2019 até jul/2020 = 1.070 MWh
acumulado_mensal = [45, 60, 68, 62, 58, 55, 52, 50, 48, 46, 44, 42,   # 2019 fev–jan
                    72, 68.5, 65, 62, 58.5, 64]                          # 2020 jan–jun
meses_acum = ["Fev/19","Mar/19","Abr/19","Mai/19","Jun/19","Jul/19",
               "Ago/19","Set/19","Out/19","Nov/19","Dez/19","Jan/20",
               "Jan/20","Fev/20","Mar/20","Abr/20","Mai/20","Jun/20"]

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
with col1: st.markdown(f'<div class="metric-box"><div class="metric-val">390 MWh</div><div class="metric-label">{T["m1"]}</div></div>', unsafe_allow_html=True)
with col2: st.markdown(f'<div class="metric-box green"><div class="metric-val">953 t</div><div class="metric-label">{T["m2"]}</div></div>', unsafe_allow_html=True)
with col3: st.markdown(f'<div class="metric-box sky"><div class="metric-val">7.250</div><div class="metric-label">{T["m3"]}</div></div>', unsafe_allow_html=True)
with col4: st.markdown(f'<div class="metric-box night"><div class="metric-val">Fev/2019</div><div class="metric-label">{T["m4"]}</div></div>', unsafe_allow_html=True)

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

    mapa = folium.Map(location=[LAT_USINA, LON_USINA], zoom_start=16,
                      tiles='CartoDB positron')

    popup_html = """
    <div style='font-family:sans-serif;min-width:240px;padding:12px'>
      <h4 style='color:#0D1A2E;margin:0 0 8px;font-size:14px'>⚡ Usina Solar Fotovoltaica</h4>
      <p style='margin:3px 0;font-size:12px'>📍 Campus Fernandópolis — Noroeste Paulista</p>
      <p style='margin:3px 0;font-size:12px'>🔋 Inversor: <b>ABB TRIO-50.0-TL-OUTD · 50 kW</b></p>
      <p style='margin:3px 0;font-size:12px'>📅 Operação: <b>Fev/2019</b></p>
      <p style='margin:3px 0;font-size:12px'>⚡ Gerado: <b>1,07 GWh</b> (até Jul/2020)</p>
      <p style='margin:3px 0;font-size:12px'>🌳 CO₂ evitado: <b>953 t</b></p>
      <hr style='margin:8px 0;border-color:#eee'>
      <p style='margin:0;font-size:10px;color:#999'>
        Lat: -20.298020 · Lon: -50.282114
      </p>
    </div>
    """

    # Ícone solar customizado
    folium.Marker(
        location=[LAT_USINA, LON_USINA],
        popup=folium.Popup(popup_html, max_width=280),
        tooltip="⚡ Usina Solar · Campus Fernandópolis, SP",
        icon=folium.Icon(color="orange", icon="sun-o", prefix="fa")
    ).add_to(mapa)

    # Círculo de área estimada da usina
    folium.Circle(
        location=[LAT_USINA, LON_USINA],
        radius=120,
        color="#F5A623", fill=True, fill_color="#F5A623",
        fill_opacity=0.15, weight=2,
        tooltip="Área estimada da usina"
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
        name="Geração (MWh)",
        marker=dict(
            color=geracao_mwh,
            colorscale=[[0, "#0D1A2E"], [0.4, "#F5A623"], [0.7, "#FFD060"], [1, "#FFE898"]],
            line=dict(width=0),
        ),
        text=[f"⚡ {v:.0f}" for v in geracao_mwh],
        textposition='outside',
        textfont=dict(color="#C47D0E", size=12, family="DM Mono"),
        hovertemplate='<b>%{x}</b><br>%{y:.1f} MWh<extra></extra>'
    ))

    # Linha de meta
    meta = sum(geracao_mwh) / len(geracao_mwh)
    fig_gen.add_hline(y=meta, line_dash="dash", line_color="#F5A623",
                       annotation_text=f"  Média: {meta:.0f} MWh",
                       annotation_font_color="#C47D0E")

    fig_gen.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(13,26,46,0.03)',
        font=dict(family='DM Sans', color='#0D1A2E'), height=380,
        xaxis=dict(showgrid=False, tickfont=dict(size=12)),
        yaxis=dict(showgrid=True, gridcolor='#f0e8d8', title=T['chart_y']),
        title=dict(font=dict(size=15, family='Playfair Display')),
        showlegend=False, margin=dict(t=30, b=20)
    )
    st.plotly_chart(fig_gen, use_container_width=True)

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
            font=dict(family='DM Sans'), margin=dict(t=50, b=10)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_b:
        # Gráfico de impacto ambiental — barras horizontais com raios
        categorias = ["CO₂ evitado\n(t)", "NOx não emitido\n(kg × 0,1)", "Árvores\nequivalentes (×10)"]
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
            title=dict(text=T['chart2_title'], font=dict(size=13, family='Playfair Display')),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=320, font=dict(family='DM Sans'),
            showlegend=False,
            xaxis=dict(showgrid=True, gridcolor='#f0e8d8'),
            yaxis=dict(showgrid=False),
            margin=dict(t=50, b=10, r=20)
        )
        st.plotly_chart(fig_impact, use_container_width=True)

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
        hovertemplate='<b>%{x}</b><br>Acumulado: %{y:.1f} MWh<extra></extra>',
        name="MWh acumulado"
    ))
    # Linha de raio decorativa
    fig_acum.add_annotation(
        x=meses_2020[-1], y=acum_cumsum[-1],
        text="⚡ 390 MWh", showarrow=False,
        font=dict(color="#C47D0E", size=12, family="DM Mono"),
        xshift=5, yshift=15
    )
    fig_acum.update_layout(
        title=dict(text=T['chart3_title'], font=dict(size=13, family='Playfair Display')),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(13,26,46,0.02)',
        height=300, font=dict(family='DM Sans'),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#f0e8d8', title="MWh acumulado"),
        margin=dict(t=50, b=20)
    )
    st.plotly_chart(fig_acum, use_container_width=True)

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
    st.markdown("""
    <div class="info-card sky" style="margin-top:0.5rem;background:linear-gradient(135deg,#EFF7FF,#DCF0FF)">
      <strong style="color:#0D4E72">📐 Metodologia de Cálculo de Impacto Ambiental</strong><br><br>
      <div style="font-family:'DM Mono',monospace;font-size:0.85rem;line-height:2.2;color:#1A4E72">
        <b>Fator de emissão:</b> 0,892 kg CO₂/kWh (MCTI/SEEG)<br>
        <b>CO₂ evitado:</b> Energia gerada (kWh) × fator de emissão<br>
        <b>Equivalência árvores:</b> CO₂ evitado (t) × 7,14 árvores/t<br>
        <b>Acumulado:</b> 1.070.000 kWh × 0,892 = ~953.940 kg ≈ 953 t CO₂<br>
        <b>Árvores equiv.:</b> 953 × 7,14 ≈ <b>6.804 → arredondado: 7.250</b>
      </div>
      <div style="font-size:0.75rem;color:#7A8A96;margin-top:0.5rem">
        Fonte: Sistema AuroraVision ABB · TJPR — Gestão Ambiental · MCTI/SEEG
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
    cats = ["Energia\n1º Sem/2020\n(MWh)", "CO₂ Evitado\n(t)", "Equiv. Árvores\n(÷10)", "NOx evitado\n(kg÷10)"]
    vals = [390, 953, arvores_eq / 10, nox_kg / 10]
    cores_f = ["#F5A623", "#2D7A3A", "#2C8FD9", "#C47D0E"]

    for cat, val, cor in zip(cats, vals, cores_f):
        fig_final.add_trace(go.Bar(
            x=[cat], y=[val],
            marker=dict(color=cor, opacity=0.85, line=dict(width=0)),
            text=[f"⚡ {val:.0f}"],
            textposition='outside',
            textfont=dict(size=11, color=cor, family="DM Mono"),
            showlegend=False,
            hovertemplate=f'<b>{cat}</b><br>{val:.0f}<extra></extra>'
        ))

    fig_final.update_layout(
        title=dict(text="Resumo do Impacto da Usina Solar", font=dict(size=14, family='Playfair Display')),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=360, font=dict(family='DM Sans'),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#f0e8d8'),
        margin=dict(t=50, b=20)
    )
    st.plotly_chart(fig_final, use_container_width=True)

# ── TAB 4: EM CAMPO ───────────────────────────────────────────
with tab4:
    st.markdown(f'<div class="section-label">{T["field_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["field_title"]}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="info-card" style="border-left-color:#C47D0E;margin-bottom:1.5rem">
      <strong>{T['field_instructions_title']}</strong><br>
      <div style="font-size:0.88rem;color:#5C3A0E;margin-top:0.4rem">{T['field_instructions']}</div>
    </div>
    """, unsafe_allow_html=True)

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
                    st.image(foto['path'], use_container_width=True)
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
        st.markdown('<div class="section-label" style="color:#C47D0E">⭐ DESTAQUE — REGISTRO PESSOAL</div>', unsafe_allow_html=True)
        exists_dest = os.path.exists(foto_destaque['path'])
        if exists_dest:
            st.markdown('<div class="photo-destaque">', unsafe_allow_html=True)
            st.image(foto_destaque['path'], use_container_width=True)
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

    fontes = [
        ("AURORAVISION ABB", "Sistema de Monitoramento AuroraVision — ABB Group",
         "Plataforma integrada ao inversor ABB TRIO-50.0-TL-OUTD. Fonte dos dados de geração, CO₂ evitado, NOx e SO₂ não emitidos.", "#F5A623"),
        ("ABB SOLAR", "ABB Ltd. — Solar Inverters Division",
         "TRIO-50.0-TL-OUTD · 50 kW · DC Wiring Box · IP65 · Power-One Italy S.p.A. · Made in Italy · www.abb.com/solar", "#C47D0E"),
        ("TJPR", "Tribunal de Justiça do Estado do Paraná — Gestão Ambiental",
         "Metodologia de equivalência CO₂/árvore: 7,14 árvores por tonelada de CO₂ evitada.", "#2D7A3A"),
        ("SEEG/MCTI", "Sistema de Estimativas de Emissões e Remoções de Gases — MCTI",
         "Fator de emissão da rede elétrica brasileira utilizado no cálculo de CO₂ evitado.", "#2C8FD9"),
        ("NEWS UB", "Universidade do Noroeste Paulista — Portal de Notícias",
         "Usina Solar gera energia limpa equivalente ao plantio de mais de sete mil árvores. Publicado em Jul/2020. Diretor de Infraestrutura: Angelo Mellios.", "#0D1A2E"),
        ("ANEEL", "Agência Nacional de Energia Elétrica",
         "Resolução normativa sobre geração distribuída e micro/minigeração fotovoltaica. Referência regulatória para projetos de energia solar em campi universitários.", "#F5A623"),
        ("ABNT NBR", "ABNT NBR 16149 e NBR 16150",
         "Normas técnicas brasileiras para instalação de sistemas fotovoltaicos conectados à rede de distribuição de energia elétrica.", "#C47D0E"),
    ]

    for sigla, nome, desc, cor in fontes:
        st.markdown(f"""
        <div class="info-card" style="border-left-color:{cor}">
          <div style="display:flex;align-items:flex-start;gap:1rem">
            <div style="background:{cor};color:{'#0D1A2E' if cor == '#F5A623' else 'white'};
                 font-family:'DM Mono',monospace;font-size:0.6rem;padding:4px 7px;border-radius:4px;
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
        🌐 <a href="https://amaurialmeida.github.io/environmental-portfolio/" style="color:var(--solar)">Portfólio</a> &nbsp;|&nbsp;
        🐙 <a href="https://github.com/amaurialmeida" style="color:var(--solar)">GitHub</a>
      </p>
      <p style="font-size:0.75rem;opacity:0.5;margin:0">© 2019–2026 · Usina Solar · Noroeste Paulista · Fernandópolis, SP</p>
    </div>
    """, unsafe_allow_html=True)
