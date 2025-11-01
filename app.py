"""
Biological Relativity: Methylome Manifold Aging Trajectory Visualization
A tool for practitioners to visualize organ aging trajectories and treatment effects
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd

from methylome_trajectory import (
    generate_patient_trajectory,
    generate_healthy_trajectory,
    calculate_modified_trajectory,
    calculate_aging_metrics
)

# Page configuration
st.set_page_config(
    page_title="Biological Relativity - Methylome Manifold",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .warning-text {
        color: #ff4b4b;
        font-weight: bold;
    }
    .success-text {
        color: #00cc00;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.baseline_trajectory = None
    st.session_state.healthy_trajectory = None

# Header
st.markdown('<div class="main-header">🧬 Biological Relativity: Methylome Manifold</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Visualize Organ Aging Trajectories & Treatment Effects</div>', unsafe_allow_html=True)

# Patient case information
with st.expander("📋 Patient Case Summary", expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**Patient ID:** LVR-2024-047")
        st.write("**Organ:** Liver")
        st.write("**Age:** 42 years")
    with col2:
        st.write("**First Visit:** 3 months ago")
        st.write("**Measurements:** 3 weeks (weekly)")
        st.write("**Status:** Active Treatment")
    with col3:
        st.write("**Risk Factors:**")
        st.write("- Alcohol consumption")
        st.write("- Caffeine addiction")
        st.write("- Sedentary lifestyle")

# Main layout: Split screen
left_col, right_col = st.columns([2, 1])

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
    
    st.markdown("---")
    st.markdown("#### Lifestyle Modifications")
    
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
    
    st.markdown("---")
    st.markdown("#### Pharmacological Interventions")
    
    # NAC supplementation
    nac_dose = st.slider(
        "N-Acetylcysteine (mg/day)",
        min_value=0,
        max_value=2000,
        value=0,
        step=200,
        help="Antioxidant support for liver health"
    )
    
    # Metformin
    metformin_dose = st.slider(
        "Metformin (mg/day)",
        min_value=0,
        max_value=2000,
        value=0,
        step=500,
        help="Metabolic intervention"
    )
    
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

# LEFT PANEL: 3D Visualization
with left_col:
    st.markdown("### 📊 3D Methylome Manifold Trajectory")
    
    # Generate trajectories
    with st.spinner("Calculating trajectories on methylome manifold..."):
        # Patient baseline trajectory (no interventions)
        patient_baseline = generate_patient_trajectory(
            weeks_historical=3,
            months_future=time_horizon,
            patient_type='high_risk'
        )
        
        # Healthy population reference
        healthy_ref = generate_healthy_trajectory(
            months_future=time_horizon
        )
        
        # Modified trajectory with interventions
        patient_modified = calculate_modified_trajectory(
            baseline=patient_baseline,
            interventions=interventions,
            time_horizon=time_horizon
        )
    
    # Create 3D plot
    fig = go.Figure()
    
    # Healthy population reference trajectory (green, transparent)
    fig.add_trace(go.Scatter3d(
        x=healthy_ref['x'],
        y=healthy_ref['y'],
        z=healthy_ref['z'],
        mode='lines',
        name='Healthy Population',
        line=dict(color='green', width=6, dash='dash'),
        opacity=0.5
    ))
    
    # Historical measurements (patient - first 3 weeks)
    hist_mask = patient_baseline['time'] <= 0
    fig.add_trace(go.Scatter3d(
        x=patient_baseline['x'][hist_mask],
        y=patient_baseline['y'][hist_mask],
        z=patient_baseline['z'][hist_mask],
        mode='markers+lines',
        name='Historical Data (3 weeks)',
        marker=dict(size=8, color='blue', symbol='diamond'),
        line=dict(color='blue', width=4)
    ))
    
    # Baseline prediction (no intervention) - red
    future_mask = patient_baseline['time'] >= 0
    fig.add_trace(go.Scatter3d(
        x=patient_baseline['x'][future_mask],
        y=patient_baseline['y'][future_mask],
        z=patient_baseline['z'][future_mask],
        mode='lines',
        name='Baseline (No Change)',
        line=dict(color='red', width=6),
        opacity=0.7
    ))
    
    # Modified trajectory with interventions (if any)
    if any_intervention:
        future_mask_mod = patient_modified['time'] >= 0
        fig.add_trace(go.Scatter3d(
            x=patient_modified['x'][future_mask_mod],
            y=patient_modified['y'][future_mask_mod],
            z=patient_modified['z'][future_mask_mod],
            mode='lines',
            name='With Interventions',
            line=dict(color='orange', width=8),
            opacity=1.0
        ))
        
        # Current position marker
        fig.add_trace(go.Scatter3d(
            x=[patient_modified['x'][future_mask_mod][0]],
            y=[patient_modified['y'][future_mask_mod][0]],
            z=[patient_modified['z'][future_mask_mod][0]],
            mode='markers',
            name='Current Position',
            marker=dict(size=12, color='yellow', symbol='circle',
                       line=dict(color='black', width=2))
        ))
    
    # Uncertainty cone for baseline
    if not any_intervention:
        uncertainty_indices = [len(patient_baseline['x']) // 2, -1]
        for idx in uncertainty_indices:
            center = [patient_baseline['x'][idx], 
                     patient_baseline['y'][idx], 
                     patient_baseline['z'][idx]]
            uncertainty = patient_baseline['uncertainty'][idx]
            
            # Create uncertainty sphere
            u = np.linspace(0, 2 * np.pi, 20)
            v = np.linspace(0, np.pi, 20)
            x_sphere = center[0] + uncertainty * np.outer(np.cos(u), np.sin(v))
            y_sphere = center[1] + uncertainty * np.outer(np.sin(u), np.sin(v))
            z_sphere = center[2] + uncertainty * np.outer(np.ones(np.size(u)), np.cos(v))
            
            fig.add_trace(go.Surface(
                x=x_sphere, y=y_sphere, z=z_sphere,
                opacity=0.1,
                showscale=False,
                colorscale=[[0, 'red'], [1, 'red']],
                name=f'Uncertainty (t+{idx})',
                showlegend=False
            ))
    
    # Layout configuration
    fig.update_layout(
        scene=dict(
            xaxis_title='Methylation PC1 (Metabolic)',
            yaxis_title='Methylation PC2 (Inflammation)',
            zaxis_title='Methylation PC3 (Oxidative)',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.3)
            ),
            bgcolor='rgba(240, 240, 240, 0.9)'
        ),
        height=600,
        margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.8)"
        ),
        title=dict(
            text=f"Liver Aging Trajectory ({time_horizon} months projection)",
            x=0.5,
            xanchor='center'
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Bottom metrics panel
st.markdown("---")
st.markdown("### 📈 Aging Dynamics Metrics")

metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)

# Calculate metrics
baseline_metrics = calculate_aging_metrics(patient_baseline)
modified_metrics = calculate_aging_metrics(patient_modified) if any_intervention else baseline_metrics
healthy_metrics = calculate_aging_metrics(healthy_ref)

with metrics_col1:
    st.metric(
        label="Current Aging Velocity",
        value=f"{baseline_metrics['velocity']:.3f}",
        delta=f"{modified_metrics['velocity'] - baseline_metrics['velocity']:.3f}" if any_intervention else None,
        delta_color="inverse"
    )
    st.caption("units/month on manifold")

with metrics_col2:
    st.metric(
        label="Aging Acceleration",
        value=f"{baseline_metrics['acceleration']:.3f}",
        delta=f"{modified_metrics['acceleration'] - baseline_metrics['acceleration']:.3f}" if any_intervention else None,
        delta_color="inverse"
    )
    st.caption("units/month² on manifold")

with metrics_col3:
    deviation = abs(baseline_metrics['velocity'] - healthy_metrics['velocity']) / healthy_metrics['velocity'] * 100
    deviation_modified = abs(modified_metrics['velocity'] - healthy_metrics['velocity']) / healthy_metrics['velocity'] * 100
    st.metric(
        label="Deviation from Healthy",
        value=f"{deviation:.1f}%",
        delta=f"{deviation_modified - deviation:.1f}%" if any_intervention else None,
        delta_color="inverse"
    )
    st.caption("vs. population average")

with metrics_col4:
    if any_intervention:
        time_dilation = (modified_metrics['velocity'] / baseline_metrics['velocity']) * 100
        st.metric(
            label="Biological Time Dilation",
            value=f"{time_dilation:.1f}%",
            delta=f"{time_dilation - 100:.1f}%",
            delta_color="inverse"
        )
        st.caption("with interventions")
    else:
        st.metric(
            label="Trajectory Uncertainty",
            value=f"{baseline_metrics['uncertainty']:.2f}",
            delta=None
        )
        st.caption("σ at time horizon")

# Recommendations panel
if any_intervention:
    st.markdown("---")
    st.markdown("### 💡 Intervention Impact Analysis")
    
    # Calculate individual intervention effects
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Estimated Time to Healthy Trajectory")
        
        improvement_rate = baseline_metrics['velocity'] - modified_metrics['velocity']
        if improvement_rate > 0:
            time_to_healthy = (baseline_metrics['velocity'] - healthy_metrics['velocity']) / improvement_rate
            st.success(f"**~{time_to_healthy:.1f} months** with current interventions")
        else:
            st.warning("Current interventions show minimal effect. Consider adjusting.")
    
    with col2:
        st.markdown("#### 🔬 Key Contributing Factors")
        
        # Rank interventions by impact (simplified model)
        impacts = []
        if alcohol_reduction > 0:
            impacts.append(("Alcohol reduction", alcohol_reduction * 0.015))
        if vo2max_change > 0:
            impacts.append(("VO₂max improvement", vo2max_change * 0.012))
        if sleep_change > 0:
            impacts.append(("Sleep increase", sleep_change * 0.008))
        if caffeine_reduction > 0:
            impacts.append(("Caffeine reduction", caffeine_reduction * 0.0002))
        if nac_dose > 0:
            impacts.append(("NAC supplementation", nac_dose * 0.0003))
        if metformin_dose > 0:
            impacts.append(("Metformin", metformin_dose * 0.0004))
        
        impacts.sort(key=lambda x: x[1], reverse=True)
        
        for i, (factor, impact) in enumerate(impacts[:3], 1):
            st.write(f"{i}. **{factor}**: {impact:.3f} velocity reduction")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>🧬 Biological Relativity Framework v1.0 | Methylome Manifold Analysis</p>
    <p><em>This is a research tool for visualization purposes. Always consult with medical professionals for treatment decisions.</em></p>
</div>
""", unsafe_allow_html=True)

