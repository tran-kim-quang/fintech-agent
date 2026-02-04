import requests
import json

def test_api():
    url = "http://localhost:8000/api/v1/research/"
    payload = {
        "query": "Giá vàng SJC ngày 3/2/2026 là bao nhiêu?"
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"Testing API: {url}")
    print(f"Query: {payload['query']}")
    print("Processing (this may take a while)...")
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        print("\n" + "="*80)
        print("API Response Received!")
        print("="*80)
        print(f"Status: {result.get('status')}")
        print(f"Next Step: {result.get('next_step')}")
        
        print("\nFinal Report:")
        print("-" * 80)
        print(result.get('final_report'))
        print("-" * 80)
        
    except Exception as e:
        print(f"Error: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")

if __name__ == "__main__":
    test_api()
