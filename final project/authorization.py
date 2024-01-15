from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import json

CLIENT_SECRET = "6eaRF63ryNuxfgJ2ePoySBrhf8Bpbphv"
ALGORITHM = "RS256"


class KeycloakJWTBearerHandler(HTTPBearer):
    def __init__(self) -> None:
        super(KeycloakJWTBearerHandler, self).__init__()

    async def __call__(self, request: Request):
        KeycloakJWTBearerHandler._check_request_headers(request._headers)

        credentials: HTTPAuthorizationCredentials = await super(KeycloakJWTBearerHandler, self).__call__(request)
        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
        if not credentials.scheme == "Bearer":
            raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
        role = KeycloakJWTBearerHandler._verify_jwt(credentials.credentials)
        return role
    
    @staticmethod
    def _verify_jwt(credentials):
        decode_credentials = KeycloakJWTBearerHandler._decode_jwt(credentials)
        
        # check if the user has the role: my-role
        roles: list = decode_credentials["payload"]["realm_access"]["roles"]
        if "client_role" in roles:
            return "client_role"
        elif "manager_role" in roles:
            return "manager_role"
        else:
            raise HTTPException(status_code=403, detail="The user does not have the required role")


    @staticmethod
    def _check_request_headers(headers):
        # check there is an authorization header
        if "authorization" not in headers.keys():
            raise HTTPException(status_code=403, detail="Header has not attribute: authorization")
        
        # check if the authorization token is empty
        auth_value = headers.getlist("authorization")
        if len(auth_value) == 0:
            raise HTTPException(status_code=403, detail="Authorization token is empty")
        
        # check if the token begins with the word Bearer
        value = auth_value[0].split(" ")
        if value[0] != "Bearer":
            raise HTTPException(status_code=403, detail="The authorization token must begin with the word 'Bearer'")
        
        # check if there is a token after the word Bearer
        if len(value) != 2 or value[1] == "":
            raise HTTPException(status_code=403, detail="Authorization token is wrong")

        return True

    @staticmethod
    def _decode_jwt(token):
        try:    
            header = jwt.get_unverified_header(token)
            data = jwt.decode(
                        jwt=token,
                        key="secret",
                        algorithms=[ALGORITHM],
                        options={"verify_signature": False}
                    )
        except Exception as e:
            raise HTTPException(status_code=400, detail="{e}".format(e))
        
        payload = json.loads(json.dumps(data))

        return {"header": header, "payload": payload}
    