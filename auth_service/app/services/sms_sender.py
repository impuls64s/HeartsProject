import asyncio

import aiohttp
from twilio.rest import Client

from app.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER


# async def send_sms(to_phone_number: str, message: str):
#     auth = aiohttp.BasicAuth(login=TWILIO_ACCOUNT_SID, password=TWILIO_AUTH_TOKEN)
#     async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(
#             login=TWILIO_ACCOUNT_SID, password=TWILIO_AUTH_TOKEN)) as session:
#         return await session.post(
#             f'https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json',
#             data={'From': TWILIO_PHONE_NUMBER, 'To': to_phone_number, 'Body': message})


def send_sms(to_phone_number: str, message: str):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    try:
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_phone_number
        )
        print(f"Message sent to {to_phone_number}. SID: {message.sid}")
    except Exception as e:
        print(f"Failed to send message to {to_phone_number}: {e}")

# Пример использования
# asyncio.run(send_sms('+79268172844', 'Ваш проверочный код: 1234'))


# send_sms('+79268172844', 'Ваш проверочный код: 1234666')

