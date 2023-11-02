from fastapi import FastAPI, HTTPException
from fastapi import Form, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import util
from app.predict import predict_price

# c:\users\sudha\appdata\roaming\python\python311\scripts\uvicorn main:app --host 0.0.0.0 --port 8000 --reload

app = FastAPI()

class HousePredictionRequest(BaseModel):
    total_sqft: float
    location: str
    bhk: int
    bath: int
    
# Enable CORS to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("app/static/index.html")

@app.get("/buy")
async def read_buy():
    return FileResponse("app/static/buy.html")

@app.get("/sell")
async def read_sell():
    return FileResponse("app/static/sell.html")

@app.post("/predict_house_price")
async def predict_house_price():
    try:
        # Your data processing logic here
        # estimated_price = util.get_estimated_price(request_data.total_sqft, request_data.location, request_data.bhk, request_data.bath)
        total_sqft=float(request.form['total_sqft'])
        location=request.form['location']
        bhk=int(request.form['bhk'])
        bath=int(request.form['bath'])

        result = response.json()
        estimated_price = result["estimated_price"]
        return estimated_price
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/uploadfile")
async def upload_photo(file: UploadFile):
    with open(os.path.join("app/photos", file.filename), "wb") as f:
        f.write(file.file.read())
    return {"filename": file.filename}

@app.get("/get_location_names")
def get_location_names():
    return {'locations': util.get_location_names()}


if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI Server For Home Price Prediction...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000)