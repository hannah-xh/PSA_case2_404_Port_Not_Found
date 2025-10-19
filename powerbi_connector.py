import requests
import pandas as pd
from msal import ConfidentialClientApplication
from typing import Optional, Dict, List
from config import powerbi_config

class PowerBIConnector:
    def __init__(self):
        self.config = powerbi_config
        self.access_token = None
        self.base_url = "https://api.powerbi.com/v1.0/myorg"
        self.dataset_id = None
        
    def authenticate(self) -> str:
        app = ConfidentialClientApplication(
            self.config.client_id,
            authority=f"{self.config.authority_url}/{self.config.tenant_id}",
            client_credential=self.config.client_secret
        )
        
        result = app.acquire_token_for_client(scopes=self.config.scope)
        
        if "access_token" in result:
            self.access_token = result["access_token"]
            return self.access_token
        raise Exception(f"Authentication failed: {result.get('error_description')}")
    
    def _get_headers(self) -> Dict[str, str]:
        if not self.access_token:
            self.authenticate()
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def _get_dataset_id(self) -> str:
        if self.dataset_id:
            return self.dataset_id
            
        report_url = f"{self.base_url}/groups/{self.config.workspace_id}/reports/{self.config.report_id}"
        report_response = requests.get(report_url, headers=self._get_headers())
        
        if report_response.status_code != 200:
            raise Exception(f"Failed to get report: {report_response.text}")
        
        self.dataset_id = report_response.json().get("datasetId")
        return self.dataset_id
    
    def execute_dax_query(self, dax_query: str) -> pd.DataFrame:
        dataset_id = self._get_dataset_id()
        url = f"{self.base_url}/groups/{self.config.workspace_id}/datasets/{dataset_id}/executeQueries"
        
        payload = {
            "queries": [{"query": dax_query}],
            "serializerSettings": {"includeNulls": True}
        }
        
        response = requests.post(url, headers=self._get_headers(), json=payload)
        
        if response.status_code == 200:
            data = response.json()
            rows = data["results"][0]["tables"][0]["rows"]
            df = pd.DataFrame(rows)
            
            df.columns = [col.replace('data[', '').replace(']', '') for col in df.columns]
            return df
        else:
            raise Exception(f"Query failed: {response.text}")
    
    def get_operator_data(self, operator: Optional[str] = None) -> pd.DataFrame:
        base_query = "EVALUATE TOPN(300, 'Data')"
        
        if operator:
            base_query = f"EVALUATE FILTER('Data', 'Data'[Operator] = \"{operator}\")"
        
        return self.execute_dax_query(base_query)
    
    def get_key_metrics(self) -> Dict[str, float]:
        query = """
        EVALUATE 
        SUMMARIZE(
            'Data',
            "AvgWaitTime", AVERAGE('Data'[Wait Time (Hours): ATB-BTR]),
            "TotalBunkerSaved", SUM('Data'[Bunker Saved (USD)]),
            "TotalCarbonAbatement", SUM('Data'[Carbon Abatement (Tonnes)]),
            "AvgArrivalVariance", AVERAGE('Data'[Arrival Variance (within 4h target)])
        )
        """
        
        df = self.execute_dax_query(query)
        return df.iloc[0].to_dict()
    
    def get_operators_comparison(self, operators: List[str]) -> pd.DataFrame:
        query = f"""
        EVALUATE 
        SUMMARIZECOLUMNS(
            'Data'[Operator],
            "AvgWaitTime", AVERAGE('Data'[Wait Time (Hours): ATB-BTR]),
            "BunkerSaved", SUM('Data'[Bunker Saved (USD)]),
            "CarbonAbatement", SUM('Data'[Carbon Abatement (Tonnes)])
        )
        """
        
        df = self.execute_dax_query(query)
        return df[df['Operator'].isin(operators)]