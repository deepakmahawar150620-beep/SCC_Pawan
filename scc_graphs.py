import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import base64
from io import BytesIO

# ✅ Load Excel file from GitHub
url = "https://raw.githubusercontent.com/deepakmahawar150620-beep/SCC_Pawan/main/Pipeline_data.xlsx"
df = pd.read_excel(url, engine='openpyxl')
df.columns = [col.strip() for col in df.columns]

# ✅ Data cleaning
if 'OFF PSP (VE V)' in df.columns:
    df['OFF PSP (VE V)'] = df['OFF PSP (VE V)'].astype(float).abs()

if 'Hoop stress% of SMYS' in df.columns:
    df['Hoop stress% of SMYS'] = df['Hoop stress% of SMYS'].astype(str).str.replace('%', '').astype(float)
    if df['Hoop stress% of SMYS'].max() < 10:
        df['Hoop stress% of SMYS'] *= 100

# ✅ Define column mapping
plot_columns = {
    'Depth (mm)': 'Depth (mm)',
    'OFF PSP (VE V)': 'OFF PSP (-ve Volt)',
    'Soil Resistivity (Ω-cm)': 'Soil Resistivity (Ω-cm)',
    'Distance from Pump(KM)': 'Distance from Pump (KM)',
    'Operating Pr.': 'Operating Pressure',
    'Remaining Thickness(mm)': 'Remaining Thickness (mm)',
    'Hoop stress% of SMYS': 'Hoop Stress (% of SMYS)',
    'CoatingType': 'Coating Type',
    'nmConstrYear': 'Construction Year',
    'Pipe Age': 'Pipe Age',
    'Temperature': 'Temperature (°C)'
}

st.set_page_config(page_title="SCC Graph Viewer", layout="wide")
st.title("📊 SCC Graph Viewer with Download Option")

selected_col = st.selectbox("Select parameter to plot vs Stationing:", list(plot_columns.keys()))
label = plot_columns[selected_col]

# ✅ Create the Plotly figure
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['Stationing (m)'],
    y=df[selected_col],
    mode='lines+markers',
    name=label,
    line=dict(width=2),
    marker=dict(size=6)
))

# ➤ Threshold lines
if label == 'Hoop Stress (% of SMYS)':
    fig.add_shape(
        type='line',
        x0=df['Stationing (m)'].min(), x1=df['Stationing (m)'].max(),
        y0=60, y1=60,
        line=dict(color='red', width=2, dash='dash')
    )

elif label == 'OFF PSP (-ve Volt)':
    for yval in [0.85, 1.2]:
        fig.add_shape(
            type='line',
            x0=df['Stationing (m)'].min(), x1=df['Stationing (m)'].max(),
            y0=yval, y1=yval,
            line=dict(color='red', width=2, dash='dash')
        )

# ✅ Update layout
fig.update_layout(
    title=f"Stationing vs {label}",
    xaxis_title="Stationing (m)",
    yaxis_title=label,
    height=550,
    template='plotly_white',
    xaxis=dict(showline=True, linecolor='black', mirror=True),
    yaxis=dict(showline=True, linecolor='black', mirror=True, gridcolor='lightgray'),
    margin=dict(l=60, r=40, t=50, b=60)
)

# ✅ Display plot
st.plotly_chart(fig, use_container_width=True)

# ✅ Downloadable Image Button
buffer = BytesIO()
pio.write_image(fig, buffer, format='png', width=1200, height=700, scale=3)
b64 = base64.b64encode(buffer.getvalue()).decode()
href = f'<a href="data:image/png;base64,{b64}" download="Stationing_vs_{label.replace(" ", "_")}.png">📥 Download this graph as PNG</a>'
st.markdown(href, unsafe_allow_html=True)
