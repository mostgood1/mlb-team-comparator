#!/usr/bin/env python3
"""
Test Auto-Refresh Integration
Tests the auto-refresh functionality integrated into the ultra-fast engine
"""

from ultra_fast_engine import FastPredictionEngine
import os
import time
import json

def test_auto_refresh_integration():
    print("🎯 TESTING AUTO-REFRESH INTEGRATION")
    print("=" * 50)
    
    # Test 1: Check current file ages
    print("1. 📅 Current file ages:")
    
    files_to_check = [
        'team_strength_cache.json',
        'pitcher_stats_2025_and_career.json',
        'ProjectedStarters.json'
    ]
    
    for filename in files_to_check:
        if os.path.exists(filename):
            file_age = time.time() - os.path.getmtime(filename)
            hours_old = file_age / 3600
            print(f"   {filename}: {hours_old:.1f} hours old")
        else:
            print(f"   {filename}: NOT FOUND")
    
    # Test 2: Initialize engine (should trigger auto-refresh if needed)
    print("\n2. 🔄 Initializing prediction engine...")
    print("   (This should auto-refresh stale data)")
    
    try:
        engine = FastPredictionEngine()
        print("   ✅ Engine initialized successfully")
        
        # Test 3: Make a prediction to verify data is working
        print("\n3. 🎯 Testing prediction with refreshed data...")
        result = engine.get_fast_prediction("Yankees", "Red Sox", sim_count=1000)
        
        print(f"   ✅ Prediction successful:")
        print(f"     Total runs: {result['predictions']['predicted_total_runs']}")
        print(f"     Home win prob: {result['predictions']['home_win_prob']:.1%}")
        
        # Test 4: Check if team strengths are loaded
        print("\n4. 📊 Checking team strength data...")
        if hasattr(engine, 'team_strengths') and engine.team_strengths:
            team_count = len(engine.team_strengths)
            print(f"   ✅ Loaded {team_count} team strengths")
            
            # Show top teams
            sorted_teams = sorted(engine.team_strengths.items(), 
                                key=lambda x: x[1], reverse=True)[:3]
            print("   Top 3 teams:")
            for team, strength in sorted_teams:
                print(f"     {team}: {strength:+.3f}")
        else:
            print("   ⚠️ No team strength data loaded")
        
        # Test 5: Check if pitcher stats are loaded
        print("\n5. ⚾ Checking pitcher stats data...")
        if hasattr(engine, 'pitcher_stats') and engine.pitcher_stats:
            pitcher_count = len(engine.pitcher_stats)
            print(f"   ✅ Loaded {pitcher_count} pitcher records")
            
            # Test a pitcher lookup
            test_quality = engine.get_pitcher_quality_factor("Jacob deGrom")
            print(f"   Sample pitcher quality factor: {test_quality:.3f}")
        else:
            print("   ⚠️ No pitcher stats data loaded")
        
        print("\n🎉 Auto-refresh integration test COMPLETED!")
        return True
        
    except Exception as e:
        print(f"   ❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_auto_refresh_integration()
