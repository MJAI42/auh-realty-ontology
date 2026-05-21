from pydantic import BaseModel, Field
from datetime import UTC, date, datetime
from typing import Literal
from uuid import UUID, uuid4
from decimal import Decimal


Jurisdiction = Literal["AUH", "DXB", "TBS", "BUS", "TIA"]
# AUH=Abu Dhabi, DXB=Dubai, TBS=Tbilisi, BUS=Batumi, TIA=Tirana

PropertyType = Literal["villa", "apartment", "townhouse", "plot", "commercial"]

Currency = Literal["AED", "USD", "EUR", "GEL", "ALL"]


class Neighborhood(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    jurisdiction: Jurisdiction
    # boundary: optional GeoJSON polygon — add when needed


class Developer(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    jurisdiction: Jurisdiction


class Agent(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    agency: str | None = None


class Property(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    property_type: PropertyType
    neighborhood_id: UUID
    developer_id: UUID | None = None
    bedrooms: int | None = None
    bathrooms: int | None = None
    size_sqft: float | None = None
    latitude: float | None = None
    longitude: float | None = None
    completion_year: int | None = None
    jurisdiction: Jurisdiction


class Listing(BaseModel):
    """A snapshot of a Property at a point in time, from one source."""
    id: UUID = Field(default_factory=uuid4)
    property_id: UUID
    source: Literal["bayut", "property_finder", "dld", "manual"]
    source_url: str | None = None
    listed_price: Decimal
    currency: Currency
    listed_date: date
    agent_id: UUID | None = None
    status: Literal["active", "sold", "withdrawn", "unknown"] = "unknown"
    scraped_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Transaction(BaseModel):
    """An actual transacted price from a government register (e.g., DLD)."""
    id: UUID = Field(default_factory=uuid4)
    property_id: UUID
    transacted_price: Decimal
    currency: Currency
    transacted_date: date
    source: Literal["dld", "adrec", "georgian_register", "albanian_register", "private"]
