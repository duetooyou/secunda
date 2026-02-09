from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class BuildingEntity:
    id: int
    address: str
    latitude: float
    longitude: float
    created_at: datetime | None = None


@dataclass
class ActivityEntity:
    id: int
    name: str
    level: int
    parent_id: int | None = None
    created_at: datetime | None = None
    children: list["ActivityEntity"] = field(default_factory=list)


@dataclass
class OrganizationEntity:
    id: int
    name: str
    phones: list[str]
    building_id: int
    building: BuildingEntity | None = None
    activities: list[ActivityEntity] = field(default_factory=list)
    created_at: datetime | None = None
