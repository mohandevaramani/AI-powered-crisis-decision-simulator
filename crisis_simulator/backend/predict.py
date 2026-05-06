import random
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import json

class OutcomePredictor:
    """Predicts consequences of decision paths probabilistically"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize prediction models"""
        # In a real system, these would be trained on historical data
        self.models = {
            'healthcare': self._create_healthcare_model(),
            'disaster': self._create_disaster_model(),
            'finance': self._create_finance_model()
        }
    
    def _create_healthcare_model(self):
        """Create healthcare outcome prediction model"""
        return {
            'type': 'healthcare',
            'base_factors': {
                'patient_survival_base': 0.92,
                'quality_of_care_factor': 0.8,
                'infection_risk_factor': 0.15
            }
        }
    
    def _create_disaster_model(self):
        """Create disaster outcome prediction model"""
        return {
            'type': 'disaster',
            'base_factors': {
                'rescue_success_base': 0.65,
                'shelter_adequacy_factor': 0.75,
                'resource_availability_factor': 0.7
            }
        }
    
    def _create_finance_model(self):
        """Create finance outcome prediction model"""
        return {
            'type': 'finance',
            'base_factors': {
                'market_recovery_base': 0.55,
                'confidence_restoration_factor': 0.8,
                'systemic_stability_factor': 0.9
            }
        }
    
    def predict_outcomes(self, scenario, agent_decisions):
        """Predict outcomes for each agent decision"""
        scenario_type = scenario.get('type', 'healthcare')
        outcomes = []
        
        for decision in agent_decisions:
            outcome = self._predict_decision_outcome(scenario, decision)
            outcomes.append(outcome)
        
        return outcomes
    
    def _predict_decision_outcome(self, scenario, decision):
        """Predict specific outcome for a decision"""
        scenario_type = scenario.get('type', 'healthcare')
        
        if scenario_type == 'healthcare':
            return self._predict_healthcare_outcome(scenario, decision)
        elif scenario_type == 'disaster':
            return self._predict_disaster_outcome(scenario, decision)
        elif scenario_type == 'finance':
            return self._predict_finance_outcome(scenario, decision)
    
    def _predict_healthcare_outcome(self, scenario, decision):
        """Predict healthcare scenario outcome"""
        variables = scenario.get('variables', {})
        patient_count = variables.get('patient_count', 100)
        icu_available = variables.get('icu_available', 10)
        
        # Base survival probability
        base_survival = 0.92
        
        # Adjust based on resource availability
        if icu_available > 0:
            resource_factor = min(1.0, (icu_available / 50))
        else:
            resource_factor = 0.6
        
        # Factor in agent's decision quality
        agent_confidence = decision.get('confidence', 0.7)
        decision_factor = 0.8 + (agent_confidence * 0.4)  # 0.8 to 1.2 range
        
        # Different outcomes based on agent role
        agent_name = decision.get('agent', '')
        if 'Chief Medical Officer' in agent_name:
            # Triage protocol - better survival but higher resource strain
            survival_modifier = 1.1
            quality_modifier = 1.0
        elif 'Resource Manager' in agent_name:
            # Resource optimization - balanced approach
            survival_modifier = 1.0
            quality_modifier = 1.1
        else:  # Patient Safety
            # Safety focus - slightly lower survival but better quality
            survival_modifier = 0.95
            quality_modifier = 1.15

        predicted_survival_rate = base_survival * resource_factor * decision_factor * survival_modifier
        predicted_survival_rate = min(0.95, max(0.5, predicted_survival_rate))

        # Add some randomization for variability
        random_factor = random.uniform(0.95, 1.05)
        predicted_survival_rate *= random_factor
        predicted_survival_rate = min(0.98, max(0.5, predicted_survival_rate))  # Re-clamp after randomization

        predicted_deaths = int(patient_count * (1 - predicted_survival_rate))
        predicted_recoveries = patient_count - predicted_deaths
        
        # Add uncertainty
        survival_confidence = 0.70 + (resource_factor * 0.20) + (agent_confidence * 0.10)
        
        return {
            'decision': decision['action'],
            'agent': decision['agent'],
            'expected_outcomes': {
                'predicted_recoveries': predicted_recoveries,
                'predicted_deaths': predicted_deaths,
                'survival_rate': round(predicted_survival_rate, 3),
                'quality_of_care_score': round(resource_factor * 10, 2)
            },
            'timeline': '72 hours',
            'confidence_interval': {
                'lower_bound': round(predicted_survival_rate - 0.1, 3),
                'upper_bound': round(predicted_survival_rate + 0.1, 3),
                'confidence': round(survival_confidence, 2)
            },
            'secondary_effects': [
                'Staff exhaustion increases adverse events by 15%',
                'Delayed treatment increases infection risk',
                'Resource scarcity may lead to triage failures'
            ]
        }
    
    def _predict_disaster_outcome(self, scenario, decision):
        """Predict disaster scenario outcome"""
        variables = scenario.get('variables', {})
        affected_pop = variables.get('affected_population', 10000)
        injured = variables.get('injured_count', 500)
        rescue_teams = variables.get('rescue_teams', 20)
        
        # Base rescue efficiency
        base_rescue_rate = 0.65
        
        # Adjust based on rescue teams
        team_factor = min(1.0, (rescue_teams / 50))
        
        # Factor in agent's decision quality
        agent_confidence = decision.get('confidence', 0.7)
        decision_factor = 0.8 + (agent_confidence * 0.4)  # 0.8 to 1.2 range
        
        # Different outcomes based on agent role
        agent_name = decision.get('agent', '')
        if 'Rescue Commander' in agent_name:
            # Rescue focus - higher rescue rate but higher risk
            rescue_modifier = 1.15
            risk_modifier = 1.2
        elif 'Logistics Coordinator' in agent_name:
            # Logistics focus - better resource distribution
            rescue_modifier = 1.05
            risk_modifier = 0.9
        else:  # Communications Officer
            # Communication focus - better coordination
            rescue_modifier = 1.0
            risk_modifier = 0.95
        
        # Calculate outcomes
        predicted_rescue_rate = base_rescue_rate * team_factor * decision_factor * rescue_modifier
        predicted_rescue_rate = min(0.95, max(0.3, predicted_rescue_rate))  # Clamp between 30% and 95%
        
        # Add some randomization for variability
        random_factor = random.uniform(0.92, 1.08)
        predicted_rescue_rate *= random_factor
        predicted_rescue_rate = min(0.95, max(0.3, predicted_rescue_rate))  # Re-clamp after randomization
        
        rescued = int(injured * predicted_rescue_rate)
        mortality = injured - rescued
        
        rescue_confidence = 0.65 + (team_factor * 0.25) + (agent_confidence * 0.10)
        
        return {
            'decision': decision['action'],
            'agent': decision['agent'],
            'expected_outcomes': {
                'rescued_count': rescued,
                'mortality_count': mortality,
                'rescue_rate': round(predicted_rescue_rate, 3),
                'shelter_coverage': round((variables.get('shelter_capacity', 50000) / affected_pop), 2)
            },
            'timeline': '48 hours',
            'confidence_interval': {
                'lower_bound': round(predicted_rescue_rate - 0.15, 3),
                'upper_bound': round(predicted_rescue_rate + 0.15, 3),
                'confidence': round(rescue_confidence, 2)
            },
            'secondary_effects': [
                'Infrastructure damage delays rescue operations by 20-30%',
                'Aftershock risk increases rescue team casualties',
                'Supply delays may increase disease/infection risks'
            ]
        }
    
    def _predict_finance_outcome(self, scenario, decision):
        """Predict finance scenario outcome"""
        variables = scenario.get('variables', {})
        market_index = variables.get('market_index', 75)
        volatility = variables.get('market_volatility', 0.5)
        
        # Base recovery probability
        base_recovery = 0.55
        
        # Adjust based on volatility
        volatility_factor = max(0.3, (1 - volatility))
        
        # Factor in agent's decision quality
        agent_confidence = decision.get('confidence', 0.7)
        decision_factor = 0.8 + (agent_confidence * 0.4)  # 0.8 to 1.2 range
        
        # Different outcomes based on agent role
        agent_name = decision.get('agent', '')
        if 'Risk Manager' in agent_name:
            # Risk management focus - more stable recovery
            recovery_modifier = 1.1
            volatility_modifier = 0.9
        elif 'Market Analyst' in agent_name:
            # Market analysis focus - better market prediction
            recovery_modifier = 1.05
            volatility_modifier = 1.0
        else:  # Policy Advisor
            # Policy focus - better systemic stability
            recovery_modifier = 0.95
            volatility_modifier = 0.85
        
        # Calculate outcomes
        recovery_probability = base_recovery * volatility_factor * decision_factor * recovery_modifier
        recovery_probability = min(0.9, max(0.2, recovery_probability))  # Clamp between 20% and 90%
        
        # Add some randomization for variability
        random_factor = random.uniform(0.9, 1.1)
        recovery_probability *= random_factor
        recovery_probability = min(0.9, max(0.2, recovery_probability))  # Re-clamp after randomization
        
        market_gain = int(market_index * (recovery_probability - 0.5) * 40)
        confidence_restoration = round(recovery_probability * 100, 1)
        
        # Adjust volatility factor for this agent
        adjusted_volatility_factor = volatility_factor * volatility_modifier
        
        return {
            'decision': decision['action'],
            'agent': decision['agent'],
            'expected_outcomes': {
                'market_index_recovery': market_index + market_gain,
                'recovery_probability': round(recovery_probability, 3),
                'confidence_restoration_percent': confidence_restoration,
                'systemic_risk_reduction': round(adjusted_volatility_factor * 100, 1)
            },
            'timeline': '7-14 days',
            'confidence_interval': {
                'lower_bound': round(recovery_probability - 0.12, 3),
                'upper_bound': round(recovery_probability + 0.12, 3),
                'confidence': round(0.72 + (agent_confidence * 0.08), 2)
            },
            'secondary_effects': [
                'Moral hazard may encourage excessive risk-taking',
                'Inflation concerns emerge in 2-3 months',
                'Regulatory changes may be required',
                'Asset bubbles may form in alternative markets'
            ]
        }
    
    def predict_specific_path(self, scenario, decision_path):
        """Predict outcome for a specific decision path"""
        # Combine multiple decisions
        combined_effect = self._combine_decisions(decision_path)
        
        return {
            'path_length': len(decision_path),
            'cumulative_effect': combined_effect,
            'sequential_impact': self._calculate_sequential_impact(decision_path),
            'probability_of_success': round(combined_effect.get('effectiveness', 0.5), 3),
            'time_to_resolution': self._estimate_resolution_time(decision_path)
        }
    
    def _combine_decisions(self, decision_path):
        """Combine effects of multiple decisions"""
        if not decision_path:
            return {'effectiveness': 0.5}
        
        total_effectiveness = 0
        for decision in decision_path:
            effectiveness = random.uniform(0.5, 0.95)
            total_effectiveness += effectiveness
        
        avg_effectiveness = total_effectiveness / len(decision_path)
        
        return {
            'effectiveness': round(avg_effectiveness, 3),
            'decisions_count': len(decision_path),
            'expected_impact': 'High' if avg_effectiveness > 0.75 else ('Medium' if avg_effectiveness > 0.5 else 'Low')
        }
    
    def _calculate_sequential_impact(self, decision_path):
        """Calculate how decisions build on each other"""
        if len(decision_path) <= 1:
            return 0.0
        
        # Decisions in sequence have synergistic or conflicting effects
        synergy = sum([0.05 * i for i in range(len(decision_path)-1)])
        return round(min(0.3, synergy), 3)
    
    def _estimate_resolution_time(self, decision_path):
        """Estimate time to crisis resolution"""
        base_time = 24  # hours
        time_per_decision = 6  # hours
        total_time = base_time + (len(decision_path) * time_per_decision)
        
        return {
            'estimated_hours': total_time,
            'estimated_days': round(total_time / 24, 1)
        }
