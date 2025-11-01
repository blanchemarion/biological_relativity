# 🚀 Quick Start Guide

Get the Biological Relativity Methylome Manifold tool running in 3 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Run the Application

### Windows
Double-click `run.bat` or run in command prompt:
```bash
run.bat
```

### Mac/Linux
Make the script executable and run:
```bash
chmod +x run.sh
./run.sh
```

### Or directly:
```bash
streamlit run app.py
```

## Step 3: Explore the Interface

The app will open in your browser at `http://localhost:8501`

### What You'll See

**📊 Left Side - 3D Visualization:**
- **Blue diamonds**: Patient's 3 historical measurements (3 weeks)
- **Red line**: Predicted path without changes (baseline)
- **Green dashed**: Healthy population reference
- **Orange line**: Modified path with your interventions

**🎛️ Right Side - Controls:**
1. Select time horizon (3/6/12 months)
2. Adjust lifestyle interventions:
   - Sleep hours
   - Exercise (VO₂max)
   - Alcohol reduction
   - Caffeine reduction
3. Add pharmacological interventions:
   - NAC (antioxidant)
   - Metformin (metabolic)

### Try This Example

1. **Baseline**: Keep all sliders at 0 - see the red trajectory
2. **Alcohol Reduction**: Move slider to 80% - watch orange line bend toward green
3. **Add Exercise**: Set VO₂max to 30% - see additional improvement
4. **Add Sleep**: Increase sleep by 2 hours - observe combined effect

### Understanding the Metrics

**🎯 Bottom Panel:**
- **Aging Velocity**: Lower is better (slower aging)
- **Acceleration**: Lower is better (stable aging rate)
- **Deviation**: Lower % means closer to healthy population
- **Time Dilation**: Higher % = biological time slowing down

### Recommended Scenarios to Explore

#### Scenario 1: Minimal Intervention
- Alcohol reduction: 50%
- Sleep: +1 hour
- See modest improvement

#### Scenario 2: Moderate Intervention
- Alcohol reduction: 80%
- VO₂max: 20%
- Sleep: +2 hours
- Caffeine reduction: 200mg
- See significant trajectory change

#### Scenario 3: Aggressive Intervention
- Alcohol reduction: 100%
- VO₂max: 40%
- Sleep: +3 hours
- Caffeine reduction: 300mg
- NAC: 1200mg
- Metformin: 1000mg
- Maximum trajectory correction

## Troubleshooting

**App won't start:**
- Check Python version: `python --version` (need 3.8+)
- Reinstall packages: `pip install -r requirements.txt --force-reinstall`

**Visualization not showing:**
- Clear browser cache
- Try different browser (Chrome recommended)
- Restart Streamlit: Ctrl+C then restart

**Slow performance:**
- Reduce time horizon to 3 months
- Close other browser tabs
- Restart the app

## Next Steps

Once comfortable with the interface:
1. Read the full `README.md` for conceptual details
2. Explore the code in `app.py` and `methylome_trajectory.py`
3. Modify parameters to test different scenarios
4. Consider how real methylation data would integrate

## Questions?

This is a mockup demonstrating the concept. For production use:
- Real methylation data input needed
- Clinical validation required
- Regulatory approval necessary

---

**Enjoy exploring biological aging dynamics!** 🧬

