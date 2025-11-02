# Setting Up Claude AI for Clinical Reports

## Overview

ChronOS now includes an AI-powered clinical report generator that uses Claude (Anthropic) to provide intelligent, personalized recommendations based on the patient's aging trajectory and intervention protocol.

## Setup Instructions

### 1. Get Your API Key

1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (it starts with `sk-ant-...`)

### 2. Set Environment Variable

#### Method 1: Using .env File (Recommended - Already Set Up!)

The app now automatically loads your API key from a `.env` file in the project root.

**Your `.env` file should contain:**
```bash
ANTHROPIC_API_KEY=your_key_here
```

✅ **This is already configured!** The app will automatically load the key from `.env` when it starts.

**Security Note:** The `.env` file is already in `.gitignore`, so it won't be committed to version control.

#### Method 2: Environment Variable (Alternative)

If you don't want to use `.env`, you can set it manually:

**On Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="your_key_here"
```

**On Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=your_key_here
```

**On macOS/Linux:**
```bash
export ANTHROPIC_API_KEY="your_key_here"
```

#### Method 3: Permanent System Setup

**Windows:**
1. Open System Properties → Environment Variables
2. Add new User Variable:
   - Name: `ANTHROPIC_API_KEY`
   - Value: `your_key_here`

**macOS/Linux:**
Add to your `~/.bashrc` or `~/.zshrc`:
```bash
export ANTHROPIC_API_KEY="your_key_here"
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
streamlit run app.py
```

## Features

The Clinical Report Generator:

1. **Analyzes Trajectory Metrics**
   - Compares Status Quo vs. With Interventions
   - Evaluates distance to Healthy Population trajectory
   - Calculates percentage improvements in velocity and acceleration

2. **Identifies Key Drivers**
   - Determines which interventions are most impactful
   - Explains the biological mechanisms at play
   - Prioritizes recommendations by effectiveness

3. **Generates Personalized Reports**
   - Warm, professional tone suitable for patient communication
   - Clear sections: Summary, Analysis, Recommendations, Concerns, Motivation
   - Actionable insights with specific timelines

4. **Export Capability**
   - Download report as text file
   - Share directly with patients
   - Include in medical records

## Usage Tips

1. **Adjust Interventions First**: Use the sliders to simulate different intervention protocols before generating the report
2. **Wait for Metrics**: Ensure the 3D visualization has loaded and metrics are displayed
3. **Review Output**: The report is generated in real-time by Claude - review for clinical appropriateness
4. **Iterate**: Try different intervention combinations to compare recommendations

## Model Details

- **Model**: Claude 3.5 Sonnet (claude-3-5-sonnet-20241022)
- **Max Tokens**: 2000 (sufficient for detailed reports)
- **Temperature**: 0.7 (balanced creativity and consistency)
- **Context**: Includes patient case, metrics, interventions, and trajectory analysis

## Pricing

Claude API pricing (as of 2024):
- Input: ~$3 per million tokens
- Output: ~$15 per million tokens

A typical report generation costs approximately $0.01-0.02 per report.

## Troubleshooting

### "API Key Not Found"
- Ensure environment variable is set correctly
- Restart your terminal/IDE after setting the variable
- Verify the key starts with `sk-ant-`

### "Rate Limit Exceeded"
- Anthropic has rate limits based on your plan
- Wait a moment and try again
- Consider upgrading your API plan if needed

### "Invalid Request"
- Check your API key is active in the Anthropic Console
- Ensure you have sufficient credits/quota
- Verify network connectivity

## Security Notes

⚠️ **Important**:
- Never commit your API key to version control
- Don't share your API key publicly
- Rotate keys periodically
- Use environment variables (not hardcoded values)
- Consider using a `.env` file with `.gitignore` for local development

## Support

For issues with:
- **ChronOS App**: Check this repository's Issues
- **Claude API**: Visit [Anthropic Support](https://support.anthropic.com/)
- **API Key Management**: [Anthropic Console](https://console.anthropic.com/)

