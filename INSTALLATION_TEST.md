# ✅ Installation & Testing Checklist

Use this checklist to verify your Biological Relativity installation is working correctly.

## Pre-Installation Checklist

- [ ] Python 3.8 or higher installed (`python --version`)
- [ ] pip package manager available (`pip --version`)
- [ ] Command line / terminal access
- [ ] Web browser installed (Chrome/Firefox recommended)

## Installation Steps

### Step 1: Verify Files
- [ ] app.py exists
- [ ] methylome_trajectory.py exists
- [ ] requirements.txt exists
- [ ] README.md exists

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Expected Output:**
```
Successfully installed streamlit-1.29.0 numpy-1.24.3 plotly-5.18.0 pandas-2.0.3 scipy-1.11.3
```

**Verify Installation:**
```bash
pip list | grep streamlit
pip list | grep plotly
pip list | grep numpy
```

- [ ] All packages installed successfully
- [ ] No error messages during installation

## Running the Application

### Step 3: Launch Application
```bash
streamlit run app.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

- [ ] Application starts without errors
- [ ] Browser opens automatically or URL displayed
- [ ] No Python exceptions in terminal

### Step 4: Initial Load
- [ ] Page loads within 5 seconds
- [ ] Title displays: "🧬 Biological Relativity: Methylome Manifold"
- [ ] No error messages on page
- [ ] Interface layout appears correct

## Functional Testing

### Test 1: 3D Visualization
- [ ] 3D plot renders on left side
- [ ] Can see blue line with diamond markers (historical data)
- [ ] Can see red line (baseline trajectory)
- [ ] Can see green dashed line (healthy reference)
- [ ] Plot is rotatable with mouse
- [ ] Plot is zoomable with scroll wheel
- [ ] Axes labels visible: "Methylation PC1/PC2/PC3"
- [ ] Legend shows all trajectory types

**If plot not visible:**
- Try refreshing browser (F5)
- Check browser console for errors (F12)
- Try different browser

### Test 2: Control Panel
- [ ] Right panel shows "Treatment Interventions"
- [ ] Time horizon selector visible (3/6/12 months)
- [ ] All 6 sliders visible and functional
- [ ] Can drag sliders smoothly
- [ ] Slider values update as you drag
- [ ] Reset button visible

**Test Each Slider:**
- [ ] Sleep Duration (-2.0 to 4.0)
- [ ] VO₂max (0 to 50%)
- [ ] Alcohol Reduction (0 to 100%)
- [ ] Caffeine Reduction (0 to 400mg)
- [ ] NAC (0 to 2000mg)
- [ ] Metformin (0 to 2000mg)

### Test 3: Real-Time Updates
- [ ] Adjust Sleep slider to +2 hours
- [ ] Orange line appears in 3D plot
- [ ] Orange line is different from red line
- [ ] Update happens within 1 second
- [ ] Metrics panel updates
- [ ] Delta indicators appear (arrows)

### Test 4: Metrics Panel
- [ ] "Aging Dynamics Metrics" section visible at bottom
- [ ] 4 metric cards displayed
- [ ] Current Aging Velocity shown
- [ ] Aging Acceleration shown
- [ ] Deviation from Healthy shown
- [ ] When interventions active, deltas appear (arrows)

### Test 5: Intervention Impact
- [ ] Adjust multiple sliders (e.g., Alcohol 80%, VO₂max 30%, Sleep +2)
- [ ] "Intervention Impact Analysis" section appears
- [ ] "Time to healthy trajectory" estimate shown
- [ ] "Key Contributing Factors" listed
- [ ] Top 3 factors ranked

### Test 6: Patient Case Summary
- [ ] Expandable panel at top works
- [ ] Patient details visible: LVR-2024-047
- [ ] Organ: Liver, Age: 42
- [ ] Risk factors listed

### Test 7: Time Horizon Change
- [ ] Select 3 months → trajectories shorten
- [ ] Select 6 months → trajectories medium length
- [ ] Select 12 months → trajectories full length
- [ ] 3D plot updates smoothly
- [ ] Metrics recalculate correctly

### Test 8: Reset Functionality
- [ ] Adjust several sliders to non-zero values
- [ ] Orange trajectory visible
- [ ] Click "Reset All Interventions" button
- [ ] Page refreshes or sliders return to zero
- [ ] Orange trajectory disappears
- [ ] Back to baseline state

## Performance Testing

### Load Time
- [ ] Initial page load: < 5 seconds
- [ ] 3D plot render: < 2 seconds
- [ ] Slider response: < 200ms

### Smoothness
- [ ] 3D plot rotation is smooth (no lag)
- [ ] Slider dragging is smooth
- [ ] No flickering or artifacts
- [ ] Transitions are fluid

### Memory
- [ ] No memory warnings in browser
- [ ] Application doesn't slow down over time
- [ ] Can use app for 5+ minutes without issues

## Edge Case Testing

### Test 9: Extreme Values
- [ ] Set all sliders to maximum
- [ ] Orange trajectory dramatically different from red
- [ ] Metrics show large improvements
- [ ] No errors or crashes

- [ ] Set all sliders to minimum/zero
- [ ] Back to baseline state
- [ ] No errors

### Test 10: Rapid Changes
- [ ] Quickly drag multiple sliders
- [ ] Change time horizon repeatedly
- [ ] Application remains responsive
- [ ] No crashes or freezing

### Test 11: Browser Compatibility
Test in multiple browsers:
- [ ] Chrome
- [ ] Firefox
- [ ] Edge
- [ ] Safari (if on Mac)

## Troubleshooting Guide

### Problem: App won't start
```
Error: No module named 'streamlit'
```
**Solution:**
```bash
pip install -r requirements.txt --force-reinstall
```

### Problem: 3D plot not showing
**Solution:**
- Clear browser cache (Ctrl+Shift+Del)
- Try different browser
- Check browser console (F12) for JavaScript errors
- Restart Streamlit: Ctrl+C, then `streamlit run app.py`

### Problem: Slow performance
**Solution:**
- Close other browser tabs
- Reduce time horizon to 3 months
- Restart application
- Check system resources (RAM, CPU)

### Problem: Sliders not responding
**Solution:**
- Refresh browser (F5)
- Clear Streamlit cache: Click "☰ → Clear cache"
- Restart application

### Problem: Import errors
```
ImportError: cannot import name 'X' from 'Y'
```
**Solution:**
```bash
pip install --upgrade streamlit plotly numpy pandas scipy
```

## Post-Installation Verification

### Final Checklist
- [ ] All core features working
- [ ] No console errors
- [ ] Smooth performance
- [ ] Can create 3+ different intervention scenarios
- [ ] Can export/screenshot results
- [ ] Documentation is clear and helpful

### Success Criteria
✅ **You should be able to:**
1. See 3D visualization of aging trajectory
2. Adjust treatment interventions via sliders
3. See real-time trajectory changes (orange line)
4. View aging metrics with improvements
5. Understand intervention impact analysis
6. Navigate and use interface intuitively

## Optional: Advanced Testing

### Test 12: Data Validation
Open Python console and test trajectory calculations:
```python
from methylome_trajectory import generate_patient_trajectory, calculate_aging_metrics

# Generate trajectory
trajectory = generate_patient_trajectory(weeks_historical=3, months_future=12)

# Check data structure
assert 'x' in trajectory
assert 'y' in trajectory
assert 'z' in trajectory
assert len(trajectory['x']) > 0

# Calculate metrics
metrics = calculate_aging_metrics(trajectory)
assert 'velocity' in metrics
assert 'acceleration' in metrics
assert metrics['velocity'] > 0

print("✅ All trajectory calculations working correctly")
```

### Test 13: Example Scenarios
Load example scenarios:
```python
from example_scenarios import list_all_scenarios, get_scenario

# List scenarios
scenarios = list_all_scenarios()
print(f"Available scenarios: {scenarios}")

# Get a scenario
scenario = get_scenario('moderate_comprehensive')
print(f"Interventions: {scenario['interventions']}")
```

## Getting Help

### If Tests Fail
1. Check Python version: `python --version` (need 3.8+)
2. Verify all files present: `ls -la` or `dir`
3. Review error messages in terminal
4. Check browser console (F12)
5. Read troubleshooting section above

### Documentation Resources
- **Quick Start**: QUICKSTART.md
- **Full Guide**: README.md
- **Technical Details**: MANIFOLD_GUIDE.md
- **Visual Reference**: VISUAL_GUIDE.md
- **Project Overview**: PROJECT_SUMMARY.md

## Report Card

**Total Tests:** 13 categories
**Passed:** _____ / 13
**Status:** ⬜ All Pass ⬜ Minor Issues ⬜ Major Issues

### Notes:
```
[Space for noting any issues, quirks, or observations]
```

---

## Next Steps After Successful Installation

1. ✅ Read QUICKSTART.md for usage tutorial
2. ✅ Try example scenarios (moderate intervention, aggressive protocol)
3. ✅ Explore 3D visualization from different angles
4. ✅ Experiment with different time horizons
5. ✅ Read MANIFOLD_GUIDE.md for conceptual understanding
6. ✅ Consider customization for your use case

**Congratulations! Your Biological Relativity installation is complete.** 🧬

---

**Installation Date:** _____________
**Tested By:** _____________
**System:** _____________
**Status:** ✅ Ready for Use

