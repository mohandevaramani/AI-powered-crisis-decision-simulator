import random
import numpy as np

class RiskAnalyzer:
    """Analyzes risks and uncertainties in decision paths"""
    
    def __init__(self):
        self.risk_factors = {}
    
    def analyze_risks(self, scenario, agent_decisions, outcomes):
        """Analyze risks for all decision paths"""
        scenario_type = scenario.get('type', 'healthcare')
        risks = []
        
        for i, decision in enumerate(agent_decisions):
            outcome = outcomes[i] if i < len(outcomes) else None
            risk_analysis = self._analyze_decision_risk(scenario, decision, outcome)
            risks.append(risk_analysis)
        
        return risks
    
    def _analyze_decision_risk(self, scenario, decision, outcome):
        """Analyze risk for a specific decision"""
        scenario_type = scenario.get('type', 'healthcare')
        
        if scenario_type == 'healthcare':
            return self._analyze_healthcare_risks(scenario, decision, outcome)
        elif scenario_type == 'disaster':
            return self._analyze_disaster_risks(scenario, decision, outcome)
        elif scenario_type == 'finance':
            return self._analyze_finance_risks(scenario, decision, outcome)
    
    def _analyze_healthcare_risks(self, scenario, decision, outcome):
        """Analyze healthcare-specific risks"""
        variables = scenario.get('variables', {})
        identified_risks = []

        # Clinical risks
        icu_available = variables.get('icu_available', 10)
        if icu_available < 20:
            identified_risks.append({
                'risk': 'ICU Capacity Shortage',
                'severity': 'Critical',
                'probability': 0.85,
                'impact': 'Increased mortality rate',
                'mitigation': 'Activate surge capacity protocol'
            })

        # Decision-specific healthcare risks
        if 'Triage Protocol' in decision['action']:
            identified_risks.append({
                'risk': 'Overtriage Risk',
                'severity': 'High',
                'probability': 0.72,
                'impact': 'Unnecessary use of critical care resources',
                'mitigation': 'Refine triage criteria based on severity'
            })
        elif 'Resource Allocation' in decision['action']:
            identified_risks.append({
                'risk': 'Resource Misallocation',
                'severity': 'High',
                'probability': 0.68,
                'impact': 'Critical supplies sent to lower-priority needs',
                'mitigation': 'Continuously reassess allocation priorities'
            })
        else:
            identified_risks.append({
                'risk': 'Discharge Complication Risk',
                'severity': 'Medium',
                'probability': 0.58,
                'impact': 'Increased readmissions and care gaps',
                'mitigation': 'Monitor discharged patients closely'
            })

        # Shared healthcare risks
        identified_risks.extend([
            {
                'risk': 'Healthcare Worker Fatigue',
                'severity': 'High',
                'probability': 0.78,
                'impact': 'Increased medical errors',
                'mitigation': 'Implement mandatory rest periods'
            },
            {
                'risk': 'Supply Chain Disruption',
                'severity': 'High',
                'probability': 0.65,
                'impact': 'Shortage of critical medical supplies',
                'mitigation': 'Activate emergency procurement'
            },
            {
                'risk': 'Coordination Failures',
                'severity': 'Medium',
                'probability': 0.45,
                'impact': 'Delayed treatment, redundant efforts',
                'mitigation': 'Establish clear command structure'
            }
        ])

        identified_risks = self._adjust_risk_probabilities(identified_risks, decision, outcome, 'healthcare')
        aggregate_risk = self._calculate_aggregate_risk(identified_risks)

        return {
            'decision': decision['action'],
            'agent': decision['agent'],
            'identified_risks': identified_risks,
            'aggregate_risk_score': aggregate_risk,
            'risk_level': self._get_risk_level(aggregate_risk),
            'success_probability': round(1 - aggregate_risk / 10, 3),
            'failure_scenarios': self._generate_failure_scenarios('healthcare', identified_risks)
        }

    def _analyze_disaster_risks(self, scenario, decision, outcome):
        """Analyze disaster-specific risks"""
        variables = scenario.get('variables', {})
        identified_risks = []

        # Structural risks
        if variables.get('infrastructure_damage_percent', 50) > 60:
            identified_risks.append({
                'risk': 'Infrastructure Collapse Risk',
                'severity': 'Critical',
                'probability': 0.72,
                'impact': 'Additional casualties, rescue difficulty',
                'mitigation': 'Deploy structural engineers for assessment'
            })

        hours_to_aftershock = variables.get('hours_to_aftershocks', 24)
        aftershock_prob = max(0.3, 1 - (hours_to_aftershock / 48))
        identified_risks.append({
            'risk': 'Aftershock Damage',
            'severity': 'High' if aftershock_prob > 0.6 else 'Medium',
            'probability': aftershock_prob,
            'impact': 'Additional structural damage, rescue team casualties',
            'mitigation': 'Evacuate rescue teams during high-risk periods'
        })

        if 'Rescue Operations' in decision['action']:
            identified_risks.append({
                'risk': 'Rescue Team Exposure',
                'severity': 'High',
                'probability': 0.74,
                'impact': 'Higher injury risk for responders',
                'mitigation': 'Rotate teams and enforce safety protocols'
            })
        elif 'Supply Lines' in decision['action']:
            identified_risks.append({
                'risk': 'Route Blockages',
                'severity': 'Medium',
                'probability': 0.67,
                'impact': 'Delayed aid delivery',
                'mitigation': 'Identify alternate routes and preposition supplies'
            })
        else:
            identified_risks.append({
                'risk': 'Communication Breakdown',
                'severity': 'Medium',
                'probability': 0.60,
                'impact': 'Public panic and misdirected response',
                'mitigation': 'Use redundant communication channels'
            })

        identified_risks.extend([
            {
                'risk': 'Supply Shortages',
                'severity': 'High',
                'probability': 0.68,
                'impact': 'Inadequate food, water, medical supplies',
                'mitigation': 'Establish secure supply chain'
            },
            {
                'risk': 'Security & Looting',
                'severity': 'Medium',
                'probability': 0.55,
                'impact': 'Resource theft, population unrest',
                'mitigation': 'Deploy security forces, establish safe zones'
            }
        ])

        identified_risks = self._adjust_risk_probabilities(identified_risks, decision, outcome, 'disaster')
        aggregate_risk = self._calculate_aggregate_risk(identified_risks)

        return {
            'decision': decision['action'],
            'agent': decision['agent'],
            'identified_risks': identified_risks,
            'aggregate_risk_score': aggregate_risk,
            'risk_level': self._get_risk_level(aggregate_risk),
            'success_probability': round(1 - aggregate_risk / 10, 3),
            'failure_scenarios': self._generate_failure_scenarios('disaster', identified_risks)
        }

    def _analyze_finance_risks(self, scenario, decision, outcome):
        """Analyze finance-specific risks"""
        variables = scenario.get('variables', {})
        identified_risks = []

        volatility = variables.get('market_volatility', 0.5)
        identified_risks.append({
            'risk': 'Continued Market Volatility',
            'severity': 'Critical' if volatility > 0.6 else 'High',
            'probability': volatility,
            'impact': 'Further market decline, confidence erosion',
            'mitigation': 'Implement circuit breakers, announce support measures'
        })

        days_to_default = variables.get('days_until_default', 10)
        default_prob = max(0.2, 1 - (days_to_default / 15))
        identified_risks.append({
            'risk': 'Systemic Banking Collapse',
            'severity': 'Critical',
            'probability': default_prob,
            'impact': 'Economic recession, unemployment spike',
            'mitigation': 'Central bank emergency support, regulatory relaxation'
        })

        if 'Monetary Policy' in decision['action']:
            identified_risks.append({
                'risk': 'Inflation Surge',
                'severity': 'High',
                'probability': 0.66,
                'impact': 'Higher prices from excessive liquidity',
                'mitigation': 'Tighten policy once stability returns'
            })
        elif 'Stabilization Measures' in decision['action']:
            identified_risks.append({
                'risk': 'Market Distortion',
                'severity': 'Medium',
                'probability': 0.58,
                'impact': 'Reduced price discovery',
                'mitigation': 'Gradually unwind emergency measures'
            })
        else:
            identified_risks.append({
                'risk': 'Regulatory Overreach',
                'severity': 'Medium',
                'probability': 0.54,
                'impact': 'Unintended financial distortions',
                'mitigation': 'Calibrate policy actions with market feedback'
            })

        identified_risks.extend([
            {
                'risk': 'International Contagion',
                'severity': 'High',
                'probability': 0.72,
                'impact': 'Global recession, emerging market crisis',
                'mitigation': 'Coordinate with international central banks'
            },
            {
                'risk': 'Moral Hazard',
                'severity': 'Medium',
                'probability': 0.50,
                'impact': 'Future excessive risk-taking by institutions',
                'mitigation': 'Structure support with conditions and clawbacks'
            }
        ])

        identified_risks = self._adjust_risk_probabilities(identified_risks, decision, outcome, 'finance')
        aggregate_risk = self._calculate_aggregate_risk(identified_risks)

        return {
            'decision': decision['action'],
            'agent': decision['agent'],
            'identified_risks': identified_risks,
            'aggregate_risk_score': aggregate_risk,
            'risk_level': self._get_risk_level(aggregate_risk),
            'success_probability': round(1 - aggregate_risk / 10, 3),
            'failure_scenarios': self._generate_failure_scenarios('finance', identified_risks)
        }
    
    def _severity_to_score(self, severity):
        """Convert severity level to numeric score"""
        severity_map = {
            'Critical': 10,
            'High': 7,
            'Medium': 5,
            'Low': 3
        }
        return severity_map.get(severity, 5)

    def _calculate_aggregate_risk(self, identified_risks):
        """Compute aggregate risk score from identified risks."""
        risk_scores = [r['probability'] * self._severity_to_score(r['severity'])
                       for r in identified_risks]
        return round(sum(risk_scores) / len(risk_scores), 3)

    def _adjust_risk_probabilities(self, identified_risks, decision, outcome, scenario_type):
        """Adjust risk probabilities based on decision confidence and outcome."""
        confidence = decision.get('confidence', 0.7)
        decision_modifier = 1.0 - ((confidence - 0.7) * 0.25)

        if outcome and isinstance(outcome.get('expected_outcomes'), dict):
            outcome_metrics = outcome['expected_outcomes']
            if scenario_type == 'healthcare' and 'survival_rate' in outcome_metrics:
                survival = outcome_metrics['survival_rate']
                decision_modifier *= 1.0 - ((survival - 0.75) * 0.2)
            elif scenario_type == 'disaster' and 'rescue_rate' in outcome_metrics:
                rescue = outcome_metrics['rescue_rate']
                decision_modifier *= 1.0 - ((rescue - 0.6) * 0.18)
            elif scenario_type == 'finance' and 'recovery_probability' in outcome_metrics:
                recovery = outcome_metrics['recovery_probability']
                decision_modifier *= 1.0 - ((recovery - 0.55) * 0.2)

        adjusted_risks = []
        for risk in identified_risks:
            probability = risk['probability'] * decision_modifier
            probability = max(0.1, min(0.95, round(probability, 3)))
            adjusted_risks.append({**risk, 'probability': probability})

        return adjusted_risks

    def _get_risk_level(self, aggregate_score):
        """Determine overall risk level"""
        if aggregate_score >= 8:
            return 'Critical'
        elif aggregate_score >= 6:
            return 'High'
        elif aggregate_score >= 4:
            return 'Medium'
        else:
            return 'Low'
    
    def _generate_failure_scenarios(self, scenario_type, risks):
        """Generate potential failure scenarios"""
        worst_case = []
        if scenario_type == 'healthcare':
            worst_case = [
                'System overwhelmed, triage protocol fails',
                'Supply shortages lead to equipment rationing',
                'Staff strike or mass resignation',
                'Hospital-acquired infections spike'
            ]
        elif scenario_type == 'disaster':
            worst_case = [
                'Aftershock triggers secondary collapse',
                'Supply chain completely severed',
                'Security breakdown leads to chaos',
                'Disease outbreak in shelter areas'
            ]
        elif scenario_type == 'finance':
            worst_case = [
                'Bank run despite intervention',
                'Market continues free fall',
                'Credit market freezes completely',
                'Global recession triggered'
            ]
        
        return worst_case
    
    def analyze_specific_path(self, scenario, decision_path, outcome):
        """Analyze risk for a specific decision path"""
        # Accumulate risks across decision sequence
        cumulative_risk = 0
        decision_risks = []
        
        for decision in decision_path:
            decision_risk = random.uniform(0.3, 0.8)
            cumulative_risk += decision_risk
            decision_risks.append(decision_risk)
        
        avg_risk = cumulative_risk / len(decision_path) if decision_path else 0
        
        return {
            'path_risk_level': self._get_risk_level(avg_risk * 10),
            'average_decision_risk': round(avg_risk, 3),
            'cumulative_uncertainty': round(cumulative_risk, 3),
            'decision_sequence_risks': [round(r, 3) for r in decision_risks],
            'dependency_risks': self._analyze_dependencies(decision_path),
            'confidence_in_prediction': round(0.6 + (0.4 * (1 - avg_risk)), 3)
        }
    
    def _analyze_dependencies(self, decision_path):
        """Analyze how decisions depend on each other"""
        if len(decision_path) <= 1:
            return 'No dependencies'
        
        return 'Sequential decisions: each depends on previous execution success'
