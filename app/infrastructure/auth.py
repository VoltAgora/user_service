import os
from jose import jwt, JWTError

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def decode_token(authorization_header: str) -> dict:
    """
    Espera header con formato: "Bearer <token>"
    Retorna payload (dict) o lanza Exception con mensaje legible.
    """
    if not authorization_header:
        raise Exception("Authorization header missing")
    if not authorization_header.startswith("Bearer "):
        raise Exception("Formato de token inválido")
    token = authorization_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise Exception("Token inválido o expirado")