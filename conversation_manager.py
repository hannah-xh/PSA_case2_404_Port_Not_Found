from typing import List, Dict, Optional
from datetime import datetime
import json

class ConversationManager:
    def __init__(self):
        self.history: List[Dict] = []
        self.context = {
            'user_focus': [],
            'operators_mentioned': set(),
            'vessels_mentioned': set(),
            'current_topic': None,
            'decision_context': {}
        }
        self.max_history = 10
        
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        self.history.append(message)
        
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        
        if role == 'user':
            self._update_context(content)
    
    def _update_context(self, user_input: str):
        operators = ['GRN', 'NVX', 'DPT', 'EVO', 'SVQ', 'AZQ', 'UVX', 'BLX', 'OPR', 'CRY']
        
        for op in operators:
            if op in user_input.upper():
                self.context['operators_mentioned'].add(op)
        
        keywords = {
            'performance': ['performance', 'efficiency', 'score'],
            'comparison': ['compare', 'versus', 'vs', 'between'],
            'carbon': ['carbon', 'emission', 'environmental'],
            'cost': ['cost', 'bunker', 'savings'],
            'delay': ['delay', 'wait', 'late']
        }
        
        for topic, words in keywords.items():
            if any(word in user_input.lower() for word in words):
                self.context['current_topic'] = topic
                break
    
    def get_conversation_context(self) -> str:
        if not self.history:
            return ""
        
        recent = self.history[-3:]
        context_str = "Recent conversation:\n"
        
        for msg in recent:
            context_str += f"{msg['role']}: {msg['content'][:100]}...\n"
        
        if self.context['operators_mentioned']:
            context_str += f"\nOperators discussed: {', '.join(self.context['operators_mentioned'])}\n"
        
        if self.context['current_topic']:
            context_str += f"Current topic: {self.context['current_topic']}\n"
        
        return context_str
    
    def infer_intent(self, user_input: str) -> Dict[str, any]:
        intent = {
            'type': 'general',
            'entities': {
                'operators': [],
                'comparison': False,
                'time_period': None
            },
            'requires_data': True
        }
        
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['compare', 'versus', 'vs', 'between', 'difference']):
            intent['type'] = 'comparison'
            intent['entities']['comparison'] = True
        elif any(word in user_lower for word in ['top', 'best', 'worst', 'rank']):
            intent['type'] = 'ranking'
        elif any(word in user_lower for word in ['predict', 'forecast', 'expect', 'will']):
            intent['type'] = 'prediction'
        elif any(word in user_lower for word in ['recommend', 'suggest', 'should', 'advice']):
            intent['type'] = 'recommendation'
        elif any(word in user_lower for word in ['explain', 'what is', 'how does', 'why']):
            intent['type'] = 'explanation'
            intent['requires_data'] = False
        
        operators = ['GRN', 'NVX', 'DPT', 'EVO', 'SVQ', 'AZQ', 'UVX', 'BLX', 'OPR', 'CRY']
        for op in operators:
            if op in user_input.upper():
                intent['entities']['operators'].append(op)
        
        return intent
    
    def build_prompt(self, user_query: str, data_summary: Optional[str] = None) -> str:
        context = self.get_conversation_context()
        intent = self.infer_intent(user_query)
        
        prompt = f"""You are an intelligent assistant for PSA's Global Insights Dashboard.

{context}

User Query: {user_query}
Intent: {intent['type']}

"""
        
        if data_summary:
            prompt += f"Data Analysis:\n{data_summary}\n\n"
        
        prompt += """Provide a clear, actionable response that:
1. Directly answers the question
2. Includes specific metrics when relevant
3. Offers 2-3 actionable recommendations
4. Maintains professional tone

Keep response concise and focused."""
        
        return prompt
    
    def clear_context(self):
        self.history = []
        self.context = {
            'user_focus': [],
            'operators_mentioned': set(),
            'vessels_mentioned': set(),
            'current_topic': None,
            'decision_context': {}
        }
    
    def export_conversation(self) -> str:
        return json.dumps(self.history, indent=2)