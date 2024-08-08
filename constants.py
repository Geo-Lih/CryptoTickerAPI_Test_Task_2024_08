# URLs for WebSocket and API endpoints
BINANCE_PAIR_WEBSOCKET_URL = "wss://stream.binance.com:9443/ws/{}@ticker"
BINANCE_ALL_PAIRS_WEBSOCKET_URL = "wss://stream.binance.com:9443/ws/!ticker@arr"
KRAKEN_ASSET_PAIRS_URL = "https://api.kraken.com/0/public/AssetPairs"
KRAKEN_WEBSOCKET_URL = "wss://ws.kraken.com/v2"


# Batch size for splitting lists
BATCH_SIZE = 400


# Exchange names
BINANCE = 'binance'
KRAKEN = 'kraken'

# Exchange-specific keys for processing data
EXCHANGE_KEYS = {
    BINANCE: {
        'bid': 'b',
        'ask': 'a',
        'symbol': 's'
    },
    KRAKEN: {
        'bid': 'bid',
        'ask': 'ask',
        'symbol': 'symbol'
    }
}
