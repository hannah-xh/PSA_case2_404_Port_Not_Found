import requests
from typing import Dict, Optional
from config import gpt_config

class LLMClient:
    def __init__(self):
        self.config = gpt_config
        self.api_url = f"{self.config.endpoint}openai/deployments/{self.config.deployment_name}/chat/completions"
        
    def generate_response(self, prompt: str, system_message: Optional[str] = None) -> Dict:
        headers = {
            "Content-Type": "application/json",
            "api-key": self.config.api_key
        }
        
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "top_p": 0.95,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }
        
        params = {"api-version": self.config.api_version}
        
        response = requests.post(
            self.api_url,
            headers=headers,
            json=payload,
            params=params,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                'content': result['choices'][0]['message']['content'],
                'tokens_used': result['usage']['total_tokens'],
                'success': True
            }
        else:
            return {
                'content': f"Error: {response.text}",
                'success': False
            }
    
    def summarize_data(self, data_dict: Dict) -> str:
        summary_prompt = f"""Analyze this operational data and provide key insights:

{data_dict}

Focus on:
- Notable patterns or outliers
- Performance indicators
- Areas requiring attention

Keep summary under 150 words."""
        
        response = self.generate_response(summary_prompt)
        return response['content'] if response['success'] else "Unable to generate summary"
    
    def generate_recommendations(self, analysis: str, context: str = "") -> str:
        rec_prompt = f"""Based on this analysis:

{analysis}

Context: {context}

Provide 3 specific, actionable recommendations for PSA operations team.
Format as numbered list, each recommendation in one sentence."""
        
        response = self.generate_response(rec_prompt)
        return response['content'] if response['success'] else "Unable to generate recommendations"