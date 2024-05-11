import base64
from typing import Optional

from pydantic import BaseModel, HttpUrl, field_validator


class ImageInput(BaseModel):
    image_base64: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    image_file: Optional[bytes] = None

    @field_validator("image_base64", pre=True, always=True)
    def validate_base64(cls, v, values):
        if v is not None:
            # Try to decode to verify if it is correct base64
            try:
                base64.b64decode(v)
            except ValueError as e:
                raise ValueError(f"Invalid base64 string {e}") from e
        # Ensure only one input is provided
        if (
            sum(
                x is not None
                for x in [v, values.get("image_url"), values.get("image_file")]
            )
            > 1
        ):
            raise ValueError("Please provide only one type of image input")
        return v

    @field_validator("image_url", pre=True, always=True)
    def validate_url(cls, v, values):
        # Ensure only one input is provided
        if (
            sum(
                x is not None
                for x in [values.get("image_base64"), v, values.get("image_file")]
            )
            > 1
        ):
            raise ValueError("Please provide only one type of image input")
        return v

    @field_validator("image_file", pre=True, always=True)
    def validate_file(cls, v, values):
        # Ensure only one input is provided
        if (
            sum(
                x is not None
                for x in [values.get("image_base64"), values.get("image_url"), v]
            )
            > 1
        ):
            raise ValueError("Please provide only one type of image input")
        return v


class PDFInputModel(BaseModel):
    pdf_file: bytes  # Uploaded PDF file data


# Assuming we will extract and return structured data as a dictionary
class ExtractedDataModel(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    number_of_pages: Optional[int] = None


class TrainPayload(BaseModel):
    file: str
    model_name: str
    model_path: str
    test_size: int = 25
    ncpu: int = 4
    mlflow_tracking_uri: str
    mlflow_new_experiment: str = None
    mlflow_experiment: str = None


class PredictionPayload(BaseModel):
    model_name: str
    stage: str
    sample: list
    model_run_id: str
    scaler_file_name: str
    scaler_destination: str = "./"
