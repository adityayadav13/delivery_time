import streamlit as st
import requests

st.set_page_config(page_title="Delivery Time Predictor", layout="centered")

st.title("📦 Delivery Time Prediction App")

distance_km = st.number_input("Distance (km)", min_value=0.0, step=0.1)
preparation_time_min = st.number_input("Preparation Time (min)", min_value=0.0, step=1.0)
courier_experience_yrs = st.number_input("Courier Experience (yrs)", min_value=0.0, step=0.5)

weather = st.selectbox(
    "Weather",
    options=[1, 2, 3, 4],
    format_func=lambda x: {1: "Clear", 2: "Windy", 3: "Rainy", 4: "Foggy"}[x]
)

traffic = st.selectbox(
    "Traffic",
    options=[1, 2, 3],
    format_func=lambda x: {1: "Low", 2: "Medium", 3: "High"}[x]
)

time_of_day = st.selectbox(
    "Time of Day",
    options=[1, 2, 3, 4],
    format_func=lambda x: {1: "Morning", 2: "Afternoon", 3: "Evening", 4: "Night"}[x]
)

BACKEND_URL = "https://delivery-time-8qxy.onrender.com/predict"

if st.button("Predict Delivery Time"):
    payload = {
        "distance_km": distance_km,
        "preparation_time_min": preparation_time_min,
        "courier_experience_yrs": courier_experience_yrs,
        "weather": weather,
        "traffic": traffic,
        "time_of_day": time_of_day
    }

    try:
        response = requests.post(BACKEND_URL, json=payload)
        result = response.json()

        st.write("Backend Response:", result)

        if "predicted_time" in result:
            st.success(f"Estimated Delivery Time: {result['predicted_time']:.2f} minutes")
        else:
            st.error("Prediction failed. Check backend logs.")
            st.write(result)

    except Exception as e:
        st.error("❌ Could not connect to backend. Check the URL or backend status.")
        st.exception(e)
