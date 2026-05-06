import random
from typing import List, Dict

class Agent:
    """Base class for decision-making agents"""
    
    def __init__(self, name, expertise, bias=None):
        self.name = name
        self.expertise = expertise
        self.bias = bias or []
    
    def make_decision(self, scenario):
        """Make a decision based on scenario"""
        raise NotImplementedError

class HealthcareAgent(Agent):
    """Healthcare expert agent"""
    
    def __init__(self, role):
        super().__init__(
            name=f"Healthcare {role}",
            expertise=['medical', 'triage', 'patient_care'],
            bias=['favor_patient_care', 'risk_averse']
        )
        self.role = role
    
    def make_decision(self, scenario):
        if self.role == 'Chief Medical Officer':
            return {
                'agent': self.name,
                'action': 'Implement Crisis Triage Protocol',
                'actions': [
                    'Activate emergency triage standards',
                    'Convert non-ICU beds to critical care',
                    'Request mutual aid from other hospitals',
                    'Establish field hospital in parking lot'
                ],
                'rationale': 'Maximize patient throughput while maintaining care standards',
                'confidence': 0.85,
                'risks': ['Staff burnout', 'Legal liability', 'Patient complications'],
                'timeline': '2-4 hours'
            }
        elif self.role == 'Resource Manager':
            return {
                'agent': self.name,
                'action': 'Optimize Resource Allocation',
                'actions': [
                    'Commandeer supplies from elective surgery stores',
                    'Activate emergency procurement',
                    'Request state/federal medical supply assistance',
                    'Implement strict resource rationing'
                ],
                'rationale': 'Ensure critical supplies reach maximum patients',
                'confidence': 0.78,
                'risks': ['Supply shortages', 'Delayed delivery', 'Coordination issues'],
                'timeline': '1-3 hours'
            }
        else:
            return {
                'agent': self.name,
                'action': 'Patient Safety Protocol',
                'actions': [
                    'Establish patient communication center',
                    'Begin emergency discharge of stable patients',
                    'Coordinate with clinics for follow-up care'
                ],
                'rationale': 'Safe patient disposition to free beds',
                'confidence': 0.82,
                'risks': ['Patient readmission', 'Liability concerns'],
                'timeline': '3-6 hours'
            }

class DisasterAgent(Agent):
    """Disaster management expert agent"""
    
    def __init__(self, role):
        super().__init__(
            name=f"Disaster {role}",
            expertise=['logistics', 'rescue', 'coordination'],
            bias=['efficiency_focused', 'speed_critical']
        )
        self.role = role
    
    def make_decision(self, scenario):
        if self.role == 'Rescue Commander':
            return {
                'agent': self.name,
                'action': 'Maximize Rescue Operations',
                'actions': [
                    'Deploy rescue teams to highest casualty areas',
                    'Establish triage centers at damage perimeter',
                    'Set up field hospitals',
                    'Coordinate with international rescue teams'
                ],
                'rationale': 'Save maximum lives in critical first 72 hours',
                'confidence': 0.80,
                'risks': ['Rescue team casualties', 'Aftershock dangers', 'Resource depletion'],
                'timeline': '0-6 hours'
            }
        elif self.role == 'Logistics Coordinator':
            return {
                'agent': self.name,
                'action': 'Establish Supply Lines',
                'actions': [
                    'Secure regional supply hubs',
                    'Establish convoy routes',
                    'Coordinate food, water, shelter distribution',
                    'Setup temporary power stations'
                ],
                'rationale': 'Ensure sustained resource flow to affected areas',
                'confidence': 0.75,
                'risks': ['Route blockages', 'Corruption', 'Distribution chaos'],
                'timeline': '6-12 hours'
            }
        else:
            return {
                'agent': self.name,
                'action': 'Public Communication Strategy',
                'actions': [
                    'Establish emergency broadcast system',
                    'Deploy information centers',
                    'Create crisis information hotline',
                    'Manage media and public information'
                ],
                'rationale': 'Reduce panic and ensure population compliance',
                'confidence': 0.77,
                'risks': ['Misinformation spread', 'Public panic', 'Resource misallocation'],
                'timeline': '1-3 hours'
            }

class FinanceAgent(Agent):
    """Financial expert agent"""
    
    def __init__(self, role):
        super().__init__(
            name=f"Finance {role}",
            expertise=['markets', 'risk_management', 'policy'],
            bias=['market_stability', 'systemic_risk_reduction']
        )
        self.role = role
    
    def make_decision(self, scenario):
        if self.role == 'Central Banker':
            return {
                'agent': self.name,
                'action': 'Emergency Monetary Policy',
                'actions': [
                    'Inject emergency liquidity into banking system',
                    'Lower interest rates to zero',
                    'Establish emergency lending facilities',
                    'Guarantee deposits to prevent runs'
                ],
                'rationale': 'Prevent systemic collapse and restore confidence',
                'confidence': 0.88,
                'risks': ['Inflation', 'Asset bubbles', 'Moral hazard'],
                'timeline': '2-4 hours'
            }
        elif self.role == 'Risk Manager':
            return {
                'agent': self.name,
                'action': 'Implement Stabilization Measures',
                'actions': [
                    'Halt short selling',
                    'Suspend mark-to-market accounting',
                    'Implement circuit breakers',
                    'Coordinate with other central banks'
                ],
                'rationale': 'Stop market free fall and stabilize pricing',
                'confidence': 0.82,
                'risks': ['Market manipulation concerns', 'Delayed price discovery'],
                'timeline': '1-2 hours'
            }
        else:
            return {
                'agent': self.name,
                'action': 'Regulatory Response',
                'actions': [
                    'Fast-track regulatory relief',
                    'Implement capital controls if needed',
                    'Coordinate with regulators globally',
                    'Protect essential infrastructure'
                ],
                'rationale': 'Enable normal functioning while preventing contagion',
                'confidence': 0.79,
                'risks': ['Regulatory overreach', 'Unintended consequences'],
                'timeline': '3-6 hours'
            }

class AgentSystem:
    """Multi-agent decision system"""
    
    def __init__(self):
        self.agents = {}
    
    def get_agent_decisions(self, scenario):
        """Get decisions from all relevant agents"""
        scenario_type = scenario.get('type', 'healthcare')
        decisions = []
        
        if scenario_type == 'healthcare':
            agents = [
                HealthcareAgent('Chief Medical Officer'),
                HealthcareAgent('Resource Manager'),
                HealthcareAgent('Patient Advocate')
            ]
        elif scenario_type == 'disaster':
            agents = [
                DisasterAgent('Rescue Commander'),
                DisasterAgent('Logistics Coordinator'),
                DisasterAgent('Communications Officer')
            ]
        elif scenario_type == 'finance':
            agents = [
                FinanceAgent('Central Banker'),
                FinanceAgent('Risk Manager'),
                FinanceAgent('Regulatory Officer')
            ]
        else:
            agents = []
        
        for agent in agents:
            decision = agent.make_decision(scenario)
            decision['agent_expertise'] = agent.expertise
            decision['agent_bias'] = agent.bias
            decisions.append(decision)
        
        return decisions
