from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from auth import keycloak_auth
from keycloak_service import create_user_in_idp

app = FastAPI()
LOGIN_URL = "http://localhost:8081/realms/SP_realm/protocol/openid-connect/auth?client_id=frontend&response_type=code&redirect_uri=http://localhost:8083%2F&kc_idp_hint=SAML_IDP"

@app.get("/")
def protected_route(user=Depends(keycloak_auth)):
    if not user:
        return RedirectResponse(LOGIN_URL)

    print(f"User: {user}")
    roles = user.get("realm_access").get("roles")
    return {"message": f"You are authenticated as user {user['preferred_username']} with roles {roles}"}

if __name__ == "__main__":
    create_user_in_idp("john", "john")

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8083)
