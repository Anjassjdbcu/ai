"""
Crypto Analyzer Module - Technical and fundamental analysis
"""
import pandas as pd
import numpy as np
from typing import Dict, Tuple, List
import ta  # Technical Analysis Library
import logging
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CryptoAnalyzer:
    """Advanced cryptocurrency technical analysis"""

    def __init__(self):
        self.scaler = StandardScaler()

    def calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        return ta.momentum.rsi(df['close'], length=period)

    def calculate_macd(self, df: pd.DataFrame) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Calculate MACD indicator"""
        macd = ta.trend.macd(df['close'], window_fast=12, window_slow=26, window_sign=9)
        return macd.iloc[:, 0], macd.iloc[:, 1], macd.iloc[:, 2]

    def calculate_bollinger_bands(self, df: pd.DataFrame, period: int = 20) -> Dict[str, pd.Series]:
        """Calculate Bollinger Bands"""
        bb = ta.volatility.bollinger_bands(df['close'], window=period, window_dev=2)
        return {
            'upper': bb.iloc[:, 2],
            'middle': bb.iloc[:, 1],
            'lower': bb.iloc[:, 0]
        }

    def calculate_moving_averages(self, df: pd.DataFrame, 
                                 periods: List[int] = [20, 50, 200]) -> Dict[str, pd.Series]:
        """Calculate Simple and Exponential Moving Averages"""
        mas = {}
        for period in periods:
            mas[f'sma_{period}'] = ta.trend.sma_indicator(df['close'], window=period)
            mas[f'ema_{period}'] = ta.trend.ema_indicator(df['close'], window=period)
        return mas

    def calculate_volume_indicators(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        """Calculate volume-based indicators"""
        return {
            'obv': ta.volume.on_balance_volume(df['close'], df['volume']),
            'cmf': ta.volume.chaikin_money_flow(df['high'], df['low'], df['close'], df['volume']),
            'ad': ta.volume.accumulation_distribution_line(df['high'], df['low'], df['close'], df['volume'])
        }

    def calculate_atr(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Average True Range for volatility"""
        return ta.volatility.average_true_range(df['high'], df['low'], df['close'], window=period)

    def calculate_stochastic(self, df: pd.DataFrame, period: int = 14) -> Dict[str, pd.Series]:
        """Calculate Stochastic Oscillator"""
        stoch = ta.momentum.stoch(df['high'], df['low'], df['close'], window=period, smooth_window=3)
        return {
            'k': stoch.iloc[:, 0],
            'd': stoch.iloc[:, 1]
        }

    def calculate_roc(self, df: pd.DataFrame, period: int = 12) -> pd.Series:
        """Calculate Rate of Change"""
        return ta.momentum.roc(df['close'], window=period)

    def detect_divergence(self, df: pd.DataFrame) -> Dict[str, bool]:
        """Detect bullish/bearish divergences"""
        rsi = self.calculate_rsi(df)
        
        # Simple divergence detection
        bullish_div = (df['close'].iloc[-1] > df['close'].iloc[-20] and 
                       rsi.iloc[-1] < rsi.iloc[-20])
        bearish_div = (df['close'].iloc[-1] < df['close'].iloc[-20] and 
                       rsi.iloc[-1] > rsi.iloc[-20])
        
        return {
            'bullish_divergence': bullish_div,
            'bearish_divergence': bearish_div
        }

    def identify_candlestick_patterns(self, df: pd.DataFrame) -> Dict[str, bool]:
        """Identify common candlestick patterns"""
        patterns = {}
        
        # Doji
        patterns['doji'] = self._detect_doji(df)
        
        # Hammer
        patterns['hammer'] = self._detect_hammer(df)
        
        # Engulfing
        patterns['bullish_engulfing'] = self._detect_bullish_engulfing(df)
        patterns['bearish_engulfing'] = self._detect_bearish_engulfing(df)
        
        # Morning Star / Evening Star
        patterns['morning_star'] = self._detect_morning_star(df)
        patterns['evening_star'] = self._detect_evening_star(df)
        
        return patterns

    def _detect_doji(self, df: pd.DataFrame) -> bool:
        """Detect Doji pattern"""
        last = df.iloc[-1]
        body = abs(last['close'] - last['open'])
        wick = max(last['high'] - max(last['open'], last['close']),
                   min(last['open'], last['close']) - last['low'])
        return body < (wick / 2)

    def _detect_hammer(self, df: pd.DataFrame) -> bool:
        """Detect Hammer pattern"""
        last = df.iloc[-1]
        body = abs(last['close'] - last['open'])
        lower_wick = min(last['open'], last['close']) - last['low']
        return lower_wick > (body * 2)

    def _detect_bullish_engulfing(self, df: pd.DataFrame) -> bool:
        """Detect Bullish Engulfing pattern"""
        if len(df) < 2:
            return False
        prev = df.iloc[-2]
        curr = df.iloc[-1]
        return (prev['close'] < prev['open'] and 
                curr['close'] > curr['open'] and
                curr['open'] <= prev['close'] and
                curr['close'] >= prev['open'])

    def _detect_bearish_engulfing(self, df: pd.DataFrame) -> bool:
        """Detect Bearish Engulfing pattern"""
        if len(df) < 2:
            return False
        prev = df.iloc[-2]
        curr = df.iloc[-1]
        return (prev['close'] > prev['open'] and 
                curr['close'] < curr['open'] and
                curr['open'] >= prev['close'] and
                curr['close'] <= prev['open'])

    def _detect_morning_star(self, df: pd.DataFrame) -> bool:
        """Detect Morning Star pattern"""
        if len(df) < 3:
            return False
        return (df.iloc[-3]['close'] < df.iloc[-3]['open'] and
                df.iloc[-1]['close'] > df.iloc[-1]['open'] and
                df.iloc[-2]['close'] < min(df.iloc[-3]['close'], df.iloc[-1]['open']))

    def _detect_evening_star(self, df: pd.DataFrame) -> bool:
        """Detect Evening Star pattern"""
        if len(df) < 3:
            return False
        return (df.iloc[-3]['close'] > df.iloc[-3]['open'] and
                df.iloc[-1]['close'] < df.iloc[-1]['open'] and
                df.iloc[-2]['close'] > max(df.iloc[-3]['close'], df.iloc[-1]['open']))

    def calculate_fibonacci_levels(self, high: float, low: float) -> Dict[str, float]:
        """Calculate Fibonacci retracement levels"""
        diff = high - low
        return {
            'level_0': high,
            'level_23.6': high - (diff * 0.236),
            'level_38.2': high - (diff * 0.382),
            'level_50': high - (diff * 0.5),
            'level_61.8': high - (diff * 0.618),
            'level_100': low
        }

    def predict_price_trend(self, df: pd.DataFrame, periods_ahead: int = 5) -> Dict:
        """Simple linear regression for price prediction"""
        try:
            X = np.arange(len(df)).reshape(-1, 1)
            y = df['close'].values
            
            model = LinearRegression()
            model.fit(X, y)
            
            future_X = np.arange(len(df), len(df) + periods_ahead).reshape(-1, 1)
            predictions = model.predict(future_X)
            
            return {
                'predictions': predictions,
                'confidence': model.score(X, y),
                'trend': 'bullish' if model.coef_[0] > 0 else 'bearish'
            }
        except Exception as e:
            logger.error(f"Error predicting trend: {str(e)}")
            return {}

    def analyze_volume_profile(self, df: pd.DataFrame, bins: int = 20) -> Dict:
        """Analyze volume distribution by price level"""
        df['price_bin'] = pd.cut(df['close'], bins=bins)
        volume_by_price = df.groupby('price_bin')['volume'].sum()
        
        return {
            'poc': df['close'].iloc[volume_by_price.idxmax()],  # Point of Control
            'high_volume_nodes': volume_by_price.nlargest(3).index.tolist(),
            'volume_distribution': volume_by_price.to_dict()
        }

    def calculate_win_rate(self, df: pd.DataFrame) -> float:
        """Calculate win rate based on historical data"""
        df['returns'] = df['close'].pct_change()
        wins = (df['returns'] > 0).sum()
        total = len(df) - 1
        return (wins / total * 100) if total > 0 else 0

    def comprehensive_analysis(self, df: pd.DataFrame) -> Dict:
        """Perform comprehensive technical analysis"""
        analysis = {
            'timestamp': pd.Timestamp.now(),
            'price_current': df['close'].iloc[-1],
            'price_high_24h': df['high'].tail(24).max(),
            'price_low_24h': df['low'].tail(24).min(),
            'rsi': self.calculate_rsi(df).iloc[-1],
            'macd': self.calculate_macd(df),
            'bollinger_bands': {k: v.iloc[-1] for k, v in self.calculate_bollinger_bands(df).items()},
            'moving_averages': {k: v.iloc[-1] for k, v in self.calculate_moving_averages(df).items()},
            'volume_indicators': {k: v.iloc[-1] for k, v in self.calculate_volume_indicators(df).items()},
            'atr': self.calculate_atr(df).iloc[-1],
            'stochastic': {k: v.iloc[-1] for k, v in self.calculate_stochastic(df).items()},
            'patterns': self.identify_candlestick_patterns(df),
            'divergence': self.detect_divergence(df),
        }
        return analysis
