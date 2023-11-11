from fastapi import FastAPI, Depends
from auth import keycloak_auth
from keycloak_service import create_user_in_idp

app = FastAPI()

@app.get("/")
def protected_route(user=Depends(keycloak_auth)):
    return {"message": f"You are authenticated with email {user['email']}"}

if __name__ == "__main__":
    create_user_in_idp("john", "john")

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8083)
