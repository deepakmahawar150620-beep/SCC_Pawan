import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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

# ✅ Plotting column options
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

# ✅ App UI
st.set_page_config(page_title="SCC Graph Explorer", layout="wide")
st.title("📊 SCC Graph Explorer")

# ✅ Dropdown
selected_col = st.selectbox("Choose a parameter to compare with Stationing (m):", list(plot_columns.keys()))
label = plot_columns[selected_col]

# ✅ Create Graph
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['Stationing (m)'],
    y=df[selected_col],
    mode='lines+markers',
    name=label,
    line=dict(width=2),
    marker=dict(size=6)
))

# ➤ Add Threshold Lines
if label == 'Hoop Stress (% of SMYS)':
    fig.add_shape(
        type='line',
        x0=df['Stationing (m)'].min(),
        x1=df['Stationing (m)'].max(),
        y0=60,
        y1=60,
        line=dict(color='red', width=2, dash='dash')
    )

elif label == 'OFF PSP (-ve Volt)':
    for yval in [0.85, 1.2]:
        fig.add_shape(
            type='line',
            x0=df['Stationing (m)'].min(),
            x1=df['Stationing (m)'].max(),
            y0=yval,
            y1=yval,
            line=dict(color='red', width=2, dash='dash')
        )

# ✅ Graph layout
fig.update_layout(
    title=f'Stationing vs {label}',
    xaxis_title='Stationing (m)',
    yaxis_title=label,
    height=500,
    template='plotly_white',
    showlegend=False,
    xaxis=dict(showline=True, linecolor='black', mirror=True),
    yaxis=dict(showline=True, linecolor='black', mirror=True, gridcolor='lightgray'),
    margin=dict(l=60, r=40, t=50, b=60)
)

# ✅ Display Graph
st.plotly_chart(fig, use_container_width=True)
