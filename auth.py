from passlib.context import CryptContext
from jose import jwt
from datetime import datetime,timedelta

Secret_key = "financialproject"

pwd_context = CryptContext(
    schemes = ["bcrypt"],
    deprecated ="auto"
)
def  hashing_password(password):
    return pwd_context.hash(password) 
def verifying_password(plain,hashed):
    return pwd_context.verify(plain,hashed)      

def create_access_tokens(data):
    payload = data.copy()
    payload["exp"]= (
        datetime.utcnow() + timedelta(hours=1)
    )
    token = jwt.encode(
        payload,
        Secret_key,
        algorithm="HS256"
    )

    return token