from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Advertisement(BaseModel):
    title: str
    description: str
    price: float
    author: str
    contacts: str

class AdvertisementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    author: Optional[str] = None
    contacts: Optional[str] = None

advertisements = []
@app.get("/")
async def root():
    return {"message": "Привет, это сервис объявлений!"}

@app.post("/advertisement")
async def create_advertisement(ad: Advertisement):
    ad_id = len(advertisements) + 1
    ad_dict = ad.model_dump()
    ad_dict["id"] = ad_id
    advertisements.append(ad_dict)
    return{"id": ad_id, "message": "Объявление успешно создано!", "data": ad_dict}

@app.get("/advertisement/{advertisement_id}")
async def get_advertisement(advertisement_id: int):
    for ad in advertisements:
        if ad["id"] == advertisement_id:
            return ad

    return {"message": "Объявление с таким id не найдено!"}

@app.get("/advertisement")
async def search_advertisements(
    title: Optional[str] = None,
    price: Optional[float] = None
):

    if title is None and price is None:
        return advertisements

    filtered_ads = []
    for ad in advertisements:
        matches_title = True
        if title:
            matches_title = title.lower() in ad["title"].lower()
        matches_price = True
        if price:
            matches_price = ad["price"] == price
        if matches_title and matches_price:
            filtered_ads.append(ad)

    return filtered_ads

@app.delete("/advertisement/{advertisement_id}")
async def delete_advertisement(advertisement_id: int):
    for index, ad in enumerate(advertisements):
        if ad["id"] == advertisement_id:
            advertisements.pop(index)
            return {"message": "Объявление успешно удалено!"}
    return {"message": "Объявление с таким id не найдено!"}

@app.patch("/advertisement/{advertisement_id}")
async def update_advertisement(advertisement_id: int, ad_update: AdvertisementUpdate):
    for ad in advertisements:
        if ad["id"] == advertisement_id:
            
            if ad_update.title:
                ad["title"] = ad_update.title
            if ad_update.description:
                ad["description"] = ad_update.description
            if ad_update.price:
                ad["price"] = ad_update.price
            if ad_update.author:
                ad["author"] = ad_update.author
            if ad_update.contacts:
                ad["contacts"] = ad_update.contacts
                
            return {"message": "Объявление обновлено", "data": ad}
            
    return {"message": "Объявление с таким id не найдено!"}
