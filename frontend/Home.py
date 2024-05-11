from PIL import Image
from streamlit import (
    caption,
    columns,
    divider,
    header,
    image,
    markdown,
    subheader,
    title,
)

from constants import ASSETS_PATH


title("Form Recognition & Document Extraction")
header("Insurance Carrier")
markdown("Building a Prototype for the Intel MLOps Capstone Project.")

divider()

col1, col2 = columns(2)

with col1:
    subheader("Document Extraction")
    forecasting_image = Image.open(ASSETS_PATH / "robot_arm.png")
    image(forecasting_image)
    caption(
        "Computer vision form recognition and document extraction using pre-trained models."
    )

with col2:
    subheader("Monitoring Dashboard")
    forecasting_image = Image.open(ASSETS_PATH / "stats.png")
    image(forecasting_image)
    caption(
        "Customer support chatbot based on pre-trained Phi-3 large language model"
    )

divider()

markdown("##### Notices & Disclaimers")
caption("""
        Performance varies by use, configuration, and other factors. 
        Learn more on the Performance Index site. 
        Performance results are based on testing as of dates 
        shown in configurations and may not reflect all publicly available updates.
        See backup for configuration details. No product or component can be absolutely secure.
        """)
divider()


if __name__ == "__main__":
    print("Frontend: Home Page Loaded.")