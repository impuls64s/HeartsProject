from datetime import datetime, timedelta, timezone

import jwt

from app.config import JWTSettings


TYPE_ACCESS_TOKEN = 'access'
TYPE_REFRESH_TOKEN = 'refresh'


def create_access_token(
        payload: dict,
        type: str = TYPE_ACCESS_TOKEN,
        algorithm: str = JWTSettings.algorithm,
        private_key: str = JWTSettings.private_key_path.read_text(),
        expire_minutes: int = JWTSettings.access_token_expire_minutes
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expire_minutes)
    to_encode.update({'exp': expire, 'type': type, 'iat': now})
    encoded_jwt = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded_jwt


def create_refresh_token(
        payload: dict,
        type: str = TYPE_REFRESH_TOKEN,
        algorithm: str = JWTSettings.algorithm,
        private_key: str = JWTSettings.private_key_path.read_text(),
        expire_minutes: int = JWTSettings.refresh_token_expire_minutes
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expire_minutes)
    to_encode.update({'exp': expire, 'type': type, 'iat': now})
    encoded_jwt = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded_jwt


def verify_token(
        token: str,
        algorithm: str = JWTSettings.algorithm,
        public_key: str = JWTSettings.public_key_path.read_text(),
) -> dict | str:
    decoded_token = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded_token


class InvalidTokenTypeError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


def refresh_access_token(refresh_token: str) -> str:
    payload = verify_token(refresh_token)
    token_type = payload.get('type')
    if token_type == TYPE_REFRESH_TOKEN:
        new_access_token = create_access_token(payload)
        return new_access_token
    else:
        raise InvalidTokenTypeError('The token type must be refresh')



# a_payload = {'sub': 1, 'name': 'oleg'}
# access_token = create_access_token(a_payload)
# print(access_token)

# r_payload = {'sub': 1, 'name': 'oleg'}
# refresh_token = create_refresh_token(r_payload)
# print(refresh_token)

# t = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsIm5hbWUiOiJvbGVnIiwiZXhwIjoxNzIzMTk4OTMyLCJ0eXBlIjoicmVmcmVzaCJ9.ckpLVRBhD5Is72y7X-q1mT4op4h6041gxAPDVnkcAAh17D2iHHEF-7AmR90-7f2rT2g37DwB1fDPx_jcOjsW5N_MWSo87QbhG5vTWOs4F-sOFPTu7NkSqIQzmRESpDExSLs7mGqHqapZK-xxZS57KEvkSIfswjkMm-9kgi__1-QSrJf57BDSi20sImTfQxRVxNrutVpR9Jy0l5CszSIdMAcTf3H1kA8z9fZv1hC9RRK4WcW1FN6oXdudH1FieRpUP7l05aTOCkWr-nGDJLE7nCq5k3pF42u_Ec506BXrjZsvmYSX-z-xuHYf7ENm-QPMhim_haVhkev-CdRYeCUZjw'
# print(verify_token(t))


# r = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjksIm5hbWUiOiJPbGVnZ2ciLCJleHAiOjE3MjMxMTg0NzQsInR5cGUiOiJhY2Nlc3MifQ.XrHSxD5FlrYzbJ9FUvTNnV8r-AjIp91IsIzTInREtJGT1meKTystF41Hyhtp9Z8sD40GidtvGEQUpDf67_WyzK1sP2m-_j2CnwdRe3TyZ7UnRKBIwo8FK1mxitkSLKE65nyA9U1bd8TIL7MDJTwXwb7-dHv1SwlwaJGNzfv_yIJOJveGhKk_UOu6g4yFsZ0NJo8PgS8_Xjw_6pn5GbKukFyTAhz6pktF0I0zPE0iOb_6y_mUBGxHhdxOBmlM6SxslmcWl6kQj6wFeLbkbBLGXTh1e_Y11OTRrT3yOdVSinG7NK2kye4ZOZ8hQHUHdV3ETf2VGdnW0kgHPL0xOTZJyA'
# n = refresh_access_token(r)
# print(n)

