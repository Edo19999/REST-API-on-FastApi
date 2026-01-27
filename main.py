from fastapi import Query
from fastapi import FastAPI, HTTPException
from typing import Optional
from datetime import datetime
from schemas import Advertisement, AdvertisementCreate, AdvertisementUpdate, User, UserCreate
from auth import get_password_hash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from schemas import UserLogin
from auth import verify_password, create_access_token
from jose import JWTError, jwt
from auth import SECRET_KEY, ALGORITHM

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
advertisements = []
users = []

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    for user in users:
        if user["username"] == username:
            return user
    
    raise credentials_exception

@app.get("/")
async def root():
    return {"message": "Привет, это сервис объявлений!"}

@app.post("/advertisement", status_code=201)
async def create_advertisement(ad: AdvertisementCreate, current_user: User = Depends(get_current_user)):
    ad_id = len(advertisements) + 1
    ad_dict = ad.model_dump()
    ad_dict["id"] = ad_id
    ad_dict["created_at"] = datetime.now().isoformat()
    ad_dict["author"] = current_user.username
    advertisements.append(ad_dict)
    return{"id": ad_id, "message": "Объявление успешно создано!", "data": ad_dict}

@app.get("/advertisement/{advertisement_id}")
async def get_advertisement(advertisement_id: int):
    for ad in advertisements:
        if ad["id"] == advertisement_id:
            return ad
    raise HTTPException(status_code=404, detail="Объявление с таким id не найдено!")

@app.get("/advertisement")
async def search_advertisements(
    title: Optional[str] = None,
    price_min: Optional[float] = Query(None, description="Минимальная цена"),
    price_max: Optional[float] = Query(None, description="Максимальная цена"),
    limit: int = Query(10, ge=1, le=100, description="Максимальное количество объявлений в ответе"),
    offset: int = Query(0, ge=0, description="Смещение (сколько пропустить)")
):

    filtered_ads = []

    for ad in advertisements:
        if title and title.lower() not in ad["title"].lower():
            continue

        if price_min is not None and ad["price"] < price_min:
            continue
        
        if price_max is not None and ad["price"] > price_max:
            continue

        filtered_ads.append(ad)

    return filtered_ads[offset:offset+limit]

@app.delete("/advertisement/{advertisement_id}", status_code=204)
async def delete_advertisement(advertisement_id: int, current_user: User = Depends(get_current_user)):
    for index, ad in enumerate(advertisements):
        if ad["id"] == advertisement_id:
            if ad["author"] != current_user.username and current_user.role != "admin":
                raise HTTPException(status_code=403, detail="Недостаточно прав для удаления")
            
            advertisements.pop(index)
            return 
    raise HTTPException(status_code=404, detail="Объявление с таким id не найдено!")

@app.patch("/advertisement/{advertisement_id}")
async def update_advertisement(advertisement_id: int, ad_update: AdvertisementUpdate, current_user: User = Depends(get_current_user)):
    for ad in advertisements:
        if ad["id"] == advertisement_id:
            # Проверяем права
            if ad["author"] != current_user.username and current_user.role != "admin":
                raise HTTPException(status_code=403, detail="Недостаточно прав для редактирования")

            if ad_update.title:
                ad["title"] = ad_update.title
            if ad_update.description:
                ad["description"] = ad_update.description
            if ad_update.price:
                ad["price"] = ad_update.price
            # Автор не может поменять автора объявления! (убрали обновление author)
            if ad_update.contacts:
                ad["contacts"] = ad_update.contacts
                
            return {"message": "Объявление обновлено", "data": ad} 
            
    raise HTTPException(status_code=404, detail="Объявление с таким id не найдено!")

@app.post("/register", response_model=User)
async def register_user(user: UserCreate):
    for u in users:
        if u["username"] ==  user.username:
            raise HTTPException(status_code=400, detail="Пользователь с таким именем уже зарегистрирован!")

    hashed_password = get_password_hash(user.password)

    new_user = user.model_dump()
    new_user["id"] = len(users) + 1
    new_user["password"] = hashed_password

    users.append(new_user)
    return new_user

@app.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_found = None
    for u in users:
        if u["username"] == form_data.username:
            user_found = u
            break
    
    if not user_found or not verify_password(form_data.password, user_found["password"]):
         raise HTTPException(status_code=401, detail="Неверное имя пользователя или пароль")
    
    access_token = create_access_token(data={"sub": user_found["username"]})
    return {"access_token": access_token, "token_type": "bearer"}