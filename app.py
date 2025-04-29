import streamlit as st
import requests

# ------------------------------
# 🔗 API Endpoint (FastAPI)
# ------------------------------
api_url = "https://image-saudi-413246863948.europe-west1.run.app/predict"

# ------------------------------
# 🎨 Page Configuration
# ------------------------------
st.set_page_config(page_title="Saudi Arabia Tourism Forecast", layout="centered")

# ------------------------------
# 🖼️ Optional Background Image (local)
# ------------------------------
def add_bg_from_local(image_path):
    with open(image_path, "rb") as image_file:
        encoded = image_file.read()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded.hex()}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Uncomment this line and add your image path if you want background
# add_bg_from_local("background.jpg")  # put your image in the same directory

# ------------------------------
# 🧾 App Title & Instructions
# ------------------------------
st.title("🇸🇦 Saudi Arabia Tourism Forecast")
st.markdown("### Select a year between **2024 and 2100** to see forecasted tourism data:")

# ------------------------------
# 📅 Year Input
# ------------------------------
year_input = st.slider(
    "Year:",
    min_value=2024,
    max_value=2100,
    value=2024,
    step=1,
)

# Convert year to format expected by FastAPI (e.g., "2026-07-01")

# ------------------------------
# 🔘 Predict Button
# ------------------------------
if st.button("Predict"):
    try:
        response = requests.get(api_url, params={"year": year_input})
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                st.error(f"API Error: {data['error']}")
            else:
                st.success("✅ Prediction retrieved successfully!")
                st.markdown(f"### 📊 Forecast for **{data['year']}**:")
                st.write(f"**Domestic Visitors:** {data['predicted number of domestic visitors']:.2f}")
                st.write(f"**Domestic Spending:** {data['predicted spending of domestic  visitors']:.2f} SAR")
                st.write(f"**Inbound Visitors:** {data['predicted number of inbound visitors']:.2f}")
                st.write(f"**Inbound Spending:** {data['predicted spending of inbound visitors']:.2f} SAR")
        else:
            st.error(f"Failed to fetch data: {response.status_code}")
    except Exception as e:
        st.error(f"Connection error: {e}")
