'''
Helper functions for dealing with JWT tokens on backend API sessions
'''
from env import secret_key
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException, Header

def jwt_token_verification(access_token: str = Header()):
    try:
        # decode and verify the JWT using the application's secret key.
        # if it is successfully decoded, we allow the route to run.
        valid = jwt.decode(access_token, secret_key, algorithms=["HS256"])

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="The JWT submitted is expired. Please login again")

    except JWTError as e:
        raise HTTPException(status_code=401, detail="The JWT submitted is invalid")

