"""
Methylome Manifold Trajectory Calculations
Product-grade 3D visualization using parametric torus surface
All trajectories constrained to surface with smooth interpolation
"""

import numpy as np
from scipy.interpolate import CubicSpline
from typing import Dict, Tuple, List
import hashlib


def torus_uv_to_xyz(u, v, R=3.0, r=1.15):
    """
    Parametric torus: maps (u, v) coordinates to 3D space
    
    Args:
        u: Angular coordinate around major circle [0, 2π)
        v: Angular coordinate around minor circle [0, 2π)
        R: Major radius (distance from center to tube center)
        r: Minor radius (tube thickness)
    
    Returns:
        Tuple of (x, y, z) coordinates
    """
    x = (R + r * np.cos(v)) * np.cos(u)
    y = (R + r * np.cos(v)) * np.sin(u)
    z = r * np.sin(v)
    
    return x, y, z


def build_torus_mesh(nu=160, nv=70, R=3.0, r=1.15):
    """
    Generate triangle mesh for torus surface
    
    Args:
        nu: Number of segments around major circle
        nv: Number of segments around minor circle
        R: Major radius
        r: Minor radius
    
    Returns:
        Dictionary with positions, normals, and triangle indices
    """
    u = np.linspace(0, 2 * np.pi, nu, endpoint=False)
    v = np.linspace(0, 2 * np.pi, nv, endpoint=False)
    
    positions = []
    normals = []
    
    for vi in v:
        for ui in u:
            # Position
            x, y, z = torus_uv_to_xyz(ui, vi, R, r)
            positions.append([x, y, z])
            
            # Normal vector (pointing outward from tube)
            nx = np.cos(vi) * np.cos(ui)
            ny = np.cos(vi) * np.sin(ui)
            nz = np.sin(vi)
            normals.append([nx, ny, nz])
    
    positions = np.array(positions, dtype=np.float32)
    normals = np.array(normals, dtype=np.float32)
    
    # Generate triangle indices
    indices = []
    for i in range(nv):
        for j in range(nu):
            # Current quad vertices
            v0 = i * nu + j
            v1 = i * nu + (j + 1) % nu
            v2 = ((i + 1) % nv) * nu + (j + 1) % nu
            v3 = ((i + 1) % nv) * nu + j
            
            # Two triangles per quad
            indices.extend([v0, v1, v2])
            indices.extend([v0, v2, v3])
    
    indices = np.array(indices, dtype=np.uint32)
    
    return {
        'positions': positions,
        'normals': normals,
        'indices': indices,
        'num_vertices': len(positions),
        'num_triangles': len(indices) // 3
    }


def baseline_points_on_surface(start_uv=(1.5, 0.8), weeks=3, seed=42):
    """
    Generate baseline measurement points (historical data)
    
    Args:
        start_uv: Starting (u, v) coordinates on torus
        weeks: Number of weekly measurements
        seed: Random seed for reproducibility
    
    Returns:
        Dictionary with u, v, x, y, z arrays
    """
    np.random.seed(seed)
    
    u_vals = [start_uv[0]]
    v_vals = [start_uv[1]]
    
    # Small random walk for historical measurements
    for i in range(weeks - 1):
        du = np.random.uniform(-0.12, 0.18)
        dv = np.random.uniform(-0.10, 0.12)
        u_vals.append((u_vals[-1] + du) % (2 * np.pi))
        v_vals.append((v_vals[-1] + dv) % (2 * np.pi))
    
    u_arr = np.array(u_vals)
    v_arr = np.array(v_vals)
    x, y, z = torus_uv_to_xyz(u_arr, v_arr)
    
    return {
        'u': u_arr,
        'v': v_arr,
        'x': x,
        'y': y,
        'z': z,
        'num_points': weeks
    }


def status_quo_path(start_uv=(1.5, 0.8), months=12, seed=43):
    """
    Generate status quo trajectory (no interventions)
    
    Args:
        start_uv: Starting (u, v) coordinates  
        months: Number of months to project
        seed: Random seed
    
    Returns:
        Dictionary with smooth path on surface
    """
    np.random.seed(seed)
    
    num_samples = 30 + 10 * months
    
    # Control points for path (coarser)
    num_control = max(5, months + 2)
    u_control = [start_uv[0]]
    v_control = [start_uv[1]]
    
    for i in range(num_control - 1):
        # Status quo shows gradual drift toward unhealthy region
        du = np.random.uniform(0.15, 0.30)
        dv = np.random.uniform(0.10, 0.25)
        u_control.append((u_control[-1] + du) % (2 * np.pi))
        v_control.append((v_control[-1] + dv) % (2 * np.pi))
    
    # Smooth interpolation using cubic spline
    t_control = np.linspace(0, 1, num_control)
    t_fine = np.linspace(0, 1, num_samples)
    
    cs_u = CubicSpline(t_control, u_control, bc_type='natural')
    cs_v = CubicSpline(t_control, v_control, bc_type='natural')
    
    u_arr = cs_u(t_fine) % (2 * np.pi)
    v_arr = cs_v(t_fine) % (2 * np.pi)
    
    x, y, z = torus_uv_to_xyz(u_arr, v_arr)
    
    return {
        'u': u_arr,
        'v': v_arr,
        'x': x,
        'y': y,
        'z': z,
        'num_points': num_samples
    }


def intervention_path(start_uv=(1.5, 0.8), months=12, sliders=None, base_seed=44):
    """
    Generate intervention trajectory with controls affecting path
    
    Args:
        start_uv: Starting (u, v) coordinates
        months: Number of months to project
        sliders: Dictionary of intervention values
        base_seed: Base random seed (modified by sliders)
    
    Returns:
        Dictionary with smooth path on surface
    """
    if sliders is None:
        sliders = {
            'sleep_change': 0,
            'vo2max_change': 0,
            'alcohol_reduction': 0,
            'caffeine_reduction': 0,
            'nac_dose': 0,
            'metformin_dose': 0
        }
    
    # Create seed from slider values for reproducible randomness
    slider_str = f"{sliders['sleep_change']:.1f}_{sliders['vo2max_change']:.1f}_" + \
                 f"{sliders['alcohol_reduction']:.1f}_{sliders['caffeine_reduction']:.1f}_" #+ \
                 #f"{sliders['nac_dose']}_{sliders['metformin_dose']}"
    slider_hash = int(hashlib.md5(slider_str.encode()).hexdigest()[:8], 16)
    seed = (base_seed + slider_hash) % (2**32)
    np.random.seed(seed)
    
    num_samples = 30 + 10 * months
    
    # Control points for path
    num_control = max(5, months + 2)
    u_control = [start_uv[0]]
    v_control = [start_uv[1]]
    
    # Calculate intervention effects on step length and curvature
    # More positive interventions = smaller steps (calmer path)
    intervention_score = (
        sliders['sleep_change'] * 0.08 +
        sliders['vo2max_change'] * 0.006 +
        sliders['alcohol_reduction'] * 0.004 +
        sliders['caffeine_reduction'] * 0.0003 +
        sliders.get('nac_dose', 0) * 0.0002 +
        sliders.get('metformin_dose', 0) * 0.0002
    )
    
    # Step length decreases with more interventions
    base_step_u = 0.22
    base_step_v = 0.18
    step_factor = np.clip(1.0 - intervention_score * 0.6, 0.3, 1.0)
    
    # Curvature slightly increases with caffeine/drugs
    curvature_factor = 1.0 + (sliders['caffeine_reduction'] / 400.0) * 0.3 #+ \
                       #(sliders['nac_dose'] + sliders['metformin_dose']) / 4000.0 * 0.2
    
    for i in range(num_control - 1):
        du = np.random.uniform(0.05, base_step_u) * step_factor
        dv = np.random.uniform(0.03, base_step_v) * step_factor
        
        # Add slight curvature
        angle = np.random.uniform(0, 2 * np.pi) * curvature_factor
        du_rot = du * np.cos(angle) - dv * np.sin(angle)
        dv_rot = du * np.sin(angle) + dv * np.cos(angle)
        
        u_control.append((u_control[-1] + du_rot) % (2 * np.pi))
        v_control.append((v_control[-1] + dv_rot) % (2 * np.pi))
    
    # Smooth interpolation
    t_control = np.linspace(0, 1, num_control)
    t_fine = np.linspace(0, 1, num_samples)
    
    cs_u = CubicSpline(t_control, u_control, bc_type='natural')
    cs_v = CubicSpline(t_control, v_control, bc_type='natural')
    
    u_arr = cs_u(t_fine) % (2 * np.pi)
    v_arr = cs_v(t_fine) % (2 * np.pi)
    
    x, y, z = torus_uv_to_xyz(u_arr, v_arr)
    
    return {
        'u': u_arr,
        'v': v_arr,
        'x': x,
        'y': y,
        'z': z,
        'num_points': num_samples,
        'step_factor': step_factor,
        'curvature_factor': curvature_factor
    }


def healthy_population_path(start_uv=(0.0, 0.0), months=12, seed=100):
    """
    Generate healthy population average trajectory
    
    Args:
        start_uv: Starting (u, v) coordinates (healthy region)
        months: Number of months to project
        seed: Random seed for reproducibility
    
    Returns:
        Dictionary with smooth path on surface
    """
    np.random.seed(seed)
    
    num_samples = 30 + 10 * months
    
    # Control points for path (healthy trajectory is slow and stable)
    num_control = max(5, months + 2)
    u_control = [start_uv[0]]
    v_control = [start_uv[1]]
    
    for i in range(num_control - 1):
        # Healthy population shows very slow, stable progression
        du = np.random.uniform(0.08, 0.15)
        dv = np.random.uniform(0.05, 0.12)
        u_control.append((u_control[-1] + du) % (2 * np.pi))
        v_control.append((v_control[-1] + dv) % (2 * np.pi))
    
    # Smooth interpolation using cubic spline
    t_control = np.linspace(0, 1, num_control)
    t_fine = np.linspace(0, 1, num_samples)
    
    cs_u = CubicSpline(t_control, u_control, bc_type='natural')
    cs_v = CubicSpline(t_control, v_control, bc_type='natural')
    
    u_arr = cs_u(t_fine) % (2 * np.pi)
    v_arr = cs_v(t_fine) % (2 * np.pi)
    
    x, y, z = torus_uv_to_xyz(u_arr, v_arr)
    
    return {
        'u': u_arr,
        'v': v_arr,
        'x': x,
        'y': y,
        'z': z,
        'num_points': num_samples
    }


def healthy_population_band(healthy_path, band_width=0.15):
    """
    Generate error band around healthy population trajectory
    
    Args:
        healthy_path: Dictionary with healthy path data
        band_width: Width of band in UV space
    
    Returns:
        Dictionary with upper and lower band paths
    """
    u_arr = healthy_path['u']
    v_arr = healthy_path['v']
    
    # Create upper and lower bounds by offsetting in v direction
    u_upper = u_arr
    v_upper = (v_arr + band_width) % (2 * np.pi)
    
    u_lower = u_arr
    v_lower = (v_arr - band_width) % (2 * np.pi)
    
    # Map to XYZ
    x_upper, y_upper, z_upper = torus_uv_to_xyz(u_upper, v_upper)
    x_lower, y_lower, z_lower = torus_uv_to_xyz(u_lower, v_lower)
    
    return {
        'upper': {'x': x_upper, 'y': y_upper, 'z': z_upper},
        'lower': {'x': x_lower, 'y': y_lower, 'z': z_lower}
    }


def blend_toward_healthy(intervention_path, healthy_path, alpha=0.35):
    """
    Blend intervention path toward healthy population path
    
    Args:
        intervention_path: Dictionary with intervention UV coordinates
        healthy_path: Dictionary with healthy UV coordinates
        alpha: Blending factor (0=no blend, 1=fully healthy)
    
    Returns:
        Dictionary with blended path
    """
    u_interv = intervention_path['u']
    v_interv = intervention_path['v']
    
    u_healthy = healthy_path['u']
    v_healthy = healthy_path['v']
    
    # Match lengths by interpolation if needed
    if len(u_interv) != len(u_healthy):
        from scipy.interpolate import interp1d
        t_healthy = np.linspace(0, 1, len(u_healthy))
        t_interv = np.linspace(0, 1, len(u_interv))
        
        interp_u_h = interp1d(t_healthy, u_healthy, kind='cubic', fill_value='extrapolate')
        interp_v_h = interp1d(t_healthy, v_healthy, kind='cubic', fill_value='extrapolate')
        
        u_healthy_matched = interp_u_h(t_interv)
        v_healthy_matched = interp_v_h(t_interv)
    else:
        u_healthy_matched = u_healthy
        v_healthy_matched = v_healthy
    
    # Blend in UV space
    u_blended = (1 - alpha) * u_interv + alpha * u_healthy_matched
    v_blended = (1 - alpha) * v_interv + alpha * v_healthy_matched
    
    # Wrap to [0, 2π)
    u_blended = u_blended % (2 * np.pi)
    v_blended = v_blended % (2 * np.pi)
    
    # Map to XYZ
    x_blended, y_blended, z_blended = torus_uv_to_xyz(u_blended, v_blended)
    
    return {
        'u': u_blended,
        'v': v_blended,
        'x': x_blended,
        'y': y_blended,
        'z': z_blended,
        'num_points': len(u_blended),
        'alpha': alpha
    }


def hud_metrics_from_xyz(x, y, z):
    """
    Calculate fake HUD metrics from 3D path
    
    Args:
        x, y, z: Arrays of coordinates along path
    
    Returns:
        Dictionary with velocity, acceleration, uncertainty
    """
    # Velocity: mean segment length
    if len(x) > 1:
        dx = np.diff(x)
        dy = np.diff(y)
        dz = np.diff(z)
        segment_lengths = np.sqrt(dx**2 + dy**2 + dz**2)
        velocity = np.mean(segment_lengths) * 100  # Scale for display
    else:
        velocity = 0.1
    
    # Acceleration: curvature proxy (change in direction)
    if len(x) > 2:
        # Second derivative magnitude
        ddx = np.diff(dx)
        ddy = np.diff(dy)
        ddz = np.diff(dz)
        curvatures = np.sqrt(ddx**2 + ddy**2 + ddz**2)
        acceleration = np.mean(curvatures) * 1000  # Scale for display
    else:
        acceleration = 0.01
    
    # Uncertainty: small random walk magnitude
    if len(x) > 3:
        # Local deviation from smoothed path
        from scipy.ndimage import gaussian_filter1d
        x_smooth = gaussian_filter1d(x, sigma=3)
        y_smooth = gaussian_filter1d(y, sigma=3)
        z_smooth = gaussian_filter1d(z, sigma=3)
        
        deviations = np.sqrt((x - x_smooth)**2 + (y - y_smooth)**2 + (z - z_smooth)**2)
        uncertainty = np.mean(deviations) * 50 + np.random.uniform(0.05, 0.15)
    else:
        uncertainty = 0.1
    
    return {
        'velocity': float(velocity),
        'acceleration': float(acceleration),
        'uncertainty': float(uncertainty)
    }


# Legacy compatibility functions (deprecated but kept for backwards compatibility)
def generate_patient_trajectory(
    weeks_historical: int = 3,
    months_future: int = 12,
    patient_type: str = 'high_risk'
) -> Dict:
    """
    Generate patient trajectory on methylome manifold
    Trajectory is constrained to lie on the manifold surface
    
    Args:
        weeks_historical: Number of weeks of historical data
        months_future: Number of months to project into future
        patient_type: 'healthy', 'moderate_risk', 'high_risk'
    
    Returns:
        Dictionary with trajectory data including position, velocity, acceleration
    """
    
    # Time points: negative for historical, 0 for current, positive for future
    # Historical: weekly measurements
    t_hist = np.linspace(-weeks_historical, 0, weeks_historical)
    
    # Future: monthly predictions
    t_future = np.linspace(0, months_future, months_future * 4)  # Weekly resolution
    
    # Combine time arrays
    t_all = np.concatenate([t_hist, t_future[1:]])  # Avoid duplicating t=0
    
    # Generate trajectory in manifold coordinates (u, v)
    # u ~ epigenetic age progression
    # v ~ tissue state / damage accumulation
    
    if patient_type == 'high_risk':
        # Start at unhealthy region of manifold
        u0, v0 = 1.5, 2.0
        # Velocities in manifold coordinates (rapid aging)
        vu, vv = 0.30, 0.25
        # Acceleration (accelerating aging)
        au, av = 0.012, 0.010
        noise_scale = 0.12
    elif patient_type == 'moderate_risk':
        u0, v0 = 0.5, 0.8
        vu, vv = 0.15, 0.12
        au, av = 0.005, 0.004
        noise_scale = 0.08
    else:  # healthy
        u0, v0 = -0.5, 0.0
        vu, vv = 0.08, 0.05
        au, av = 0.001, 0.001
        noise_scale = 0.05
    
    # Calculate trajectory in manifold coordinates using kinematic equations
    u = u0 + vu * t_all + 0.5 * au * t_all**2
    v = v0 + vv * t_all + 0.5 * av * t_all**2
    
    # Add measurement noise to historical data
    hist_len = len(t_hist)
    u[:hist_len] += np.random.normal(0, noise_scale * 0.5, hist_len)
    v[:hist_len] += np.random.normal(0, noise_scale * 0.5, hist_len)
    
    # Add slight stochastic variation to future trajectory
    future_len = len(t_all) - hist_len
    u[hist_len:] += np.random.normal(0, noise_scale * 0.3, future_len) * np.linspace(0, 1, future_len)
    v[hist_len:] += np.random.normal(0, noise_scale * 0.3, future_len) * np.linspace(0, 1, future_len)
    
    # Project trajectory onto the 3D manifold surface
    x, y, z = manifold_surface(u, v)
    
    # Calculate uncertainty (grows with time into future)
    uncertainty = np.zeros_like(t_all)
    future_mask = t_all >= 0
    uncertainty[future_mask] = 0.1 + 0.05 * t_all[future_mask]
    uncertainty[~future_mask] = 0.05  # Historical uncertainty (measurement error)
    
    return {
        'x': x,
        'y': y,
        'z': z,
        'u': u,  # Store manifold coordinates
        'v': v,
        'time': t_all,
        'uncertainty': uncertainty,
        'velocity_u': vu,
        'velocity_v': vv,
        'acceleration_u': au,
        'acceleration_v': av
    }


def generate_healthy_trajectory(months_future: int = 12) -> Dict:
    """
    Generate reference trajectory for healthy population
    Trajectory lies on the manifold surface
    
    Args:
        months_future: Number of months to project
    
    Returns:
        Dictionary with healthy reference trajectory
    """
    
    # Time points (only future, as reference)
    t = np.linspace(0, months_future, months_future * 4)
    
    # Healthy trajectory: slow, steady aging in manifold coordinates
    # Stays in healthy region (valley) of manifold
    u0, v0 = -1.0, -0.5
    vu, vv = 0.10, 0.06  # Slow aging velocity
    au, av = 0.001, 0.001  # Minimal acceleration
    
    # Calculate trajectory in manifold coordinates
    u = u0 + vu * t + 0.5 * au * t**2
    v = v0 + vv * t + 0.5 * av * t**2
    
    # Add slight natural variation
    u += np.random.normal(0, 0.02, len(t)) * np.linspace(0, 0.5, len(t))
    v += np.random.normal(0, 0.02, len(t)) * np.linspace(0, 0.5, len(t))
    
    # Project onto manifold
    x, y, z = manifold_surface(u, v)
    
    return {
        'x': x,
        'y': y,
        'z': z,
        'u': u,
        'v': v,
        'time': t,
        'uncertainty': 0.1 + 0.02 * t
    }


def calculate_modified_trajectory(
    baseline: Dict,
    interventions: Dict,
    time_horizon: int = 12
) -> Dict:
    """
    Calculate modified trajectory based on interventions
    Trajectory remains constrained to the manifold surface
    
    Args:
        baseline: Baseline trajectory dictionary
        interventions: Dictionary of intervention parameters
        time_horizon: Months to project
    
    Returns:
        Modified trajectory dictionary
    """
    
    # Extract baseline parameters in manifold coordinates
    current_idx = np.where(baseline['time'] == 0)[0][0]
    u0 = baseline['u'][current_idx]
    v0 = baseline['v'][current_idx]
    
    vu_base = baseline['velocity_u']
    vv_base = baseline['velocity_v']
    
    au_base = baseline['acceleration_u']
    av_base = baseline['acceleration_v']
    
    # Calculate intervention effects on velocity and acceleration in manifold coordinates
    # u ~ epigenetic age progression
    # v ~ tissue state / damage accumulation
    
    # Sleep affects both directions (general health improvement)
    sleep_factor = 1.0 - (interventions['sleep_change'] * 0.06)
    
    # VO2max primarily affects epigenetic age progression (u)
    vo2_factor_u = 1.0 - (interventions['vo2max_change'] * 0.010)
    vo2_factor_v = 1.0 - (interventions['vo2max_change'] * 0.006)
    
    # Alcohol reduction strongly affects tissue damage (v) and age progression (u)
    alcohol_factor_u = 1.0 - (interventions['alcohol_reduction'] / 100.0 * 0.30)
    alcohol_factor_v = 1.0 - (interventions['alcohol_reduction'] / 100.0 * 0.45)
    
    # Caffeine affects both dimensions moderately
    caffeine_factor_u = 1.0 - (interventions['caffeine_reduction'] / 400.0 * 0.12)
    caffeine_factor_v = 1.0 - (interventions['caffeine_reduction'] / 400.0 * 0.10)
    
    # NAC (antioxidant) primarily affects tissue damage state (v)
    #nac_factor_u = 1.0 - (interventions['nac_dose'] / 2000.0 * 0.15)
    #nac_factor_v = 1.0 - (interventions['nac_dose'] / 2000.0 * 0.35)
    
    # Metformin affects epigenetic age (u) and tissue state (v)
    metformin_factor_u = 1.0 - (interventions['metformin_dose'] / 2000.0 * 0.38)
    metformin_factor_v = 1.0 - (interventions['metformin_dose'] / 2000.0 * 0.22)
    
    # Combine factors for each manifold direction
    total_factor_u = (sleep_factor * vo2_factor_u * alcohol_factor_u * 
                     caffeine_factor_u)# * nac_factor_u * metformin_factor_u)
    total_factor_v = (sleep_factor * vo2_factor_v * alcohol_factor_v * 
                     caffeine_factor_v)# * nac_factor_v * metformin_factor_v)
    
    # Ensure factors don't go below 0.2 (can't reverse aging completely)
    total_factor_u = max(0.2, total_factor_u)
    total_factor_v = max(0.2, total_factor_v)
    
    # Apply factors to velocity and acceleration in manifold coordinates
    vu_mod = vu_base * total_factor_u
    vv_mod = vv_base * total_factor_v
    
    au_mod = au_base * (total_factor_u ** 1.5)  # Acceleration responds more strongly
    av_mod = av_base * (total_factor_v ** 1.5)
    
    # Generate modified trajectory in manifold coordinates
    t_future = baseline['time'][baseline['time'] >= 0]
    
    u_mod = u0 + vu_mod * t_future + 0.5 * au_mod * t_future**2
    v_mod = v0 + vv_mod * t_future + 0.5 * av_mod * t_future**2
    
    # Add slight stochastic variation
    noise_scale = 0.10
    u_mod += np.random.normal(0, noise_scale * 0.3, len(t_future)) * np.linspace(0, 0.8, len(t_future))
    v_mod += np.random.normal(0, noise_scale * 0.3, len(t_future)) * np.linspace(0, 0.8, len(t_future))
    
    # Project onto manifold surface
    x_mod, y_mod, z_mod = manifold_surface(u_mod, v_mod)
    
    # Reduced uncertainty with interventions (more predictable)
    uncertainty = 0.08 + 0.03 * t_future
    
    return {
        'x': x_mod,
        'y': y_mod,
        'z': z_mod,
        'u': u_mod,
        'v': v_mod,
        'time': t_future,
        'uncertainty': uncertainty,
        'velocity_u': vu_mod,
        'velocity_v': vv_mod,
        'acceleration_u': au_mod,
        'acceleration_v': av_mod
    }


def calculate_aging_metrics(trajectory: Dict) -> Dict:
    """
    Calculate key aging dynamics metrics from trajectory on manifold
    
    Args:
        trajectory: Trajectory dictionary
    
    Returns:
        Dictionary of metrics
    """
    
    # Get velocity components in manifold coordinates
    if 'velocity_u' in trajectory:
        vu = trajectory['velocity_u']
        vv = trajectory['velocity_v']
        au = trajectory['acceleration_u']
        av = trajectory['acceleration_v']
    else:
        # Calculate from trajectory if not provided
        if 'u' in trajectory and 'v' in trajectory:
            u, v = trajectory['u'], trajectory['v']
            t = trajectory['time']
            
            # Numerical derivatives
            if len(t) > 1:
                dt = t[1] - t[0] if t[1] != t[0] else 1.0
                vu = np.gradient(u, dt)[-1]
                vv = np.gradient(v, dt)[-1]
                
                au = np.gradient(np.gradient(u, dt), dt)[-1]
                av = np.gradient(np.gradient(v, dt), dt)[-1]
            else:
                vu = vv = 0
                au = av = 0
        else:
            vu = vv = 0.1
            au = av = 0.01
    
    # Total velocity magnitude in manifold coordinates (aging speed)
    velocity = np.sqrt(vu**2 + vv**2)
    
    # Total acceleration magnitude
    acceleration = np.sqrt(au**2 + av**2)
    
    # Uncertainty at time horizon
    uncertainty = trajectory['uncertainty'][-1] if len(trajectory['uncertainty']) > 0 else 0.1
    
    return {
        'velocity': velocity,
        'acceleration': acceleration,
        'uncertainty': uncertainty,
        'velocity_components': (vu, vv),
        'acceleration_components': (au, av)
    }


def calculate_geodesic_distance(point1: Tuple[float, float, float], 
                                point2: Tuple[float, float, float]) -> float:
    """
    Calculate geodesic distance on methylome manifold
    (Simplified as Euclidean for this mockup)
    
    Args:
        point1: (x, y, z) coordinates
        point2: (x, y, z) coordinates
    
    Returns:
        Distance on manifold
    """
    return np.sqrt(sum((p1 - p2)**2 for p1, p2 in zip(point1, point2)))


def estimate_biological_age_delta(trajectory: Dict, healthy_ref: Dict) -> float:
    """
    Estimate biological age difference from healthy reference
    
    Args:
        trajectory: Patient trajectory
        healthy_ref: Healthy reference trajectory
    
    Returns:
        Estimated years of biological age difference
    """
    
    # Get current positions
    current_idx = np.argmin(np.abs(trajectory['time']))
    patient_pos = (trajectory['x'][current_idx], 
                  trajectory['y'][current_idx], 
                  trajectory['z'][current_idx])
    
    # Find closest point on healthy trajectory
    distances = [calculate_geodesic_distance(patient_pos, 
                                             (healthy_ref['x'][i], 
                                              healthy_ref['y'][i], 
                                              healthy_ref['z'][i]))
                for i in range(len(healthy_ref['x']))]
    
    min_dist = min(distances)
    
    # Convert distance to years (calibration factor)
    # In this model, 1 unit of distance ≈ 5 years of biological age
    biological_age_delta = min_dist * 5.0
    
    return biological_age_delta

