# ⚡ Usina Solar do Noroeste Paulista — Fernandópolis, SP

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://solar-university-nw-sp.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://python.org)
[![License: Academic](https://img.shields.io/badge/License-Academic-green.svg)]()
[![Solar](https://img.shields.io/badge/Energia-Solar_Fotovoltaica-F5A623)]()

> **Observatório Solar · Acompanhamento de Campo e Resultados**  
> Campus de Fernandópolis — Noroeste Paulista · SP · 2019–2020  
> Documentação técnica: **Amauri Almeida** · Tecnólogo em Gestão Ambiental

---

## ❓ Pergunta Central

> *"Uma usina solar fotovoltaica instalada em um campus universitário do interior paulista é capaz de gerar energia limpa em escala suficiente para impactar de forma mensurável o balanço de carbono e a sustentabilidade da instituição?"*

**Resposta:** Sim. Em menos de dois anos de operação, a usina gerou **1,07 GWh** de energia renovável, evitando **953 toneladas de CO₂** — equivalente ao plantio de **7.250 árvores**.

---

## 📊 Resultados Principais

| Indicador | Valor |
|---|---|
| Energia gerada (1º sem/2020) | **~390.000 kWh** |
| Energia acumulada (fev/2019–jul/2020) | **1,07 GWh** |
| CO₂ evitado (acumulado) | **953 toneladas** |
| NOx não emitido | **1.568 kg** |
| SO₂ não emitido | **5,45 kg** |
| Equivalência ambiental | **~7.250 árvores** |
| Início de operação | **Fevereiro de 2019** |
| Inversor | **ABB TRIO-50.0-TL-OUTD · 50 kW · IP65** |

### ⚡ Descobertas Principais

1. **390.000 kWh** gerados só no 1º semestre de 2020
2. **1,07 GWh** em 17 meses — suficiente para ~357 residências/ano
3. **953 t de CO₂** evitadas via fonte fotovoltaica
4. **Expansão de 50%** em estudo com base nos resultados
5. Modelo replicável para instituições do interior paulista

---

## 🗺️ Localização

```
Usina Solar Fotovoltaica
Campus Fernandópolis — Noroeste Paulista, SP
Coordenadas: -20.298020, -50.282114
Inversor: ABB TRIO-50.0-TL-OUTD (IP65 · Made in Italy)
Monitoramento: Sistema AuroraVision ABB
```

---

## 🔬 Pipeline de Documentação

```
Campo         →   Acompanhamento da instalação física
                  Desembalagem → Suportes → Fileiras → Energização

Técnico       →   Estudo dos componentes: módulos monocristalinos + inversor ABB
                  Registro do 1º teste de carga a 100%

Monitoramento →   AuroraVision ABB — dados horários, diários e acumulados
                  Cálculo automático de CO₂, NOx e SO₂ evitados

Análise       →   Consolidação de 17 meses de geração
                  Fator CO₂: 0,892 kg/kWh · Equiv. árvores: 7,14 árv./t CO₂
```

---

## 📁 Estrutura do Repositório

```
solar-university-nw-sp/
├── app.py                          # Dashboard principal
├── requirements.txt                # Dependências Python
├── README.md                       # Este arquivo
└── assets/
    └── campo/                      # ← COLOQUE SUAS FOTOS AQUI
        ├── 01_placas_desembalagem.jpeg
        ├── 02_placas_no_suporte.jpeg
        ├── 03_fileira_instalada.jpeg
        ├── 04_amauri_frente_paineis.jpeg    ← foto destaque (largura total)
        ├── 05_mini_painel_revista.jpeg
        ├── 06_inversor_abb.jpeg
        └── 07_primeiro_teste_carga.jpeg
```

> 💡 **Fotos ausentes** exibem placeholders automáticos com descrição técnica. Adicione as fotos na pasta correta e recarregue a página.

---

## 🚀 Como Executar Localmente

```bash
# Clone o repositório
git clone https://github.com/amaurialmeida/solar-university-nw-sp.git
cd solar-university-nw-sp

# Instale as dependências
pip install -r requirements.txt

# Crie a pasta de fotos
mkdir -p assets/campo

# Execute
streamlit run app.py
```

---

## 🛠️ Stack Tecnológica

| Tecnologia | Uso |
|---|---|
| `Python 3.11` | Linguagem principal |
| `Streamlit` | Dashboard interativo |
| `Plotly` | Gráficos dinâmicos com tema elétrico |
| `Folium` | Mapeamento geoespacial (ponto único) |
| `Pandas / NumPy` | Processamento de dados |

---

## 📚 Referências

- **AuroraVision ABB** — Sistema de monitoramento: dados de geração e impacto ambiental
- **ABB Group** — TRIO-50.0-TL-OUTD Inverter datasheet · www.abb.com/solar
- **TJPR — Gestão Ambiental** — Metodologia CO₂/árvore: 7,14 árvores/tonelada
- **ANEEL** — Resolução normativa 482/2012 (micro/minigeração fotovoltaica)
- **ABNT NBR 16149 e 16150** — Normas para sistemas fotovoltaicos conectados à rede

---

## 🌿 Portfólio Ambiental

Este projeto é parte do portfólio de pesquisa ambiental do autor.  
🔗 [amaurialmeida.github.io/environmental-portfolio](https://amaurialmeida.github.io/environmental-portfolio/)

---

*© 2019–2026 · Amauri Almeida · Usina Solar · Noroeste Paulista · Fernandópolis, SP*
