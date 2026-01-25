from fastapi import Query
from schemas import Advertisement, AdvertisementUpdate
from fastapi import FastAPI, HTTPException
from typing import Optional
from datetime import datetime

app = FastAPI()

advertisements = []
@app.get("/")
async def root():
    return {"message": "Привет, это сервис объявлений!"}

@app.post("/advertisement", status_code=201)
async def create_advertisement(ad: Advertisement):
    ad_id = len(advertisements) + 1
    ad_dict = ad.model_dump()
    ad_dict["id"] = ad_id
    ad_dict["created_at"] = datetime.now().isoformat()
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
async def delete_advertisement(advertisement_id: int):
    for index, ad in enumerate(advertisements):
        if ad["id"] == advertisement_id:
            advertisements.pop(index)
            return 
    raise HTTPException(status_code=404, detail="Объявление с таким id не найдено!")

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
            
    raise HTTPException(status_code=404, detail="Объявление с таким id не найдено!")
