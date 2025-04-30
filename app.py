import streamlit as st
import requests

# ------------------------------
# 🔗 API Endpoint (FastAPI)
# ------------------------------
api_url = "https://image-saudi-413246863948.europe-west1.run.app/predict"

# ------------------------------
# 🎨 Page Configuration
# ------------------------------
st.set_page_config(page_title="Tura 2030", layout="centered")

st.markdown(
    """
    <style>
    /* Make all text white */
    html, body, .stApp, h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: white !important;
    }

    /* Override button text color to black */
    .stButton>button {
        color: black !important;
        background-color: white !important;  /* optional: makes background white */
        font-weight: bold;
    }

    /* Optional: change hover effect */
    .stButton>button:hover {
        background-color: #f0f0f0 !important;
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    /* Make the Get Forecast button black with white text */
    .stButton > button {
        background-color: black !important;
        color: white !important;
        border: none;
        padding: 0.5em 1.2em;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 500;
    }

    /* Optional: change on hover */
    .stButton > button:hover {
        background-color: #333 !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <style>
    /* Change the font size of the label */
    label[for="Enter the year to predict:"] {
        font-size: 20px; /* Change label font size */
        font-weight: 500; /* Optional: Make it bold */
        color: white;
    }

    /* Change the font size of the text input field */
    .stTextInput input {
        font-size: 30px; /* Change input text font size */
        height: 35px; /* Optional: Adjust input height */
    }

    /* Change font size for all placeholders (text displayed in st.empty()) */
    .stMarkdown {
        font-size: 20px;  /* Change to desired font size */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ------------------------------
# 🖼️ Optional Background Image (local)
# ------------------------------
def add_bg_from_url(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# مثال الاستخدام:
add_bg_from_url("https://media-hosting.imagekit.io/0bd921cb58fd4ac7/Image20250429160529.jpg?Expires=1840539945&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=ltP9fxiLonYZtIXRSkpEyiHr9t7e5tTKLIPVcm1~jHVHvNl2bRFotbpZpJwpMx3~BSXwYgYucHYuqI1IhPFz9TDxOT4RR7KVt8C98x4KwS3OtPmR7gHFhJga-U588yIzU0Dd6FaKnYLMslS~Q7giaM44wYsy3KEhw6x1TDFkIRLLYDjnshUkQLWnAvmzygKn33ufIL4nNpYwwLkHqpVP18KhBJ3M0V0mB7vK6bQ555w9K~vMOOUpLSLI7U3DsCyFbZ9aCdRukFMk~beWEfwVwR59BMnBt7EB6OsQibWQvZ3C26uU6mTN7XpLSCmnXcZex6JzjMDFgA4Fc1Z9Mtj7eA__")

# Uncomment this line and add your image path if you want background
# add_bg_from_local("background.jpg")  # put your image in the same directory

# ------------------------------
# 🧾 App Title & Instructions
# ------------------------------
st.title("Tura2030")
st.markdown("### Select a year to see forecasted tourism data:")
st.markdown("<br>", unsafe_allow_html=True)
# ------------------------------
# 📅 Year Input
# ------------------------------

# Input
input_year = st.text_input("Enter the year to predict:", max_chars=4)

st.markdown("<br>", unsafe_allow_html=True)

trigger_forecast = st.button("🔍 Get Forecast")
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"### 📊 Forecast for {input_year}:")

st.markdown("<br>", unsafe_allow_html=True)

# Setup placeholders with labels shown before request
row1 = st.columns(2)
st.markdown("<br>", unsafe_allow_html=True)
row2 = st.columns(2)

with row1[0]:
    dom_vis_placeholder = st.empty()
    dom_vis_placeholder.markdown("**🏠 Domestic Visitors:** —")

with row1[1]:
    dom_spend_placeholder = st.empty()
    dom_spend_placeholder.markdown("**💰 Domestic Spending:** —")

with row2[0]:
    inb_vis_placeholder = st.empty()
    inb_vis_placeholder.markdown("**✈️ Inbound Visitors:** —")
with row2[1]:
    inb_spend_placeholder = st.empty()
    inb_spend_placeholder.markdown("**🌍 Inbound Spending:** —")

# Action button
if trigger_forecast:
    if not input_year.isdigit() or len(input_year) != 4:
        st.error("❌ Please enter a valid 4-digit year.")
    else:
        try:
            # Construct API request with year as parameter
            params = {"year": input_year}
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            data = response.json()
            st.success("✅ Prediction retrieved successfully!")


            # Update the placeholders with real data
            dom_vis_placeholder.markdown(f"**🏠 Domestic Visitors:** {int(data['predicted number of domestic visitors']/100):,} M")
            dom_spend_placeholder.markdown(f"**💰 Domestic Spending:** {int(data['predicted spending of domestic  visitors']/100):,} B SAR")

            inb_vis_placeholder.markdown(f"**✈️ Inbound Visitors:** {int(data['predicted number of inbound visitors']/100):,} M")
            inb_spend_placeholder.markdown(f"**🌍 Inbound Spending:** {int(data['predicted spending of inbound visitors']/100):,} B SAR")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ API request failed: {e}")

st.markdown("<br><br><br>", unsafe_allow_html=True)  # Adjust the number of <br> as needed

st.markdown(
    """
    <style>
    html, body, .stApp {
        height: 100%;
        margin: 0;
        padding: 0;
    }

    .stApp {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .footer {
        background-color: transparent;
        color: #000;
        text-align: center;
        padding: 20px 0;
        font-size: 20px;
        border-top: 1px solid #ccc;
    }

    .footer a {
        color: white;
        text-decoration: none;
        margin: 0 15px;
        font-weight: 500;
    }

    .footer a:hover {
        text-decoration: underline;
    }
    </style>

    <div class="footer">
        📎 <a href="https://github.com/sukainahAlramadhan/saudi_arabia_tourism_forecast" target="_blank">Github</a>
        📊 <a href="https://www.kaggle.com/datasets/sukainahalramadhan/domestic-inbound-tourism-indicators" target="_blank">Project Data</a>

    </div>
    """,
    unsafe_allow_html=True
)
