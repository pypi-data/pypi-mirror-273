import httpx
import jwt
import sentry_sdk
from datetime import (datetime, timedelta)
from enum import (Enum, unique)
from pydantic import (BaseModel)
from urllib.parse import (urljoin)
from typing import (List)


@unique
class IError(Enum):
    OK = 0
    Request_Kong_Error = -60062


class ConsumerModel(BaseModel):
    id: str
    username: str
    custom_id: str
    tags: List[str] = []


class JWTModel(BaseModel):
    key: str
    secret: str
    algorithm: str


class KongAdmin:

    def __init__(self, host):
        self.host = host
        self.max_age = 2600 * 24 * 5

    def get_url(self, path: str) -> str:
        return urljoin(self.host, path)

    async def request(self, method: str, path: str, json: dict = None):
        url = self.get_url(path)
        try:
            async with httpx.AsyncClient() as client:
                r = await client.request(method, url, json=json)

                if r.status_code == 204:
                    return r.status_code, None
                if r.status_code != 200 and r.status_code != 201:
                    return r.status_code, r.json()
                return IError.Ok.value, r.json()
        except httpx.ConnectError as e:
            sentry_sdk.capture_exception(e)
            return IError.Request_Kong_Error.value, None
        except Exception as e:
            sentry_sdk.capture_exception(e)
            return IError.Request_Kong_Error.value, None

    async def get_consumer(self, username) -> (int, ConsumerModel):
        path = f"/consumers/{username}"
        ret, j = await self.request("get", path)
        if ret != IError.Ok.value:
            return ret, None

        return ret, ConsumerModel(**j)

    async def update_or_create_consumer(self, user) -> (int, ConsumerModel):
        path = f"/consumers/{user.userid}"
        custom_id = f"{user.name}/{user.email}"
        data = {
            "username": user.userid,
            "custom_id": custom_id,
            "tags": user.get_tags(),
        }
        ret, j = await self.request("put", path, json=data)
        if ret != IError.Ok.value:
            return ret, None

        return ret, ConsumerModel(**j)

    async def delete_consumer(self, username) -> int:
        path = f"/consumers/{username}"
        err, _ = await self.request("delete", path)
        if err == 204:
            return IError.Ok.value
        return err

    async def list_jwt(self, consumer: str) -> (int, List[JWTModel]):
        path = f"/consumers/{consumer}/jwt"
        ret, j = await self.request("get", path)
        if ret != IError.Ok.value:
            return ret, None

        return ret, [JWTModel(**x) for x in j["data"]]

    async def create_jwt_model(self, username: str) -> (int, JWTModel):
        path = f"/consumers/{username}/jwt"
        ret, j = await self.request("post", path)

        if ret != IError.Ok.value and ret != 201:
            return ret, None

        return IError.Ok.value, JWTModel(**j)

    async def generate_token(self, user):
        await self.update_or_create_consumer(user)

        ret, jwt_models = await self.list_jwt(user.userid)
        if ret != IError.Ok.value:
            return ret, None

        if not jwt_models or len(jwt_models) == 0:
            ret, jwt_model = await self.create_jwt_model(user.userid)
            if ret != IError.Ok.value:
                return ret, None
        else:
            jwt_model = jwt_models[0]

        token = JWT.create_jwt(jwt_model, expires_delta=timedelta(seconds=self.max_age))

        return ret, token


class JWT:
    @staticmethod
    def create_jwt(jwt_model: JWTModel, expires_delta: timedelta = None) -> str:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(seconds=10)
        to_encode = {"iss": jwt_model.key, "exp": expire}
        return jwt.encode(
            to_encode, jwt_model.secret, algorithm=jwt_model.algorithm
        ).decode()
