from temperature import crud
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from temperature.schemas import Temperature, TemperatureBase
from city.crud import get_all_city
import httpx

URL = "http://api.weatherapi.com/v1/current.json"
API_KEY = "011a043214a540a8ad5125858243001"
router = APIRouter()


@router.get("/temperatures/", response_model=list[TemperatureBase])
def get_all_temperature(db: Session = Depends(get_db)):
    return crud.get_all_temperature(db=db)


@router.get("/temperatures/{temperature_id}", response_model=Temperature)
def get_temperature(temperature_id: int,
                    db: Session = Depends(get_db)):
    temperature = crud.get_temperature(db=db, temperature_id=temperature_id)
    if temperature is None:
        raise HTTPException(status_code=404, detail="Temperature not found")
    return temperature


@router.post("/temperatures/update")
async def update_all_temperature_into_city(db: Session = Depends(get_db)):
    cities = get_all_city(db)

    async with httpx.AsyncClient() as client:
        for city in cities:
            city_name = city.name
            params = {"key": API_KEY, "q": city_name}
            try:
                response = await client.get(URL, params=params)
                response.raise_for_status()
                data = response.json()
                temperature = data["current"]["temp_c"]

                crud.update_temperature(db, city.id, temperature)

            except httpx.HTTPError as e:
                raise HTTPException(status_code=404, detail=f"Failed to update temperature for {city_name}. {str(e)}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Temperature update"}
