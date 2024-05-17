from .utils import (
    Singleton,
)
from .urls import (
    KAPIURL,
    KAUTHURL
)
from .types import (
    KakaoTokenResponse,
    PropertyKeys,
    KakaoUserInfo,
    KakaoUserListResponse
)
from .exceptions import (
    KakaoApiBadRequest
)

from typing import (
    Literal
)

from httpx import (
    AsyncClient
)
from json import dumps

class KakaoApi(metaclass=Singleton):
    content_type = 'application/x-www-form-urlencoded;charset=utf-8'

    def __init__(
            self,
            client_id: str,
            admin_key: str,
            redirect_uri: str | None = None,
            client_secret: str | None = None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.admin_key = admin_key
        self.redirect_uri = redirect_uri

    def get_authorze_uri(
            self,
            client_id: str | None = None,
            redirect_uri: str | None = None,
            scope: str | None = None,
            prompt: str | None = None,
            login_hint: str | None = None,
            service_terms: str | None = None,
            state: str | None = None,
            nonce: str | None = None
    ) -> str:
        """
        Args:
            client_id:
            redirect_uri:
            scope:
            prompt:
            login_hint:
            service_terms:
            state:
            nonce:
        """
        client_id = client_id or self.client_id
        redirect_uri = redirect_uri or self.redirect_uri
        assert redirect_uri is not None, "redirect_uri is required"

        url = (f"{KAUTHURL.AUTHORIZE.value}?"
                f"response_type=code&"
                f"client_id={client_id}&"
                f"redirect_uri={redirect_uri}")
        if state:
            url += f"&state={state}"
        if scope:
            url += f"&scope={scope}"
        if prompt:
            url += f"&prompt={prompt}"
        if login_hint:
            url += f"&login_hint={login_hint}"
        if service_terms:
            url += f"&service_terms={service_terms}"
        if nonce:
            url += f"&nonce={nonce}"
        return url

    async def get_token(
            self,
            code: str,
            client_id: str | None = None,
            redirect_uri: str | None = None,
            client_secret: str | None = None,
            grant_type: str = 'authorization_code',
    ) -> KakaoTokenResponse:
        """ 토큰 요청
        Args:
            code:
            client_id:
            redirect_uri:
            client_secret:
            grant_type: authorization_code 고정

        Raises:
            KakaoApiBadRequest:
        """
        client_id = client_id or self.client_id,
        redirect_uri = redirect_uri or self.redirect_uri
        assert redirect_uri is not None, "redirect_uri is required"
        headers = {
            "Content-Type": self.content_type
        }

        async with AsyncClient(headers=headers) as session:
            res = await session.post(
                url=KAUTHURL.TOKEN.value,
                data={
                    'grant_type': grant_type,
                    'client_id': client_id,
                    'redirect_uri': redirect_uri,
                    'code': code,
                    'client_secret': client_secret
                },
            )

        if not res.is_success:
            raise KakaoApiBadRequest

        res = res.json()
        return KakaoTokenResponse(**res)

    async def refresh_token(
            self,
            refresh_token: str,
            client_id: str | None = None,
            client_secret: str | None = None
    ) -> KakaoTokenResponse:
        client_id = client_id or self.client_id
        assert client_id is not None, "client_id is required"
        headers = {
            "Content-Type": self.content_type
        }
        data = {
            "grent_type": "refresh_token",
            "client_id": client_id,
            "refresh_token": refresh_token,
            "client_secret": client_secret,
        }
        async with AsyncClient(
                headers=headers
        ) as session:
            res = await session.post(
                data=data
            )
        if not res.is_success:
            raise KakaoApiBadRequest
        return KakaoTokenResponse(**res.json())

    async def get_user_info(
            self,
            access_token: str,
            secure_resource: bool | None = False,
            property_keys: list[PropertyKeys] | None = None
    ) -> KakaoUserInfo:
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': self.content_type
        }
        params = {
            "secure_resource": secure_resource
        }
        async with AsyncClient(
                headers=headers,
                params=params
        ) as session:
            url = KAPIURL.USERINFO.value
            if property_keys is None:
                res = await session.get(url)
            else:
                res = await session.post(
                    url=url,
                    params={
                        "property_keys": dumps(property_keys)
                    }
                )

        if not res.is_success:
            raise KakaoApiBadRequest

        return KakaoUserInfo(**res.json())

    async def get_user_info_by_admin(
            self,
            target_id: str,
            admin_key: str | None = None,
            secure_resource: bool | None = False,
            property_keys: list[PropertyKeys] | None = None
    ) -> KakaoUserInfo:
        admin_key = admin_key or self.admin_key
        headers = {
            'Authorization': f'KakaoAK {admin_key}',
            'Content-Type': self.content_type
        }
        params = {
            "secure_resource": secure_resource
        }
        if property_keys:
            params.update({"property_keys": dumps(property_keys)})

        async with AsyncClient(
                headers=headers,
                params=params
        ) as session:
            url = KAPIURL.USERINFO.value
            res = await session.post(
                url=url,
                data={
                    "target_id_type": "user_id",
                    "target_id": target_id
                }
            )

        if not res.is_success:
            raise KakaoApiBadRequest

        return KakaoUserInfo(**res.json())

    async def get_users_info(
            self,
            admin_key: str | None = None,
            target_ids: list[int] | None = None,
            property_keys: list[PropertyKeys] | None = None
    ) -> list[KakaoUserInfo]:
        admin_key = admin_key or self.admin_key
        assert admin_key is not None, "Admin key is required"

        property_keys = property_keys or ["kakao_account.", "has_signed_up"]

        url = KAPIURL.USERSINFO.value
        headers = {
            "Content-Type": self.content_type,
            "Authorization": f'KakaoAK {admin_key}'
        }
        params = {
            "target_id_type": "user_id",
            "target_ids": dumps(target_ids[:1]),
            "property_keys": dumps(property_keys)
        }

        async with AsyncClient(
            headers=headers,
            params=params
        ) as session:
            res = await session.get(
                url=url
            )

        if not res.is_success:
            raise KakaoApiBadRequest
        return [KakaoUserInfo(**i) for i in res.json()]

    async def get_user_list(
            self,
            admin_key: str | None = None,
            limit: int | None = 100,
            from_id: str | None = None,
            order: Literal["asc", "desc"] = "asc",
    ) -> KakaoUserListResponse:
        """
        Args:
            admin_key:
            limit: 최소 1 최대 100
            from_id:
            order:
        """
        admin_key = admin_key or self.admin_key
        assert admin_key is not None, "Admin key required"

        headers = {
            "Authorization": f'KakaoAK {admin_key}',
            "Content-Type": self.content_type
        }
        params = {
            "limit": limit,
            "from_id": from_id,
            "order": order,
        }
        url = KAPIURL.USERLIST.value
        async with AsyncClient(
            headers=headers,
            params=params
        ) as session:
            res = await session.get(
                url=url
            )

        if not res.is_success:
            raise KakaoApiBadRequest

        return KakaoUserListResponse(**res.json())
