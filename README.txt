# PRAXIS - PSA INTELLIGENT CONVERSATION ASSISTANT
Where Thought Becomes Action

From the Greek πρᾶξις, meaning the passage from understanding to doing.
PRAXIS reflects how structured analysis can take the shape of reasoning.
A study in how data can think with purpose.

Code Submission - Problem Statement 2
Team: 404 Port Not Found


# PROJECT OVERVIEW

PRAXIS is an AI-powered conversational assistant for PSA's Global Insights 
Dashboard. The system uses Azure OpenAI to interpret vessel operations data 
and provide intelligent recommendations, transforming operational data into 
clarity and supporting decisions with intent.

Key Achievement: 142x faster than manual analysis (2.1s vs 300s)


# SYSTEM ARCHITECTURE

The solution consists of modular Python components:

## Main Entry Point

job_planner.py (MODIFIED)
- Orchestrates all system components
- Fetches data via powerbi_connector
- Analyzes performance via decision_engine
- Generates AI recommendations via llm_client
- Tracks performance metrics via evaluation_system
- Outputs results to data/output.csv with performance logs

## Supporting Modules

- powerbi_connector.py: Power BI data access via Service Principal
- decision_engine.py: DIS score calculation and performance analysis
- llm_client.py: Azure OpenAI GPT-4.1-nano integration
- conversation_manager.py: Query intent detection and context management
- evaluation_system.py: Performance metrics (response time, speedup)
- config.py: Centralized configuration management
- frontend_app.py: Streamlit web interface
- test_system.py: System validation and testing

## Integration Approach

job_planner.py imports and utilizes functions from existing modules rather 
than duplicating code. This modular approach ensures maintainability and 
follows software engineering best practices.


# SYSTEM REQUIREMENTS

- Python 3.9 or higher
- Internet connection for Azure OpenAI API
- 4GB RAM minimum
- Windows/Linux/MacOS
- Virtual environment recommended


# INSTALLATION

1. Extract all files to your working directory

2. Navigate to project folder:
   cd PSA_Case_2

3. Create and activate virtual environment:
   
   Windows:
   python -m venv .venv
   .venv\Scripts\activate
   
   Mac/Linux:
   python3 -m venv .venv
   source .venv/bin/activate

4. Install dependencies:
   pip install -r requirements.txt

5. Verify all files present:
   config.py
   conversation_manager.py
   decision_engine.py
   evaluation_system.py
   frontend_app.py
   job_planner.py
   llm_client.py
   powerbi_connector.py
   test_system.py
   requirements.txt
   README.txt


# RUNNING THE SYSTEM

Important: Always activate virtual environment before running.
Windows: .venv\Scripts\activate
Mac/Linux: source .venv/bin/activate

## Option 1: Generate Simulation Results (Primary Method)

python job_planner.py

This will:
- Authenticate with Power BI
- Fetch 300 vessel operation records
- Run Decision Intelligence Score analysis
- Generate AI recommendations
- Export to data/output.csv
- Create performance log in logs/

Expected output:
- data/output.csv (analyzed vessel data sorted by DIS score)
- logs/job_planner_YYYYMMDD_HHMMSS.log (performance metrics)

Typical execution time: 2-3 seconds

## Option 2: Run Interactive Web Interface

streamlit run frontend_app.py

Launches PRAXIS at http://localhost:8501

Features:
- Natural language queries
- Real-time dashboard integration
- Interactive performance metrics
- Strategy selection

## Option 3: Run System Tests

python test_system.py

Validates Power BI authentication, decision engine, and LLM connectivity.


# CONFIGURATION

## Power BI Settings (in config.py)

- Authentication: Service Principal
- Client ID: d4513e50-29a7-4f57-a41f-68fae5006b67
- Workspace ID: 41675240-7b6e-4163-a0ed-52b5c3b13e01
- Report ID: 06bdda3d-459c-4632-8784-d43e6b208aab

## Azure OpenAI Settings

- Endpoint: https://psacodesprint2025.azure-api.net/
- Deployment: gpt-4.1-nano
- API Version: 2025-01-01-preview

## Decision Weights

- Time Efficiency: 30%
- Cost Efficiency: 30%
- Environmental Impact: 20%
- Risk Level: 20%


# OUTPUT FILES

## data/output.csv

Analyzed vessel data with columns:
- Operator, Vessel, BU
- DIS_Score (Decision Intelligence Score 0-100)
- Time_Efficiency, Cost_Efficiency, Environmental_Score, Risk_Score
- Wait Time, Arrival Accuracy, Bunker Saved, Carbon Abatement

Sorted by DIS_Score (highest priority first)

## logs/job_planner_[timestamp].log

Execution log containing:
- Data fetch time and record count
- Analysis metrics
- AI recommendations
- Performance comparison (AI vs Manual)
- Speedup factor and time saved


# KEY FEATURES

## Decision Intelligence Score (DIS)

Composite metric combining:
- Time Efficiency: Wait time and arrival accuracy
- Cost Efficiency: Bunker fuel savings
- Environmental Impact: Carbon abatement
- Risk Level: Operational reliability

Configurable weights support different strategic priorities.

## AI-Powered Recommendations

Azure OpenAI provides:
- Vessel attention priorities
- Operator performance insights
- Environmental optimization opportunities
- Actionable next steps

## Performance Optimization

Manual Process: ~300 seconds
- Dashboard navigation: 60s
- Data interpretation: 120s
- Decision making: 120s

AI Process: ~2.1 seconds
- Data fetch: 2.1s
- Analysis: 0.01s
- Recommendations: 0.01s

Result: 142x speedup

## Multi-Strategy Support

- Balanced: Equal weighting
- Carbon Reduction: Emphasizes environmental impact (40%)
- Cost Efficiency: Prioritizes bunker savings (40%)
- Reliability: Focuses on on-time performance (40%)


# TROUBLESHOOTING

## ModuleNotFoundError
Activate virtual environment and run: pip install -r requirements.txt

## Power BI authentication failed
Verify credentials in config.py and check internet connection

## Empty data returned
Confirm Power BI workspace access and dataset availability

## Streamlit won't start
Use custom port: streamlit run frontend_app.py --server.port 8502


# PERFORMANCE METRICS

Based on simulation results in logs/:
- Average processing time: 2.1 seconds
- Data capacity: 300+ vessel records
- AI recommendation generation: <1 second
- Manual equivalent: 300 seconds
- Speedup factor: 142x
- Time saved per query: 4.9 minutes


# TECHNICAL DETAILS

- Language: Python 3.9+
- Frontend: Streamlit 1.28.0
- AI Model: Azure OpenAI GPT-4.1-nano
- Data Source: Power BI REST API
- Authentication: MSAL (Microsoft Authentication Library)
- Analysis: Custom Decision Intelligence Score algorithm


# PRAXIS PHILOSOPHY

PRAXIS embodies the journey from data to decision:
- Understanding: AI analyzes vessel operations data
- Reasoning: Structured analysis identifies patterns and priorities
- Action: Clear recommendations enable confident decisions

This transforms passive dashboard viewing into active operational intelligence.


# CONTACT

For questions about this submission, contact Team 404 Port Not Found through
the hackathon platform.


# ACKNOWLEDGMENTS

PRAXIS was developed by Team 404 Port Not Found for the PSA Code Sprint 2025 
Hackathon. Special thanks to PSA International for providing the challenge 
and supporting innovation in maritime operations.

"When the port is not found, we build a new route." - Team 404 Port Not Found