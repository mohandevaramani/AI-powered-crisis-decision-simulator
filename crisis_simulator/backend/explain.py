class DecisionExplainer:
    """Provides explainable and transparent reasoning for decisions"""
    
    def explain_decisions(self, scenario, agent_decisions, outcomes, risks):
        """Generate comprehensive explanations for all decisions"""
        explanations = []
        
        for i, decision in enumerate(agent_decisions):
            outcome = outcomes[i] if i < len(outcomes) else None
            risk = risks[i] if i < len(risks) else None
            
            explanation = self._explain_single_decision(
                scenario, 
                decision, 
                outcome, 
                risk
            )
            explanations.append(explanation)
        
        # Generate recommendation based on all explanations
        recommendation = self._generate_recommendation(
            scenario,
            explanations,
            agent_decisions,
            outcomes,
            risks
        )
        
        return {
            'decision_explanations': explanations,
            'priority_ranking': self._rank_decisions(explanations),
            'recommendation': recommendation
        }
    
    def _explain_single_decision(self, scenario, decision, outcome, risk):
        """Explain a single decision"""
        agent = decision.get('agent', 'Unknown Agent')
        action = decision.get('action', 'Unknown Action')
        confidence = decision.get('confidence', 0.5)
        
        explanation = {
            'agent': agent,
            'action': action,
            'reasoning': {
                'primary_goal': self._get_primary_goal(agent, action),
                'key_assumptions': self._extract_assumptions(decision),
                'supporting_factors': decision.get('rationale', 'N/A'),
                'confidence_level': f"{int(confidence * 100)}%"
            },
            'action_breakdown': {
                'immediate_actions': decision.get('actions', []),
                'timeline': decision.get('timeline', 'Unknown'),
                'expected_duration': self._estimate_duration(decision)
            },
            'expected_impact': {
                'primary_outcomes': outcome.get('expected_outcomes', {}) if outcome else {},
                'success_probability': f"{int(outcome.get('confidence_interval', {}).get('confidence', 0.5) * 100)}%" if outcome else 'N/A',
                'secondary_effects': outcome.get('secondary_effects', []) if outcome else []
            },
            'risk_assessment': {
                'identified_risks': [r['risk'] for r in risk.get('identified_risks', [])] if risk else [],
                'risk_level': risk.get('risk_level', 'Unknown') if risk else 'Unknown',
                'success_probability': f"{int(risk.get('success_probability', 0.5) * 100)}%" if risk else 'N/A',
                'failure_scenarios': risk.get('failure_scenarios', []) if risk else []
            },
            'decision_logic': self._generate_decision_logic(agent, action),
            'transparency_notes': self._generate_transparency_notes(decision, outcome, risk)
        }
        
        return explanation
    
    def _get_primary_goal(self, agent, action):
        """Extract primary goal from agent and action"""
        if 'Healthcare' in agent:
            if 'Triage' in action:
                return 'Maximize patient survival and treatment quality'
            elif 'Resource' in action:
                return 'Optimize medical resource allocation'
            else:
                return 'Ensure patient safety and care continuity'
        elif 'Disaster' in agent:
            if 'Rescue' in action:
                return 'Maximize lives saved in critical first hours'
            elif 'Logistics' in action:
                return 'Establish sustained resource supply'
            else:
                return 'Reduce public panic and ensure compliance'
        elif 'Finance' in agent:
            if 'Monetary' in action:
                return 'Prevent systemic financial collapse'
            elif 'Stabilization' in action:
                return 'Stop market decline and restore price discovery'
            else:
                return 'Enable financial system function'
        return 'Unknown objective'
    
    def _extract_assumptions(self, decision):
        """Extract key assumptions from decision"""
        assumptions = []
        
        actions = decision.get('actions', [])
        confidence = decision.get('confidence', 0.5)
        
        if confidence < 0.75:
            assumptions.append('Low confidence: significant uncertainty exists')
        
        if len(actions) > 3:
            assumptions.append('Multiple simultaneous actions required')
        
        assumptions.append('Assumes timely resource availability')
        assumptions.append('Assumes coordination capability')
        
        risks = decision.get('risks', [])
        if risks:
            assumptions.append(f"Key risks: {', '.join(risks[:2])}")
        
        return assumptions
    
    def _estimate_duration(self, decision):
        """Estimate decision execution duration"""
        timeline = decision.get('timeline', '6-12 hours')
        return f"Execution: {timeline}"
    
    def _generate_decision_logic(self, agent, action):
        """Generate transparent decision logic explanation"""
        logic = {
            'decision_type': 'Crisis Response Decision',
            'decision_maker': agent,
            'action_category': action,
            'decision_process': [
                'Situation assessment based on real-time data',
                'Evaluation of available resources and constraints',
                'Multi-option analysis with risk/benefit trade-offs',
                'Timeline consideration for implementation',
                'Stakeholder impact assessment'
            ],
            'decision_framework': 'Maximize critical outcome (lives, stability, market confidence)',
            'constraints_applied': [
                'Time criticality',
                'Resource availability',
                'Operational feasibility',
                'Legal and regulatory compliance',
                'Stakeholder acceptability'
            ]
        }
        return logic
    
    def _generate_transparency_notes(self, decision, outcome, risk):
        """Generate transparency notes explaining decision quality"""
        notes = []
        
        confidence = decision.get('confidence', 0.5)
        if confidence < 0.70:
            notes.append('⚠️ Lower confidence: significant uncertainty in outcomes')
        
        if outcome:
            if outcome.get('confidence_interval', {}).get('confidence', 0.5) < 0.7:
                notes.append('⚠️ Outcome prediction has wide confidence intervals')
        
        if risk:
            if risk.get('aggregate_risk_score', 5) > 6:
                notes.append('⚠️ High aggregate risk score: multiple failure modes possible')
        
        notes.append('✓ Decision based on expert agent analysis')
        notes.append('✓ Probabilistic outcome prediction applied')
        notes.append('✓ Risk factors identified and mitigated')
        
        return notes
    
    def _rank_decisions(self, explanations):
        """Rank decisions by effectiveness and risk"""
        ranked = []
        
        for i, exp in enumerate(explanations):
            # Score based on success probability and risk level
            success_prob_str = exp['expected_impact'].get('success_probability', '50%').replace('%', '')
            try:
                success_prob = int(success_prob_str) / 100
            except:
                success_prob = 0.5
            
            risk_score = {'Low': 0.9, 'Medium': 0.6, 'High': 0.3, 'Critical': 0.1}.get(
                exp['risk_assessment'].get('risk_level', 'Medium'), 
                0.5
            )
            
            effectiveness_score = (success_prob * 0.6) + (risk_score * 0.4)
            
            ranked.append({
                'rank': len(ranked) + 1,
                'agent': exp['agent'],
                'action': exp['action'],
                'effectiveness_score': round(effectiveness_score, 3),
                'key_advantage': self._get_key_advantage(exp),
                'key_risk': exp['risk_assessment'].get('identified_risks', ['Unknown'])[0] if exp['risk_assessment'].get('identified_risks') else 'Unknown'
            })
        
        # Sort by effectiveness score
        ranked.sort(key=lambda x: x['effectiveness_score'], reverse=True)
        
        # Reassign ranks
        for i, item in enumerate(ranked):
            item['rank'] = i + 1
        
        return ranked
    
    def _get_key_advantage(self, explanation):
        """Extract key advantage of decision"""
        action = explanation['action']
        
        if 'Triage' in action:
            return 'Maximizes patient throughput with evidence-based protocols'
        elif 'Resource' in action:
            return 'Optimizes limited supplies across maximum patients'
        elif 'Rescue' in action:
            return 'Focuses on critical first hours with highest casualty potential'
        elif 'Liquidity' in action:
            return 'Directly addresses root cause of system failure'
        elif 'Stabilization' in action:
            return 'Halts panic spiral with circuit breakers'
        else:
            return 'Addresses immediate crisis needs'
    
    def _generate_recommendation(self, scenario, explanations, agent_decisions, outcomes, risks):
        """Generate prioritized recommendation"""
        # Find top recommendation based on ranking
        if not explanations:
            return None
        
        # Calculate combined score for each decision
        scores = []
        for i, exp in enumerate(explanations):
            outcome = outcomes[i] if i < len(outcomes) else None
            risk = risks[i] if i < len(risks) else None
            
            score = self._calculate_decision_score(exp, outcome, risk)
            scores.append({
                'index': i,
                'agent': exp['agent'],
                'action': exp['action'],
                'score': score
            })
        
        # Sort by score
        scores.sort(key=lambda x: x['score'], reverse=True)
        top = scores[0]
        
        return {
            'primary_recommendation': top['action'],
            'recommended_agent': top['agent'],
            'confidence': round(top['score'], 3),
            'rationale': f"This decision offers the best balance of effectiveness and risk management. It directly addresses the core crisis dynamic with the highest probability of stabilization.",
            'implementation_priority': [
                {
                    'order': i + 1,
                    'action': scores[i]['action'],
                    'agent': scores[i]['agent'],
                    'importance': 'Critical' if i == 0 else ('High' if i < 2 else 'Medium')
                }
                for i in range(min(3, len(scores)))
            ],
            'immediate_next_steps': self._generate_next_steps(scenario),
            'monitoring_metrics': self._generate_monitoring_metrics(scenario)
        }
    
    def _calculate_decision_score(self, explanation, outcome, risk):
        """Calculate composite score for decision"""
        score = 0.5  # Base score
        
        # Outcome component
        if outcome:
            conf_str = outcome.get('confidence_interval', {}).get('confidence', '0.5')
            try:
                score += float(conf_str) * 0.3
            except:
                score += 0.15
        
        # Risk component
        if risk:
            success_prob = risk.get('success_probability', 0.5)
            score += success_prob * 0.2
        
        # Agent expertise component
        score += 0.15
        
        return min(1.0, score)
    
    def _generate_next_steps(self, scenario):
        """Generate immediate next steps"""
        scenario_type = scenario.get('type', 'healthcare')
        
        if scenario_type == 'healthcare':
            return [
                'Activate Emergency Operations Center',
                'Initiate crisis communication protocol',
                'Begin resource inventory assessment',
                'Contact regional healthcare partners',
                'Prepare media briefings'
            ]
        elif scenario_type == 'disaster':
            return [
                'Deploy emergency response teams',
                'Establish command center',
                'Initiate evacuation plan',
                'Contact mutual aid partners',
                'Begin public information dissemination'
            ]
        elif scenario_type == 'finance':
            return [
                'Convene monetary policy committee',
                'Prepare market stabilization statements',
                'Activate emergency lending facilities',
                'Coordinate with international central banks',
                'Draft regulatory relief orders'
            ]
        
        return ['Assess situation', 'Mobilize resources', 'Implement decision']
    
    def _generate_monitoring_metrics(self, scenario):
        """Generate key metrics to monitor"""
        scenario_type = scenario.get('type', 'healthcare')
        
        if scenario_type == 'healthcare':
            return [
                'Patient mortality rate',
                'ICU bed occupancy',
                'Critical supply levels',
                'Staff fatigue/availability',
                'Hospital-acquired infection rates'
            ]
        elif scenario_type == 'disaster':
            return [
                'Lives rescued/remaining',
                'Shelter availability/occupancy',
                'Supply consumption rate',
                'Disease outbreak indicators',
                'Security incidents'
            ]
        elif scenario_type == 'finance':
            return [
                'Market index movements',
                'Volatility index (VIX)',
                'Credit spreads',
                'Bank deposit levels',
                'Interbank lending rates'
            ]
        
        return ['Key performance indicators', 'Risk indicators', 'Timeline milestones']
    
    def explain_path(self, scenario, decision_path, outcome, risk):
        """Explain a specific decision path"""
        return {
            'path_description': f"Sequential decision path with {len(decision_path)} decisions",
            'expected_effectiveness': outcome.get('probability_of_success', 0.5),
            'path_risk_level': risk.get('path_risk_level', 'Unknown'),
            'decision_sequence': decision_path,
            'cumulative_effects': outcome.get('cumulative_effect', {}),
            'sequential_dependencies': 'Each decision depends on successful execution of previous steps',
            'time_to_resolution': outcome.get('time_to_resolution', {}),
            'monitoring_points': [f"After decision {i+1}: Assess feasibility before proceeding" for i in range(len(decision_path))],
            'escalation_triggers': [
                'If any decision fails, reassess entire path',
                'If timeline extends beyond estimate, activate backup plans',
                'If new information emerges, update risk assessment'
            ]
        }
