"""
Test the cumulative simulation app
"""
from app import app

def test_cumulative_app():
    with app.test_client() as client:
        print('🧪 Testing cumulative simulation API...')
        response = client.get('/api/fast-predictions')
        
        if response.status_code == 200:
            data = response.get_json()
            if data.get('success'):
                print(f'✅ API working: {len(data["predictions"])} predictions')
                
                for pred in data['predictions'][:2]:
                    meta = pred.get('meta', {})
                    if meta.get('cumulative_mode'):
                        print(f'📊 Cumulative: {pred["away_team"]} @ {pred["home_team"]} - {meta["simulations_run"]} total sims')
                    else:
                        print(f'⚡ Standard: {pred["away_team"]} @ {pred["home_team"]} - {meta["simulations_run"]} sims')
            else:
                print('❌ API error:', data.get('error'))
        else:
            print(f'❌ HTTP error: {response.status_code}')

if __name__ == "__main__":
    test_cumulative_app()
