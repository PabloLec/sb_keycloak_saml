## Goal

The primary objective of this project is to implement SAML authentication using Keycloak by setting up all the necessary components.
One instance of Keycloak serves as the Identity Provider (IdP), while another operates as the Service Provider (SP).
Additionally, a demo application is included to act as an application secured by the Keycloak SP, and the associated workflow exclusively accepts SAML authentications.

```mermaid
sequenceDiagram
    actor User
    participant Application
    participant SP as Service Provider
    participant IdP as Identity Provider
    User->>Application: Requests access
    Application->>SP: Checks if user is authenticated
    SP->>Application: User not authenticated
    Application->>SP: Redirects user for authentication
    SP->>IdP: Redirects user for authentication
    IdP->>User: Prompts user to log in
    User->>IdP: Logs in
    IdP->>SP: Redirects authenticated user
    Note over SP: Maps user to existing account or prompts to create a new one
    SP->>Application: Redirects authenticated user
```

## Context

- Keycloak IdP runs on `http://localhost:8081`
- Keycloak SP runs on `http://localhost:8082`
- Demo app runs on `http://localhost:8083`
- IdP SAML descriptor can be obtained with `http://localhost:8082/realms/IdP_realm/protocol/saml/descriptor`
- SP SAML broker descriptor can then be obtained with `http://localhost:8081/realms/SP_realm/broker/saml/endpoint/descriptor`

## Pre-prepared Steps

**On IdP:**
- Create realm `IdP_realm`.
- On realm `IdP_realm`, go to Realm Settings > Keys > Providers. Disable `rsa-generated` and click on Add Provider > rsa and add a provider with private key (see `keys/idp_private_key.pem`).

**On SP:**
- Create realm `internal`.
- Create client `app` on realm `internal` for an example Python app with `Client authentication` on (for client ID / client secret).
- Create realm `SP_realm`.
- On realm `SP_realm`, go to Realm Settings > Keys > Providers. Disable `rsa-generated` and click on Add Provider > rsa and add a provider with private key (see `keys/sp_private_key.pem`).
- Create an OpenID Connect client on realm `SP_realm` with client id `frontend` setting "Root URL", "Home URL" and "Valid redirect URIs" to `http://localhost:8083/`.
- Add SAML identity provider with name `saml` on `SP_realm` with "Service provider entity ID" set to `http://localhost:8081/realms/SP_realm` and "SAML entity descriptor" set to `http://localhost:8082/realms/IdP_realm/protocol/saml/descriptor`.
- Set `saml` as default identity provider (to bypass default login form) on `SP_realm` by going to Authentication > Flows > `browser` and setting "Identity provider redirector" to `required`, then clicking on the cog icon and setting "Default identity provider" to `saml` (with any alias).

**Back to IdP:**
- Create a new client on realm `IdP_realm` with the UI using Clients > Import Client and import SP SAML XML descriptor.

## Startup

Docker compose runs 3 containers: Keycloak IdP, Keycloak SP, and a demo Python app. Keycloak containers load pre-configured realms stored in the `realms` folder.
On startup, the Python app waits for Keycloak to be ready then creates a new user on IdP with username `john` and password `john`.

## Testing

1. Go to `http://localhost:8081/realms/SP_realm/protocol/openid-connect/auth?client_id=frontend&response_type=code&redirect_uri=http://localhost:8083%2F`.
2. You should be redirected to the IdP login page.
3. Login with username `john` and password `john`.
4. You should be redirected to the SP and be prompted to create a new user.
5. Finally, you should be redirected to the demo app and see a welcome message.

## Notes

RSA private keys were added in exported realms JSON in plain text for convenience.

## Enhancements

- A custom mapping could be added in SP to link users from IdP thus avoiding the user creation step.
- Demo app could redirect to SP if user is not logged in.
