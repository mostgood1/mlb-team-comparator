"""
Debug the web interface API error
"""
from app import app
import json

def debug_api_response():
    with app.test_client() as client:
        print('🔍 Testing API endpoint directly...')
        response = client.get('/api/fast-predictions')
        print(f'Status: {response.status_code}')
        
        if response.status_code == 200:
            try:
                data = response.get_json()
                print(f'Response keys: {list(data.keys()) if data else "No data"}')
                
                if data and 'predictions' in data:
                    print(f'Predictions count: {len(data["predictions"])}')
                    if data['predictions']:
                        pred = data['predictions'][0]
                        print(f'First prediction keys: {list(pred.keys())}')
                        print(f'Sample prediction structure: {type(pred)}')
                        
                        # Check for potential undefined access points
                        print('\n🔍 Checking prediction structure:')
                        print(f'  away_team: {pred.get("away_team", "MISSING")}')
                        print(f'  home_team: {pred.get("home_team", "MISSING")}')
                        print(f'  predictions: {type(pred.get("predictions", "MISSING"))}')
                        print(f'  meta: {type(pred.get("meta", "MISSING"))}')
                        print(f'  recommendations: {type(pred.get("recommendations", "MISSING"))}')
                        
                        # Check meta structure
                        meta = pred.get('meta', {})
                        if meta:
                            print(f'\n  Meta keys: {list(meta.keys())}')
                        
                        # Check predictions structure  
                        predictions = pred.get('predictions', {})
                        if predictions:
                            print(f'  Predictions keys: {list(predictions.keys())}')
                            
                            # Show specific values that JavaScript is trying to access
                            print(f'\n🎯 JavaScript expects these properties:')
                            print(f'  predicted_total_runs: {predictions.get("predicted_total_runs", "MISSING")}')
                            print(f'  predicted_total: {predictions.get("predicted_total", "MISSING")}')
                            print(f'  predicted_away_score: {predictions.get("predicted_away_score", "MISSING")}')
                            print(f'  predicted_home_score: {predictions.get("predicted_home_score", "MISSING")}')
                            
                        # Show the issue
                        print(f'\n❌ Likely JavaScript issue:')
                        print(f'  JavaScript tries to access: prediction.predictions.predicted_total_runs')
                        print(f'  But property might be named: prediction.predictions.predicted_total')
                        
                        # Show full first prediction for debugging
                        print(f'\n📋 Full first prediction:')
                        import json
                        print(json.dumps(pred, indent=2)[:1000] + '...')
                            
                else:
                    print('❌ No predictions in response')
                    print(f'Full response: {json.dumps(data, indent=2)[:500]}')
                    
            except Exception as e:
                print(f'JSON parsing error: {e}')
                raw_data = response.get_data().decode('utf-8')
                print(f'Raw response (first 500 chars): {raw_data[:500]}')
        else:
            error_data = response.get_data().decode('utf-8')
            print(f'Error response: {error_data}')

if __name__ == "__main__":
    debug_api_response()
