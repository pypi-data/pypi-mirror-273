from pydantic import BaseModel
from typing import Literal, NewType
from datetime import datetime

PropertyKeys = NewType("PropertyKeys", Literal["kakao_account.profile", "kakao_account.name", "kakao_account.email", "kakao_account.age_range", "kakao_account.birthday", "kakao_account.gender"])
AgeRange = NewType("AgeRange", Literal[
    "1~9",
    "10~14",
    "15~19",
    "20~29",
    "30~39",
    "40~49",
    "50~59",
    "60~69",
    "70~79",
    "80~89",
    "90~"
])
class KakaoIdTokenPayload(BaseModel):
    iss: str
    aud: str
    sub: str
    iat: int
    exp: int
    auth_time: int
    nonce: str
    nickname: str
    picture: str
    email: str

class KakaoTokenResponse(BaseModel):
    token_type: str
    access_token: str
    expires_in: int
    refresh_token: str
    refresh_token_expires_in: int
    id_token: KakaoIdTokenPayload | None = None
    scope: str | None = None


class KakaoProfile(BaseModel):
    nickname: str | None = None
    thumbnail_image_url: str | None = None
    profile_image_url: str | None = None
    is_default_image: bool | None = None
    is_default_nickname: bool | None = None


class KakaoAccount(BaseModel):
    profile_needs_agreement: bool | None = None
    profile_nickname_needs_agreement: bool | None = None
    profile_image_needs_agreement: bool | None = None
    profile: KakaoProfile | None = None
    name_needs_agreement: bool | None = None
    name: str | None = None
    email_needs_agreement: bool | None = None
    is_email_valid: bool | None = None
    is_email_verified: bool | None = None
    email: str | None = None
    age_range_needs_agreement: bool | None = None
    age_range: AgeRange | None = None
    birthyear_needs_agreement: bool | None = None
    birthyear: str | None = None
    birthday_needs_agreement: bool | None = None
    birthday: str | None = None
    birthday_type: Literal["SOLAR", "LUNAR"] | None = None
    gender_needs_agreement: bool | None = None
    gender: Literal["female", "male"] | None = None
    phone_number_needs_agreement: bool | None = None
    phone_number: str | None = None
    ci_needs_aggreement: bool | None = None
    ci: str | None = None
    ci_authenticated_at: datetime | None = None

class KakaoUserInfo(BaseModel):
    id: int
    has_signed_up: bool | None = None
    connected_at: datetime | None = None
    synched_at: datetime | None = None
    properties: dict | None = None
    kakao_account: KakaoAccount | None = None

class KakaoUserListResponse(BaseModel):
    elements: list[int]
    before_url: str | None = None
    after_url: str | None = None