import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from config import decision_weights

class DecisionEngine:
    def __init__(self, strategy_priority: str = "balanced"):
        self.weights = decision_weights.update_for_strategy(strategy_priority)
        
    def calculate_time_efficiency(self, row: pd.Series) -> float:
        wait_time_score = max(0, 1 - abs(row['Wait Time (Hours): ATB-BTR']) / 20)
        arrival_accuracy_score = 1 if row['Arrival Accuracy (Final BTR)'] == 'Y' else 0
        return (wait_time_score * 0.6 + arrival_accuracy_score * 0.4) * 100
    
    def calculate_cost_efficiency(self, row: pd.Series) -> float:
        bunker_saved = row['Bunker Saved (USD)']
        max_bunker = 70000
        return min(100, (bunker_saved / max_bunker) * 100)
    
    def calculate_environmental_impact(self, row: pd.Series) -> float:
        carbon_abatement = row['Carbon Abatement (Tonnes)']
        max_carbon = 1.0
        return min(100, (carbon_abatement / max_carbon) * 100)
    
    def calculate_risk_level(self, row: pd.Series) -> float:
        berth_time = row['Berth Time (hours): ATU - ATB']
        wait_time = abs(row['Wait Time (Hours): ATB-BTR'])
        
        risk_score = 100
        if wait_time > 10:
            risk_score -= 30
        if berth_time > 50:
            risk_score -= 20
        if row['Arrival Accuracy (Final BTR)'] == 'N':
            risk_score -= 30
            
        return max(0, risk_score)
    
    def calculate_dis(self, row: pd.Series) -> float:
        time_eff = self.calculate_time_efficiency(row)
        cost_eff = self.calculate_cost_efficiency(row)
        env_impact = self.calculate_environmental_impact(row)
        risk = self.calculate_risk_level(row)
        
        dis = (
            time_eff * self.weights['time_efficiency'] +
            cost_eff * self.weights['cost_efficiency'] +
            env_impact * self.weights['environmental_impact'] +
            risk * self.weights['risk_level']
        )
        
        return round(dis, 2)
    
    def analyze_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        df['DIS_Score'] = df.apply(self.calculate_dis, axis=1)
        df['Time_Efficiency'] = df.apply(self.calculate_time_efficiency, axis=1)
        df['Cost_Efficiency'] = df.apply(self.calculate_cost_efficiency, axis=1)
        df['Environmental_Score'] = df.apply(self.calculate_environmental_impact, axis=1)
        df['Risk_Score'] = df.apply(self.calculate_risk_level, axis=1)
        return df
    
    def get_top_performers(self, df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
        analyzed_df = self.analyze_dataframe(df)
        return analyzed_df.nlargest(n, 'DIS_Score')[
            ['Operator', 'Vessel', 'DIS_Score', 'Time_Efficiency', 
             'Cost_Efficiency', 'Environmental_Score', 'Risk_Score']
        ]
    
    def compare_operators(self, df: pd.DataFrame, operators: List[str]) -> Dict:
        operator_data = df[df['Operator'].isin(operators)]
        analyzed = self.analyze_dataframe(operator_data)
        
        comparison = {}
        for op in operators:
            op_data = analyzed[analyzed['Operator'] == op]
            comparison[op] = {
                'avg_dis': round(op_data['DIS_Score'].mean(), 2),
                'avg_wait_time': round(op_data['Wait Time (Hours): ATB-BTR'].mean(), 2),
                'total_bunker_saved': round(op_data['Bunker Saved (USD)'].sum(), 2),
                'total_carbon_abatement': round(op_data['Carbon Abatement (Tonnes)'].sum(), 2),
                'on_time_rate': round((op_data['Arrival Accuracy (Final BTR)'] == 'Y').mean() * 100, 1)
            }
        
        return comparison
    
    def generate_recommendations(self, df: pd.DataFrame, top_n: int = 3) -> List[str]:
        analyzed = self.analyze_dataframe(df)
        recommendations = []
        
        avg_wait_time = analyzed['Wait Time (Hours): ATB-BTR'].mean()
        if avg_wait_time > 5:
            recommendations.append(f"High average wait time ({avg_wait_time:.1f}h). Consider berth scheduling optimization.")
        
        low_performers = analyzed[analyzed['DIS_Score'] < 50]
        if len(low_performers) > 0:
            recommendations.append(f"{len(low_performers)} vessels with DIS < 50. Review operational efficiency.")
        
        high_carbon = analyzed.nlargest(top_n, 'Carbon Abatement (Tonnes)')
        best_ops = high_carbon['Operator'].unique()
        recommendations.append(f"Top environmental performers: {', '.join(best_ops[:3])}")
        
        return recommendations