class ExchangeConnector:
    """
    Manages exchange connections.

    Methods:
    - start: Starts a new exchange connection and adds it to the connections list.
    - stop_connections: Stops all active connections and clears the list.
    """
    def __init__(self):
        self.connections = []

    async def start(self, exchange_class, websocket, pair):
        exchange = exchange_class(websocket, pair)
        self.connections.append(exchange)
        await exchange.start()

    async def stop_connections(self):
        for connection in self.connections:
            await connection.close()
        self.connections.clear()
