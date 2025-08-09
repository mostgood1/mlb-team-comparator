"""
Simple Flask server to debug the web interface issue
"""
from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/debug')
def debug_page():
    """Serve the debug HTML page"""
    return send_from_directory('.', 'debug_web_interface.html')

if __name__ == '__main__':
    print("🚀 Starting debug server...")
    print("📝 Visit http://localhost:5001/debug to test the debug interface")
    print("🔧 This will help identify why games aren't loading")
    app.run(host='localhost', port=5001, debug=True)
