from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

router = APIRouter(prefix="/jwtauth",
                   tags=["jwtauth"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

# Generar Key para Token -> openssl rand -hex 32
SECRET_KEY = "a073f74e61ee75b6d0e42e8897ede90cb95301af45544847927d75d72ca6b8b8"
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    username: str
    full_name: str
    email: str
    enabled: bool


class UserDB(User):
    password: str


users_db = {
    "roespino": {
        "username": "roespino",
        "full_name": "Robin Espinoza Rossi",
        "email": "robin.espinozar@gmail.com",
        "enabled": True,
        "password": "$2a$12$BcAQAdqqKv705.3vEfGhIOeemUk9J7l8.P7V.LMcJxU.WXN1d7lHO"  # 123456
    },
    "katylaz": {
        "username": "katylaz",
        "full_name": "Katherine Lazaro Concepción",
        "email": "katy.lazaroc@gmail.com",
        "enabled": False,
        "password": "$2a$12$dMGSEWrW/Rgd9UCcA0sj7OXoP8gofZ8Gq3gtgl0gIU5IeGm41uOrG"  # 654321
    },
    "joaqesp": {
        "username": "joaqesp",
        "full_name": "Joaquín Espinoza Lazaro",
        "email": "joaquin.espinozal@gmail.com",
        "enabled": True,
        "password": "$2a$12$b09JX8DxazS5Upm/4J.WyOsG.YO64hFeXn0xu6VpYxd.J5/Atg.Ym"  # 123
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        username = jwt.decode(token, SECRET_KEY, [ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception

    return search_user(username)


async def current_user(user: User = Depends(auth_user)):
    if not user.enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )

    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario no es correcto"
        )

    user = search_user_db(form.username)
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña no es correcta"
        )

    acces_token = {"sub": user.username,
                   "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    return {"access_token": jwt.encode(claims=acces_token, key=SECRET_KEY, algorithm=ALGORITHM), "token_type": "bearer"}


@router.get("/users/me")
async def get_my_user(user: User = Depends(current_user)):
    return user
