import requests
from config import KEYCLOAK_URL, KEYCLOAK_REALM, KEYCLOAK_CLIENT_ID, ADMIN_USER, ADMIN_PASSWORD
from keycloak import KeycloakOpenID
import time

def wait_for_keycloak():
    while True:
        try:
            response = requests.get(KEYCLOAK_URL)
            if response.status_code == 200:
                break
        except requests.ConnectionError as e:
            print(e)
            print("Waiting for Keycloak to start...")
        time.sleep(5)

def get_keycloak_admin_token() -> str:
    data = {
        'client_id': 'admin-cli',
        'username': ADMIN_USER,
        'password': ADMIN_PASSWORD,
        'grant_type': 'password'
    }
    response = requests.post(f"{KEYCLOAK_URL}realms/master/protocol/openid-connect/token", data=data)
    return response.json()["access_token"]

def get_client_secret() -> str:
    wait_for_keycloak()
    admin_token = get_keycloak_admin_token()
    clients_response = requests.get(
        f"{KEYCLOAK_URL}admin/realms/{KEYCLOAK_REALM}/clients",
        headers={"Authorization": f"Bearer {admin_token}"},
        params={"clientId": KEYCLOAK_CLIENT_ID}
    )
    client_id = clients_response.json()[0]['id']
    secret_response = requests.get(
        f"{KEYCLOAK_URL}admin/realms/{KEYCLOAK_REALM}/clients/{client_id}/client-secret",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    return secret_response.json()["value"]

def create_keycloak_openid_instance() -> KeycloakOpenID:
    return KeycloakOpenID(server_url=KEYCLOAK_URL,
                          client_id=KEYCLOAK_CLIENT_ID,
                          realm_name=KEYCLOAK_REALM,
                          client_secret_key=get_client_secret())
