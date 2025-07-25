
import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="RCD-Based Recidivism Simulator (3D + Bars)", layout="wide")

st.title("RCD-Based Recidivism Simulator with 3D Surface and Bar Chart")

st.markdown("""
This tool visualizes symbolic identity phase-space dynamics using psychological assessment data.
The 3D attractor surface shows how symbolic stability (γ), drift (δ), and entropy (∇S) interact.
The bar chart reflects the symbolic health of each core RCD variable.
""")

# Sidebar inputs
st.sidebar.header("Psychological Inputs")

eid = st.sidebar.slider("MMPI-3: EID", 0, 100, 50)
bxd = st.sidebar.slider("MMPI-3: BXD", 0, 100, 50)
thd = st.sidebar.slider("MMPI-3: THD", 0, 100, 50)
intr = st.sidebar.slider("MMPI-3: INTR", 0, 100, 50)
somc = st.sidebar.slider("MMPI-3: SOM-C", 0, 100, 50)
cog = st.sidebar.slider("MMPI-3: COG", 0, 100, 50)

impulsivity = st.sidebar.slider("HCR-20: Impulsivity", 0, 100, 50)
support = st.sidebar.slider("HCR-20: Lack of Support", 0, 100, 50)
pclr_aff = st.sidebar.slider("PCL-R: Affective Deficits", 0, 100, 50)
pclr_antisocial = st.sidebar.slider("PCL-R: Antisocial Behavior", 0, 100, 50)
pai_agg = st.sidebar.slider("PAI: Aggression", 0, 100, 50)
pai_bor = st.sidebar.slider("PAI: Impulsivity", 0, 100, 50)
mcmi_antisocial = st.sidebar.slider("MCMI-IV: Antisocial", 0, 100, 50)
mcmi_borderline = st.sidebar.slider("MCMI-IV: Borderline", 0, 100, 50)

# Derived RCD variables
gamma = max(0, 100 - (eid + thd + cog) / 3 - mcmi_borderline / 4)
delta = (bxd + impulsivity + pclr_antisocial + pai_bor + mcmi_antisocial) / 5
theta = max(0, 100 - bxd)
mu = max(0, 100 - (intr + support + pclr_aff + mcmi_borderline) / 4)
entropy = (eid + somc + pai_agg) / 3

st.subheader("RCD Variables")
st.write(f"**γ (Phase Stability)**: {gamma:.2f}")
st.write(f"**δ (Symbolic Drift)**: {delta:.2f}")
st.write(f"**Θ (Karmic Resistance)**: {theta:.2f}")
st.write(f"**μ (Recursive Coherence)**: {mu:.2f}")
st.write(f"**∇S (Entropy Gradient)**: {entropy:.2f}")

# 3D Plot
st.subheader("Symbolic Attractor Surface (3D)")
x = np.linspace(0, 1, 50)
y = np.linspace(0, 1, 50)
x, y = np.meshgrid(x, y)
z = gamma/100 * np.exp(-delta/100 * x) + (entropy/100) * np.sin(2 * np.pi * y)

fig3d = go.Figure(data=[go.Surface(z=z, x=x, y=y, colorscale='Viridis')])
fig3d.update_layout(
    scene=dict(
        xaxis_title='Symbolic Time',
        yaxis_title='Phase Angle',
        zaxis_title='Stability / Drift'
    ),
    height=600
)
st.plotly_chart(fig3d)

# 2D Bar Chart
st.subheader("RCD Variable Snapshot (Bar Chart)")

def get_color(value, var):
    if var == 'γ':
        if value < 40: return 'crimson'
        elif value < 70: return 'gold'
        else: return 'limegreen'
    elif var == 'δ':
        if value > 60: return 'crimson'
        elif value > 30: return 'gold'
        else: return 'limegreen'
    elif var == 'Θ':
        if value < 40: return 'crimson'
        elif value < 70: return 'gold'
        else: return 'limegreen'
    elif var == 'μ':
        if value < 40: return 'crimson'
        elif value < 70: return 'gold'
        else: return 'limegreen'
    elif var == '∇S':
        if value > 60: return 'crimson'
        elif value > 30: return 'gold'
        else: return 'limegreen'
    return 'gray'

rcd_labels = ['γ (Phase Stability)', 'δ (Symbolic Drift)', 'Θ (Karmic Resistance)', 'μ (Recursive Coherence)', '∇S (Entropy Gradient)']
rcd_values = [gamma, delta, theta, mu, entropy]
rcd_colors = [get_color(v, l[0]) for v, l in zip(rcd_values, rcd_labels)]

fig_bar = go.Figure(data=[
    go.Bar(
        x=rcd_labels,
        y=rcd_values,
        marker_color=rcd_colors,
        text=[f"{v:.2f}" for v in rcd_values],
        textposition='outside'
    )
])
fig_bar.update_layout(
    yaxis=dict(title='Score (0–100)', range=[0, 100]),
    xaxis=dict(title='RCD Variables'),
    height=500
)
st.plotly_chart(fig_bar)
