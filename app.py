import streamlit as st
from pathlib import Path
import google.generativeai as genai, types
from api_key import API_KEY
import imghdr
import base64
import os

# # Configure the API with your key
# genai.configure(api_key=API_KEY)
    
# # Function to call the API with the image bytes
# def generate_content(image_bytes):
    
#     # client = genai.Client(api_key=api_key)
#     model = "gemini-2.0-flash"

#     # Prepare the content using the image bytes (no need to decode Base64 manually)
#     contents = [
#         types.Content(
#             role="user",
#             parts=[
#                 types.Part.from_bytes(
#                     mime_type="mime_type",
#                     data=image_bytes
#                 )
#             ]
#         )
#     ]

#     generate_content_config = types.GenerateContentConfig(
#         response_mime_type="text/plain",
#     )

#     # Collect the streamed response
#     response_text = ""
#     for chunk in client.models.generate_content_stream(
#         model=model,
#         contents=contents,
#         config=generate_content_config,
#     ):
#         response_text += chunk.text
#     return response_text



# Configure the API
genai.configure(api_key=API_KEY)

# Function to determine MIME type
def get_mime_type(image_bytes):
    img_type = imghdr.what(None, h=image_bytes)
    if img_type == "jpeg":
        return "image/jpeg"
    elif img_type == "png":
        return "image/png"
    else:
        return "application/octet-stream"  # Default if unknown type

# Function to call the API with the image bytes
def generate_content(image_bytes):
    mime_type = get_mime_type(image_bytes)  # Detect MIME type

    model = genai.GenerativeModel("gemini-2.0-flash")  # Ensure correct model
    
    prompt = (
        "Analyze this medical image and provide a detailed diagnosis. "
        "Explain key features, possible conditions, and relevant medical insights."
    )

    # Prepare the content with the correct MIME type
    contents = [prompt, {"mime_type": mime_type, "data": image_bytes}]

    # Generate response
    response = model.generate_content(contents)

    return response.text  # Extract response text

def main():
    
    st.set_page_config(
        page_title="Medical Image Detection",
        page_icon=":mag:",
        layout="wide",
    )
    
    # Set the title
    st.title("Welcome to Medical Image Detection and Diagnosis App")

    # Set subtitle
    st.subheader("An application that help users to identify medical images")

    # Upload the image
    uploaded_file = st.file_uploader("Upload the medical image for analysis", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        # Read image bytes from the uploaded file
        image_bytes = uploaded_file.read()

        # Optionally, display the uploaded image
        st.image(image_bytes, caption="Uploaded Image", use_container_width=True)

        # When the user clicks the button, call the generate_content function
        if st.button("Analyze Image"):
            with st.spinner("Processing..."):
                result = generate_content(image_bytes)
            st.success("Analysis Complete!")
            st.write("**Generated Output:**")
            st.write(result)

if __name__ == "__main__":
    main()

















