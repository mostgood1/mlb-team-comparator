"""
Ultra-Fast MLB Prediction System
Clean repository deployment with essential optimized files only
"""

__version__ = "1.0.0"
__author__ = "MLB Prediction System"
__description__ = "Ultra-fast MLB prediction engine with professional betting analysis"

# Production-ready components
from .ultra_fast_engine import FastPredictionEngine
from .ultra_fast_web import app
from .TodaysGames import TodaysGames

__all__ = ['FastPredictionEngine', 'TodaysGames', 'app']
