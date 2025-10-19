from dataclasses import dataclass
from typing import Dict

@dataclass
class PowerBIConfig:
    client_id: str = "d4513e50-29a7-4f57-a41f-68fae5006b67"
    client_secret: str = "uF08Q~1sS-bSDi4bZe8JuOyPrIZglZ4zRqgKLbMp"
    tenant_id: str = "27fa816c-95b5-4431-90d9-4d0ac1986f71"
    workspace_id: str = "41675240-7b6e-4163-a0ed-52b5c3b13e01"
    report_id: str = "06bdda3d-459c-4632-8784-d43e6b208aab"
    authority_url: str = "https://login.microsoftonline.com"
    scope: list = None
    
    def __post_init__(self):
        if self.scope is None:
            self.scope = ["https://analysis.windows.net/powerbi/api/.default"]

@dataclass
class AzureGPTConfig:
    api_key: str = "86c77ec16ee3459695611c11da824b03"
    endpoint: str = "https://psacodesprint2025.azure-api.net/"
    deployment_name: str = "gpt-4.1-nano"
    api_version: str = "2025-01-01-preview"
    temperature: float = 0.7
    max_tokens: int = 1500

@dataclass
class DecisionWeights:
    time_efficiency: float = 0.3
    cost_efficiency: float = 0.3
    environmental_impact: float = 0.2
    risk_level: float = 0.2
    
    def update_for_strategy(self, priority: str) -> Dict[str, float]:
        if priority == "carbon_reduction":
            return {"time_efficiency": 0.2, "cost_efficiency": 0.2, 
                    "environmental_impact": 0.4, "risk_level": 0.2}
        elif priority == "cost_efficiency":
            return {"time_efficiency": 0.2, "cost_efficiency": 0.4,
                    "environmental_impact": 0.2, "risk_level": 0.2}
        elif priority == "reliability":
            return {"time_efficiency": 0.3, "cost_efficiency": 0.2,
                    "environmental_impact": 0.1, "risk_level": 0.4}
        return self.__dict__

powerbi_config = PowerBIConfig()
gpt_config = AzureGPTConfig()
decision_weights = DecisionWeights()