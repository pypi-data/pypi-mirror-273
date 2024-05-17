from .bybit import ByBitManager
from .log import LogMessage, write_file
from .telegram import Telegram


class Framework:
    def __init__(self, bot_name, telegram_api_key, telegram_chat_id, bybit_api_key, bybit_api_secret, quiet_mode=False, testnet=False):
        # Set the bot name
        self.bot_name = bot_name
        # Set the quiet mode of the bot
        self.quiet_mode = quiet_mode
        # Check if we are in testnet, if so set demo to True
        demo = True if testnet else False
        # Try to create a LogMessage object
        try:
            # Create a Telegram object
            self.telegram = Telegram(telegram_api_key, telegram_chat_id)
            # Create a ByBit object
            self.bybit = ByBitManager(api_key=bybit_api_key, api_secret=bybit_api_secret, testnet=testnet, demo=demo)
            # Create a LogMessage object
            self.log = LogMessage(telegram_api_key, telegram_chat_id, quiet_mode=quiet_mode)
        # If an error occurs, log the error
        except:
            # Log the error, we use the write_file function from the log module 
            # since we don't know if telegram is working
            write_file('', 'log_errors.txt', f"Framework __init__ error")
        
        # Check if the bot is in quiet mode, if not, send a message to the Telegram chat
        if not self.quiet_mode:
            # Confirm the initialization of the bot
            self.telegram.send_message(f'{self.bot_name} initialized successfully.')

    def set_parameters(self, symbol, qty, tp, sl):
        ''' Set the parameters for the bot

        Parameters:
            - symbol (str): Symbol
            - qty (float): Quantity
            - tp (float): Take profit
            - sl (float): Stop loss
        '''
        # Set the information for the strategy
        self.symbol = symbol
        self.qty = qty
        self.tp = tp
        self.sl = sl

        # Set the information for the ByBit object
        self.bybit.set_info(symbol, qty, tp, sl)

        # Check if the bot is in quiet mode, if not, send a message to the Telegram chat
        if not self.quiet_mode:
            # Confirm the parameters were set successfully
            self.telegram.send_message(
                f'{self.bot_name} parameters has been set.\
                \nSymbol: {self.symbol} \nQuantity: {self.qty}\
                \nTake Profit: {self.tp} \nStop Loss: {self.sl}')
        
    def check_status(self):
        ''' Check the status of the bot for the symbol. The status can be 'NEUTRAL', 'LONG' or 'SHORT'. '''
        # Check in the status folder which is the last status of the bot for the symbol
        # If the file doesn't exist, create it with the default content 'NEUTRAL'
        self.status = self.log.read_file(
            folder='status',
            filename=f'{self.symbol}.txt',
            default_content='NEUTRAL'
        )

    def set_status(self, status):
        ''' Set the status of the bot for the symbol. The status can be 'NEUTRAL', 'LONG' or 'SHORT'. '''
        # Save the status in the status folder
        self.log.write_file(
            folder='status',
            filename=f'{self.symbol}.txt',
            message=status
        )

    def check_signal(self, entry, exit, short_entry, short_exit):
        # First we check the status of the bot
        self.check_status()

        # Mask for each type of signal (entry, exit, short_entry, short_exit)
        # Long signals
        entry_mask = (entry == True) & (exit == False) & (self.status == 'NEUTRAL')
        exit_mask = (entry == False) & (exit == True) & (self.status == 'LONG')
        # Short signals
        short_entry_mask = (short_entry == True) & (short_exit == False) & (self.status == 'NEUTRAL')
        short_exit_mask = (short_entry == False) & (short_exit == True) & (self.status == 'SHORT')
        # Reverse position signals
        reverse_mask = (entry == False) & (exit == True) & \
                       (short_entry == True) & (short_exit == False) & \
                       (self.status == 'LONG')
        short_reverse_mask = (entry == True) & (exit == False) & \
                             (short_entry == False) & (short_exit == True) & \
                             (self.status == 'SHORT')
        
        #  Now, verify if current position should be modified
        # Long entry signal
        if entry_mask and not short_entry_mask:
            # Open a long position
            order = self.bybit.market_order('Buy')
            # Save the status
            self.set_status('LONG')
            # Send a message to the Telegram chat
            self.telegram.send_message(f'{self.bot_name} opened a LONG position for {self.symbol}.')
        # Long exit signal
        if exit_mask and not short_exit_mask:
            # Close the long position
            order = self.bybit.market_order('Sell')
            # Save the status
            self.set_status('NEUTRAL')
            # Send a message to the Telegram chat
            self.telegram.send_message(f'{self.bot_name} closed the LONG position for {self.symbol}.')
        # Short entry signal
        if short_entry_mask and not entry_mask:
            # Open a short position
            order = self.bybit.market_order('Sell')
            # Save the status
            self.set_status('SHORT')
            # Send a message to the Telegram chat
            self.telegram.send_message(f'{self.bot_name} opened a SHORT position for {self.symbol}.')

        # Short exit signal
        if short_exit_mask and not entry_mask:
            # Close the short position
            order = self.bybit.market_order('Buy')
            # Save the status
            self.set_status('NEUTRAL')
            # Send a message to the Telegram chat
            self.telegram.send_message(f'{self.bot_name} closed the SHORT position for {self.symbol}.')
        
        ''' TODO: Implement the reverse position signals 
        # Reverse position signal
        if reverse_mask:
            # Close the long position
            order = self.bybit.market_order('Sell')
            # Open a short position
            order = self.bybit.market_order('Sell')
            # Save the status
            self.set_status('SHORT')
            # Send a message to the Telegram chat
            self.telegram.send_message(f'{self.bot_name} reversed the LONG position for {self.symbol} to SHORT.')

        # Short reverse position signal
        if short_reverse_mask:
            # Close the short position
            order = self.bybit.market_order('Buy')
            # Open a long position
            order = self.bybit.market_order('Buy')
            # Save the status
            self.set_status('LONG')
            # Send a message to the Telegram chat
            self.telegram.send_message(f'{self.bot_name} reversed the SHORT position for {self.symbol} to LONG.')
        '''

        
    

