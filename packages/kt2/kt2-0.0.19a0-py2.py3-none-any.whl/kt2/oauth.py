import base64
import hashlib
import time
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, Generic, List, Optional, TypeVar, cast
from urllib.parse import urlencode

import httpx
import jwt
from jwt import PyJWK
from jwt.algorithms import RSAAlgorithm
from pydantic import AnyUrl, BaseModel

from kt2.errors import AuthorizeError, GetAccessTokenError
from kt2.jwks import JWKS, get_signing_key_from_jwks

algorithm = RSAAlgorithm(RSAAlgorithm.SHA384)


def generate_code_challenge(code_verifier: str) -> str:
    h = hashlib.sha256()
    h.update(code_verifier.encode(encoding='ascii'))
    sha256_val = h.digest()
    code_challenge = bytes.decode(base64.urlsafe_b64encode(sha256_val))
    return code_challenge.replace("+", "-").replace("/", "_").replace("=", "")


class AuthorizeParams(BaseModel):
    aud: str
    launch: str
    client_id: str
    redirect_uri: str
    scope: str
    state: str
    code_challenge: str
    code_challenge_method: str = "S256"
    response_type: str = "code"


class TokenPayload(BaseModel):
    iss: str
    sub: str
    exp: datetime
    aud: AnyUrl
    jti: str


class OIDCTokenBodyAssert(BaseModel):
    client_assertion: str
    redirect_uri: str
    code_verifier: str
    code: str
    client_assertion_type: str = (
        'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'
    )
    grant_type: str = 'authorization_code'


class TokenBodyAssert(BaseModel):
    client_assertion: str
    aud: AnyUrl
    client_assertion_type: str = (
        'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'
    )
    grant_type: str = 'client_credentials'
    scope: str = ""


class OIDCToken(BaseModel):
    access_token: str
    id_token: str
    scope: str
    token_type: str
    expires_in: str
    resource: str
    definition: str
    sub: str
    patient: str
    intent: str


class HTIToken(BaseModel):
    resource: str
    definition: str
    sub: str
    patient: str
    intent: str


class OAuth2Token(Dict[str, Any]):
    def __init__(self, token_dict: Dict[str, Any], signing_key: PyJWK | None = None):
        if "expires_at" in token_dict:
            token_dict["expires_at"] = int(token_dict["expires_at"])
        elif "expires_in" in token_dict:
            token_dict["expires_at"] = int(time.time()) + int(token_dict["expires_in"])
        if signing_key:
            token_dict["signing_key"] = signing_key

        super().__init__(token_dict)

    @property
    def bearer_token(self) -> str:

        access_token: str = self.get("access_token", None)
        signing_key: PyJWK = self.get("signing_key", None)

        if not access_token:
            return ""

        # If we have a signing key, we decode with signing_key signature.
        # If signing_key is given, we verify it's signature but we don't verify the audience.
        # Please note that the JWT headers specificies `algorithms` and `kid`, but we should NEVER
        # read them from unverified header because these values are presented by other party.
        # Instead we should fetch them from configuration and use sensible defaults for `algorithms` list.

        try:
            (
                jwt.decode(
                    access_token,
                    signing_key.key,
                    algorithms=["RS512"],
                    options={"verify_aud": False, "verify_signature": True},
                )
                if signing_key
                else None
            )

        except Exception as e:
            raise jwt.InvalidSignatureError("Accesstoken could not be verified.")

        return f'Bearer {access_token}'

    def is_expired(self):
        if "expires_at" not in self:
            return True
        return time.time() > self["expires_at"]


T = TypeVar("T")


class SmartFHIROAuth2(Generic[T]):
    name: str
    client_id: str
    authorize_endpoint: str
    access_token_endpoint: str
    jwks: JWKS
    introspection_token_endpoint: Optional[str]
    jwks_endpoint: Optional[str]
    jwks_kid: Optional[str]
    base_scopes: List[str] = []
    request_headers: Dict[str, str]
    enable_logger: bool = False

    def __init__(
        self,
        client_id: str,
        authorize_endpoint: str,
        access_token_endpoint: str,
        fhir_url: str,
        jwks: JWKS,
        introspection_token_endpoint: Optional[str] = None,
        jwks_endpoint: Optional[str] = None,
        jwks_kid: Optional[str] = "",
        name: str = "smart-on-fhir",
    ):
        self.client_id = client_id
        self.authorize_endpoint = authorize_endpoint
        self.access_token_endpoint = access_token_endpoint
        self.fhir_url = fhir_url
        self.jwks = jwks
        self.introspection_token_endpoint = introspection_token_endpoint
        self.name = name

        self.token: OAuth2Token = None

        self.signing_key = (
            get_signing_key_from_jwks(url=jwks_endpoint, kid=jwks_kid)
            if jwks_endpoint
            else None
        )

        self.request_headers = {
            "Accept": "application/json",
        }

    @property
    def token(self) -> OAuth2Token:
        return self._token

    @token.setter
    def token(self, value) -> None:
        self._token = value

    def get_authorization_url(
        self,
        redirect_uri: str,
        iss: str,
        launch: str,
        state: str,
        code_verifier: str,
        scope: Optional[List[str]] = "launch openid fhirUser",
    ) -> str:
        try:
            params = AuthorizeParams(
                aud=iss,
                launch=launch,
                client_id=self.client_id,
                redirect_uri=redirect_uri,
                code_challenge=generate_code_challenge(code_verifier),
                scope=scope,
                state=state,
            )

            return f"{self.authorize_endpoint}?{urlencode(params.dict())}"
        except:
            raise AuthorizeError(f"Cannot building authorize request: {params.dict()}")

    async def get_soph_access_token(
        self, redirect_uri: str, code_verifier: str, code: str
    ) -> OIDCToken:
        """
        Generate OIDC token on Smart FHIR server

        Raises:
            GetAccessTokenError: token request failed

        Returns:
            OIDCToken: token

        """

        async with httpx.AsyncClient() as client:
            payload = TokenPayload(
                iss=self.client_id,
                sub=self.client_id,
                exp=datetime.now() + timedelta(minutes=5),
                aud=self.access_token_endpoint,
                jti=str(uuid.uuid4().hex),
            )

            token = jwt.encode(
                payload.dict(),
                self.jwks.private_key,
                algorithm="RS512",
                headers={"alg": "RS512", "kid": self.jwks.kid, "typ": "JWT"},
            )

            data = OIDCTokenBodyAssert(
                client_assertion=token,
                redirect_uri=redirect_uri,
                code_verifier=code_verifier,
                code=code,
            )

            token_headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                **self.request_headers,
            }

            self.logger.info("== SMART OIDC AcccesToken ==")
            self.logger.info(f"data: {data.dict()}")
            self.logger.info(f"url:  {self.access_token_endpoint}")
            self.logger.info(f"headers: {token_headers}")

            response = await client.post(
                self.access_token_endpoint,
                data=data.dict(),
                headers=token_headers,
            )

            data = cast(OIDCToken, response.json())

            if response.status_code == 400:
                raise GetAccessTokenError(data)

            token = OIDCToken(**data)

            return token

    async def get_access_token(self) -> OAuth2Token:
        """
        Generate token on Smart FHIR server

        Raises:
            GetAccessTokenError: token request failed

        Returns:
            OAuth2Token: token
        """

        async with httpx.AsyncClient() as client:
            payload = TokenPayload(
                iss=self.client_id,
                sub=self.client_id,
                exp=datetime.now() + timedelta(minutes=5),
                aud=self.access_token_endpoint,
                jti=str(uuid.uuid4().hex),
            )

            token = jwt.encode(
                payload.dict(),
                self.jwks.private_key,
                algorithm="RS512",
                headers={"alg": "RS512", "kid": self.jwks.kid, "typ": "JWT"},
            )

            data = TokenBodyAssert(client_assertion=token, aud=self.fhir_url)

            token_headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                **self.request_headers,
            }

            self.logger.info("== SMART FHIR AcccesToken ==")
            self.logger.info(f"data: {data.dict()}")
            self.logger.info(f"url:  {self.access_token_endpoint}")
            self.logger.info(f"headers: {token_headers}")

            response = await client.post(
                self.access_token_endpoint,
                data=data.dict(),
                headers=token_headers,
            )

            data = cast(Dict[str, Any], response.json())

            if response.status_code == 400:
                raise GetAccessTokenError(data)

            # Set token on client and return for further processing
            token = OAuth2Token(data, signing_key=self.signing_key)

            # Store on client
            self.token = token

            return token

    async def introspect_token(self, access_token: str): ...


OAuth2 = SmartFHIROAuth2[Dict[str, Any]]
