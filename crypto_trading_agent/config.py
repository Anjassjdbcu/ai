"""
Configuration settings for Crypto Trading AI Agent
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Environment Configuration
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ENV = os.getenv("ENV", "production")

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Crypto Exchange APIs
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
COINBASE_API_KEY = os.getenv("COINBASE_API_KEY")
KRAKEN_API_KEY = os.getenv("KRAKEN_API_KEY")

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_NAME = os.getenv("DB_NAME", "crypto_trading")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Redis Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)

# Notification Settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")

# Trading Parameters
DEFAULT_TIMEFRAME = "1h"  # 1m, 5m, 15m, 1h, 4h, 1d
DEFAULT_LOOKBACK = 100  # Number of candles for analysis
RISK_PER_TRADE = 0.02  # 2% risk per trade
MAX_OPEN_POSITIONS = 5
STOP_LOSS_PERCENT = 0.05  # 5%
TAKE_PROFIT_PERCENT = 0.15  # 15%

# AI Model Configuration
MODEL_TYPE = os.getenv("MODEL_TYPE", "gpt-4")  # gpt-4, claude-3, command
TEMPERATURE = 0.7
MAX_TOKENS = 2000

# Supported Cryptocurrencies
WATCH_LIST = [
    "BTC/USDT",
    "ETH/USDT",
    "BNB/USDT",
    "SOL/USDT",
    "ADA/USDT",
    "XRP/USDT",
    "DOGE/USDT",
    "AVAX/USDT",
    "LINK/USDT",
    "MATIC/USDT",
]

# Analysis Indicators
USE_INDICATORS = {
    "RSI": True,
    "MACD": True,
    "Bollinger_Bands": True,
    "Moving_Averages": True,
    "Volume": True,
    "Fibonacci": True,
}

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = "logs/crypto_agent.log"

# Server Configuration
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", 5000))
