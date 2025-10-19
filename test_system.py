from powerbi_connector import PowerBIConnector
from decision_engine import DecisionEngine
from llm_client import LLMClient
import pandas as pd

def test_powerbi_connection():
    print("Testing Power BI connection...")
    pbi = PowerBIConnector()
    
    try:
        token = pbi.authenticate()
        print(f"Authentication successful: {token[:20]}...")
        
        data = pbi.get_operator_data()
        print(f"Retrieved {len(data)} records")
        print(data.head())
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_decision_engine():
    print("\nTesting Decision Engine...")
    engine = DecisionEngine()
    
    sample_data = {
        'Wait Time (Hours): ATB-BTR': 3.5,
        'Arrival Variance (within 4h target)': 'Y',
        'Bunker Saved (USD)': 25000,
        'Carbon Abatement (Tonnes)': 0.25,
        'Berth Time (hours): ATU - ATB': 35
    }
    
    df = pd.DataFrame([sample_data])
    result = engine.analyze_dataframe(df)
    print(f"DIS Score: {result['DIS_Score'].iloc[0]}")
    print(result[['DIS_Score', 'Time_Efficiency', 'Cost_Efficiency']].to_string())
    return True

def test_llm_client():
    print("\nTesting LLM Client...")
    llm = LLMClient()
    
    response = llm.generate_response("What is maritime operational efficiency?")
    
    if response['success']:
        print(f"Response: {response['content'][:100]}...")
        print(f"Tokens used: {response.get('tokens_used', 'N/A')}")
        return True
    else:
        print(f"Error: {response['content']}")
        return False

def run_all_tests():
    print("=" * 50)
    print("PSA Intelligent Assistant - System Tests")
    print("=" * 50)
    
    tests = [
        ("Power BI Connection", test_powerbi_connection),
        ("Decision Engine", test_decision_engine),
        ("LLM Client", test_llm_client)
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"Test {name} failed: {e}")
            results[name] = False
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    for name, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        print(f"{name}: {status}")
    print("=" * 50)

if __name__ == "__main__":
    run_all_tests()