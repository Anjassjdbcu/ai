"""
Data Fetcher Module - Collect crypto market data from multiple sources
"""
import ccxt
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import logging
from .config import BINANCE_API_KEY, BINANCE_API_SECRET, WATCH_LIST, DEFAULT_TIMEFRAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataFetcher:
    """Fetch cryptocurrency market data from exchanges"""

    def __init__(self):
        self.exchange = ccxt.binance({
            'apiKey': BINANCE_API_KEY,
            'secret': BINANCE_API_SECRET,
            'enableRateLimit': True,
        })
        self.symbols = WATCH_LIST

    def fetch_ohlcv(self, symbol: str, timeframe: str = "1h", limit: int = 100) -> pd.DataFrame:
        """
        Fetch OHLCV data from exchange
        
        Args:
            symbol: Trading pair (e.g., BTC/USDT)
            timeframe: Candle timeframe (1m, 5m, 1h, 4h, 1d)
            limit: Number of candles to fetch
            
        Returns:
            DataFrame with OHLCV data
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(
                ohlcv,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df['symbol'] = symbol
            return df
        except Exception as e:
            logger.error(f"Error fetching OHLCV for {symbol}: {str(e)}")
            return pd.DataFrame()

    def fetch_multiple_symbols(self, timeframe: str = "1h", limit: int = 100) -> Dict[str, pd.DataFrame]:
        """
        Fetch OHLCV data for multiple symbols
        
        Args:
            timeframe: Candle timeframe
            limit: Number of candles
            
        Returns:
            Dictionary with DataFrames for each symbol
        """
        data = {}
        for symbol in self.symbols:
            df = self.fetch_ohlcv(symbol, timeframe, limit)
            if not df.empty:
                data[symbol] = df
        return data

    def fetch_ticker(self, symbol: str) -> Dict:
        """
        Fetch current ticker data
        
        Args:
            symbol: Trading pair
            
        Returns:
            Ticker information
        """
        try:
            return self.exchange.fetch_ticker(symbol)
        except Exception as e:
            logger.error(f"Error fetching ticker for {symbol}: {str(e)}")
            return {}

    def fetch_order_book(self, symbol: str, limit: int = 20) -> Dict:
        """
        Fetch order book data
        
        Args:
            symbol: Trading pair
            limit: Depth of order book
            
        Returns:
            Order book data
        """
        try:
            return self.exchange.fetch_order_book(symbol, limit=limit)
        except Exception as e:
            logger.error(f"Error fetching order book for {symbol}: {str(e)}")
            return {}

    def fetch_recent_trades(self, symbol: str, limit: int = 50) -> pd.DataFrame:
        """
        Fetch recent trades
        
        Args:
            symbol: Trading pair
            limit: Number of trades
            
        Returns:
            DataFrame with recent trades
        """
        try:
            trades = self.exchange.fetch_trades(symbol, limit=limit)
            df = pd.DataFrame(trades)
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df[['timestamp', 'symbol', 'price', 'amount', 'side']]
        except Exception as e:
            logger.error(f"Error fetching trades for {symbol}: {str(e)}")
            return pd.DataFrame()

    def calculate_market_dominance(self) -> Dict[str, float]:
        """
        Calculate market dominance for watched symbols
        
        Returns:
            Dictionary with dominance percentages
        """
        tickers = {}
        for symbol in self.symbols:
            ticker = self.fetch_ticker(symbol)
            if ticker and 'quoteVolume' in ticker:
                tickers[symbol] = ticker['quoteVolume']

        total_volume = sum(tickers.values())
        dominance = {symbol: (volume / total_volume * 100) 
                     for symbol, volume in tickers.items()}
        return dominance

    def get_funding_rates(self) -> Dict[str, float]:
        """
        Get funding rates for perpetual trading
        
        Returns:
            Dictionary with funding rates
        """
        try:
            funding_rates = {}
            for symbol in self.symbols:
                # Using Binance public API for funding rates
                # This would need to be expanded based on actual API
                pass
            return funding_rates
        except Exception as e:
            logger.error(f"Error fetching funding rates: {str(e)}")
            return {}

    def calculate_vwap(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate Volume Weighted Average Price
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            Series with VWAP values
        """
        typical_price = (df['high'] + df['low'] + df['close']) / 3
        vwap = (typical_price * df['volume']).cumsum() / df['volume'].cumsum()
        return vwap

    def detect_support_resistance(self, df: pd.DataFrame, window: int = 20) -> Tuple[List[float], List[float]]:
        """
        Detect support and resistance levels
        
        Args:
            df: DataFrame with price data
            window: Lookback window
            
        Returns:
            Tuple of (support_levels, resistance_levels)
        """
        high = df['high'].rolling(window).max()
        low = df['low'].rolling(window).min()
        
        resistance = high[high.diff() == 0].unique()
        support = low[low.diff() == 0].unique()
        
        return support.tolist(), resistance.tolist()
