"""
Crypto Trading AI Agent - Premium Version
Advanced analysis and trading signals for cryptocurrency markets
"""

__version__ = "1.0.0"
__author__ = "Anjassjdbcu"
__description__ = "Premium AI Agent for Crypto Trading & Analysis"

from .agent import CryptoTradingAgent
from .analyzer import CryptoAnalyzer
from .data_fetcher import DataFetcher

__all__ = [
    "CryptoTradingAgent",
    "CryptoAnalyzer",
    "DataFetcher"
]
