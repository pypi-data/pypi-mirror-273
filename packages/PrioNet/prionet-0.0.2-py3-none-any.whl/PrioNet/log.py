import os

from .telegram import Telegram

class LogMessage:
    def __init__(self, api_key, chat_id, quiet_mode=False):
        ''' Initialize the LogMessage class with the Telegram API key and chat ID.

            Parameters:
                - api_key (str): The API key of the Telegram bot
                - chat_id (str): The chat ID of the Telegram chat
                - quiet_mode (bool): If True, the bot won't send messages to the Telegram chat
        '''
        # Create a Telegram object
        self.telegram = Telegram(api_key, chat_id)
        # Set the quiet mode of the bot
        self.quiet_mode = quiet_mode

    def read_file(self, folder, filename, default_content=None):
        ''' Read a file from a folder, if the file doesn't exist, create it with default content\
            and return the default content. If the file exists, return the content of the file.

            Parameters:
                - folder (str): The folder where the file is located
                - filename (str): The name of the file
                - default_content (str): The default content of the file (if the file doesn't exist)

            Returns:
                - content (str): The content of the file
        '''
        ## Folder Check
        # Check if the folder exists, if not, create it
        if not os.path.exists(folder):
            # Create a folder
            os.makedirs(folder)
            
        # Join the folder path with the file name
        file_path = os.path.join(folder, filename)

        ## File Check
        # Try to open the file, if it doesn't exist, create it
        try:
            # Try to open the file for reading
            with open(file_path, 'r') as file:
                # Read the contents of the file
                content = file.read()
    
        except FileNotFoundError:
            # Check if the bot is in quiet mode, if not, send a message to the Telegram chat
            if not self.quiet_mode:
                # Send a message to the Telegram chat with the error
                self.telegram.send_message(f'Error: File {filename} not found in {folder}. \
                                        \nCreating file with default content: {default_content}.')
            # If the file doesn't exist, create it with default content
            with open(file_path, 'w') as file:
                file.write(default_content)
            # Return the default content
            return default_content

        # Return the content
        return content

    def write_file(self, folder, filename, message, append=False):
        ''' Write a message to a file in a folder. If the file doesn't exist, create it with the message.
            Append the message to the file if append is True, otherwise write the message to the file.

            Parameters:
                - folder (str): The folder where the file is located
                - filename (str): The name of the file
                - message (str): The message to write to the file
                - append (bool): If True, append the message to the file, if False, write the message to the file
        '''
        ## Folder Check
        # Check if the folder exists, if not, create it
        if not os.path.exists(folder):
            # Create a folder
            os.makedirs(folder)
            
        # Join the folder path with the file name
        file_path = os.path.join(folder, filename)

        ## File Check
        # Try to open the file, if it doesn't exist, create it
        try:
            # Check if we are appending or writing
            if append: 
                # Open the file for appending
                with open(file_path, 'a') as file:
                    # Append new content to the file
                    file.write(message)
            else:
                # Open the file for writing
                with open(file_path, 'w') as file:
                    # Write new content to the file
                    file.write(message)

        except FileNotFoundError:
            # Check if the bot is in quiet mode, if not, send a message to the Telegram chat
            if not self.quiet_mode:
                # Send a message to the Telegram chat with the error
                self.telegram.send_message(f'Error: File {filename} not found in {folder}')
            # If the file doesn't exist, create it with the message
            with open(file_path, 'w') as file:
                # In this case, we don't need to check if we are appending or writing
                # because we are creating the file from scratch
                file.write(message)

def read_file(folder, filename, default_content=None):
    ''' Read a file from a folder, if the file doesn't exist, create it with default content\
        and return the default content. If the file exists, return the content of the file.

        Parameters:
            - folder (str): The folder where the file is located
            - filename (str): The name of the file
            - default_content (str): The default content of the file

        Returns:
            - content (str): The content of the file

        Observations:
            - This function is not part of the LogMessage class, it is a standalone function.
              The difference is that this function doesn't send a message to the Telegram chat.
              I kept this function as a standalone function because it can be useful in other contexts.
    '''
    ## Folder Check
    # Check if the folder exists, if not, create it
    if not os.path.exists(folder):
        # Create a folder
        os.makedirs(folder)
        
    # Join the folder path with the file name
    file_path = os.path.join(folder, filename)

    ## File Check
    # Try to open the file, if it doesn't exist, create it
    try:
        # Try to open the file for reading
        with open(file_path, 'r') as file:
            # Read the contents of the file
            content = file.read()
 
    except FileNotFoundError:
        # If the file doesn't exist, create it with default content
        with open(file_path, 'w') as file:
            file.write(default_content)
        # Return the default content
        return default_content

    # Return the content
    return content

def write_file(folder, filename, message, append=False):
    ''' Write a message to a file in a folder. If the file doesn't exist, create it with the message.
        Append the message to the file if append is True, otherwise write the message to the file.

        Parameters:
            - folder (str): The folder where the file is located
            - filename (str): The name of the file
            - message (str): The message to write to the file
            - append (bool): If True, append the message to the file, if False, write the message to the file

        Observations:
            - This function is not part of the LogMessage class, it is a standalone function.
              The difference is that this function doesn't send a message to the Telegram chat.
              I kept this function as a standalone function because it can be useful in other contexts.
    '''
    ## Folder Check
    # Check if the folder exists, if not, create it
    if not os.path.exists(folder):
        # Create a folder
        os.makedirs(folder)
        
    # Join the folder path with the file name
    file_path = os.path.join(folder, filename)

    ## File Check
    # Try to open the file, if it doesn't exist, create it
    try:
        # Check if we are appending or writing
        if append: 
            # Open the file for appending
            with open(file_path, 'a') as file:
                # Append new content to the file
                file.write(message)
        else:
            # Open the file for writing
            with open(file_path, 'w') as file:
                # Write new content to the file
                file.write(message)

    except FileNotFoundError:
        # If the file doesn't exist, create it with the message
        with open(file_path, 'w') as file:
            # In this case, we don't need to check if we are appending or writing
            # because we are creating the file from scratch
            file.write(message)