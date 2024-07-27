from typing import Optional

import requests
from fastapi import Depends, HTTPException, Request

from config import KEYCLOAK_CLIENT_ID, KEYCLOAK_SP_URL, SP_REALM
from keycloak_service import create_keycloak_openid_instance

KEYCLOAK_OPENID = create_keycloak_openid_instance()


def keycloak_auth(request: Request):
    return handle_keycloak_auth(request, "OIDC_FRONTEND_CLIENT")


def idp_initiated_keycloak_auth(request: Request):
    return handle_keycloak_auth(request, "OIDC_FRONTEND_CLIENT_IDP_INITIATED")


def handle_keycloak_auth(request: Request, client_id: str) -> Optional[dict]:
    print(f"Handling keycloak auth for client {client_id}")
    print(f"Query params: {request.query_params}")

    code = request.query_params.get("code")
    if not code:
        print("No code found in query params")
        return None

    token = exchange_code_for_token(client_id, code)
    return decode_token(token)


def exchange_code_for_token(client_id: str, code: str) -> str:
    data = {
        "client_id": client_id,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:8083/",
    }
    response = requests.post(
        f"{KEYCLOAK_SP_URL}realms/{SP_REALM}/protocol/openid-connect/token", data=data
    )
    response_data = response.json()
    print(f"Token response: {response_data}")
    return response_data.get("access_token")


def decode_token(token: str) -> dict:
    return KEYCLOAK_OPENID.decode_token(
        token,
        key=KEYCLOAK_OPENID.public_key,
        options={"verify_signature": False, "verify_aud": False, "verify_exp": False},
    )
