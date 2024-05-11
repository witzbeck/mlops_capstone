"""This page is the main interface for uploading and extracting output for the end user."""

from base64 import b64decode

from requests import get, post
from streamlit import (
    button,
    error,
    file_uploader,
    header,
    json,
    markdown,
    radio,
    success,
    tabs,
    text_area,
    text_input,
    title,
)

from constants import APP_URL_BASE
from utils import process_response

title("Form Recognition & Document Extraction")

app_tab, help_tab = tabs(["Application", "Help"])

with app_tab:
    header("Upload or Link Document for Data Extraction")
    upload_method = radio(
        "Select your input method:",
        ("Upload PDF", "Upload Image", "Image URL", "Paste Image Data (Base64)"),
    )

    # PDF Upload
    if upload_method == "Upload PDF":
        uploaded_pdf = file_uploader("Choose your PDF file", type=["pdf"])
        if uploaded_pdf is not None:
            pdf_bytes = uploaded_pdf.getvalue()
            URL = f"{APP_URL_BASE}/extract/pdf"
            files = {"file": ("document.pdf", pdf_bytes, "application/pdf")}
            response = post(URL, files=files)
            process_response(response)

    # Image Upload
    elif upload_method == "Upload Image":
        uploaded_image = file_uploader("Choose your image file", type=["jpg", "png"])
        if uploaded_image is not None:
            image_bytes = uploaded_image.getvalue()
            URL = f"{APP_URL_BASE}/extract/image"
            files = {"file": ("image.jpg", image_bytes, "image/jpeg")}
            response = post(URL, files=files)
            process_response(response)

    # Image URL
    elif upload_method == "Image URL":
        image_url = text_input("Enter the URL of the image")
        if button("Extract from URL"):
            response = get(image_url)
            if response.status_code == 200:
                URL = f"{APP_URL_BASE}/extract/image"
                files = {"file": ("image.jpg", response.content, "image/jpeg")}
                response = post(URL, files=files)
                process_response(response)
            else:
                error("Failed to download image from URL.")

    # Base64 Image Data
    elif upload_method == "Paste Image Data (Base64)":
        base64_string = text_area("Paste Base64 Image Data")
        if button("Extract from Base64"):
            if base64_string.startswith("data:image"):
                base64_string = base64_string.split(",")[
                    1
                ]  # Remove the "data:image/png;base64," part
            image_data = b64decode(base64_string)
            URL = f"{APP_URL_BASE}/extract/image"
            files = {"file": ("image.jpg", image_data, "image/jpeg")}
            response = post(URL, files=files)
            process_response(response)

with help_tab:
    header("Help")
    markdown(
        """
        - **Upload PDF/Image**: You can upload PDF files or images directly from your device.
        - **Image URL**: Provide a direct URL to an image for data extraction.
        - **Paste Image Data (Base64)**: Paste Base64 encoded image data directly into the text area.

        This application allows you to extract structured data from documents in various formats. After choosing your preferred input method and submitting your document, extracted data will be displayed below.

        **Note:** Ensure the Base64 string or URL is correct and accessible.
        """
    )


def process_response(response):
    """Utility function to process the API response."""
    if response.status_code == 200:
        extracted_data = response.json()
        success("Data extracted successfully!")
        json(extracted_data)
    else:
        error("Failed to extract data.")
