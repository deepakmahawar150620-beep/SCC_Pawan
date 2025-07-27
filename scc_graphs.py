# ✅ Step 1: Install required libraries (only once)
!pip install pandas openpyxl plotly --quiet

# ✅ Step 2: Import libraries
import pandas as pd
import plotly.graph_objects as go
from IPython.display import display

# ✅ Step 3: Load Excel file from GitHub
url = "https://github.com/deepakmahawar150620-beep/SCC_Pawan/raw/23a388180a79f39abdf87e5084deb9c73762b069/Pipeline_data.xlsx"
df = pd.read_excel(url, engine='openpyxl')
df.columns = [col.strip() for col in df.columns]  # Clean whitespace

# ✅ Step 4: Data Cleaning
if 'OFF PSP (VE V)' in df.columns:
    df['OFF PSP (VE V)'] = df['OFF PSP (VE V)'].astype(float).abs()

if 'Hoop stress% of SMYS' in df.columns:
    df['Hoop stress% of SMYS'] = df['Hoop stress% of SMYS'].astype(str).str.replace('%', '').astype(float)
    if df['Hoop stress% of SMYS'].max() < 10:
        df['Hoop stress% of SMYS'] *= 100

# ✅ Step 5: Define which columns to plot (and their labels)
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

# ✅ Step 6: Plot graphs one by one
for col, label in plot_columns.items():
    if col not in df.columns:
        continue

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Stationing (m)'],
        y=df[col],
        mode='lines+markers',
        name=label,
        line=dict(width=2),
        marker=dict(size=6)
    ))

    # ➤ Add threshold lines
    if label == 'Hoop Stress (% of SMYS)':
        fig.add_shape(type='line',
            x0=df['Stationing (m)'].min(), x1=df['Stationing (m)'].max(),
            y0=60, y1=60,
            line=dict(color='red', width=2, dash='dash')
        )

    if label == 'OFF PSP (-ve Volt)':
        for yval in [0.85, 1.2]:
            fig.add_shape(type='line',
                x0=df['Stationing (m)'].min(), x1=df['Stationing (m)'].max(),
                y0=yval, y1=yval,
                line=dict(color='red', width=2, dash='dash')
            )

    # ➤ Graph formatting
    fig.update_layout(
        title=f'Stationing vs {label}',
        xaxis_title='Stationing (m)',
        yaxis_title=label,
        height=500,
        template='plotly_white',
        showlegend=False,
        xaxis=dict(showline=True, linecolor='black', mirror=True),
        yaxis=dict(showline=True, linecolor='black', mirror=True, gridcolor='lightgray')
    )

    display(fig)
