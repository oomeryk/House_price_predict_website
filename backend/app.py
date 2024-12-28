from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import r 

app = FastAPI()

class RentalRequest(BaseModel):
    city: str
    district: str
    neighborhood: str
    room: str
    metrekare: str

@app.post("/rentalhouse")
async def rental_house(request: RentalRequest):
    try:
        result = r.pred_price(request.city, request.district, request.neighborhood, request.room, request.metrekare)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sunucu hatası: {str(e)}")


@app.get("/")
async def root():
    return "hello world"