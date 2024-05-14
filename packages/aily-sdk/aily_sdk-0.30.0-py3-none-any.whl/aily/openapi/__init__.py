import arrow
import requests
from loguru import logger


class OpenAPIClient:
    def __init__(self, user_access_token=None, app_id=None, app_secret=None):
        self.token = None
        if user_access_token:
            self.token = user_access_token
        if app_id and app_secret:
            self.token = self.get_tenant_access_token(app_id, app_secret)

    def use_user_access_token(self, user_access_token):
        self.token = user_access_token

    def use_tenant_access_token(self, tenant_access_token=None, app_id=None, app_secret=None):
        if tenant_access_token:
            self.token = tenant_access_token

        if app_id and app_secret:
            self.token = self.get_tenant_access_token(app_id, app_secret)

    @staticmethod
    def get_tenant_access_token(app_id, app_secret):
        url = "https://open.larkoffice.com/open-apis/auth/v3/tenant_access_token/internal"

        headers = {
            "Content-Type": "application/json; charset=utf-8"
        }

        data = {
            "app_id": app_id,
            "app_secret": app_secret
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            code = result.get("code")
            if code == 0:
                return result.get("tenant_access_token")
            else:
                logger.info(f"获取 tenant_access_token 失败,错误码: {code}, 错误信息: {result.get('msg')}")
        else:
            logger.info(f"请求失败,状态码: {response.status_code}, 错误信息: {response.text}")

        return None

    def get(self, url, headers=None, data=None, query=None):
        _headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
            'User-Agent': 'Aily Python SDK'
        }
        if headers:
            _headers.update(headers)
        resp = requests.get(url, headers=_headers, json=data, params=query)

        logger.info(f'logid= {resp.headers["X-Tt-Logid"]} content= {resp.content}')

        if resp.json()['code'] != 0:
            logger.error(f'response = {resp.json()}')
            raise Exception(f'OpenAPI 错误:{resp.json()}')
        return resp.json()

    def post(self, url, headers=None, data=None, query=None, files=None, json=None):
        _headers = {
            'Authorization': f'Bearer {self.token}',
            'User-Agent': 'Aily Python SDK'
        }
        if headers:
            _headers.update(headers)
        resp = requests.post(url, headers=_headers, json=json, data=data, params=query, files=files)
        logger.info(f'logid= {resp.headers["X-Tt-Logid"]} content= {resp.content}')
        if resp.json()['code'] != 0:
            logger.error(f'response = {resp.json()}')
            raise Exception(f'OpenAPI 错误:{resp.json()}')
        return resp.json()


class UserAccessTokenClient:
    def __init__(self, app_id, app_secret, user_access_token=None, refresh_token=None, expires_in=None,
                 refresh_expires_in=None):
        self.app_id = app_id
        self.app_secret = app_secret
        self.user_access_token = user_access_token
        self.refresh_token = refresh_token

        self.user_access_token_expires_at = None
        if expires_in is not None:
            self.user_access_token_expires_at = arrow.now().shift(seconds=expires_in)

        self.refresh_token_expires_at = None
        if refresh_expires_in is not None:
            self.refresh_token_expires_at = arrow.now().shift(seconds=refresh_expires_in)

    def init_with_code(self, code):
        url = f"https://open.larkoffice.com/open-apis/authen/v1/oidc/access_token"
        headers = {
            "Authorization": f'Bearer {self.get_app_access_token()}',
            "Content-Type": "application/json; charset=utf-8",
            'User-Agent': 'Aily Python SDK'
        }
        data = {
            "code": code,
            "grant_type": "authorization_code"
        }
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        if result.get("data"):
            self.user_access_token = result["data"]["access_token"]
            self.refresh_token = result["data"]["refresh_token"]
            expires_in = result["data"]["expires_in"]
            refresh_expires_in = result["data"]["refresh_expires_in"]
            self.user_access_token_expires_at = arrow.now().shift(seconds=expires_in)
            self.refresh_token_expires_at = arrow.now().shift(seconds=refresh_expires_in)
        else:
            raise Exception(f"Failed to get user access token: {result}")

    def get_app_access_token(self):
        url = f"https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            'User-Agent': 'Aily Python SDK'
        }
        data = {"app_id": self.app_id, "app_secret": self.app_secret}
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        if result.get("app_access_token"):
            return result["app_access_token"]
        else:
            raise Exception(f"Failed to get app access token: {result}")

    def get_user_access_token(self):
        current_time = arrow.now()

        # 如果user_access_token存在且未过期,则直接返回
        if self.user_access_token and current_time < self.user_access_token_expires_at:
            return self.user_access_token

        # 如果refresh_token存在且未过期,则尝试刷新user_access_token
        if self.refresh_token and current_time < self.refresh_token_expires_at:
            self.refresh_user_access_token()
            return self.user_access_token

        raise Exception("User access token not available")

    def refresh_user_access_token(self):
        url = f"https://open.larkoffice.com/open-apis/authen/v1/oidc/refresh_access_token"
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {self.get_app_access_token()}",
            'User-Agent': 'Aily Python SDK'
        }
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        if result.get("data"):
            self.user_access_token = result["data"]["access_token"]
            self.refresh_token = result["data"]["refresh_token"]
            expires_in = result["data"]["expires_in"]
            refresh_expires_in = result["data"]["refresh_expires_in"]
            self.user_access_token_expires_at = arrow.now().shift(seconds=expires_in)
            self.refresh_token_expires_at = arrow.now().shift(seconds=refresh_expires_in)
        else:
            raise Exception(f"Failed to refresh user access token: {result}")
