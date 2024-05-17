from enum import Enum

auth = r"https://kauth.kakao.com"
api = r"https://kapi.kakao.com"

class KAUTHURL(str, Enum):
    AUTHORIZE = f"{auth}/oauth/authorize"
    TOKEN = f"{auth}/oauth/token"
    LOGOUT = f"{auth}/oauth/logout"


class KAPIURL(str, Enum):
    LOGOUT = f"{api}/v1/user/logout"
    UNLINK = f"{api}/v1/user/unlink"
    TOKENINFO = f"{api}/v1/user/access_token_info"
    USERINFO = f"{api}/v2/user/me"
    USERSINFO = f"{api}/v2/app/users"
    USERLIST = f"{api}/v1/user/ids"
    SCOPES = f"{api}/v2/user/scopes"
    REVOKE_SOCPES = f"{api}/v2/user/revoke/scpoes"