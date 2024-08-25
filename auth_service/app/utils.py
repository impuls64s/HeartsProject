import random
from typing import Dict, Union

import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUD_User
from app.models import User



def generate_verification_code() -> int:
    return random.randint(1000, 9999)


def string_to_number_conversion(data: Dict[str, Union[str, int]]) -> Dict[str, int]:
    for key, value in data.items():
        if isinstance(value, str) and value.isdigit():
            data[key] = int(value)
    return data


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt() 
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def check_password(hashed: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


async def authenticate_user(
        async_session: AsyncSession,
        email: str,
        password: str
    ) -> User | bool:
    user = await CRUD_User(async_session).read(email=email)
    if not user:
        return False
    if not check_password(user.password, password):
        return False
    return user


# payload = {
#     'sub': 1,
#     'username': 'imp64'
# }
# # print(encode_jwt(payload))
# token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsInVzZXJuYW1lIjoiaW1wNjQiLCJleHAiOjE3MjMwMzY0NDgsImlhdCI6MTcyMzAzNjI2OH0.efeavsFXG-Fx2tZS0DcHva-H9yQXAhWPp1goF7Q23ctunSEbbbM3XE2c_Lff-R1TGlPA-snZNwwl_Xm8T2jIqHPDwwB7fSuwv3r7DQr-Zp1v3s13MZRujNFqBJQot9_w84enVmOQ9CMyDpe9i6iZ6ZVlfUHbrfHxtXeL5fcCarGovHbj6p3ehKM3iKDgQEMNfNcYijyGFoTs8FwW23e3p-2w2LvGV9Y-A9b7_P8448VbBxolhih-L5LBEuhaY5AUnbpRvltmxuatAg5e6e_b3XRi4Oj1pZgLMJaemHXeCZLD9pQ9nBl0lsWYQnTvvW7K8xHDaQT6inA2CiU-iNI_fQ'
# print(decode_jwt(token))
