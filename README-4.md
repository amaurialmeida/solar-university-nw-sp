# ⚡ Northwest São Paulo University Solar Plant — Fernandópolis, SP

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live_App-FF4B4B?logo=streamlit&logoColor=white)](https://solar-university-nw-sp.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: Academic](https://img.shields.io/badge/License-Academic-blue.svg)]()
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()

🌐 **Languages:** English | [Português](README.pt-BR.md) | [Español](README.es.md)

**Solar Energy Observatory — Field Documentation & Impact Analysis**
Fernandópolis, SP · 2019–2020
**Author:** Amauri Almeida de Souza Junior

---

## ❓ Project Question

> "Can a photovoltaic solar plant installed at a university campus in inland São Paulo generate clean energy at a scale sufficient to measurably impact the institution's carbon balance and sustainability?"

**Answer:** Yes. In under two years of operation, the campus solar plant generated 1.07 GWh of clean energy — enough to power roughly 357 Brazilian households for a year — avoiding an estimated 953 tonnes of CO₂, the equivalent of planting ~7,250 trees, establishing a replicable model for institutional renewable energy adoption.

---

## 📊 Data Summary

| Indicator | Value |
|---|---|
| Energy generated (H1 2020) | ~390,000 kWh |
| Cumulative generation (Feb/2019 – Jul/2020) | 1.07 GWh |
| CO₂ avoided (cumulative) | 953 t |
| NOx avoided | 1,568 kg |
| SO₂ avoided | 5.45 kg |
| Equivalent trees planted | ~7,250 |
| Operation start | February 2019 |
| Inverter | ABB TRIO-50.0-TL-OUTD (50 kW) |

*Environmental indicators calculated via the ABB AuroraVision monitoring system; tree-equivalence uses the Paraná State Court of Justice methodology (7.14 trees per tonne of CO₂).*

---

## 🔵 Key Findings

- **390,000 kWh generated in H1 2020 alone** — clean electricity supplying campus operations and reducing reliance on the conventional grid.
- **1.07 GWh cumulative in 17 months of operation** — enough renewable energy to power approximately 357 Brazilian households for a full year.
- **Equivalent to planting ~7,250 trees** — the 953 t of avoided CO₂ translate into a concrete, measurable environmental impact.
- **Greenhouse gases avoided beyond CO₂** — solar generation also prevented 1,568 kg of NOx and 5.45 kg of SO₂ emissions, gases linked to acid rain and respiratory illness.
- **~50% capacity expansion in planning** — based on these results, the institution began technical studies to scale the plant further, alongside a campus-wide energy efficiency diagnostic.

---

## 🗺️ Location

```
Plant location   → University campus, Fernandópolis, SP, Brazil
Panel tilt       → Calculated for local latitude (~20° S) to maximize
                    year-round solar irradiance capture
Grid connection  → Internal campus electrical network
```

The dashboard's interactive map (Folium) marks the exact plant location with technical installation details on click.

---

## 🔬 Methodology

```
Physical installation  →  Documented step by step: module unboxing, mounting
                           on inclined metal supports, row alignment, and
                           connection verification

Component analysis      →  Monocrystalline PV modules + ABB TRIO-50.0-TL-OUTD
                           central inverter (50 kW, IP65, made in Italy),
                           converting DC output to grid-compatible AC

Energization             →  Documented switch-on event: first connection to the
                           campus grid at 100% load, marking the start of
                           photovoltaic generation

Monitoring               →  Real-time data collection via ABB's AuroraVision
                           platform, integrated with the TRIO-50 inverter —
                           hourly, daily, and cumulative generation, plus
                           automatic environmental indicators (CO₂, NOx, SO₂)

Impact calculation       →  Consolidated generation data converted into
                           avoided-emissions equivalents using standard
                           utility methodologies
```

---

## 🖥️ Dashboard Overview

The Streamlit app is organized into five tabs:

1. **🗺️ Map & Analysis** — interactive Folium map of the plant location, plus monthly generation charts and a solar-vs-estimated-campus-consumption comparison.
2. **🔬 Methodology & Pipeline** — the six-step documentation pipeline, from physical installation to expansion planning, plus technical specs.
3. **💡 What We Found** — the five key findings above, plus the project's overall conclusion.
4. **📷 In the Field** — real installation photos: module unboxing, mounting, the completed row, the inverter/DC wiring box, and the first load test.
5. **📚 Sources & Credits** — technical references and author credentials.

The full interface — labels, chart titles, and narrative text — is natively trilingual (PT/EN/ES), switchable from the sidebar.

---

## 🛠️ Tech Stack

| Technology | Use |
|---|---|
| Python 3.11 | Core language |
| Streamlit | Dashboard framework |
| Folium + streamlit-folium | Interactive plant-location mapping |
| Plotly (Express & Graph Objects) | Generation, impact, and comparison charts |
| Pandas / NumPy | Data processing |

---

## 📁 Repository Structure

```
solar-university-nw-sp/
├── app.py                    # Main dashboard (5 tabs, PT/EN/ES)
├── requirements.txt          # Python dependencies
├── README.md                   # This file (English)
├── README.pt-BR.md             # Portuguese version
├── README.es.md                # Spanish version
└── assets/
    └── campo/                 # Field photos (see LEIA_ME_FOTOS_solar.md for filenames)
        ├── 01_placas_desembalagem.jpeg
        ├── 02_placas_no_suporte.jpeg
        ├── 03_fileira_instalada.jpeg
        ├── 04_amauri_frente_paineis.jpeg   ← featured (full width)
        ├── 05_mini_painel_revista.jpeg
        ├── 06_inversor_abb.jpeg
        └── 07_primeiro_teste_carga.jpeg
```

💡 Missing photos automatically render as labeled placeholders. Drop files into `assets/campo/` using the exact filenames and the app detects them on next run.

---

## 🚀 Run Locally

```bash
# Clone the repository
git clone https://github.com/amaurialmeida/solar-university-nw-sp.git
cd solar-university-nw-sp

# Install dependencies
pip install -r requirements.txt

# Run
streamlit run app.py
```

---

## 🌐 Live App

🔗 **[solar-university-nw-sp.streamlit.app](https://solar-university-nw-sp.streamlit.app/)**

Available in 🇧🇷 Portuguese, 🇺🇸 English, and 🇪🇸 Spanish.

---

## 🔗 Academic / Professional Links

| Platform | Link |
|---|---|
| Lattes | http://lattes.cnpq.br/9545242042800090 |
| Escavador | https://www.escavador.com/sobre/8577779/amauri-almeida-de-souza-junior |

---

## 🌿 Environmental Portfolio

This project is part of the author's environmental research and data science portfolio.
🔗 [amaurialmeida.github.io/environmental-portfolio](https://amaurialmeida.github.io/environmental-portfolio)

---

© 2019–2026 · Amauri Almeida de Souza Junior · Field Research & Portfolio Project
