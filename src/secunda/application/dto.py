from dataclasses import dataclass


@dataclass
class CreateBuildingDTO:
    address: str
    latitude: float
    longitude: float


@dataclass
class CreateActivityDTO:
    name: str
    parent_id: int | None = None


@dataclass
class CreateOrganizationDTO:
    name: str
    phones: list[str]
    building_id: int
    activity_ids: list[int]


@dataclass
class GeoSearchDTO:
    latitude: float
    longitude: float
    radius_km: float | None = None
    min_lat: float | None = None
    max_lat: float | None = None
    min_lon: float | None = None
    max_lon: float | None = None
