# Crisis Decision Simulator - Terminal Execution Guide

## Quick Start (Recommended)

### Windows Users - EASIEST METHOD
```
Simply double-click: run.bat
```
This automatically sets up everything and launches the system.

---

## Manual Terminal Execution

### Step 1: Navigate to Project Directory
```bash
cd c:\Users\devar\OneDrive\Desktop\new
```

### Step 2: Create Python Virtual Environment (First time only)
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```bash
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install --upgrade pip
pip install -r crisis_simulator/requirements.txt
```

This installs:
- Flask (web framework)
- Flask-CORS (cross-origin support)
- NumPy & Pandas (data processing)
- Scikit-learn (machine learning)
- Matplotlib (visualization)

### Step 5: Start Backend API

**Windows:**
```bash
cd crisis_simulator\backend
python app.py
```

**Linux/Mac:**
```bash
cd crisis_simulator/backend
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 6: Open Frontend (in another terminal)

**Keep the backend running (don't close the terminal)**

Open a NEW terminal window and navigate to the project:

**Windows:**
```bash
cd c:\Users\devar\OneDrive\Desktop\new
start crisis_simulator\frontend\index.html
```

**Linux/Mac:**
```bash
cd /path/to/project
open crisis_simulator/frontend/index.html
```

---

## Verification

### Check Backend is Running
- Open browser: http://localhost:5000/api/health
- Should show: `{"status": "healthy", "message": "..."}`

### Check Frontend is Loading
- Frontend dashboard should appear with 3 scenario buttons
- Message shows "API Status: ✓ Connected"

### Test Simulation
1. Click "Healthcare Crisis" button
2. Click "Simulate Crisis" button
3. Wait 1-2 seconds
4. Results should display on page

---

## Stopping the System

### Backend Terminal
```
Press Ctrl + C
```

### All Other Windows
- Close normally

---

## Troubleshooting

### Python not found
```bash
# Check if Python is installed
python --version
# If not, download from: https://www.python.org/downloads/
```

### Port 5000 already in use
```bash
# Find what's using port 5000:
netstat -ano | findstr :5000

# Kill the process (note the PID number from above):
taskkill /PID <PID> /F

# Or use a different port in backend/app.py:
# Change: app.run(port=5000)
# To: app.run(port=5001)
```

### Dependencies installation fails
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Try installing requirements again
pip install -r crisis_simulator/requirements.txt --upgrade
```

### Frontend shows "API Disconnected"
- Ensure backend terminal is still running
- Check backend shows "Running on http://127.0.0.1:5000"
- Browser console (F12) may show CORS errors - these can be ignored if API works

### Simulation doesn't run
- Check browser console (Press F12)
- Check backend terminal for error messages
- Ensure all Python dependencies are installed

---

## Full System Architecture

```
┌─────────────────────────────────────────────────────┐
│           FRONTEND (HTML/CSS/JavaScript)            │
│     - Dashboard UI                                   │
│     - Scenario Selection                             │
│     - Results Display                                │
│     - Risk Visualization                             │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP Requests (JSON)
                   │
┌──────────────────▼──────────────────────────────────┐
│    BACKEND API (Flask on localhost:5000)            │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Scenario Generator                           │  │
│  │ - Healthcare scenarios                       │  │
│  │ - Disaster scenarios                         │  │
│  │ - Finance scenarios                          │  │
│  └──────────────────────────────────────────────┘  │
│                      ↓                               │
│  ┌──────────────────────────────────────────────┐  │
│  │ Agent System                                 │  │
│  │ - Healthcare agents                          │  │
│  │ - Disaster agents                            │  │
│  │ - Finance agents                             │  │
│  │ - Decision making                            │  │
│  └──────────────────────────────────────────────┘  │
│                      ↓                               │
│  ┌──────────────────────────────────────────────┐  │
│  │ Outcome Predictor                            │  │
│  │ - ML-based predictions                       │  │
│  │ - Probability calculations                   │  │
│  │ - Uncertainty quantification                 │  │
│  └──────────────────────────────────────────────┘  │
│                      ↓                               │
│  ┌──────────────────────────────────────────────┐  │
│  │ Risk Analyzer                                │  │
│  │ - Risk identification                        │  │
│  │ - Probability assessment                     │  │
│  │ - Failure scenario generation                │  │
│  └──────────────────────────────────────────────┘  │
│                      ↓                               │
│  ┌──────────────────────────────────────────────┐  │
│  │ Decision Explainer                           │  │
│  │ - Transparent reasoning                      │  │
│  │ - Decision ranking                           │  │
│  │ - Recommendations                            │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## Performance Expectations

| Operation | Time |
|-----------|------|
| Python environment setup | 1-2 minutes |
| Dependency installation | 2-5 minutes |
| Backend startup | 2-3 seconds |
| Frontend load | <1 second |
| Simulation run | 500ms - 2s |
| Results display | Instant |

---

## Next Steps After Running

1. **Test Different Scenarios**
   - Try all 3 scenario types
   - Observe how agents adjust decisions

2. **Examine Detailed Analysis**
   - Click on "Decision Ranking" tab
   - Review risk assessments
   - Read recommendations

3. **Monitor Metrics**
   - See key metrics to track
   - Understand decision timeline
   - Plan implementation steps

4. **Explore Code**
   - Check backend logic in Python files
   - Understand prediction models
   - Review decision algorithms

---

## Integration Examples

### Using the API Directly
```bash
# Health check
curl http://localhost:5000/api/health

# Get available scenarios
curl http://localhost:5000/api/scenarios

# Run simulation
curl -X POST http://localhost:5000/api/simulate \
  -H "Content-Type: application/json" \
  -d "{\"scenario_type\": \"healthcare\"}"
```

### Programmatic Access (Python)
```python
import requests
import json

BASE_URL = "http://localhost:5000/api"

# Get scenarios
response = requests.get(f"{BASE_URL}/scenarios")
scenarios = response.json()

# Run simulation
data = {"scenario_type": "healthcare"}
response = requests.post(f"{BASE_URL}/simulate", json=data)
results = response.json()

print(json.dumps(results, indent=2))
```

---

## Support & Documentation

- **README.md**: Full project documentation
- **Code comments**: Detailed explanations in Python files
- **Browser console** (F12): Error messages and debugging
- **Backend logs**: In terminal running Flask app

---

**Happy Simulating! 🚀**
