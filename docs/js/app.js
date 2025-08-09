// Main application logic
let currentPrediction = null;

function makePrediction() {
    const awayTeam = document.getElementById('awayTeam').value;
    const homeTeam = document.getElementById('homeTeam').value;
    const resultsDiv = document.getElementById('predictionResults');
    const predictBtn = document.getElementById('predictBtn');
    const scenarioBtn = document.getElementById('scenarioBtn');

    if (!awayTeam || !homeTeam) {
        alert('Please select both teams');
        return;
    }

    if (awayTeam === homeTeam) {
        alert('Please select different teams');
        return;
    }

    // Show loading state
    predictBtn.disabled = true;
    predictBtn.textContent = 'Generating...';
    
    resultsDiv.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Generating ultra-fast prediction...</p>
        </div>
    `;

    // Simulate async prediction (even though it's instant)
    setTimeout(() => {
        try {
            currentPrediction = predictionEngine.generatePrediction(awayTeam, homeTeam);
            displayPrediction(currentPrediction);
            
            // Show scenario analysis button
            scenarioBtn.style.display = 'inline-block';
            
        } catch (error) {
            resultsDiv.innerHTML = `
                <div style="text-align: center; color: #ff6b6b;">
                    <h3>❌ Prediction Error</h3>
                    <p>${error.message}</p>
                </div>
            `;
        } finally {
            predictBtn.disabled = false;
            predictBtn.textContent = '🎯 Generate Prediction';
        }
    }, 500); // Small delay for UX
}

function displayPrediction(prediction) {
    const resultsDiv = document.getElementById('predictionResults');
    
    const winner = prediction.away_runs > prediction.home_runs ? prediction.away_team : 
                   prediction.home_runs > prediction.away_runs ? prediction.home_team : 'TIE';
    
    resultsDiv.innerHTML = `
        <div class="score-display">
            ${prediction.away_team} ${prediction.away_runs} - ${prediction.home_runs} ${prediction.home_team}
        </div>
        
        <div style="text-align: center; margin: 20px 0;">
            <h3>🏆 ${winner === 'TIE' ? 'Predicted Tie Game' : winner + ' Wins'}</h3>
            <p><strong>Total Runs:</strong> ${prediction.total_runs}</p>
            <p><strong>Confidence:</strong> ${(prediction.confidence * 100).toFixed(1)}%</p>
        </div>
        
        <div style="background: rgba(255,255,255,0.1); border-radius: 10px; padding: 15px; margin: 15px 0;">
            <h4>⚡ Performance Metrics</h4>
            <p><strong>Prediction Time:</strong> ${prediction.prediction_time_ms}ms</p>
            <p><strong>Engine:</strong> Client-Side Ultra-Fast</p>
        </div>
        
        <div style="text-align: center; margin-top: 20px;">
            <small style="opacity: 0.8;">
                🎲 For enhanced predictability analysis, click "Scenario Analysis" below
            </small>
        </div>
    `;
}

function runScenarioAnalysis() {
    if (!currentPrediction) {
        alert('Please generate a prediction first');
        return;
    }

    const scenarioSection = document.getElementById('scenarioSection');
    const scenarioResults = document.getElementById('scenarioResults');
    const scenarioBtn = document.getElementById('scenarioBtn');
    
    scenarioBtn.disabled = true;
    scenarioBtn.textContent = 'Analyzing...';
    
    scenarioSection.style.display = 'block';
    scenarioResults.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Running comprehensive scenario analysis...</p>
        </div>
    `;

    // Simulate analysis time
    setTimeout(() => {
        try {
            const scenarios = predictionEngine.generateScenarioAnalysis(
                currentPrediction.away_team, 
                currentPrediction.home_team
            );
            
            displayScenarioAnalysis(scenarios);
            
        } catch (error) {
            scenarioResults.innerHTML = `
                <div style="text-align: center; color: #ff6b6b;">
                    <h3>❌ Analysis Error</h3>
                    <p>${error.message}</p>
                </div>
            `;
        } finally {
            scenarioBtn.disabled = false;
            scenarioBtn.textContent = '📊 Scenario Analysis';
        }
    }, 1200); // Longer delay for scenario analysis
}

function displayScenarioAnalysis(scenarios) {
    const scenarioResults = document.getElementById('scenarioResults');
    
    scenarioResults.innerHTML = `
        <div style="text-align: center; margin-bottom: 25px;">
            <h3>🎯 Enhanced Predictability Analysis</h3>
            <p><strong>Analysis Time:</strong> ${scenarios.prediction_time_ms}ms</p>
            <p><strong>Confidence Level:</strong> ${scenarios.confidence_level.toFixed(1)}%</p>
        </div>
        
        <div class="scenario-results">
            <div class="scenario-card">
                <h4>🛡️ Conservative</h4>
                <div style="font-size: 1.8em; font-weight: 700; margin: 10px 0;">
                    ${scenarios.conservative.avg_total}
                </div>
                <p>Range: ${scenarios.conservative.range[0]}-${scenarios.conservative.range[1]} runs</p>
                <small>Lower-risk outcome</small>
            </div>
            
            <div class="scenario-card">
                <h4>🎯 Most Likely</h4>
                <div style="font-size: 1.8em; font-weight: 700; margin: 10px 0; color: #4ecdc4;">
                    ${scenarios.likely.avg_total}
                </div>
                <p>Range: ${scenarios.likely.range[0]}-${scenarios.likely.range[1]} runs</p>
                <small>Expected outcome</small>
            </div>
            
            <div class="scenario-card">
                <h4>🚀 Aggressive</h4>
                <div style="font-size: 1.8em; font-weight: 700; margin: 10px 0;">
                    ${scenarios.aggressive.avg_total}
                </div>
                <p>Range: ${scenarios.aggressive.range[0]}-${scenarios.aggressive.range[1]} runs</p>
                <small>Higher-scoring potential</small>
            </div>
        </div>
        
        <div style="background: rgba(255,255,255,0.1); border-radius: 10px; padding: 20px; margin-top: 25px;">
            <h4>📊 Analysis Summary</h4>
            <p><strong>Prediction Range:</strong> ${scenarios.conservative.range[0]} - ${scenarios.aggressive.range[1]} total runs</p>
            <p><strong>Most Reliable:</strong> ${scenarios.likely.avg_total} runs (${scenarios.confidence_level.toFixed(0)}% confidence)</p>
            <p><strong>Variance:</strong> ${(scenarios.aggressive.avg_total - scenarios.conservative.avg_total).toFixed(1)} run spread</p>
        </div>
        
        <div style="text-align: center; margin-top: 20px;">
            <small style="opacity: 0.8;">
                📈 This analysis provides outcome ranges for informed betting decisions while preserving realistic baseball unpredictability
            </small>
        </div>
    `;
}
