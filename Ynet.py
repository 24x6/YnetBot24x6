import time
import asyncio
from telethon.sync import TelegramClient

class TelegramForwarder:
    def __init__(self, api_id, api_hash, phone_number):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client = TelegramClient('session_' + phone_number, api_id, api_hash)


    async def forward_messages_to_channel(self, source_chat_id, destination_channel_id):
        await self.client.connect()
        
        if not self.client.is_user_authorized():
            self.client.send_code_request('+972504640969')
            self.client.sign_in('+972504640969', input('Enter the code: '))
        
        last_message_id = (await self.client.get_messages(source_chat_id, limit=1))[0].id

        while True:
            print("Checking for messages and forwarding them...")
            # Get new messages since the last checked message
            messages = await self.client.get_messages(source_chat_id, min_id=last_message_id, limit=None)

            for message in reversed(messages):
                # Check if the message text includes any of the keywords
                message_clean: str = message.text
                i: int =  0
                i = message_clean.rfind('http')
                if i>0:
                    message_clean = message_clean[0:i-1]
                    message_clean = message_clean.replace(']','').replace('[','')

                await self.client.send_message(destination_channel_id, message_clean)
                print("Message forwarded")

                # Update the last message ID
                last_message_id = max(last_message_id, message.id)

            # Add a delay before checking for new messages again
            await asyncio.sleep(5)  # Adjust the delay time as needed


# Function to read credentials from file
def read_credentials():
    try:
        with open("credentials.txt", "r") as file:
            lines = file.readlines()
            api_id = lines[0].strip()
            api_hash = lines[1].strip()
            phone_number = lines[2].strip()
            return api_id, api_hash, phone_number
    except FileNotFoundError:
        print("Credentials file not found.")
        return None, None, None


async def main():
    
    print('bot start')
    
    forwarder = TelegramForwarder('22701033', '9428ef925607e9afe220e31176170b70', '+972504640969')

    source_chat_id = -1001397114707 
    destination_channel_id = -1001745841781 
    phone_number = '+972504640969'
    
        
    await forwarder.forward_messages_to_channel(source_chat_id, destination_channel_id)


# Start the event loop and run the main function
if __name__ == "__main__":
    asyncio.run(main())
