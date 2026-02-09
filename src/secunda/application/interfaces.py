from typing import Protocol, runtime_checkable

from secunda.application.dto import CreateActivityDTO, CreateBuildingDTO, CreateOrganizationDTO, GeoSearchDTO
from secunda.application.entities import ActivityEntity, BuildingEntity, OrganizationEntity


@runtime_checkable
class BuildingRepositoryProtocol(Protocol):
    async def create(self, dto: CreateBuildingDTO) -> BuildingEntity:
        ...

    async def get_by_id(self, building_id: int) -> BuildingEntity | None:
        ...

    async def get_all(self) -> list[BuildingEntity]:
        ...

    async def get_in_radius(self, lat: float, lon: float, radius_km: float) -> list[BuildingEntity]:
        ...

    async def get_in_rectangle(
        self, min_lat: float, max_lat: float, min_lon: float, max_lon: float
    ) -> list[BuildingEntity]:
        ...


@runtime_checkable
class ActivityRepositoryProtocol(Protocol):
    async def create(self, dto: CreateActivityDTO) -> ActivityEntity:
        ...

    async def get_by_id(self, activity_id: int) -> ActivityEntity | None:
        ...

    async def get_all(self) -> list[ActivityEntity]:
        ...

    async def get_with_children_recursive(self, activity_id: int) -> list[int]:
        ...


@runtime_checkable
class OrganizationRepositoryProtocol(Protocol):
    async def create(self, dto: CreateOrganizationDTO) -> OrganizationEntity:
        ...

    async def get_by_id(self, organization_id: int) -> OrganizationEntity | None:
        ...

    async def get_by_building_id(self, building_id: int) -> list[OrganizationEntity]:
        ...

    async def get_by_activity_id(self, activity_id: int) -> list[OrganizationEntity]:
        ...

    async def get_by_activity_ids(self, activity_ids: list[int]) -> list[OrganizationEntity]:
        ...

    async def search_by_name(self, name: str) -> list[OrganizationEntity]:
        ...

    async def get_in_geo_area(self, dto: GeoSearchDTO) -> list[OrganizationEntity]:
        ...
