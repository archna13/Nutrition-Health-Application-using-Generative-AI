### Health Management APP
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

load_dotenv()  # Load all environment variables

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Google Gemini Pro Vision API
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, image[0], prompt])
    return response.text

# Function to prepare image data for API
def prepare_image_data(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        st.error("Please upload an image before submitting.")
        return None

# Set up the Streamlit page
st.set_page_config(page_title="Gemini Health App", page_icon=":apple:")

# Page Title and Description


# Custom CSS for styling with background image and font adjustments
st.markdown(
    """
    <style>
    body {
        background-image: url('https://source.unsplash.com/1600x900/?health,food');
        background-size: cover;
        background-position: center;
        color: white;
    }
    .custom-header {
        font-size: 36px;
        font-weight: bold;
        color: #FFD700;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .custom-text {
        font-size: 20px;
        color: #FFD700;
        text-align: center;
    }
    .css-1v3fvcr {
        background-color: rgba(0, 0, 0, 0.5);
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Page Title and Description
st.markdown("<h1 class='custom-header'>Calories Health App</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <p class='custom-text'>
    Welcome to the Health App! This tool uses advanced AI to analyze your food items from an image and provides detailed nutritional insights including total calories and health assessments.
    </p>
    """,
    unsafe_allow_html=True
)

# Sidebar for user inputs
st.sidebar.header("User Input")
input_text = st.sidebar.text_input("Describe the Image:", key="input")
uploaded_file = st.sidebar.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Input prompt for API
input_prompt = """
You are an expert nutritionist tasked with analyzing the food items in the image,
calculating the total calories, and providing detailed information for each item as follows:
1. Item 1 - number of calories
2. Item 2 - number of calories
...
Additionally, please evaluate whether the food is healthy, and provide the percentage breakdown of carbohydrates, fats, fibers, sugars, and proteins.
"""

# Submit Button
if st.sidebar.button("Analyze"):
    image_data = prepare_image_data(uploaded_file)
    if image_data:
        with st.spinner('Processing...'):
            response = get_gemini_response(input_text, image_data, input_prompt)
        st.subheader("Nutritional Analysis:")
        st.write(response)
