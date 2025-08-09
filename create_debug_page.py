"""
Create a debug version of the web page with detailed error logging
"""

debug_html = """
<!DOCTYPE html>
<html>
<head>
    <title>🔧 Debug MLB Predictions</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background: #f0f0f0; }
        .debug { background: #fff; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 3px solid #007bff; }
        .error { border-left-color: #dc3545; }
        .success { border-left-color: #28a745; }
        button { padding: 10px 20px; margin: 5px; cursor: pointer; }
        #predictions-container { margin-top: 20px; }
        .prediction-card { background: #fff; padding: 15px; margin: 10px 0; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>🔧 Debug MLB Predictions Interface</h1>
    <div id="debug-log"></div>
    
    <button onclick="testAPI()">🧪 Test API</button>
    <button onclick="loadTodaysPredictions()">📍 Load Today's Games</button>
    
    <div id="predictions-container"></div>

    <script>
        function logDebug(message, type = 'debug') {
            const debugLog = document.getElementById('debug-log');
            const logEntry = document.createElement('div');
            logEntry.className = `debug ${type}`;
            logEntry.innerHTML = `[${new Date().toLocaleTimeString()}] ${message}`;
            debugLog.appendChild(logEntry);
            console.log(message);
        }

        async function testAPI() {
            logDebug('🔍 Testing API endpoint directly...');
            
            try {
                const response = await fetch('/api/fast-predictions');
                logDebug(`📡 Response status: ${response.status}`, 'success');
                logDebug(`📄 Content-Type: ${response.headers.get('content-type')}`, 'success');
                
                const text = await response.text();
                logDebug(`📝 Response length: ${text.length} characters`, 'success');
                logDebug(`📝 Response preview: ${text.substring(0, 200)}...`, 'success');
                
                // Try to parse as JSON
                const data = JSON.parse(text);
                logDebug(`✅ JSON parsing successful`, 'success');
                
                if (data.predictions) {
                    logDebug(`📊 Found ${data.predictions.length} predictions`, 'success');
                } else if (data.error) {
                    logDebug(`❌ API returned error: ${data.error}`, 'error');
                }
                
            } catch (error) {
                logDebug(`❌ API test failed: ${error.message}`, 'error');
                logDebug(`❌ Full error: ${error.stack}`, 'error');
            }
        }

        async function loadTodaysPredictions() {
            logDebug('📍 Loading today\\'s predictions...');
            document.getElementById('predictions-container').innerHTML = '<div class="prediction-card">⚡ Loading...</div>';
            
            try {
                logDebug('📡 Fetching /api/fast-predictions...');
                const response = await fetch('/api/fast-predictions');
                
                logDebug(`📊 Response received: ${response.status} ${response.statusText}`, 'success');
                
                const data = await response.json();
                logDebug('✅ JSON parsed successfully', 'success');
                
                if (data.error) {
                    throw new Error(data.error);
                }
                
                logDebug(`📊 Processing ${data.predictions.length} predictions...`, 'success');
                displayPredictions(data.predictions);
                
            } catch (error) {
                logDebug(`❌ Load failed: ${error.message}`, 'error');
                document.getElementById('predictions-container').innerHTML = 
                    `<div class="prediction-card error">❌ Error: ${error.message}</div>`;
            }
        }

        function displayPredictions(predictions) {
            const container = document.getElementById('predictions-container');
            container.innerHTML = '';
            
            logDebug(`🎯 Displaying ${predictions.length} predictions...`, 'success');
            
            predictions.forEach((pred, index) => {
                const predictionDiv = document.createElement('div');
                predictionDiv.className = 'prediction-card';
                predictionDiv.innerHTML = `
                    <h3>${pred.away_team} @ ${pred.home_team}</h3>
                    <p>Predicted Total: ${pred.predictions?.predicted_total_runs || 'N/A'}</p>
                    <p>Away Score: ${pred.predictions?.predicted_away_score || 'N/A'}</p>
                    <p>Home Score: ${pred.predictions?.predicted_home_score || 'N/A'}</p>
                `;
                container.appendChild(predictionDiv);
                
                if (index < 3) {
                    logDebug(`📊 Game ${index + 1}: ${pred.away_team} @ ${pred.home_team}`, 'success');
                }
            });
            
            logDebug('✅ All predictions displayed successfully', 'success');
        }

        // Auto-start on page load
        window.onload = () => {
            logDebug('🚀 Page loaded, starting tests...', 'success');
            testAPI();
        };
    </script>
</body>
</html>
"""

# Write to a debug file
with open('debug_web_interface.html', 'w', encoding='utf-8') as f:
    f.write(debug_html)

print("✅ Created debug_web_interface.html")
print("📝 Open this file in a browser while running the Flask app to debug the loading issue")
print("🔧 This will show detailed error messages and API responses")
