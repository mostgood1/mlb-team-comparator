"""
Quick test to check if the JavaScript syntax error is fixed
"""
from app import app

# Test the home page to see if it loads without JavaScript errors
with app.test_client() as client:
    print("🌐 Testing home page HTML generation")
    response = client.get('/')
    
    if response.status_code == 200:
        html_content = response.data.decode('utf-8')
        
        # Check for the fixed JavaScript line
        if "Loading today's predictions" in html_content:
            print("✅ JavaScript syntax fixed - no more backslash escaping")
        else:
            print("⚠️ Could not find the fixed line")
            
        # Check for any remaining problematic escapes
        if "\\'" in html_content:
            print("❌ Still has problematic backslash escapes")
            problematic_lines = [line.strip() for line in html_content.split('\n') if "\\'" in line]
            for line in problematic_lines[:3]:
                print(f"   {line}")
        else:
            print("✅ No problematic backslash escapes found")
            
        print(f"📄 HTML generated successfully ({len(html_content)} characters)")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
