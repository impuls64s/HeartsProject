from enum import Enum
from typing import Optional, ClassVar
from typing_extensions import Self

from pydantic import BaseModel, EmailStr, ConfigDict, model_validator, Field, PrivateAttr
from pydantic_extra_types.phone_numbers import PhoneNumber


class StatusEnum(str, Enum):
    UNDER_REVIEW = "UNDER_REVIEW"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class GenderEnum(str, Enum):
    MAN = 'MAN'
    WOMAN = 'WOMAN'


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr | None = None
    phone_number: PhoneNumber | None = None
    name: str = Field(max_length=30)
    gender: GenderEnum
    age: int = Field(ge=18, lt=100)
    height: int | None = None
    weight: int | None = None
    status: StatusEnum = StatusEnum.UNDER_REVIEW


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=20)

    @model_validator(mode='after')
    def verify_login(self) -> Self:
        if not self.email and not self.phone_number:
            raise ValueError('No mail or phone number')
        return self


class UserView(UserBase):
    id: int


class UserChange(UserBase):
    name: str | None = Field(None, max_length=30)
    gender: GenderEnum | None = None
    age: int | None = Field(None, ge=18, lt=100)


class FullUserInfo(UserView):
    logged_in_at: int
    expires: int


class TempUserData(BaseModel):
    key: str
    code: int


class JWToken(BaseModel):
    access_token: str = None
    refresh_token: str = None
    token_type: str = 'Bearer'


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# u = UserBase(
#     email='oleg@mail.ru',
#     phone_number=None,
#     password='strongpassword',
#     name='Oleg',
#     gender='MAN',
#     height= None,
#     weight=None,
#     age=25,
#     status=StatusEnum.UNDER_REVIEW
# )

# print(u.model_dump(exclude_none=True))
# # print(u)

# d = {'email': 'oleg@mail.ru', 'password': 'strongpassword', 'name': 'Oleg', 'gender': 'MAN', 'age': 25, 'status': 'UNDER_REVIEW'}
# user = UserBase.model_validate(d)
# print(user)

# sh = ShortUserBase.model_validate(d)

# converted_data = {key: (value if value else '') for key, value in u}
# print(converted_data)

# user_data = {
#     "email": "user@example.com",
#     "phone_number": None,
#     "password": "securepassword",
#     "name": "John Doe",
#     "gender": "MAN",
#     "age": "25",
#     "height": "180",
#     "weight": "75",
#     "status": "UNDER_REVIEW"
# }

# user = UserBase.model_validate(user_data)
# print(user)
