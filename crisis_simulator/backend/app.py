import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from scenario import ScenarioGenerator
from agent import AgentSystem
from predict import OutcomePredictor
from risk import RiskAnalyzer
from explain import DecisionExplainer
import json

frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
app = Flask(__name__, static_folder=frontend_dir, template_folder=frontend_dir)
CORS(app)

# Initialize system components
scenario_gen = ScenarioGenerator()
agent_system = AgentSystem()
outcome_predictor = OutcomePredictor()
risk_analyzer = RiskAnalyzer()
explainer = DecisionExplainer()

@app.route('/api/scenarios', methods=['GET'])
def get_scenarios():
    """Get available crisis scenarios"""
    scenarios = scenario_gen.get_available_scenarios()
    return jsonify(scenarios)

@app.route('/api/scenarios', methods=['POST'])
def add_scenario():
    """Add a new custom crisis scenario definition"""
    data = request.json or {}
    title = data.get('title')
    description = data.get('description')
    if not title or not description:
        return jsonify({'success': False, 'message': 'Title and description are required.'}), 400

    scenario = scenario_gen.add_custom_scenario({
        'title': title,
        'description': description,
        'severity': data.get('severity', 'high'),
        'timeline': data.get('timeline', 'Next 48 hours'),
        'affected_people': data.get('affected_people', 0),
        'budget_impact': data.get('budget_impact', ''),
        'constraints': data.get('constraints', [])
    })

    return jsonify({'success': True, 'scenario': scenario})

@app.route('/api/simulate', methods=['POST'])
def simulate_crisis():
    """Simulate a crisis scenario with multi-agent decision paths"""
    data = request.json
    scenario_type = data.get('scenario_type', 'healthcare')
    
    # Generate scenario
    if scenario_type.startswith('saved:'):
        scenario_id = scenario_type.split(':', 1)[1]
        saved_scenario = scenario_gen.get_saved_scenario(scenario_id)
        if saved_scenario:
            scenario = scenario_gen.generate_scenario('custom', saved_scenario.get('custom_data', {}))
        else:
            scenario = scenario_gen.generate_scenario('healthcare')
    elif scenario_type == 'custom':
        custom_data = {
            'title': data.get('title'),
            'severity': data.get('severity'),
            'description': data.get('description'),
            'timeline': data.get('timeline'),
            'affected_people': data.get('affected_people'),
            'budget_impact': data.get('budget_impact'),
            'constraints': data.get('constraints', [])
        }
        scenario = scenario_gen.generate_scenario(scenario_type, custom_data)
    else:
        scenario = scenario_gen.generate_scenario(scenario_type)
        
        # Override specific fields if custom input provided
        custom_type = data.get('custom_type')
        if custom_type:
            if scenario_type == 'healthcare':
                scenario['disease_name'] = custom_type
            elif scenario_type == 'disaster':
                scenario['disaster_type'] = custom_type
            elif scenario_type == 'finance':
                scenario['crisis_type'] = custom_type
    
    # Get agent recommendations
    agent_decisions = agent_system.get_agent_decisions(scenario)
    
    # Predict outcomes for each decision path
    outcomes = outcome_predictor.predict_outcomes(
        scenario, 
        agent_decisions
    )
    
    # Analyze risks
    risks = risk_analyzer.analyze_risks(
        scenario, 
        agent_decisions, 
        outcomes
    )
    
    # Get explanations
    explanations = explainer.explain_decisions(
        scenario,
        agent_decisions,
        outcomes,
        risks
    )
    
    return jsonify({
        'scenario': scenario,
        'agent_decisions': agent_decisions,
        'outcomes': outcomes,
        'risks': risks,
        'explanations': explanations
    })

@app.route('/api/decision-path', methods=['POST'])
def evaluate_decision_path():
    """Evaluate a specific decision path"""
    data = request.json
    scenario = data.get('scenario')
    decision_path = data.get('decision_path', [])
    
    # Predict outcomes for the specific path
    outcome = outcome_predictor.predict_specific_path(scenario, decision_path)
    
    # Analyze risk for this path
    risk = risk_analyzer.analyze_specific_path(scenario, decision_path, outcome)
    
    # Get detailed explanation
    explanation = explainer.explain_path(scenario, decision_path, outcome, risk)
    
    return jsonify({
        'outcome': outcome,
        'risk': risk,
        'explanation': explanation
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Crisis Decision Simulator API is running'})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """Serve the frontend login page and static assets."""
    if path and os.path.exists(os.path.join(frontend_dir, path)):
        return send_from_directory(frontend_dir, path)
    return send_from_directory(frontend_dir, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
