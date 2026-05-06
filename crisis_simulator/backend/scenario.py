import random
import json
from datetime import datetime, timedelta

class ScenarioGenerator:
    """Generates dynamic crisis scenarios with real-world constraints"""
    
    def __init__(self):
        self.scenario_templates = {
            'healthcare': {
                'name': 'Healthcare Crisis',
                'description': 'Medical emergency or disease outbreak scenario',
                'variables': ['patient_count', 'severity', 'resource_availability', 'time_remaining']
            },
            'disaster': {
                'name': 'Natural Disaster',
                'description': 'Earthquake, flood, hurricane, or similar event',
                'variables': ['affected_population', 'infrastructure_damage', 'supply_status', 'rescue_capability']
            },
            'finance': {
                'name': 'Financial Crisis',
                'description': 'Market crash, banking collapse, or liquidity crisis',
                'variables': ['market_volatility', 'liquidity_level', 'asset_value', 'time_to_collapse']
            },
            'custom': {
                'name': 'Custom Crisis',
                'description': 'User-defined crisis scenario',
                'variables': ['title', 'severity', 'description', 'timeline', 'affected_people', 'budget_impact', 'constraints']
            }
        }
        self.saved_scenarios = []
        self.next_custom_id = 1
    
    def get_available_scenarios(self):
        """Return available scenario types"""
        return {
            'types': list(self.scenario_templates.keys()),
            'details': self.scenario_templates,
            'custom_scenarios': self.saved_scenarios,
            'custom_scenarios': self.saved_scenarios
        }
    
    def get_saved_scenario(self, scenario_id):
        """Return a previously saved custom scenario by id"""
        for scenario in self.saved_scenarios:
            if scenario.get('id') == scenario_id:
                return scenario
        return None

    def add_custom_scenario(self, custom_data):
        """Save a new custom scenario definition"""
        scenario_id = f'custom_{self.next_custom_id}'
        self.next_custom_id += 1
        severity = custom_data.get('severity', 'high')
        new_scenario = {
            'id': scenario_id,
            'title': custom_data.get('title', 'Custom Crisis Scenario'),
            'description': custom_data.get('description', 'User-defined crisis scenario'),
            'severity': severity,
            'timeline': custom_data.get('timeline', 'Next 48 hours'),
            'affected_people': custom_data.get('affected_people', 0),
            'budget_impact': custom_data.get('budget_impact', ''),
            'constraints': custom_data.get('constraints', []),
            'custom_data': custom_data
        }
        self.saved_scenarios.append(new_scenario)
        return new_scenario

    def generate_scenario(self, scenario_type='healthcare', custom_data=None):
        """Generate a specific crisis scenario"""
        if scenario_type == 'custom':
            return self._generate_custom_scenario(custom_data)
        elif scenario_type not in self.scenario_templates:
            scenario_type = 'healthcare'
        
        template = self.scenario_templates[scenario_type]
        
        if scenario_type == 'healthcare':
            return self._generate_healthcare_scenario()
        elif scenario_type == 'disaster':
            return self._generate_disaster_scenario()
        elif scenario_type == 'finance':
            return self._generate_finance_scenario()
    
    def _generate_healthcare_scenario(self):
        """Generate healthcare crisis scenario"""
        disease_name = random.choice([
            'Novel Respiratory Virus',
            'Antibiotic-Resistant Bacterial Outbreak',
            'Vector-Borne Disease Surge'
        ])
        disease_type = random.choice([
            'Infectious Disease',
            'Respiratory Illness',
            'Contagious Outbreak'
        ])
        return {
            'type': 'healthcare',
            'title': f'{disease_name} - Hospital Overload',
            'description': 'A surge in infectious disease cases has overwhelmed hospital capacity',
            'disease_name': disease_name,
            'disease_type': disease_type,
            'timestamp': datetime.now().isoformat(),
            'severity': random.choice(['high', 'critical']),
            'variables': {
                'patient_count': random.randint(500, 2000),
                'icu_capacity': random.randint(50, 150),
                'icu_available': random.randint(5, 40),
                'ventilators': random.randint(100, 300),
                'ventilators_available': random.randint(10, 60),
                'staff_hours_available': random.randint(100, 500),
                'mortality_rate': round(random.uniform(0.02, 0.15), 3),
                'recovery_time_days': random.randint(10, 30)
            },
            'constraints': [
                'Limited ICU beds',
                'Staff exhaustion',
                'Supply chain disruption',
                'Decision time: 24 hours'
            ],
            'timeline': 'Next 72 hours critical'
        }
    
    def _generate_disaster_scenario(self):
        """Generate natural disaster scenario"""
        disaster_type = random.choice([
            'Earthquake',
            'Flood',
            'Hurricane',
            'Wildfire',
            'Tsunami'
        ])
        affected_pop = random.randint(10000, 500000)
        return {
            'type': 'disaster',
            'title': f'{disaster_type} - Emergency Response',
            'description': f'Significant {disaster_type.lower()} has caused widespread damage and displacement',
            'disaster_type': disaster_type,
            'timestamp': datetime.now().isoformat(),
            'severity': random.choice(['critical', 'extreme']),
            'variables': {
                'affected_population': affected_pop,
                'injured_count': random.randint(int(affected_pop * 0.01), int(affected_pop * 0.1)),
                'infrastructure_damage_percent': random.randint(30, 80),
                'accessible_shelters': random.randint(50, 500),
                'shelter_capacity': random.randint(10000, 100000),
                'aid_available_tons': random.randint(50, 500),
                'rescue_teams': random.randint(10, 100),
                'hours_to_aftershocks': random.randint(6, 48)
            },
            'constraints': [
                'Limited rescue resources',
                'Infrastructure damage affects logistics',
                'Weather conditions deteriorating',
                'Decision time: 6 hours'
            ],
            'timeline': 'Next 48 hours critical'
        }
    
    def _generate_finance_scenario(self):
        """Generate financial crisis scenario"""
        crisis_type = random.choice([
            'Bank Run',
            'Currency Collapse',
            'Credit Crunch',
            'Stock Market Crash',
            'Sovereign Debt Crisis'
        ])
        return {
            'type': 'finance',
            'title': f'{crisis_type} - Liquidity Crisis',
            'description': f'Major financial sector stress from a {crisis_type.lower()}',
            'crisis_type': crisis_type,
            'timestamp': datetime.now().isoformat(),
            'severity': random.choice(['high', 'critical']),
            'variables': {
                'market_index': random.randint(60, 85),
                'market_volatility': round(random.uniform(0.3, 0.8), 2),
                'cash_reserves_billion': random.randint(10, 50),
                'daily_withdrawal_rate': round(random.uniform(0.05, 0.20), 2),
                'days_until_default': random.randint(5, 15),
                'credit_rating': random.choice(['BBB-', 'BB+', 'BB', 'B+']),
                'investor_confidence': round(random.uniform(0.2, 0.5), 2)
            },
            'constraints': [
                'Limited government intervention options',
                'Market panic spreading',
                'International market uncertainty',
                'Decision time: 12 hours'
            ],
            'timeline': 'Next 7 days critical'
        }
    
    def _generate_custom_scenario(self, custom_data):
        """Generate custom crisis scenario based on user input"""
        if not custom_data:
            return self._generate_healthcare_scenario()  # fallback
        
        # Map severity to standard levels
        severity_map = {
            'high': 'high',
            'critical': 'critical', 
            'extreme': 'extreme'
        }
        
        severity = severity_map.get(custom_data.get('severity', 'high'), 'high')
        
        # Generate dynamic variables based on user input
        variables = {}
        
        # Affected people
        affected_people = custom_data.get('affected_people', 1000)
        variables['affected_population'] = affected_people
        variables['population_density'] = round(affected_people / random.uniform(10, 100), 1)
        
        # Budget impact
        budget_str = custom_data.get('budget_impact', '$10M')
        # Extract numeric value from budget string
        import re
        budget_match = re.search(r'[\d,]+(?:\.\d+)?', budget_str.replace('$', '').replace('M', '000000').replace('B', '000000000'))
        budget_value = int(float(budget_match.group()) * 1000000) if budget_match else 10000000
        variables['budget_impact_million'] = budget_value // 1000000
        variables['economic_impact_score'] = min(100, budget_value // 100000)
        
        # Timeline
        timeline = custom_data.get('timeline', 'Next 48 hours')
        if 'hour' in timeline.lower():
            hours = int(re.search(r'\d+', timeline).group()) if re.search(r'\d+', timeline) else 48
            variables['time_remaining_hours'] = hours
            variables['urgency_level'] = 'critical' if hours < 24 else 'high'
        elif 'day' in timeline.lower():
            days = int(re.search(r'\d+', timeline).group()) if re.search(r'\d+', timeline) else 7
            variables['time_remaining_days'] = days
            variables['urgency_level'] = 'high' if days < 3 else 'medium'
        else:
            variables['time_remaining_hours'] = 48
            variables['urgency_level'] = 'high'
        
        # Constraints
        user_constraints = custom_data.get('constraints', [])
        default_constraints = [
            'Limited resources available',
            'Time pressure critical',
            'Public communication needed',
            'Stakeholder coordination required'
        ]
        constraints = user_constraints + default_constraints if user_constraints else default_constraints
        
        return {
            'type': 'custom',
            'title': custom_data.get('title', 'Custom Crisis Scenario'),
            'description': custom_data.get('description', 'User-defined crisis scenario'),
            'crisis_type': custom_data.get('title', 'Custom Crisis'),
            'timestamp': datetime.now().isoformat(),
            'severity': severity,
            'variables': variables,
            'constraints': constraints[:6],  # Limit to 6 constraints
            'timeline': timeline,
            'user_defined': True
        }
