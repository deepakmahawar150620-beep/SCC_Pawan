import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from io import BytesIO

# ✅ Load Excel file from GitHub
url = "https://raw.githubusercontent.com/deepakmahawar150620-beep/SCC_Pawan/main/Pipeline_data.xlsx"
df = pd.read_excel(url, engine="openpyxl")

# ✅ Clean column names
df.columns = [col.strip() for col in df.columns]

# ✅ Clean and convert specific columns
if 'Hoop stress% of SMYS' in df.columns:
    df['Hoop stress% of SMYS'] = df['Hoop stress% of SMYS'].astype(str).str.replace('%', '').astype(float)
    if df['Hoop stress% of SMYS'].max() < 10:
        df['Hoop stress% of SMYS'] *= 100

if 'OFF PSP (VE V)' in df.columns:
    df['OFF PSP (VE V)'] = df['OFF PSP (VE V)'].astype(float).abs()

# ✅ Dropdown options and labels
plot_columns = {
    'Depth (mm)': 'Depth (mm)',
    'OFF PSP (VE V)': 'OFF PSP (-ve Volt)',
    'Soil Resistivity (Ω-cm)': 'Soil Resistivity (Ω-cm)',
    'Distance from Pump(KM)': 'Distance from Pump (KM)',
    'Operating Pr.': 'Operating Pressure',
    'Remaining Thickness(mm)': 'Remaining Thickness (mm)',
    'Hoop stress% of SMYS': 'Hoop Stress (% of SMYS)',
    'Temperature': 'Temperature (°C)',
    'Pipe Age': 'Pipe Age'
}

st.title("📈 SCC Risk Assessment Graph Viewer")

# ✅ Select column
selected_col = st.selectbox("Select a parameter to compare with Stationing (m):", list(plot_columns.keys()))
label = plot_columns[selected_col]

# ✅ Create Plotly graph
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['Stationing (m)'],
    y=df[selected_col],
    mode='lines+markers',
    name=label,
    line=dict(width=2),
    marker=dict(size=6)
))

# ✅ Threshold lines
if label == 'Hoop Stress (% of SMYS)':
    fig.add_shape(type='line',
        x0=df['Stationing (m)'].min(),
        x1=df['Stationing (m)'].max(),
        y0=60,
        y1=60,
        line=dict(color='red', width=2, dash='dash')
    )

elif label == 'OFF PSP (-ve Volt)':
    for yval in [0.85, 1.2]:
        fig.add_shape(type='line',
            x0=df['Stationing (m)'].min(),
            x1=df['Stationing (m)'].max(),
            y0=yval,
            y1=yval,
            line=dict(color='red', width=2, dash='dash')
        )

# ✅ Layout customization
fig.update_layout(
    title=f"Stationing vs {label}",
    xaxis_title="Stationing (m)",
    yaxis_title=label,
    height=550,
    template='plotly_white',
    xaxis=dict(showline=True, linecolor='black', mirror=True),
    yaxis=dict(showline=True, linecolor='black', mirror=True, gridcolor='lightgray'),
    margin=dict(l=60, r=40, t=50, b=60),
    showlegend=False
)

# ✅ Show Plot
st.plotly_chart(fig, use_container_width=True)

# ✅ Export to high-res PNG using kaleido
buffer = BytesIO()
pio.write_image(fig, buffer, format="png", width=1400, height=700, scale=3)
st.download_button(
    label="📥 Download High-Quality Graph (PNG)",
    data=buffer.getvalue(),
    file_name=f"Stationing_vs_{label.replace(' ', '_')}.png",
    mime="image/png"
)
