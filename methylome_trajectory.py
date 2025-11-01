"""
Methylome Manifold Trajectory Calculations
Simulates aging trajectories on a 3D methylation manifold using concepts from general relativity
"""

import numpy as np
from scipy.interpolate import interp1d
from typing import Dict, Tuple


def generate_patient_trajectory(
    weeks_historical: int = 3,
    months_future: int = 12,
    patient_type: str = 'high_risk'
) -> Dict:
    """
    Generate patient trajectory on methylome manifold
    
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
    
    # Initial position on manifold (current state)
    # For high-risk liver patient: elevated metabolic stress, inflammation, oxidative damage
    if patient_type == 'high_risk':
        x0, y0, z0 = 2.5, 3.2, 2.8  # Starting position (unhealthy)
        # Velocity components (rapid aging)
        vx, vy, vz = 0.35, 0.42, 0.38
        # Acceleration (accelerating aging)
        ax, ay, az = 0.015, 0.018, 0.016
        noise_scale = 0.15
    elif patient_type == 'moderate_risk':
        x0, y0, z0 = 1.2, 1.5, 1.3
        vx, vy, vz = 0.15, 0.18, 0.16
        ax, ay, az = 0.005, 0.006, 0.005
        noise_scale = 0.10
    else:  # healthy
        x0, y0, z0 = 0.0, 0.0, 0.0
        vx, vy, vz = 0.05, 0.06, 0.05
        ax, ay, az = 0.001, 0.001, 0.001
        noise_scale = 0.05
    
    # Calculate trajectory using kinematic equations
    # Position: x(t) = x0 + v*t + 0.5*a*t²
    x = x0 + vx * t_all + 0.5 * ax * t_all**2
    y = y0 + vy * t_all + 0.5 * ay * t_all**2
    z = z0 + vz * t_all + 0.5 * az * t_all**2
    
    # Add measurement noise to historical data
    hist_len = len(t_hist)
    x[:hist_len] += np.random.normal(0, noise_scale * 0.5, hist_len)
    y[:hist_len] += np.random.normal(0, noise_scale * 0.5, hist_len)
    z[:hist_len] += np.random.normal(0, noise_scale * 0.5, hist_len)
    
    # Add slight stochastic variation to future trajectory
    future_len = len(t_all) - hist_len
    x[hist_len:] += np.random.normal(0, noise_scale * 0.3, future_len) * np.linspace(0, 1, future_len)
    y[hist_len:] += np.random.normal(0, noise_scale * 0.3, future_len) * np.linspace(0, 1, future_len)
    z[hist_len:] += np.random.normal(0, noise_scale * 0.3, future_len) * np.linspace(0, 1, future_len)
    
    # Calculate uncertainty (grows with time into future)
    uncertainty = np.zeros_like(t_all)
    future_mask = t_all >= 0
    uncertainty[future_mask] = 0.1 + 0.05 * t_all[future_mask]
    uncertainty[~future_mask] = 0.05  # Historical uncertainty (measurement error)
    
    return {
        'x': x,
        'y': y,
        'z': z,
        'time': t_all,
        'uncertainty': uncertainty,
        'velocity_x': vx,
        'velocity_y': vy,
        'velocity_z': vz,
        'acceleration_x': ax,
        'acceleration_y': ay,
        'acceleration_z': az
    }


def generate_healthy_trajectory(months_future: int = 12) -> Dict:
    """
    Generate reference trajectory for healthy population
    
    Args:
        months_future: Number of months to project
    
    Returns:
        Dictionary with healthy reference trajectory
    """
    
    # Time points (only future, as reference)
    t = np.linspace(0, months_future, months_future * 4)
    
    # Healthy trajectory: slow, steady aging
    # Starts near origin, progresses slowly
    x0, y0, z0 = 0.1, 0.15, 0.12
    vx, vy, vz = 0.08, 0.09, 0.08  # Slow aging velocity
    ax, ay, az = 0.002, 0.002, 0.002  # Minimal acceleration
    
    # Calculate trajectory
    x = x0 + vx * t + 0.5 * ax * t**2
    y = y0 + vy * t + 0.5 * ay * t**2
    z = z0 + vz * t + 0.5 * az * t**2
    
    # Add slight natural variation
    x += np.random.normal(0, 0.02, len(t)) * np.linspace(0, 0.5, len(t))
    y += np.random.normal(0, 0.02, len(t)) * np.linspace(0, 0.5, len(t))
    z += np.random.normal(0, 0.02, len(t)) * np.linspace(0, 0.5, len(t))
    
    return {
        'x': x,
        'y': y,
        'z': z,
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
    
    Args:
        baseline: Baseline trajectory dictionary
        interventions: Dictionary of intervention parameters
        time_horizon: Months to project
    
    Returns:
        Modified trajectory dictionary
    """
    
    # Extract baseline parameters
    x0 = baseline['x'][baseline['time'] == 0][0]
    y0 = baseline['y'][baseline['time'] == 0][0]
    z0 = baseline['z'][baseline['time'] == 0][0]
    
    vx_base = baseline['velocity_x']
    vy_base = baseline['velocity_y']
    vz_base = baseline['velocity_z']
    
    ax_base = baseline['acceleration_x']
    ay_base = baseline['acceleration_y']
    az_base = baseline['acceleration_z']
    
    # Calculate intervention effects on velocity and acceleration
    # Each intervention affects different dimensions of the manifold
    
    # Sleep affects all dimensions (general health)
    sleep_factor = 1.0 - (interventions['sleep_change'] * 0.06)
    
    # VO2max primarily affects metabolic axis (x) and oxidative axis (z)
    vo2_factor_x = 1.0 - (interventions['vo2max_change'] * 0.008)
    vo2_factor_z = 1.0 - (interventions['vo2max_change'] * 0.010)
    
    # Alcohol reduction strongly affects liver inflammation (y) and oxidative stress (z)
    alcohol_factor_y = 1.0 - (interventions['alcohol_reduction'] / 100.0 * 0.4)
    alcohol_factor_z = 1.0 - (interventions['alcohol_reduction'] / 100.0 * 0.35)
    alcohol_factor_x = 1.0 - (interventions['alcohol_reduction'] / 100.0 * 0.25)
    
    # Caffeine affects metabolic and inflammation axes
    caffeine_factor_x = 1.0 - (interventions['caffeine_reduction'] / 400.0 * 0.15)
    caffeine_factor_y = 1.0 - (interventions['caffeine_reduction'] / 400.0 * 0.10)
    
    # NAC (antioxidant) primarily affects oxidative stress axis (z)
    nac_factor_z = 1.0 - (interventions['nac_dose'] / 2000.0 * 0.30)
    nac_factor_y = 1.0 - (interventions['nac_dose'] / 2000.0 * 0.15)
    
    # Metformin affects metabolic axis (x) and has some anti-inflammatory effects (y)
    metformin_factor_x = 1.0 - (interventions['metformin_dose'] / 2000.0 * 0.35)
    metformin_factor_y = 1.0 - (interventions['metformin_dose'] / 2000.0 * 0.20)
    
    # Combine factors for each dimension
    total_factor_x = (sleep_factor * vo2_factor_x * alcohol_factor_x * 
                     caffeine_factor_x * metformin_factor_x)
    total_factor_y = (sleep_factor * alcohol_factor_y * caffeine_factor_y * 
                     nac_factor_y * metformin_factor_y)
    total_factor_z = (sleep_factor * vo2_factor_z * alcohol_factor_z * 
                     nac_factor_z)
    
    # Ensure factors don't go below 0.2 (can't reverse aging completely)
    total_factor_x = max(0.2, total_factor_x)
    total_factor_y = max(0.2, total_factor_y)
    total_factor_z = max(0.2, total_factor_z)
    
    # Apply factors to velocity and acceleration
    vx_mod = vx_base * total_factor_x
    vy_mod = vy_base * total_factor_y
    vz_mod = vz_base * total_factor_z
    
    ax_mod = ax_base * (total_factor_x ** 1.5)  # Acceleration responds more strongly
    ay_mod = ay_base * (total_factor_y ** 1.5)
    az_mod = az_base * (total_factor_z ** 1.5)
    
    # Generate modified trajectory
    t_future = baseline['time'][baseline['time'] >= 0]
    
    x_mod = x0 + vx_mod * t_future + 0.5 * ax_mod * t_future**2
    y_mod = y0 + vy_mod * t_future + 0.5 * ay_mod * t_future**2
    z_mod = z0 + vz_mod * t_future + 0.5 * az_mod * t_future**2
    
    # Add slight stochastic variation
    noise_scale = 0.12
    x_mod += np.random.normal(0, noise_scale * 0.3, len(t_future)) * np.linspace(0, 0.8, len(t_future))
    y_mod += np.random.normal(0, noise_scale * 0.3, len(t_future)) * np.linspace(0, 0.8, len(t_future))
    z_mod += np.random.normal(0, noise_scale * 0.3, len(t_future)) * np.linspace(0, 0.8, len(t_future))
    
    # Reduced uncertainty with interventions (more predictable)
    uncertainty = 0.08 + 0.03 * t_future
    
    return {
        'x': x_mod,
        'y': y_mod,
        'z': z_mod,
        'time': t_future,
        'uncertainty': uncertainty,
        'velocity_x': vx_mod,
        'velocity_y': vy_mod,
        'velocity_z': vz_mod,
        'acceleration_x': ax_mod,
        'acceleration_y': ay_mod,
        'acceleration_z': az_mod
    }


def calculate_aging_metrics(trajectory: Dict) -> Dict:
    """
    Calculate key aging dynamics metrics from trajectory
    
    Args:
        trajectory: Trajectory dictionary
    
    Returns:
        Dictionary of metrics
    """
    
    # Get velocity components
    if 'velocity_x' in trajectory:
        vx = trajectory['velocity_x']
        vy = trajectory['velocity_y']
        vz = trajectory['velocity_z']
        ax = trajectory['acceleration_x']
        ay = trajectory['acceleration_y']
        az = trajectory['acceleration_z']
    else:
        # Calculate from trajectory if not provided
        x, y, z = trajectory['x'], trajectory['y'], trajectory['z']
        t = trajectory['time']
        
        # Numerical derivatives
        if len(t) > 1:
            dt = t[1] - t[0]
            vx = np.gradient(x, dt)[-1]
            vy = np.gradient(y, dt)[-1]
            vz = np.gradient(z, dt)[-1]
            
            ax = np.gradient(np.gradient(x, dt), dt)[-1]
            ay = np.gradient(np.gradient(y, dt), dt)[-1]
            az = np.gradient(np.gradient(z, dt), dt)[-1]
        else:
            vx = vy = vz = 0
            ax = ay = az = 0
    
    # Total velocity magnitude (aging speed)
    velocity = np.sqrt(vx**2 + vy**2 + vz**2)
    
    # Total acceleration magnitude
    acceleration = np.sqrt(ax**2 + ay**2 + az**2)
    
    # Uncertainty at time horizon
    uncertainty = trajectory['uncertainty'][-1] if len(trajectory['uncertainty']) > 0 else 0.1
    
    return {
        'velocity': velocity,
        'acceleration': acceleration,
        'uncertainty': uncertainty,
        'velocity_components': (vx, vy, vz),
        'acceleration_components': (ax, ay, az)
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

