- Quarkus Keycloak removes /auth from path by default

Pre-prepared steps : 

- [IdP] Create realm `IdP_realm`
- [SP] Create realm `internal`
- [SP] Create client `app` on realm `internal` for example Python app with `Client authentication ` on (for client ID / client secret)
- [SP] Create realm `SP_realm`
- [SP] Create an OpenID Connect client on realm `SP_realm` with client id `frontend` setting "Root URL", "Home URL" and "Valid redirect URIs" to `http://localhost:8083/`

Steps to reproduce :

- [IdP] SAML descriptor can be obtained with http://localhost:8082/realms/IdP_realm/protocol/saml/descriptor
- [SP] Add SAML identity provider with name `saml` on `SP_realm` with "Service provider entity ID" set to `http://localhost:8081/realms/SP_realm` and "SAML entity descriptor" set to `http://localhost:8082/realms/IdP_realm/protocol/saml/descriptor`
- [SP] Set `saml` as default identity provider (to bypass default login form) on `SP_realm` by going to Authentication > Flows > `browser` >  and setting "Identity provider redirector" to `required`, then clicking on the cog icon and setting "Default identity provider" to `saml` (with any alias)
- [SP] Service provider metadata can then be obtained with http://localhost:8081/realms/SP_realm/broker/saml/endpoint/descriptor
- [IdP] Create a new client on realm `IdP_realm` with the UI using Clients > Import Client and import XML descriptor from the previous step

## TODO

- Keycloak certificates change after restart, need to find a way to persist them
- Trying to fix with `KC_HTTPS_PORT`, `https-certificate-file` and `https-certificate-key-file` in docker-compose.yml
- idp.json/sp.json = without "steps to reproduce", idp_with_sp_client.json/sp_with_idp.json = with "steps to reproduce"