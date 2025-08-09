"""
Cumulative Simulation Dashboard
Shows the benefits of accumulating simulation data over time
"""

from cumulative_simulation_manager import cumulative_manager
import json

def show_cumulative_benefits():
    """Display the benefits of cumulative simulation approach"""
    
    print("📊 CUMULATIVE SIMULATION BENEFITS DASHBOARD")
    print("=" * 60)
    
    summary = cumulative_manager.get_simulation_summary()
    
    print(f"\n🎯 CURRENT SYSTEM STATUS:")
    print(f"   • Total games tracked: {summary['total_games']}")
    print(f"   • Total simulations: {summary['total_simulations']:,}")
    print(f"   • Average per game: {summary['average_sims_per_game']:.0f}")
    
    if summary['total_games'] > 0:
        print(f"\n📈 CUMULATIVE ADVANTAGES:")
        
        # Calculate confidence improvements
        total_sims = summary['total_simulations']
        games_count = summary['total_games']
        avg_per_game = total_sims / games_count if games_count > 0 else 0
        
        print(f"   ✅ Simulation Accumulation:")
        print(f"      - OLD: 1,500 simulations per reload (start fresh)")
        print(f"      - NEW: {avg_per_game:.0f} average simulations per game (cumulative)")
        print(f"      - IMPROVEMENT: {((avg_per_game / 1500) - 1) * 100:.0f}% more data per game")
        
        print(f"\n   ✅ Confidence Levels:")
        confidence_1500 = min(95.0, (1500 / 10000) * 100)
        confidence_avg = min(95.0, (avg_per_game / 10000) * 100)
        print(f"      - OLD: {confidence_1500:.1f}% confidence with 1,500 sims")
        print(f"      - NEW: {confidence_avg:.1f}% confidence with {avg_per_game:.0f} sims")
        print(f"      - IMPROVEMENT: {confidence_avg - confidence_1500:.1f} percentage points")
        
        print(f"\n   ✅ Efficiency Gains:")
        print(f"      - Subsequent loads: Only add simulations if needed")
        print(f"      - Data persistence: Survives browser refreshes")
        print(f"      - Progressive accuracy: Gets better over time")
        print(f"      - Target awareness: Stops at optimal simulation count")
        
        # Show games by date
        if 'games_by_date' in summary:
            print(f"\n📅 GAMES BY DATE:")
            for date, games in summary['games_by_date'].items():
                print(f"\n   {date}:")
                for game in games[:3]:  # Show first 3 games
                    print(f"      {game['matchup']}: {game['simulations']} sims ({game['confidence']} confidence)")
                if len(games) > 3:
                    print(f"      ... and {len(games) - 3} more games")
    
    print(f"\n🚀 SYSTEM BENEFITS:")
    print(f"   • No more 'starting from scratch' on each reload")
    print(f"   • Progressive improvement in prediction accuracy") 
    print(f"   • Intelligent simulation management")
    print(f"   • Persistent data across sessions")
    print(f"   • Confidence-based decision making")
    
    print(f"\n💡 NEXT STEPS:")
    print(f"   • Continue using the system to build up more data")
    print(f"   • Each reload adds value instead of resetting")
    print(f"   • Watch confidence levels improve over time")
    print(f"   • Target simulation counts reached automatically")

def check_data_file():
    """Check the cumulative data file status"""
    import os
    
    print(f"\n📁 DATA FILE STATUS:")
    data_file = "cumulative_simulations.json"
    
    if os.path.exists(data_file):
        file_size = os.path.getsize(data_file)
        print(f"   ✅ File exists: {data_file}")
        print(f"   📏 File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        
        try:
            with open(data_file, 'r') as f:
                data = json.load(f)
            print(f"   📊 Games stored: {len(data)}")
            
            # Show file contents preview
            print(f"\n   📋 Sample entries:")
            for i, (key, game_data) in enumerate(list(data.items())[:2]):
                sims = game_data.get('total_simulations', 0)
                confidence = game_data.get('confidence_level', 0)
                print(f"      {i+1}. {key}: {sims} sims ({confidence:.1f}% confidence)")
                
        except Exception as e:
            print(f"   ❌ Error reading file: {e}")
    else:
        print(f"   📝 File not found - will be created on first use")

if __name__ == "__main__":
    show_cumulative_benefits()
    check_data_file()
