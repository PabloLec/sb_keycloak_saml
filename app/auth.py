from fastapi import HTTPException, Request, Depends
from keycloak_service import create_keycloak_openid_instance

KEYCLOAK_OPENID = create_keycloak_openid_instance()

def keycloak_auth(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header is missing")

    try:
        scheme, token = auth_header.split(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Unsupported authorization scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")

    try:
        KEYCLOAK_OPENID.decode_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
