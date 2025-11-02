"""
Biological Relativity: Product-Grade Methylome Manifold Visualization
Polished 3D torus with surface-constrained aging trajectories
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import anthropic
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from methylome_trajectory import (
    build_torus_mesh,
    baseline_points_on_surface,
    status_quo_path,
    intervention_path,
    healthy_population_path,
    healthy_population_band,
    blend_toward_healthy,
    hud_metrics_from_xyz,
    torus_uv_to_xyz
)

# Page configuration - Product-like dark theme
st.set_page_config(
    page_title="ChronOS",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dark theme CSS - Product aesthetic
st.markdown("""
<style>
    .main {
        background-color: #0f0f0f;
        color: #e8e8e8;
    }
    .stApp {
        background-color: #0f0f0f;
    }
    .metric-chip {
        background: linear-gradient(145deg, #1a1a1a 0%, #141414 100%);
        border: 1px solid rgba(0, 212, 255, 0.15);
        border-radius: 16px;
        padding: 20px;
        margin: 12px 0;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
    }
    .metric-label {
        font-size: 0.75rem;
        color: #808080;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 8px;
        font-weight: 600;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .metric-delta {
        font-size: 0.85rem;
        margin-top: 8px;
        font-weight: 500;
    }
    .delta-good {
        color: #00ff88;
    }
    .delta-bad {
        color: #ff4466;
    }
    h1, h2, h3, h4 {
        color: #f0f0f0 !important;
        font-weight: 300;
    }
    h1 {
        font-size: 2.8rem !important;
        margin-bottom: 0.5rem !important;
    }
    h3 {
        font-size: 1.4rem !important;
        opacity: 0.9;
    }
    .stSlider label, .stSelectSlider label {
        color: #c0c0c0 !important;
        font-size: 0.9rem !important;
    }
    .stButton button {
        background: linear-gradient(135deg, #1a1a1a 0%, #0f0f0f 100%);
        color: #00d4ff;
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 8px;
        font-weight: 600;
    }
    .stButton button:hover {
        border-color: rgba(0, 212, 255, 0.6);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
    }
    div[data-testid="stHorizontalBlock"] {
        gap: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'start_uv' not in st.session_state:
    st.session_state.start_uv = (1.5, 0.8)
    st.session_state.baseline_cache = None
    st.session_state.statusquo_cache = None
    st.session_state.healthy_cache = None

# Header - Minimal and elegant
st.markdown("# ChronOS")
st.markdown("### Jeff's Liver Aging Dynamics")
st.markdown("")


# ---- Patient Case: image left, card right (polished) ----
with st.container():
    st.markdown(
        """
        <style>
          /* Reduce default Streamlit column padding for this row */
          .patient-row [data-testid="column"] { 
            padding-left: 0 !important; 
            padding-right: 0 !important; 
          }

          /* Keep the row readable on large screens */
          .patient-row-wrap { 
            max-width: 1040px; 
            margin: 0 auto 24px auto; 
          }

          /* Photo card: match your chip/card aesthetic */
          .patient-photo-card {
            background: linear-gradient(145deg, #1a1a1a 0%, #141414 100%);
            border: 1px solid rgba(0, 212, 255, 0.2);
            border-radius: 12px;
            padding: 3px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.35);
            width: 150px;                 /* tweak to taste */
          }
          .patient-photo-card img {
            display: block;
            width: 100%;
            height: auto;
            border-radius: 10px;          /* inner rounding for the image itself */
          }
          .patient-caption {
            color: #9aa0a6; 
            font-size: 0.85rem; 
            margin-top: .4rem;
            text-align: center;
          }

          /* Right card nudged slightly left to sit closer to the photo */
          .patient-right-card {
            margin-left: -200px;            /* small negative margin brings columns closer */
            background: linear-gradient(145deg, #1a1a1a 0%, #141414 100%);
            border: 1px solid rgba(0, 212, 255, 0.2);
            border-radius: 12px;
            padding: 20px;
          }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Give this row a wrapper class so CSS targets are scoped
    st.markdown('<div class="patient-row-wrap patient-row">', unsafe_allow_html=True)

    wrapper_left, wrapper_right = st.columns([1, 2], gap="small")

    with wrapper_left:
        # --- robust image render inside the styled card (base64 embed) ---
        import base64, pathlib

        # Try a few common locations
        candidates = [
            pathlib.Path("assets/jeff.png"),
            pathlib.Path("jeff.png"),
            pathlib.Path("./assets/jeff.png"),
        ]
        img_path = next((p for p in candidates if p.exists()), None)

        if img_path is None:
            st.warning("Could not find jeff.png. Place it in ./assets or next to app.py.")
        else:
            b64 = base64.b64encode(img_path.read_bytes()).decode("utf-8")
            st.markdown(
                f"""
                <div class="patient-photo-card">
                <img src="data:image/png;base64,{b64}" alt="Jeff — Liver Care Plan" />
                <div class="patient-caption">
                </div>
                """,
                unsafe_allow_html=True,
            )


    with wrapper_right:
        st.markdown("""
        <div class="patient-right-card">
            <div style='font-size: 1.2rem; font-weight: 600; color: #00d4ff; margin-bottom: 14px;'>
                Patient Case
            </div>
            <div style='font-size: 0.95rem; color: #a0a0a0; line-height: 1.8;'>
                <strong style='color: #c0c0c0;'>First visit:</strong> 3 months ago<br>
                <strong style='color: #c0c0c0;'>Lifestyle at intake:</strong> high alcohol, high caffeine, no workouts<br>
                <strong style='color: #c0c0c0;'>Measurements:</strong> weekly DNA methylation (liver) × 3 weeks<br>
                <strong style='color: #c0c0c0;'>Goal:</strong> slow liver aging to return to healthy population trajectory
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close patient-row-wrap




# Main layout: Split screen
left_col, right_col = st.columns([2.2, 1])

# RIGHT PANEL: Treatment Controls
with right_col:
    st.markdown("### 🎛️ Treatment Interventions")
    
    # Time horizon selector
    time_horizon = st.select_slider(
        "Prediction Time Horizon",
        options=[3, 6, 12],
        value=12,
        format_func=lambda x: f"{x} months"
    )
        
    # Sleep intervention
    sleep_change = st.slider(
        "Sleep Duration Change (hours/night)",
        min_value=-2.0,
        max_value=4.0,
        value=0.0,
        step=0.5,
        help="Increase or decrease sleep hours per night"
    )
    
    # Exercise intervention (VO2max)
    vo2max_change = st.slider(
        "VO₂max Improvement (%)",
        min_value=0.0,
        max_value=50.0,
        value=0.0,
        step=5.0,
        help="Expected improvement in cardiovascular fitness"
    )
    
    # Alcohol reduction
    alcohol_reduction = st.slider(
        "Alcohol Reduction (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=10.0,
        help="Percentage reduction in alcohol consumption"
    )
    
    # Caffeine reduction
    caffeine_reduction = st.slider(
        "Caffeine Reduction (mg/day)",
        min_value=0.0,
        max_value=400.0,
        value=0.0,
        step=50.0,
        help="Reduction in daily caffeine intake"
    )
    
    # Set removed interventions to 0 (pharmacological interventions removed)
    nac_dose = 0
    metformin_dose = 0
    
    # Reset button
    if st.button("🔄 Reset All Interventions", use_container_width=True):
        st.rerun()
    
    st.markdown("---")
    
    # Treatment summary
    interventions = {
        'sleep_change': sleep_change,
        'vo2max_change': vo2max_change,
        'alcohol_reduction': alcohol_reduction,
        'caffeine_reduction': caffeine_reduction,
        'nac_dose': nac_dose,
        'metformin_dose': metformin_dose
    }
    
    # Check if any interventions are active
    any_intervention = any(v != 0 for v in interventions.values())
    
    if any_intervention:
        st.success("✅ Interventions Active")
    else:
        st.info("ℹ️ No interventions applied")

# Treatment summary
interventions = {
    'sleep_change': sleep_change,
    'vo2max_change': vo2max_change,
    'alcohol_reduction': alcohol_reduction,
    'caffeine_reduction': caffeine_reduction,
    'nac_dose': nac_dose,
    'metformin_dose': metformin_dose
}

# LEFT PANEL: 3D Visualization
with left_col:
    st.markdown("### ")  # Empty space for alignment
    
    # Generate trajectories (cache baseline, status quo, and healthy)
    if st.session_state.baseline_cache is None:
        st.session_state.baseline_cache = baseline_points_on_surface(
            start_uv=st.session_state.start_uv,
            weeks=3
        )
    
    if st.session_state.statusquo_cache is None or True:  # Always regenerate for time_horizon changes
        st.session_state.statusquo_cache = status_quo_path(
            start_uv=st.session_state.start_uv,
            months=time_horizon
        )
    
    if st.session_state.healthy_cache is None or True:  # Always regenerate for time_horizon changes
        st.session_state.healthy_cache = healthy_population_path(
            start_uv=(0.0, 0.0),  # Healthy region
            months=time_horizon,
            seed=100
        )
    
    # Generate intervention path and blend toward healthy
    intervention_data_raw = intervention_path(
        start_uv=st.session_state.start_uv,
        months=time_horizon,
        sliders=interventions
    )
    
    # Check if interventions are active to determine blending strength
    any_intervention = any(v != 0 for v in interventions.values())
    alpha_blend = 0.35 if any_intervention else 0.0
    
    intervention_data = blend_toward_healthy(
        intervention_data_raw,
        st.session_state.healthy_cache,
        alpha=alpha_blend
    )
    
    baseline_data = st.session_state.baseline_cache
    statusquo_data = st.session_state.statusquo_cache
    healthy_data = st.session_state.healthy_cache
    
    # Generate healthy error band
    healthy_band = healthy_population_band(healthy_data, band_width=0.15)
    
    # Create 3D plot - Product aesthetic (axis-free)
    fig = go.Figure()
    
    # Add torus mesh surface
    torus_mesh = build_torus_mesh(nu=120, nv=60)
    
    # Convert mesh to plotly format
    vertices = torus_mesh['positions']
    faces = torus_mesh['indices'].reshape(-1, 3)
    
    fig.add_trace(go.Mesh3d(
        x=vertices[:, 0],
        y=vertices[:, 1],
        z=vertices[:, 2],
        i=faces[:, 0],
        j=faces[:, 1],
        k=faces[:, 2],
        color='#1a1d28',
        opacity=0.35,
        hoverinfo='skip',
        lighting=dict(
            ambient=0.4,
            diffuse=0.7,
            specular=0.5,
            roughness=0.3,
            fresnel=0.2
        ),
        lightposition=dict(x=3000, y=3000, z=5000),
        showlegend=False,
        flatshading=False
    ))
    
    # Healthy Population error band (upper and lower bounds as translucent lines)
    fig.add_trace(go.Scatter3d(
        x=healthy_band['upper']['x'],
        y=healthy_band['upper']['y'],
        z=healthy_band['upper']['z'],
        mode='lines',
        name='Healthy Band',
        line=dict(color='rgba(0, 200, 100, 0.4)', width=3),
        opacity=0.4,
        hoverinfo='skip',
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter3d(
        x=healthy_band['lower']['x'],
        y=healthy_band['lower']['y'],
        z=healthy_band['lower']['z'],
        mode='lines',
        name='Healthy Band Lower',
        line=dict(color='rgba(0, 200, 100, 0.4)', width=3),
        opacity=0.4,
        hoverinfo='skip',
        showlegend=False
    ))
    
    # Healthy Population (avg) - green line
    fig.add_trace(go.Scatter3d(
        x=healthy_data['x'],
        y=healthy_data['y'],
        z=healthy_data['z'],
        mode='lines',
        name='Healthy Population (avg)',
        line=dict(color='#00cc66', width=6),
        opacity=0.9,
        hoverinfo='skip'
    ))
    
    # Historical Data: 3 anchor dots + connecting line (neutral gray)
    fig.add_trace(go.Scatter3d(
        x=baseline_data['x'],
        y=baseline_data['y'],
        z=baseline_data['z'],
        mode='markers+lines',
        name='Historical Data',
        marker=dict(size=7, color='#999999', symbol='circle'),
        line=dict(color='#999999', width=3),
        opacity=0.8,
        hoverinfo='skip'
    ))
    
    # Current Position marker (at last historical point)
    fig.add_trace(go.Scatter3d(
        x=[baseline_data['x'][-1]],
        y=[baseline_data['y'][-1]],
        z=[baseline_data['z'][-1]],
        mode='markers',
        name='Current Position',
        marker=dict(size=10, color='#ffdd00', symbol='circle',
                   line=dict(color='#ffffff', width=2)),
        opacity=1.0,
        hoverinfo='skip'
    ))
    
    # Status Quo (No Intervention): forecast (amber) - what happens without intervention
    fig.add_trace(go.Scatter3d(
        x=statusquo_data['x'],
        y=statusquo_data['y'],
        z=statusquo_data['z'],
        mode='lines',
        name='No Intervention',
        line=dict(color='#ff9933', width=6),
        opacity=0.9,
        hoverinfo='skip'
    ))
    
    # With Interventions: modified trajectory (cyan, blended toward healthy)
    line_color = '#00d4ff' if any_intervention else '#666666'
    line_width = 8 if any_intervention else 5
    
    fig.add_trace(go.Scatter3d(
        x=intervention_data['x'],
        y=intervention_data['y'],
        z=intervention_data['z'],
        mode='lines',
        name='With Interventions',
        line=dict(color=line_color, width=line_width),
        opacity=1.0,
        hoverinfo='skip'
    ))
    
    # Layout configuration - AXIS-FREE, product aesthetic
    fig.update_layout(
        scene=dict(
            # NO AXES - product-like clean look
            xaxis=dict(
                visible=False,
                showticklabels=False,
                showgrid=False,
                showbackground=False,
                zeroline=False
            ),
            yaxis=dict(
                visible=False,
                showticklabels=False,
                showgrid=False,
                showbackground=False,
                zeroline=False
            ),
            zaxis=dict(
                visible=False,
                showticklabels=False,
                showgrid=False,
                showbackground=False,
                zeroline=False
            ),
            camera=dict(
                eye=dict(x=1.6, y=1.6, z=1.4),
                center=dict(x=0, y=0, z=0)
            ),
            bgcolor='#0a0a0a',
            aspectmode='data'
        ),
        paper_bgcolor='#0f0f0f',
        plot_bgcolor='#0a0a0a',
        height=650,
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=0.02,
            bgcolor="rgba(20, 20, 20, 0.7)",
            bordercolor="rgba(0, 212, 255, 0.3)",
            borderwidth=1,
            font=dict(color='#e0e0e0', size=11)
        ),
        showlegend=True,
        hovermode=False
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# HUD Metrics - Product style chips
st.markdown("---")
st.markdown("### 📊 Metrics")
st.markdown("")

# Calculate HUD metrics from paths
statusquo_metrics = hud_metrics_from_xyz(
    statusquo_data['x'],
    statusquo_data['y'],
    statusquo_data['z']
)

healthy_metrics = hud_metrics_from_xyz(
    healthy_data['x'],
    healthy_data['y'],
    healthy_data['z']
)

intervention_metrics_raw = hud_metrics_from_xyz(
    intervention_data['x'],
    intervention_data['y'],
    intervention_data['z']
)

# Apply same-direction coupling rule:
# If velocity increases, acceleration must increase (and vice versa)
v0 = statusquo_metrics['velocity']
a0 = statusquo_metrics['acceleration']
v1 = intervention_metrics_raw['velocity']
a1_raw = intervention_metrics_raw['acceleration']

dv = v1 - v0
da_raw = a1_raw - a0

# Enforce same direction for velocity and acceleration deltas
if dv == 0:
    # No velocity change, keep acceleration stable
    da_coupled = 0.0
else:
    # Check if signs are different
    if np.sign(dv) != np.sign(da_raw):
        # Force same direction with plausible magnitude
        target_mag = max(abs(da_raw), 0.5 * abs(dv))
        da_coupled = np.sign(dv) * target_mag
    else:
        # Already same direction, keep as is
        da_coupled = da_raw

# Apply coupled acceleration
a1_coupled = a0 + da_coupled

# Create coupled metrics dict for display
intervention_metrics = {
    'velocity': v1,
    'acceleration': a1_coupled,
    'uncertainty': intervention_metrics_raw['uncertainty']
}

# Display metrics in three rows: Status Quo, Healthy, With Interventions
row1_col1, row1_col2, row1_col3 = st.columns(3)

# Row 1: Status Quo (No Intervention) metrics
with row1_col1:
    st.markdown(f"""
    <div class="metric-chip">
        <div class="metric-label">Velocity (Status Quo)</div>
        <div class="metric-value">{statusquo_metrics['velocity']:.3f}</div>
    </div>
    """, unsafe_allow_html=True)

with row1_col2:
    st.markdown(f"""
    <div class="metric-chip">
        <div class="metric-label">Acceleration (Status Quo)</div>
        <div class="metric-value">{statusquo_metrics['acceleration']:.4f}</div>
    </div>
    """, unsafe_allow_html=True)

with row1_col3:
    st.markdown(f"""
    <div class="metric-chip">
        <div class="metric-label">Uncertainty (Status Quo)</div>
        <div class="metric-value">{statusquo_metrics['uncertainty']:.3f}</div>
    </div>
    """, unsafe_allow_html=True)

# Row 2: Healthy Population metrics
row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
    st.markdown(f"""
    <div class="metric-chip" style="border-color: rgba(0, 200, 100, 0.3);">
        <div class="metric-label">Velocity (Healthy)</div>
        <div class="metric-value" style="background: linear-gradient(135deg, #00cc66 0%, #009944 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">{healthy_metrics['velocity']:.3f}</div>
    </div>
    """, unsafe_allow_html=True)

with row2_col2:
    st.markdown(f"""
    <div class="metric-chip" style="border-color: rgba(0, 200, 100, 0.3);">
        <div class="metric-label">Acceleration (Healthy)</div>
        <div class="metric-value" style="background: linear-gradient(135deg, #00cc66 0%, #009944 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">{healthy_metrics['acceleration']:.4f}</div>
    </div>
    """, unsafe_allow_html=True)

with row2_col3:
    st.markdown(f"""
    <div class="metric-chip" style="border-color: rgba(0, 200, 100, 0.3);">
        <div class="metric-label">Uncertainty (Healthy)</div>
        <div class="metric-value" style="background: linear-gradient(135deg, #00cc66 0%, #009944 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">{healthy_metrics['uncertainty']:.3f}</div>
    </div>
    """, unsafe_allow_html=True)

# Row 3: With Interventions metrics (with deltas vs Status Quo)
row3_col1, row3_col2, row3_col3 = st.columns(3)

with row3_col1:
    delta_v = intervention_metrics['velocity'] - statusquo_metrics['velocity']
    delta_class = "delta-good" if delta_v < 0 else "delta-bad"
    delta_symbol = "▼" if delta_v < 0 else "▲"
    
    st.markdown(f"""
    <div class="metric-chip">
        <div class="metric-label">Velocity (Interventions)</div>
        <div class="metric-value">{intervention_metrics['velocity']:.3f}</div>
        <div class="metric-delta {delta_class}">
            {delta_symbol} {abs(delta_v):.3f} vs Status Quo
        </div>
    </div>
    """, unsafe_allow_html=True)

with row3_col2:
    delta_a = intervention_metrics['acceleration'] - statusquo_metrics['acceleration']
    # Same-direction coupling: both should move together
    delta_class = "delta-good" if (delta_v < 0 and delta_a < 0) or (delta_v > 0 and delta_a > 0) else "delta-bad"
    delta_symbol = "▼" if delta_a < 0 else "▲"
    
    st.markdown(f"""
    <div class="metric-chip">
        <div class="metric-label">Acceleration (Interventions)</div>
        <div class="metric-value">{intervention_metrics['acceleration']:.4f}</div>
        <div class="metric-delta {delta_class}">
            {delta_symbol} {abs(delta_a):.4f} vs Status Quo
        </div>
    </div>
    """, unsafe_allow_html=True)

with row3_col3:
    delta_u = intervention_metrics['uncertainty'] - statusquo_metrics['uncertainty']
    delta_class = "delta-good" if delta_u < 0 else "delta-bad"
    delta_symbol = "▼" if delta_u < 0 else "▲"
    
    st.markdown(f"""
    <div class="metric-chip">
        <div class="metric-label">Uncertainty (Interventions)</div>
        <div class="metric-value">{intervention_metrics['uncertainty']:.3f}</div>
        <div class="metric-delta {delta_class}">
            {delta_symbol} {abs(delta_u):.3f} vs Status Quo
        </div>
    </div>
    """, unsafe_allow_html=True)

# Generate Report Section
st.markdown("---")
st.markdown("### 📋 Clinical Report Generator")
st.markdown("")

# Function to generate report using Claude
def generate_clinical_report(patient_data, metrics_data, interventions_data):
    """Generate clinical report using Claude AI"""
    
    # Check for API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return None, "⚠️ ANTHROPIC_API_KEY not found in environment variables. Please set your API key."
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        # Prepare context for Claude
        context = f"""You are a clinical advisor analyzing aging biomarker data for a physician. 

PATIENT CASE:
- Name: Jeff
- Organ: Liver
- First visit: 3 months ago
- Initial lifestyle: high alcohol consumption, high caffeine intake, no exercise
- Historical measurements: 3 weekly DNA methylation readings

CURRENT METRICS ANALYSIS:

Status Quo (No Intervention):
- Velocity: {metrics_data['statusquo']['velocity']:.3f} (aging speed on manifold)
- Acceleration: {metrics_data['statusquo']['acceleration']:.4f} (rate of change)
- Uncertainty: {metrics_data['statusquo']['uncertainty']:.3f}

Healthy Population Reference:
- Velocity: {metrics_data['healthy']['velocity']:.3f}
- Acceleration: {metrics_data['healthy']['acceleration']:.4f}
- Uncertainty: {metrics_data['healthy']['uncertainty']:.3f}

With Current Interventions:
- Velocity: {metrics_data['interventions']['velocity']:.3f} (Δ {metrics_data['delta_v']:+.3f})
- Acceleration: {metrics_data['interventions']['acceleration']:.4f} (Δ {metrics_data['delta_a']:+.4f})
- Uncertainty: {metrics_data['interventions']['uncertainty']:.3f} (Δ {metrics_data['delta_u']:+.3f})

INTERVENTION PROTOCOL APPLIED:
{interventions_data['summary']}

KEY OBSERVATIONS:
- Velocity change: {metrics_data['velocity_change_pct']:.1f}% {'decrease ✓' if metrics_data['delta_v'] < 0 else 'increase'}
- Acceleration change: {metrics_data['accel_change_pct']:.1f}% {'decrease ✓' if metrics_data['delta_a'] < 0 else 'increase'}
- Distance to healthy trajectory: reduced by ~{metrics_data['improvement_estimate']:.0f}%
- Trajectory analysis: {metrics_data['trajectory_status']}

TASK:
Generate a clear, actionable clinical report that the physician can share with Jeff. The report should:

1. START with a brief, encouraging summary of progress (2-3 sentences)
2. EXPLAIN which specific interventions are having the most impact and why
3. PROVIDE concrete, personalized recommendations for the next 3 months
4. HIGHLIGHT any concerns or areas needing attention
5. END with motivational guidance and realistic expectations

Write in a warm, professional tone. Use accessible language (avoid excessive jargon). Be specific about the interventions mentioned above. Focus on actionable insights.

Format the report with clear sections using markdown headers (##) and bullet points where appropriate."""

        # Call Claude with proper model names
        # These are the actual valid Anthropic API model identifiers
        models_to_try = [
            "claude-3-opus-20240229",      # Claude 3 Opus (most capable)
            "claude-3-sonnet-20240229",    # Claude 3 Sonnet (balanced)
            "claude-3-haiku-20240307",     # Claude 3 Haiku (fastest)
        ]
        
        message = None
        last_error = None
        
        for model_name in models_to_try:
            try:
                message = client.messages.create(
                    model=model_name,
                    max_tokens=2000,
                    temperature=0.7,
                    messages=[
                        {"role": "user", "content": context}
                    ]
                )
                # Success! Exit loop
                break
            except Exception as model_error:
                last_error = model_error
                # Try next model
                continue
        
        if message is None:
            # All models failed, return detailed error
            return None, f"Could not connect to any Claude model. Last error: {str(last_error)}"
        
        return message.content[0].text, None
        
    except Exception as e:
        return None, f"Error generating report: {str(e)}"

# Prepare data for report generation
if st.button("🔬 Generate Clinical Report", type="primary", use_container_width=True):
    # Hide placeholder immediately when button is clicked
    st.session_state.report_generated = True
    
    with st.spinner("Analyzing metrics and generating personalized report..."):
        
        # Prepare patient data
        patient_data = {
            'name': 'Jeff',
            'organ': 'Liver',
            'visit_date': '3 months ago',
            'risk_factors': ['high alcohol', 'high caffeine', 'no exercise']
        }
        
        # Prepare metrics data
        velocity_change_pct = (delta_v / statusquo_metrics['velocity']) * 100 if statusquo_metrics['velocity'] != 0 else 0
        accel_change_pct = (delta_a / statusquo_metrics['acceleration']) * 100 if statusquo_metrics['acceleration'] != 0 else 0
        
        # Estimate improvement based on velocity reduction
        improvement_estimate = abs(velocity_change_pct) * 0.6 if delta_v < 0 else 0
        
        # Trajectory status
        if delta_v < 0 and delta_a < 0:
            trajectory_status = "Both velocity and acceleration decreasing - excellent trajectory improvement"
        elif delta_v < 0:
            trajectory_status = "Velocity decreasing but acceleration stable - good progress"
        elif abs(delta_v) < 0.5:
            trajectory_status = "Minimal change - interventions may need adjustment"
        else:
            trajectory_status = "Velocity increasing - requires intervention review"
        
        metrics_data = {
            'statusquo': statusquo_metrics,
            'healthy': healthy_metrics,
            'interventions': intervention_metrics,
            'delta_v': delta_v,
            'delta_a': delta_a,
            'delta_u': intervention_metrics['uncertainty'] - statusquo_metrics['uncertainty'],
            'velocity_change_pct': velocity_change_pct,
            'accel_change_pct': accel_change_pct,
            'improvement_estimate': improvement_estimate,
            'trajectory_status': trajectory_status
        }
        
        # Prepare interventions summary
        active_interventions = []
        if sleep_change != 0:
            active_interventions.append(f"- Sleep adjustment: {sleep_change:+.1f} hours/night")
        if vo2max_change != 0:
            active_interventions.append(f"- VO₂max improvement: +{vo2max_change:.0f}% (cardiovascular exercise)")
        if alcohol_reduction != 0:
            active_interventions.append(f"- Alcohol reduction: {alcohol_reduction:.0f}%")
        if caffeine_reduction != 0:
            active_interventions.append(f"- Caffeine reduction: {caffeine_reduction:.0f} mg/day")
        # Note: NAC and Metformin removed from UI (values always 0)
        
        if not active_interventions:
            active_interventions.append("- No interventions currently applied")
        
        interventions_data = {
            'summary': '\n'.join(active_interventions),
            'count': len([i for i in active_interventions if not i.startswith("- No")])
        }
        
        # Generate report
        report, error = generate_clinical_report(patient_data, metrics_data, interventions_data)
        
        if error:
            st.error(error)
            st.info("""
            **To use this feature:**
            1. Get an API key from https://console.anthropic.com/
            2. Set the environment variable: `ANTHROPIC_API_KEY=your_key_here`
            3. Restart the Streamlit app
            """)
        else:
            # Display report in a nice format
            st.markdown("---")
            st.markdown("## 📄 Clinical Report - Jeff's Liver Aging Analysis")
            st.markdown("")
            
            # Report container with styling
            st.markdown(f"""
            <div style='background: linear-gradient(145deg, #1a1a1a 0%, #141414 100%); 
                        border: 1px solid rgba(0, 212, 255, 0.3); 
                        border-radius: 12px; 
                        padding: 30px; 
                        margin: 20px 0;
                        color: #e8e8e8;
                        line-height: 1.8;'>
            """, unsafe_allow_html=True)
            
            st.markdown(report)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Download button for report
            st.download_button(
                label="📥 Download Report as Text",
                data=f"ChronOS Clinical Report - Jeff's Liver Aging Analysis\n\n{report}\n\nGenerated by ChronOS | {st.session_state.get('report_timestamp', 'Today')}",
                file_name=f"chronos_report_jeff_liver.txt",
                mime="text/plain",
                use_container_width=True
            )

# Footer - minimal
st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #555; font-size: 0.8rem; padding: 20px;'>
    <p>🧬 ChronOS v3.0 | Powered by Claude AI</p>
    <p><em>Clinical decision support tool for demonstration</em></p>
</div>
""", unsafe_allow_html=True)

