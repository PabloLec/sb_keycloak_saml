from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse

from auth import idp_initiated_keycloak_auth, keycloak_auth
from keycloak_service import create_user_in_idp

app = FastAPI()
LOGIN_URL = "http://localhost:8081/realms/SP_realm/protocol/openid-connect/auth?client_id=OIDC_FRONTEND_CLIENT&response_type=code"


@app.get("/")
def protected_route(user=Depends(keycloak_auth)):
    if not user:
        print("User not authenticated in protected_route, redirecting to login")
        return RedirectResponse(LOGIN_URL)
    return authenticated_user_response(user)


@app.get("/idp-initiated")
def idp_initiated_protected_route(user=Depends(idp_initiated_keycloak_auth)):
    if not user:
        print("User not authenticated in idp-initiated_protected_route")
        raise HTTPException(status_code=401, detail="Not authenticated")
    return authenticated_user_response(user)


def authenticated_user_response(user):
    roles = get_user_roles(user)
    return {
        "message": f"You are authenticated as user {user['preferred_username']} with roles {roles}"
    }


def get_user_roles(user):
    roles = user.get("realm_access", {}).get("roles", [])
    return roles


if __name__ == "__main__":
    create_user_in_idp()

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8083)
