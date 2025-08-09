#!/usr/bin/env python3
"""
Test the updated API with pitcher and betting line data
"""

import json
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from app import app
    
    def test_api_with_missing_data_fixes():
        """Test that the API now returns complete data"""
        print("🧪 TESTING UPDATED API WITH MISSING DATA FIXES")
        print("=" * 55)
        
        with app.test_client() as client:
            response = client.get('/api/fast-predictions')
            
            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ API Response: {response.status_code}")
                
                if 'predictions' in data and data['predictions']:
                    print(f"✅ Found {len(data['predictions'])} predictions")
                    
                    # Check first prediction for all required data
                    first_pred = data['predictions'][0]
                    print(f"\n📝 CHECKING DATA COMPLETENESS:")
                    
                    # Check basic structure
                    required_fields = ['away_team', 'home_team', 'predictions', 'meta']
                    for field in required_fields:
                        status = "✅" if field in first_pred else "❌"
                        print(f"   {status} {field}: {type(first_pred.get(field, 'MISSING'))}")
                    
                    # Check predictions sub-object
                    if 'predictions' in first_pred:
                        pred_fields = ['home_win_probability', 'away_win_probability', 
                                     'predicted_home_score', 'predicted_away_score', 
                                     'predicted_total', 'confidence']
                        for field in pred_fields:
                            value = first_pred['predictions'].get(field, 'MISSING')
                            status = "✅" if field in first_pred['predictions'] else "❌"
                            print(f"   {status} predictions.{field}: {value}")
                    
                    # Check pitcher_quality (the missing data issue)
                    if 'pitcher_quality' in first_pred:
                        print(f"\n📝 PITCHER QUALITY DATA:")
                        pq = first_pred['pitcher_quality']
                        pitcher_fields = ['away_pitcher_name', 'home_pitcher_name', 
                                        'away_pitcher_factor', 'home_pitcher_factor']
                        for field in pitcher_fields:
                            value = pq.get(field, 'MISSING')
                            status = "✅" if field in pq else "❌"
                            print(f"   {status} {field}: {value}")
                    else:
                        print(f"   ❌ pitcher_quality: MISSING")
                    
                    # Check betting_lines
                    if 'betting_lines' in first_pred:
                        print(f"\n📝 BETTING LINES DATA:")
                        bl = first_pred['betting_lines']
                        if bl:
                            for key, value in bl.items():
                                print(f"   ✅ {key}: {value}")
                        else:
                            print(f"   ⚠️  betting_lines: Empty but present")
                    else:
                        print(f"   ❌ betting_lines: MISSING")
                    
                    # Check meta data
                    if 'meta' in first_pred:
                        print(f"\n📝 META DATA:")
                        meta = first_pred['meta']
                        meta_fields = ['execution_time_ms', 'simulations_run', 'cumulative_mode']
                        for field in meta_fields:
                            value = meta.get(field, 'MISSING')
                            status = "✅" if field in meta else "❌"
                            print(f"   {status} {field}: {value}")
                
                print(f"\n🎯 SUMMARY:")
                if all(field in first_pred for field in ['pitcher_quality', 'betting_lines', 'predictions', 'meta']):
                    print("✅ All major data fields present - missing data issue RESOLVED!")
                else:
                    missing = [field for field in ['pitcher_quality', 'betting_lines', 'predictions', 'meta'] 
                             if field not in first_pred]
                    print(f"❌ Still missing: {missing}")
                    
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.get_data()}")

    if __name__ == "__main__":
        test_api_with_missing_data_fixes()
        
except Exception as e:
    print(f"❌ Error running test: {e}")
    import traceback
    traceback.print_exc()
