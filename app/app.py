from fastapi import FastAPI, Depends
from auth import keycloak_auth

app = FastAPI()

@app.get("/")
def protected_route(user=Depends(keycloak_auth)):
    return {"message": "You are authenticated"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
