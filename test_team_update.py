#!/usr/bin/env python3
from auto_update_mlb_data import MLBDataAutoUpdater

print("🎯 TESTING TEAM STRENGTH AUTO-UPDATE")
print("=" * 40)

updater = MLBDataAutoUpdater()
success = updater.update_team_strength_cache()

if success:
    print("\n✅ Team strength update test: PASSED")
else:
    print("\n❌ Team strength update test: FAILED")
