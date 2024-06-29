
from functools import lru_cache
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt
import requests
from config import Settings, get_settings
import urllib
from models.token_models import DecodedToken, TokenData
from models.user_model import User

settings: Settings = get_settings()



authorization_url_qs = urllib.parse.urlencode({'audience': settings.auth0_audience})
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f'https://{settings.auth0_domain}/authorize?{authorization_url_qs}&scope=openid%20profile%20email',
    tokenUrl=f'https://{settings.auth0_domain}/oauth/token'
)


class Auth0(OAuth2AuthorizationCodeBearer):
    def __init(self):
        self.authorization_url_qs = urllib.parse.urlencode({'audience': settings.auth0_audience})
        self.oauth2_scheme = OAuth2AuthorizationCodeBearer(
        authorizationUrl=f'https://{settings.auth0_domain}/authorize?{authorization_url_qs}&scope=openid%20profile%20email',
        tokenUrl=f'https://{settings.auth0_domain}/oauth/token'
    )
        
        


    async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
        jwks_url = f"https://{settings.auth0_domain}/.well-known/jwks.json"
        response = requests.get(jwks_url)
        jwks = response.json()
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                
                decoded_token =jwt.decode(
                    token,
                    rsa_key,
                    algorithms=["RS256"],
                    audience=settings.auth0_audience,
                    issuer=f'https://{settings.auth0_domain}/'
                )
                token = TokenData(decoded_token=DecodedToken(**decoded_token), token=token)
                return token
            except jwt.ExpiredSignatureError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            except jwt.JWTClaimsError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token claims",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        

    async def get_current_user_info(user_token: TokenData = Depends(get_current_user)) -> User:
        url = f"https://{settings.auth0_domain}/userinfo"
        headers = {
            'Authorization': f'Bearer {user_token.token}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        user = User(**response.json())
        token:str = await get_managment_token()
        url = f"https://{settings.auth0_domain}/api/v2/users/{user_token.decoded_token.sub}/roles"
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = requests.get(url, headers=headers)
        user.roles = response.json()

        return user


    async def get_managment_token():
        url = f"https://{settings.auth0_domain}/oauth/token"
        
        payload = {
            "client_id": settings.auth0_client_id_machine,
            "client_secret": settings.auth0_client_secret_machine,
            "audience": f"https://{settings.auth0_domain}/api/v2/",
            "grant_type": "client_credentials"
        }
        
        headers = {
            'Content-Type': "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        return response.json()["access_token"]
