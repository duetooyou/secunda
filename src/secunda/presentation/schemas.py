from pydantic import BaseModel, Field


class BuildingBase(BaseModel):
    address: str = Field(..., max_length=500)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class BuildingCreate(BuildingBase):
    pass


class BuildingResponse(BuildingBase):
    id: int

    model_config = {"from_attributes": True}


class ActivityBase(BaseModel):
    name: str = Field(..., max_length=255)


class ActivityCreate(ActivityBase):
    parent_id: int | None = None


class ActivityResponse(ActivityBase):
    id: int
    level: int
    parent_id: int | None = None
    children: list["ActivityResponse"] = []

    model_config = {"from_attributes": True}


class OrganizationBase(BaseModel):
    name: str = Field(..., max_length=255)
    phones: list[str] = Field(default_factory=list)


class OrganizationCreate(OrganizationBase):
    building_id: int
    activity_ids: list[int] = Field(default_factory=list)


class OrganizationResponse(OrganizationBase):
    id: int
    building_id: int
    building: BuildingResponse | None = None
    activities: list[ActivityResponse] = []

    model_config = {"from_attributes": True}


class GeoRadiusSearch(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    radius_km: float = Field(..., gt=0)


class GeoRectangleSearch(BaseModel):
    min_lat: float = Field(..., ge=-90, le=90)
    max_lat: float = Field(..., ge=-90, le=90)
    min_lon: float = Field(..., ge=-180, le=180)
    max_lon: float = Field(..., ge=-180, le=180)
