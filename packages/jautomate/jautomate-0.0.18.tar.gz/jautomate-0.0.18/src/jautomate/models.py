"""Models for jautomate"""

from pydantic import BaseModel, Field, computed_field

from jautomate.enums import AssetType


class User(BaseModel):
    """User Model"""
    first_name: str
    last_name: str
    email: str
    student_id: int | None = Field(default=None)
    staff_id: str | None = Field(default=None)
    building: str | None = Field(default=None)
    homeroom: str | None = Field(default=None)
    grad_year: str | None = Field(default=None)
    grade: str | None = Field(default=None)
    phone_number: str | None = Field(default=None)
    position: str | None = Field(default=None)
    floor: str | None = Field(default=None)
    owner: str | None = Field(default=None)
    username: str | None = Field(default=None)

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Asset(BaseModel):
    """Asset Model"""
    serial_number: str
    asset_tag: str
    device_type: AssetType
    jamf_id: str | None = Field(default=None)
    user: User | None = Field(default=None)
