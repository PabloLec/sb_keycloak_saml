import requests
from fastapi import HTTPException, Request, Depends
from keycloak_service import create_keycloak_openid_instance
from config import KEYCLOAK_SP_URL, SP_REALM, KEYCLOAK_CLIENT_ID, KEYCLOAK_CLIENT_ID

KEYCLOAK_OPENID = create_keycloak_openid_instance()

def exchange_code_for_token(code: str) -> str:
    data = {
            'client_id': 'frontend',
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'http://localhost:8083/'
        }
    response = requests.post(f"{KEYCLOAK_SP_URL}realms/{SP_REALM}/protocol/openid-connect/token", data=data)
    print(f"Token response: {response.json()}")
    return response.json()["access_token"]

def keycloak_auth(request: Request):
    code = request.query_params.get("code")
    if not code:
        return None

    token = exchange_code_for_token(code)
    return KEYCLOAK_OPENID.decode_token(token, key=KEYCLOAK_OPENID.public_key, options={"verify_signature": False, "verify_aud": False, "verify_exp": False})