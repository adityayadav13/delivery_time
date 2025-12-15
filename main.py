from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


model = joblib.load("delivery_time_model.pkl")
preprocessor = joblib.load("encoder.pkl")  

@app.post("/predict")
def predict(data: dict):


    distance_km = data["distance_km"]
    preparation_time_min = data["preparation_time_min"]
    courier_experience_yrs = data["courier_experience_yrs"]
    weather = data["weather"]
    traffic = data["traffic"]
    time_of_day = data["time_of_day"]

    raw_input = np.array([
        distance_km,
        weather,
        traffic,
        time_of_day,
        preparation_time_min,
        courier_experience_yrs
    ]).reshape(1, -1)

   
    try:
        processed_input = preprocessor.transform(raw_input)
    except Exception as e:
        print("Preprocessing skipped:", e)
        processed_input = raw_input


    prediction = model.predict(processed_input)[0]

    return {
        "predicted_time": float(prediction)
    }
