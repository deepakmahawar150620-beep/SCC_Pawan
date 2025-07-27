# 🛠️ SCC Risk Visualization App

This project visualizes and analyzes pipeline data related to **Stress Corrosion Cracking (SCC)** using `Stationing` and various pipeline parameters like soil resistivity, PSP voltage, hoop stress, and more.

---

## 📊 Features

- Visualize graphs for:
  - Soil Resistivity vs Stationing
  - OFF PSP vs Stationing (with threshold lines at 0.85V and 1.2V)
  - Hoop Stress (% of SMYS) vs Stationing (with 60% threshold)
  - Pipe Age, Temperature, Remaining Thickness, etc.
- Highlights data points above risk thresholds.
- Designed to integrate with **Streamlit** for web-based apps.

---

## 📁 Files in This Repository

| File                      | Description                              |
|---------------------------|------------------------------------------|
| `Pipeline_data.xlsx`      | Pipeline dataset with multiple parameters |
| `scc_graphs.py`           | Python script to generate graphs         |
| `app.py` *(optional)*     | Streamlit web app file (if applicable)   |
| `README.md`               | Project instructions and documentation   |

---

## 🚀 How to Run the Graph Script

### Option 1: Google Colab

1. Open Google Colab.
2. Paste and run the content from `scc_graphs.py`.
3. It will load the Excel file from GitHub and generate graphs.

### Option 2: Local Python Environment

```bash
git clone https://github.com/deepakmahawar150620-beep/SCC_Pawan.git
cd SCC_Pawan
pip install pandas openpyxl plotly
python scc_graphs.py
