from pybit.unified_trading import HTTP

class ByBitManager:
    def __init__(self, api_key, api_secret, testnet=False, demo=False):
        ''' Initialize the ByBit API

        Parameters:
            - api_key (str): API key
            - api_secret (str): API secret
            - testnet (bool): Testnet or not
        '''
        self.session = HTTP(api_key=api_key, api_secret=api_secret, testnet=testnet, demo=demo)

    def set_info(self, symbol, qty, tp, sl):
        ''' Set information for the order

        Parameters:
            - symbol (str): Symbol
            - qty (float): Quantity
            - tp (float): Take profit
            - sl (float): Stop loss

        Returns:
            - str: Information set successfully
        '''
        # Set information
        self.symbol = symbol
        self.qty = qty
        self.tp = tp
        self.sl = sl
        # Return message
        return "Information set successfully."

    def bid_ask_prices(self):
        ''' Get bid and ask prices from the orderbook

        Returns:
            - bid_price (float): Bid price
            - bid_qty (float): Bid quantity
            - ask_price (float): Ask price
            - ask_qty (float): Ask quantity
        '''
        # Bid price -> Sell price
        self.bid_price = float(self.session.get_orderbook(category="linear", symbol=self.symbol).get('result')['b'][0][0])
        self.bid_qty = float(self.session.get_orderbook(category="linear", symbol=self.symbol).get('result')['b'][0][1])
        # Ask price -> Buy price
        self.ask_price = float(self.session.get_orderbook(category="linear", symbol=self.symbol).get('result')['a'][0][0])
        self.ask_qty = float(self.session.get_orderbook(category="linear", symbol=self.symbol).get('result')['a'][0][1])
        # Return prices
        return {
            'bid_price': self.bid_price,
            'bid_qty': self.bid_qty,
            'ask_price': self.ask_price,
            'ask_qty': self.ask_qty
        }

    def market_order(self, side):
        ''' Market order

        Parameters:
            - side (str): Buy or Sell 

        Returns:
            - bool: Order placed successfully or not       
        '''
        # Register last side
        self.side = side
        # Check if the minimum quantity is respected
        self.get_precision()
        if self.qty < self.min_qty:
            return None
        else:
            # Get bid and ask prices
            self.bid_ask_prices()
            # Based on the side, place the order
            # Set stop loss and take profit
            if side == "Buy":
                self.price = self.ask_price
                self.take_profit = self.ask_price * (1 + self.tp)
                self.stop_loss = self.ask_price * (1 - self.sl)
            elif side == "Sell":
                self.price = self.bid_price
                self.take_profit = self.bid_price * (1 - self.tp)
                self.stop_loss = self.bid_price * (1 + self.sl)
            # Place order
            order = self.session.place_order(
                category="linear", 
                side=side, 
                symbol=self.symbol, 
                order_type="Market", 
                qty=self.qty,
                takeProfit=self.take_profit,
                stopLoss=self.stop_loss,)
            # Get order ID
            self.order_id = order['result']['orderId']
            
            # Return that the order was placed successfully
            return order

    def get_position(self):
        ''' Get position informations

        Returns:
            - dict: Position informations
        '''
        # Get position
        position = self.session.get_positions(category='linear', symbol=self.symbol)['result']['list'][0]
        # Get position informations
        self.position_side = position['side']
        self.position_size = position['size']
        self.position_avgprice = position['avgPrice']
        self.position_value = position['positionValue']
        self.pnl = position['unrealisedPnl']
        self.position_price = position['markPrice']

        # Return position informations
        return {
            'side': self.position_side,
            'size': self.position_size,
            'avgprice': self.position_avgprice,
            'value': self.position_value,
            'price': self.position_price}

    def get_precision(self):
        ''' Get precision informations for the symbol
        
        Returns:
            - dict: Precision informations
        '''
        precision = self.session.get_instruments_info(
            category='linear',
            symbol=self.symbol
        )['result']['list'][0]
        # Get precision informations on quantity and price
        self.min_qty = float(precision['lotSizeFilter']['minOrderQty'])
        # At the moment, we are not using price precision
        # price = precision['priceFilter']['tickSize']

        # Return precision informations
        return {
            'min_qty': self.min_qty
        }