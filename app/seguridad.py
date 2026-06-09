from passlib.context import CryptContext # (= clase)
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
# pwd = abreviatura de "password", context = configuracion. Es un objeto.
pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")

SECRET_KEY = "abcdefghij10987654321"
ALGORITHM = "HS256"

def hashear_password(password : str):
    return pwd_context.hash(password)

def verificar_password(password: str, hash: str):
    return pwd_context.verify(password, hash)

def crear_token(datos:dict):
    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token : str):
    try:
        datos = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return datos
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    return verificar_token(token)















