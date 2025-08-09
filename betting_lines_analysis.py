#!/usr/bin/env python3
"""
Betting Lines System Analysis
Comprehensive review of current betting lines handling - both refresh and historical
"""

import os
import json
from datetime import datetime, timedelta

def analyze_betting_lines_system():
    print("🎯 MLB BETTING LINES SYSTEM - COMPLETE ANALYSIS")
    print("=" * 70)
    
    print("📊 CURRENT STATE ASSESSMENT:")
    print()
    
    # Check for betting line files in different directories
    directories_to_check = [
        "c:\\Users\\mostg\\OneDrive\\Coding\\MLBCompare\\mlb-clean-deploy",
        "c:\\Users\\mostg\\OneDrive\\Coding\\MLBCompare\\mlb-team-comparator\\src"
    ]
    
    betting_files_found = {}
    
    for directory in directories_to_check:
        if os.path.exists(directory):
            files = os.listdir(directory)
            betting_files = [f for f in files if 'betting' in f.lower() or 'odds' in f.lower()]
            if betting_files:
                betting_files_found[directory] = betting_files
    
    print("📁 BETTING LINE FILES DISCOVERED:")
    if betting_files_found:
        for directory, files in betting_files_found.items():
            print(f"   Directory: {directory}")
            for file in files:
                file_path = os.path.join(directory, file)
                if os.path.exists(file_path):
                    size_mb = os.path.getsize(file_path) / (1024 * 1024)
                    print(f"   ✅ {file} ({size_mb:.2f} MB)")
                else:
                    print(f"   ❌ {file} (not accessible)")
            print()
    else:
        print("   ❌ No dedicated betting line files found in main directories")
        print()
    
    print("🔄 BETTING LINES INTEGRATION STATUS:")
    
    # Analysis of current betting lines implementation
    betting_integration_status = [
        ("🏗️  Real-time Lines Fetching", "PARTIAL", "Odds-API integration exists but not in auto-refresh"),
        ("📊 Historical Lines Storage", "LIMITED", "JSON cache exists but manual refresh only"),
        ("🔄 Auto-refresh Integration", "MISSING", "No betting lines in auto_update_mlb_data.py"),
        ("📅 Date-aware Lines", "MISSING", "No historical betting lines for past games"),
        ("🎯 Real Lines vs Sample", "MIXED", "Ultra-fast engine uses sample lines, others use real"),
        ("💾 Lines Caching", "BASIC", "Simple JSON storage, no intelligent cache management"),
        ("🧪 Error Handling", "BASIC", "API failures not gracefully handled in auto-refresh"),
        ("📈 Lines Analysis", "COMPLETE", "Betting value analysis implemented across engines")
    ]
    
    for feature, status, description in betting_integration_status:
        status_icon = "✅" if status == "COMPLETE" else "⚠️" if status == "PARTIAL" else "❌"
        print(f"   {status_icon} {feature:<30} - {status:<10} - {description}")
    
    print("\n🎯 CURRENT BETTING LINES WORKFLOW:")
    
    workflow_steps = [
        ("1. Real-time Fetching", "fetch_mlb_betting_lines.py", "Odds-API integration for current games"),
        ("2. Data Storage", "mlb_betting_lines.json", "Simple JSON cache with date-based structure"),
        ("3. Engine Integration", "Multiple engines", "Different approaches - real vs sample lines"),
        ("4. Value Analysis", "analyze_betting_value()", "Expected value calculations implemented"),
        ("5. Web Display", "Web interfaces", "Betting recommendations shown to users"),
        ("6. Historical Access", "MISSING", "No historical betting lines for past games"),
        ("7. Auto-refresh", "MISSING", "Not integrated into auto-update system")
    ]
    
    for step, component, description in workflow_steps:
        status = "✅" if component != "MISSING" else "❌"
        print(f"   {status} {step:<20} - {component:<25} - {description}")
    
    print("\n💡 IDENTIFIED GAPS & OPPORTUNITIES:")
    
    gaps = [
        ("❌ Auto-refresh Missing", "Betting lines not included in auto_update_mlb_data.py system"),
        ("❌ Historical Lines Gap", "No historical betting lines for analyzing past games"),
        ("❌ Cache Management", "No intelligent cache expiration or cleanup"),
        ("❌ API Rate Limiting", "No protection against Odds-API rate limits"),
        ("❌ Fallback Strategy", "No graceful degradation when API fails"),
        ("❌ Real vs Sample", "Inconsistent - ultra_fast uses sample, others attempt real"),
        ("⚠️  Data Freshness", "Lines may be stale without auto-refresh integration"),
        ("⚠️  Error Recovery", "Basic error handling, could be more robust")
    ]
    
    for gap, description in gaps:
        print(f"   {gap:<25} - {description}")
    
    print("\n🚀 RECOMMENDED IMPLEMENTATION PLAN:")
    
    recommendations = [
        ("HIGH", "Integrate betting lines into auto-refresh system", "Add to auto_update_mlb_data.py"),
        ("HIGH", "Implement historical betting lines lookup", "Similar to historical pitcher lookup"),
        ("MEDIUM", "Unify betting lines approach", "Choose real vs sample strategy consistently"),
        ("MEDIUM", "Add intelligent cache management", "Expire old lines, manage storage"),
        ("MEDIUM", "Enhance error handling", "Graceful degradation and retry logic"),
        ("LOW", "Add rate limiting protection", "Respect Odds-API limits"),
        ("LOW", "Implement backup betting sources", "Multiple odds providers for redundancy")
    ]
    
    for priority, task, details in recommendations:
        priority_icon = "🔴" if priority == "HIGH" else "🟡" if priority == "MEDIUM" else "🟢"
        print(f"   {priority_icon} {priority:<8} - {task:<40} - {details}")
    
    print("\n📈 CURRENT IMPLEMENTATION STRENGTHS:")
    
    strengths = [
        "✅ Real Odds-API integration exists and functional",
        "✅ Comprehensive betting value analysis implemented",
        "✅ Multiple betting markets supported (moneyline, runline, totals)",
        "✅ Clean JSON storage format with date-based organization",
        "✅ Web interface integration with betting recommendations",
        "✅ Expected value calculations for all bet types",
        "✅ American odds format properly handled",
        "✅ Multiple prediction engines support betting analysis"
    ]
    
    for strength in strengths:
        print(f"   {strength}")
    
    # Check if we can access the actual betting lines data
    betting_lines_file = "c:\\Users\\mostg\\OneDrive\\Coding\\MLBCompare\\mlb-team-comparator\\src\\mlb_betting_lines.json"
    if os.path.exists(betting_lines_file):
        print(f"\n📊 BETTING LINES DATA SAMPLE:")
        try:
            with open(betting_lines_file, 'r') as f:
                data = json.load(f)
            
            print(f"   📅 Total dates with betting lines: {len(data)}")
            if data:
                latest_date = max(data.keys())
                print(f"   📅 Latest betting lines date: {latest_date}")
                latest_games = data[latest_date]
                print(f"   🎯 Games with lines on {latest_date}: {len(latest_games)}")
                
                # Show sample betting line structure
                if latest_games:
                    sample_game = list(latest_games.keys())[0]
                    sample_lines = latest_games[sample_game]
                    print(f"   📋 Sample game: {sample_game}")
                    if 'moneyline' in sample_lines and sample_lines['moneyline']:
                        ml = sample_lines['moneyline']
                        print(f"      💰 Moneyline: {ml}")
                    if 'total' in sample_lines and sample_lines['total']:
                        total = sample_lines['total'][0] if sample_lines['total'] else {}
                        print(f"      📊 Total: {total.get('point', 'N/A')} ({total.get('price', 'N/A')})")
        except Exception as e:
            print(f"   ❌ Error reading betting lines data: {e}")
    
    print(f"\n🎉 SUMMARY: Betting lines system exists but needs auto-refresh integration!")

if __name__ == "__main__":
    analyze_betting_lines_system()
