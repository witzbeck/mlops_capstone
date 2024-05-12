from base64 import b64decode
from dataclasses import asdict, dataclass
from json import loads
from typing import List, Optional

from faker import Faker
from pydantic import BaseModel, HttpUrl, field_validator


@dataclass
class DataModelBase:
    """Base class for all data models."""

    @classmethod
    def from_dict(cls, data: dict):
        """Create a new instance from a dictionary."""
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str):
        """Create a new instance from a JSON string."""
        return cls.from_dict(loads(json_str))

    def to_dict(self):
        """Convert the instance to a dictionary."""
        return asdict(self)

    @classmethod
    def rand(cls):
        """Generate a random instance for testing."""
        raise NotImplementedError


@dataclass
class Address(DataModelBase):
    """Represents a typical address and can be reused for both agency and insured addresses."""

    line1: str
    line2: Optional[str]
    city: str
    state: str
    zip_code: str

    @classmethod
    def rand(cls, faker: Faker = None) -> "Address":
        """Generate a random instance for testing."""
        if faker is None:
            faker = Faker()
        return cls(
            line1=faker.street_address(),
            line2=faker.secondary_address()
            if faker.boolean(chance_of_getting_true=50)
            else None,
            city=faker.city(),
            state=faker.state_abbr(),
            zip_code=faker.zipcode(),
        )


@dataclass
class ContactInfo(DataModelBase):
    """Handles contact details like phone, fax, and email."""

    full_name: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: str
    phone_type: str
    fax_number: Optional[str]
    email: str
    mailing_address: Address
    physical_address: Address

    @classmethod
    def rand(cls, faker: Faker = None) -> "ContactInfo":
        """Generate a random instance for testing."""
        if faker is None:
            faker = Faker()
        return cls(
            full_name=faker.name(),
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            phone_number=faker.phone_number(),
            phone_type=faker.random_element(elements=("Home", "Work", "Mobile", "Fax")),
            fax_number=faker.phone_number()
            if faker.boolean(chance_of_getting_true=50)
            else None,
            email=faker.email(),
        )


@dataclass
class Agency(DataModelBase):
    """Defines agency-specific information, including the contact and address."""

    agency_name: str
    agency_code: str
    contact_info: ContactInfo
    address: Address
    customer_id: str

    @classmethod
    def rand(cls, faker: Faker = None) -> "Agency":
        """Generate a random instance for testing."""
        if faker is None:
            faker = Faker()
        return cls(
            agency_name=faker.company(),
            agency_code=faker.random_int(min=1000, max=9999),
            contact_info=ContactInfo.rand(faker=faker),
            address=Address.rand(faker=faker),
            customer_id=faker.random_int(min=1000, max=9999),
        )


@dataclass
class InsuredInfo(DataModelBase):
    """Represents the insured or additional insureds' details,
    such as name and NAICS code."""

    name: str
    mailing_address: Address
    naics_code: str
    sic_code: str
    fein_or_ssn: str
    website_address: Optional[str]

    @classmethod
    def rand(cls, faker: Faker = None) -> "InsuredInfo":
        """Generate a random instance for testing."""
        if faker is None:
            faker = Faker()
        return cls(
            name=faker.company(),
            mailing_address=Address.rand(faker=faker),
            naics_code=faker.random_int(min=1000, max=9999),
            sic_code=faker.random_int(min=1000, max=9999),
            fein_or_ssn=faker.ssn(),
            website_address=faker.url()
            if faker.boolean(chance_of_getting_true=50)
            else None,
        )


@dataclass
class PolicyInfo(DataModelBase):
    """Encapsulates details about the policy,
    such as effective dates, lines of business, and premiums."""

    proposed_eff_date: str
    proposed_exp_date: str
    lines_of_business: List[str]
    premium_details: dict  # Could be a detailed breakdown

    @classmethod
    def rand(cls, faker: Faker = None) -> "PolicyInfo":
        """Generate a random instance for testing."""
        if faker is None:
            faker = Faker()
        return cls(
            proposed_eff_date=faker.date_this_year(),
            proposed_exp_date=faker.date_this_year(),
            lines_of_business=faker.random_elements(
                elements=("Collision", "Comprehensive", "Liability"),
                length=faker.random_int(min=1, max=3),
                unique=True,
            ),
            premium_details={
                "Collision": faker.random_int(min=1000, max=9999),
                "Comprehensive": faker.random_int(min=1000, max=9999),
                "Liability": faker.random_int(min=1000, max=9999),
            },
        )


@dataclass
class BusinessInfo(DataModelBase):
    """Stores detailed information about the business entity type, operation descriptions, and employee statistics."""

    entity_type: str
    number_of_members: Optional[int]
    description_of_operations: str
    business_started_date: str
    annual_revenue: float
    no_of_employees_fulltime: int
    no_of_employees_parttime: int

    @classmethod
    def rand(cls, faker: Faker = None) -> "BusinessInfo":
        """Generate a random instance for testing."""
        if faker is None:
            faker = Faker()
        return cls(
            entity_type=faker.random_element(
                elements=("Corporation", "Partnership", "Sole Proprietorship")
            ),
            number_of_members=faker.random_int(min=1, max=10)
            if faker.boolean(chance_of_getting_true=50)
            else None,
            description_of_operations=faker.catch_phrase(),
            business_started_date=faker.date_this_century(),
            annual_revenue=faker.random_int(min=10000, max=99999),
            no_of_employees_fulltime=faker.random_int(min=1, max=10),
            no_of_employees_parttime=faker.random_int(min=1, max=10),
        )


@dataclass
class Coverage(DataModelBase):
    """Represents different coverage types and their respective premiums."""

    line_of_business: str
    coverage_code: str
    premium: float

    @classmethod
    def rand(cls, faker: Faker = None) -> "Coverage":
        """Generate a random instance for testing."""
        if faker is None:
            faker = Faker()
        return cls(
            line_of_business=faker.random_element(
                elements=("Collision", "Comprehensive", "Liability")
            ),
            coverage_code=faker.random_int(min=1000, max=9999),
            premium=faker.random_int(min=1000, max=9999),
        )


@dataclass
class Application(DataModelBase):
    """The top-level class that ties all the other pieces together
    into a complete application form as defined by the PDF."""

    agency: Agency
    first_named_insured: InsuredInfo
    additional_insureds: List[InsuredInfo]
    policy_info: PolicyInfo
    business_info: BusinessInfo
    coverages: List[Coverage]

    @classmethod
    def rand(cls, faker: Faker = None) -> "Application":
        """Generate a random instance for testing."""
        if faker is None:
            faker = Faker()
        return cls(
            agency=Agency.rand(faker),
            first_named_insured=InsuredInfo.rand(faker),
            additional_insureds=[
                InsuredInfo.rand(faker) for _ in range(faker.random_int(min=0, max=3))
            ],
            policy_info=PolicyInfo.rand(faker),
            business_info=BusinessInfo.rand(faker),
            coverages=[
                Coverage.rand(faker) for _ in range(faker.random_int(min=1, max=3))
            ],
        )


class ImageInput(BaseModel):
    """Handles image input in base64, URL, or file format."""

    image_base64: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    image_file: Optional[bytes] = None

    @field_validator(
        "image_base64",
    )
    def validate_base64(cls, v, values):
        if v is not None:
            # Try to decode to verify if it is correct base64
            try:
                b64decode(v)
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

    @field_validator(
        "image_url",
    )
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

    @field_validator(
        "image_file",
    )
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

    def to_dict(self):
        """Convert the instance to a dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        """Create a new instance from a dictionary."""
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str):
        """Create a new instance from a JSON string."""
        return cls.from_dict(loads(json_str))

    def __post_init__(self):
        """Initialize the data model."""
        if self.image_base64 is not None:
            self.image_base64 = b64decode(self.image_base64)
        if self.image_file is not None:
            self.image_file = b64decode(self.image_file)


class PDFInputModel(BaseModel):
    pdf_file: bytes  # Uploaded PDF file data
    pdf_url: Optional[HttpUrl] = None  # URL to download the PDF file
    pdf_base64: Optional[str] = None  # Base64 encoded PDF file data

    @field_validator(
        "pdf_base64",
    )
    def validate_base64(cls, v, values):
        if v is not None:
            # Try to decode to verify if it is correct base64
            try:
                b64decode(v)
            except ValueError as e:
                raise ValueError(f"Invalid base64 string {e}") from e
        # Ensure only one input is provided
        if (
            sum(
                x is not None
                for x in [v, values.get("pdf_url"), values.get("pdf_file")]
            )
            > 1
        ):
            raise ValueError("Please provide only one type of PDF input")
        return v

    @field_validator(
        "pdf_url",
    )
    def validate_url(cls, v, values):
        # Ensure only one input is provided
        if (
            sum(
                x is not None
                for x in [values.get("pdf_base64"), v, values.get("pdf_file")]
            )
            > 1
        ):
            raise ValueError("Please provide only one type of PDF input")
        return v

    @field_validator(
        "pdf_file",
    )
    def validate_file(cls, v, values):
        # Ensure only one input is provided
        if (
            sum(
                x is not None
                for x in [values.get("pdf_base64"), values.get("pdf_url"), v]
            )
            > 1
        ):
            raise ValueError("Please provide only one type of PDF input")
        return v

    def to_dict(self):
        """Convert the instance to a dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        """Create a new instance from a dictionary."""
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str):
        """Create a new instance from a JSON string."""
        return cls.from_dict(loads(json_str))


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
