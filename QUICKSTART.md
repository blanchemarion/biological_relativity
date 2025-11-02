# 🚀 Quick Start Guide

Get ChronOS (Biological Relativity Methylome Manifold) running in 3 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: (Optional) Set Up Claude AI for Reports

✅ **Already configured!** The app loads your API key from the `.env` file.

**Your `.env` file should contain:**
```bash
ANTHROPIC_API_KEY=your_api_key_here
```

Get your API key from [Anthropic Console](https://console.anthropic.com/)

📖 **See `SETUP_CLAUDE.md` for detailed setup instructions**

*You can skip this step and still use all visualization features!*

## Step 3: Run the Application

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

## Step 4: Explore the Interface

The app will open in your browser at `http://localhost:8501`

### What You'll See

**📊 Left Side - 3D Visualization:**
- **Gray dots**: Jeff's 3 historical measurements (3 weeks of liver DNA methylation)
- **Amber line**: Status Quo trajectory (no intervention)
- **Green line + band**: Healthy population reference with uncertainty
- **Cyan line**: Modified path with your interventions
- **Yellow marker**: Current position

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

**🎯 HUD Metrics (below visualization):**
Shows three rows of metrics:
- **Status Quo (No Intervention)**: Baseline trajectory metrics
- **Healthy Population**: Reference values for healthy aging
- **With Interventions**: Your customized protocol with deltas (▲/▼)

Key metrics:
- **Velocity**: Aging speed on manifold (lower = slower aging)
- **Acceleration**: Rate of change (lower = more stable)
- **Uncertainty**: Trajectory confidence (lower = more predictable)

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

### 🤖 AI-Powered Reports (New!)

After adjusting interventions:

1. **Click "🔬 Generate Clinical Report"** at the bottom
2. Wait ~3-5 seconds for Claude AI to analyze
3. **Review the report** with:
   - Progress summary
   - Intervention impact analysis
   - Concrete recommendations
   - Areas of concern
   - Motivational guidance
4. **Download as text file** to share with patient

**What the AI analyzes:**
- Velocity and acceleration changes (%)
- Distance to healthy trajectory
- Which interventions are driving improvements
- Biological mechanisms at play
- Personalized next steps

**Requirements:**
- `ANTHROPIC_API_KEY` must be set (see Step 2)
- Internet connection
- ~$0.01-0.02 per report generated

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

**Report generation failing:**
- Check `ANTHROPIC_API_KEY` is set: `echo $ANTHROPIC_API_KEY`
- Verify API key is active at [console.anthropic.com](https://console.anthropic.com/)
- Check internet connection
- See `SETUP_CLAUDE.md` for detailed troubleshooting

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

