from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import aiosmtplib

from app.config import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD


async def send_verification_code(to_email: str, code: str) -> None:
    subject = f"Ваш проверочный код: {code}"
    body = f"Ваш проверочный код: {code}. Используйте его чтобы подтвердить почту."

    msg = MIMEMultipart()
    msg['From'] = SMTP_USERNAME
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        await aiosmtplib.send(
            msg,
            hostname=SMTP_SERVER,
            port=SMTP_PORT,
            username=SMTP_USERNAME,
            password=SMTP_PASSWORD,
            use_tls=True,
        )
        print(f"Verification code sent to {to_email}")
    except Exception as e:
        print(f"Failed to send verification code to {to_email}: {e}")


# import asyncio
# asyncio.run(send_verification_code('impuls_64@mail.ru', '1234'))
