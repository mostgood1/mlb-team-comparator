#!/usr/bin/env python3
"""
Simple Auto-Refresh Test
Tests the auto-refresh logic without actually fetching new data
"""

import os
import time
import json

def simulate_auto_refresh_check():
    print("🎯 AUTO-REFRESH LOGIC TEST")
    print("=" * 30)
    
    # Check current file ages
    files = {
        'team_strength_cache.json': 12,  # 12 hour refresh threshold
        'pitcher_stats_2025_and_career.json': 24,  # 24 hour threshold
        'ProjectedStarters.json': 1  # 1 hour threshold (for daily updates)
    }
    
    for filename, threshold_hours in files.items():
        if os.path.exists(filename):
            file_age = time.time() - os.path.getmtime(filename)
            hours_old = file_age / 3600
            needs_refresh = hours_old > threshold_hours
            
            status = "🔄 NEEDS REFRESH" if needs_refresh else "✅ FRESH"
            print(f"{filename}:")
            print(f"  Age: {hours_old:.1f} hours")
            print(f"  Threshold: {threshold_hours} hours")
            print(f"  Status: {status}")
            print()
        else:
            print(f"{filename}: ❌ MISSING (would trigger refresh)")
            print()
    
    # Test if auto-updater module can be imported
    try:
        from auto_update_mlb_data import MLBDataAutoUpdater
        print("✅ Auto-updater module available")
        
        updater = MLBDataAutoUpdater()
        print("✅ Auto-updater initialized")
        
        # Test file age checking without actually updating
        if updater.should_update_data('team_strength_cache.json', max_age_hours=12):
            print("🔄 Team strength cache would be refreshed")
        else:
            print("✅ Team strength cache is current")
            
    except Exception as e:
        print(f"❌ Auto-updater issue: {e}")

if __name__ == "__main__":
    simulate_auto_refresh_check()
