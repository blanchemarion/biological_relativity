# 📸 Visual Interface Guide

## What the Application Looks Like

This guide describes what you'll see when you run the Biological Relativity Methylome Manifold tool.

## Main Interface Layout

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  🧬 Biological Relativity: Methylome Manifold              ┃
┃     Visualize Organ Aging Trajectories & Treatment Effects ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┌────────────────────────────────────────────────────────────┐
│ 📋 Patient Case Summary                            [▼]     │
│  Patient: LVR-2024-047 | Liver | Age 42 | 3 measurements  │
└────────────────────────────────────────────────────────────┘

┌──────────────────────────────────┬─────────────────────────┐
│                                  │  🎛️ Treatment           │
│  📊 3D Methylome Manifold        │     Interventions       │
│      Trajectory                  │                         │
│                                  │  Time Horizon: 12 mo    │
│   [3D INTERACTIVE PLOT]          │  ━━━━━━━━━━━━━━━━━━━   │
│                                  │                         │
│   • Blue ◆◆◆ Historical          │  Lifestyle:            │
│   • Red ─── Baseline             │  Sleep:     [====    ]  │
│   • Green --- Healthy            │  VO₂max:    [====    ]  │
│   • Orange ─── Modified          │  Alcohol:   [========]  │
│   • Yellow ● Current             │  Caffeine:  [====    ]  │
│                                  │                         │
│   Axes:                          │  Pharmacological:      │
│   X: Metabolic                   │  NAC:       [====    ]  │
│   Y: Inflammation                │  Metformin: [====    ]  │
│   Z: Oxidative                   │                         │
│                                  │  [🔄 Reset All]         │
│                                  │                         │
│                                  │  ✅ Interventions       │
│                                  │     Active              │
├──────────────────────────────────┴─────────────────────────┤
│  📈 Aging Dynamics Metrics                                 │
│  ┌──────────────┬──────────────┬──────────────┬──────────┐│
│  │ Velocity     │ Acceleration │ Deviation    │ Time     ││
│  │ 0.352 ↓0.145 │ 0.016 ↓0.008 │ 165% ↓68%    │ Dilation ││
│  └──────────────┴──────────────┴──────────────┴──────────┘│
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│  💡 Intervention Impact Analysis                           │
│  Time to Healthy: ~8.2 months with current interventions  │
│  Key Factors: 1. Alcohol reduction  2. VO₂max  3. Sleep   │
└────────────────────────────────────────────────────────────┘
```

## Detailed Component Views

### 1. Header Section
```
🧬 Biological Relativity: Methylome Manifold
   Visualize Organ Aging Trajectories & Treatment Effects
```
- Large, centered title
- Blue color scheme
- Professional medical aesthetic

### 2. Patient Case Summary (Collapsible)
```
📋 Patient Case Summary [▼]
┌─────────────────┬─────────────────┬──────────────────┐
│ Patient ID:     │ First Visit:    │ Risk Factors:    │
│ LVR-2024-047    │ 3 months ago    │ • Alcohol        │
│ Organ: Liver    │ Measurements: 3 │ • Caffeine       │
│ Age: 42 years   │ Status: Active  │ • Sedentary      │
└─────────────────┴─────────────────┴──────────────────┘
```

### 3. Left Panel: 3D Visualization

**What You See:**
```
        Z (Oxidative) ↑
                      |
                   ●  |  ◆ (Historical points)
                  /│  | /
              ──────●─────  (Trajectories)
                /   |/
               /    ●
              /    /|
             /   /  |
            / /     |
          ─────────→ X (Metabolic)
         /
        /
       ↓ Y (Inflammation)
```

**Legend:**
- **Blue line with diamonds (◆◆◆)**: Your 3 historical measurements
- **Red solid line (───)**: Predicted path if you change nothing
- **Green dashed line (---)**: Healthy population reference
- **Orange solid line (───)**: Modified path with your interventions
- **Yellow circle (●)**: Your current position
- **Transparent spheres (○)**: Uncertainty regions

**Interactive Features:**
- 🖱️ Click and drag to rotate view
- 🖱️ Scroll to zoom in/out
- 🖱️ Double-click to reset view
- 📊 Hover over lines to see exact values

### 4. Right Panel: Treatment Controls

```
🎛️ Treatment Interventions
─────────────────────────────

Prediction Time Horizon
┌─────┬─────┬─────┐
│  3  │  6  │ 12  │ months
└─────┴─────┴─────┘
      Selected: 12

────────────────────────────
Lifestyle Modifications

Sleep Duration Change
[-2.0] ━━━━●━━━━━━━━━ [4.0]
         0.0 hours/night

VO₂max Improvement
[0] ━━━━━━━━━━━━━━━━━ [50%]
    0%

Alcohol Reduction
[0%] ━━━━━━━━━━━━━━━ [100%]
     0%

Caffeine Reduction
[0] ━━━━━━━━━━━━━━━━ [400mg]
    0 mg/day

────────────────────────────
Pharmacological Interventions

N-Acetylcysteine
[0] ━━━━━━━━━━━━━━━ [2000mg]
    0 mg/day

Metformin
[0] ━━━━━━━━━━━━━━━ [2000mg]
    0 mg/day

────────────────────────────
      [🔄 Reset All]

ℹ️ No interventions applied
```

**When Interventions Active:**
```
✅ Interventions Active
```

### 5. Bottom Metrics Panel

```
📈 Aging Dynamics Metrics

┌──────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┐
│ Current Aging        │ Aging Acceleration   │ Deviation from       │ Biological Time      │
│ Velocity             │                      │ Healthy              │ Dilation             │
│                      │                      │                      │                      │
│    0.352             │    0.016             │    165.2%            │    100.0%            │
│    ↓ 0.145 (better)  │    ↓ 0.008 (better)  │    ↓ 68.4% (better)  │    ↓ 20.0% (slower)  │
│                      │                      │                      │                      │
│ units/month          │ units/month²         │ vs. population avg   │ with interventions   │
└──────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┘
```

**Color Coding:**
- 🟢 Green arrows (↓): Improvement (lower is better for velocity/acceleration/deviation)
- 🔴 Red arrows (↑): Worsening
- Gray values: No change (baseline)

### 6. Intervention Impact Analysis (When Active)

```
💡 Intervention Impact Analysis

🎯 Estimated Time to Healthy Trajectory
   ~8.2 months with current interventions

🔬 Key Contributing Factors
   1. Alcohol reduction: 0.336 velocity reduction
   2. VO₂max improvement: 0.084 velocity reduction
   3. Sleep increase: 0.048 velocity reduction
```

## Color Scheme

### Primary Colors
- **Blue (#1f77b4)**: Headers, historical data
- **Red (#ff4b4b)**: Baseline trajectory (warning)
- **Green (#00cc00)**: Healthy reference (goal)
- **Orange (#ff7f0e)**: Modified trajectory (action)
- **Yellow (#ffd700)**: Current position (attention)

### UI Colors
- **Background**: Light gray (#f0f2f6)
- **Text**: Dark gray (#262730)
- **Success**: Green (#00cc00)
- **Warning**: Orange (#ffa500)
- **Error**: Red (#ff4b4b)

## Responsive Behavior

### Desktop (> 1200px)
```
┌──────────────────────────────────────────────┐
│             Full split-screen                │
│   [3D Plot 66%]  [Controls 33%]              │
└──────────────────────────────────────────────┘
```

### Tablet (768px - 1200px)
```
┌──────────────────────────────┐
│       3D Plot (full width)   │
├──────────────────────────────┤
│     Controls (full width)    │
└──────────────────────────────┘
```

### Mobile (< 768px)
```
┌──────────────┐
│   3D Plot    │
│  (stacked)   │
├──────────────┤
│   Controls   │
│  (stacked)   │
└──────────────┘
```

## Animation & Transitions

### When You Adjust a Slider
1. Slider value updates immediately
2. Orange trajectory line smoothly transitions (300ms)
3. Metrics update with animation
4. Delta indicators appear with fade-in effect

### When You Change Time Horizon
1. All trajectories extend/contract
2. Uncertainty spheres adjust size
3. Smooth transition over 500ms

### First Load
1. 3D plot renders with rotation animation
2. Components fade in sequentially
3. Welcome state with all sliders at zero

## Interaction Patterns

### Mouse Interactions
```
3D Plot:
  Left-click + drag → Rotate view
  Right-click + drag → Pan view
  Scroll → Zoom in/out
  Double-click → Reset view

Sliders:
  Click → Jump to position
  Drag → Smooth adjustment
  Hover → Show tooltip

Buttons:
  Hover → Highlight effect
  Click → Ripple effect
```

### Touch Interactions (Mobile)
```
3D Plot:
  One finger drag → Rotate
  Two finger pinch → Zoom
  Two finger drag → Pan

Sliders:
  Tap → Jump
  Drag → Adjust
```

## Visual States

### Initial State (No Interventions)
- Red trajectory diverging from green
- High velocity/acceleration metrics
- "No interventions applied" message
- Gray metric cards

### Interventions Active
- Orange trajectory bending toward green
- Reduced velocity/acceleration (green deltas)
- "Interventions Active" ✅ message
- Colored metric cards

### Optimal Configuration
- Orange trajectory merging with green
- Low velocity/acceleration
- "Time to healthy: X months" prominent
- Success indicators throughout

## Print/Export View

When printing or exporting:
- 3D plot shows static view (current rotation)
- All metrics visible
- Intervention settings listed
- Patient case summary expanded
- Clean, professional layout

## Accessibility Features

- **High contrast**: All text readable
- **Clear labels**: Every control labeled
- **Tooltips**: Hover help on all sliders
- **Keyboard navigation**: Tab through controls
- **Screen reader friendly**: Semantic HTML
- **Color blind safe**: Patterns + colors

## Performance Indicators

### Loading States
```
⏳ "Calculating trajectories on methylome manifold..."
   (Spinner animation while computing)

✅ "Ready" (Invisible, but app responsive)
```

### Update Lag
- **Target**: < 100ms for slider updates
- **Typical**: 50-80ms smooth updates
- **Maximum**: 200ms (still feels responsive)

## Tips for Best Visual Experience

1. **Screen Resolution**: Best on 1920x1080 or higher
2. **Browser**: Chrome or Firefox recommended
3. **3D View**: Start with default view, then explore angles
4. **Interventions**: Adjust one slider at a time to see individual effects
5. **Time Horizon**: Start with 3 months, increase to see long-term effects

---

**This visual interface transforms complex methylation data into intuitive, actionable insights for practitioners.** 🧬

