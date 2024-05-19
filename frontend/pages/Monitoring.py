"""This page is the main interface for monitoring the performance of the model."""

from requests import get
from matplotlib.pyplot import subplots, xticks
from pandas import DataFrame, to_datetime
from PIL import Image
from streamlit import caption, dataframe, divider, image, markdown, pyplot, title

from constants import ASSETS_PATH, MONITORING_ENDPOINT


# Example function to fetch data (adapt according to your API)
def fetch_inference_data(*args: list, url: str = MONITORING_ENDPOINT):
    response = get(url)
    data = response.json()
    return DataFrame(data)


# Load inference data
data = fetch_inference_data()

title("Monitoring Dashboard")
stats_image = Image.open(ASSETS_PATH / "stats.png")
image(stats_image)
markdown(
    "###### A simple tool for monitoring the performance of our model. This simple monitoring dashboard will help us track the inference latency and evaluate trends in prediction results."
)

markdown("### Record of Inference Results")
caption("A table containing metadata about each inference request made.")
dataframe(data[["request_id", "timestamp", "inference_time_ms", "predicted_label"]])

divider()

markdown("### Chart of Inference Time in Milliseconds (ms) vs Request DateTime Stamps")
caption("A line graph depicting the change inference time over time.")
fig, ax = subplots()
ax.plot(
    to_datetime(data["timestamp"]), data["inference_time_ms"], marker="o", linestyle="-"
)
ax.set_xlabel("Request DateTime")
ax.set_ylabel("Inference Time (ms)")
ax.set_title("Inference Time Over Time")
xticks(rotation=45)
pyplot(fig)

divider()

markdown("### Chart of Predicted Labels vs Request DateTime Stamps")
caption("A plot depicting the change predictions over time.")
fig, ax = subplots()
ax.plot(
    to_datetime(data["timestamp"]),
    data["predicted_label"],
    marker="o",
    linestyle="-",
    color="green",
)
ax.set_xlabel("Request DateTime")
ax.set_ylabel("Predicted Labels")
ax.set_title("Predictions Over Time")
xticks(rotation=45)
pyplot(fig)

divider()

markdown("### Histogram of Results")
caption("A histogram showing the frequency of each prediction label.")
fig, ax = subplots()
data["predicted_label"].value_counts().plot(kind="bar", ax=ax, color="blue")
ax.set_xlabel("Prediction Label")
ax.set_ylabel("Frequency")
ax.set_title("Frequency of Prediction Labels")
pyplot(fig)
