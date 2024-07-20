import time

import requests
from keycloak import KeycloakOpenID

from config import (ADMIN_PASSWORD, ADMIN_USER, IDP_REALM, KEYCLOAK_CLIENT_ID,
                    KEYCLOAK_IDP_URL, KEYCLOAK_INTERNAL_REALM, KEYCLOAK_SP_URL)


def wait_for_keycloak(url: str):
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                break
        except requests.ConnectionError as e:
            print(e)
            print("Waiting for Keycloak to start...")
        time.sleep(5)


def get_keycloak_admin_token(url) -> str:
    data = {
        "client_id": "admin-cli",
        "username": ADMIN_USER,
        "password": ADMIN_PASSWORD,
        "grant_type": "password",
    }
    response = requests.post(
        f"{url}realms/master/protocol/openid-connect/token", data=data
    )
    return response.json()["access_token"]


def get_client_secret() -> str:
    global KEYCLOAK_CLIENT_SECRET

    for url in (KEYCLOAK_SP_URL, KEYCLOAK_IDP_URL):
        wait_for_keycloak(url)

    admin_token = get_keycloak_admin_token(KEYCLOAK_SP_URL)
    clients_response = requests.get(
        f"{KEYCLOAK_SP_URL}admin/realms/{KEYCLOAK_INTERNAL_REALM}/clients",
        headers={"Authorization": f"Bearer {admin_token}"},
        params={"clientId": KEYCLOAK_CLIENT_ID},
    )
    client_id = clients_response.json()[0]["id"]
    secret_response = requests.get(
        f"{KEYCLOAK_SP_URL}admin/realms/{KEYCLOAK_INTERNAL_REALM}/clients/{client_id}/client-secret",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    return secret_response.json()["value"]


def create_keycloak_openid_instance() -> KeycloakOpenID:
    return KeycloakOpenID(
        server_url=KEYCLOAK_SP_URL,
        client_id=KEYCLOAK_CLIENT_ID,
        realm_name=KEYCLOAK_INTERNAL_REALM,
        client_secret_key=get_client_secret(),
    )


def create_user_in_idp():
    admin_token = get_keycloak_admin_token(KEYCLOAK_IDP_URL)
    headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json",
    }
    user_data = {
        "username": "john",
        "email": "john@john.john",
        "enabled": True,
        "credentials": [{"type": "password", "value": "john"}],
    }
    create_user_url = f"{KEYCLOAK_IDP_URL}admin/realms/{IDP_REALM}/users"
    response = requests.post(create_user_url, json=user_data, headers=headers)
    if response.status_code in [201, 204]:
        print(f"User created successfully.")
    else:
        print(
            f"Failed to create user. Status: {response.status_code}, Response: {response.text}"
        )
