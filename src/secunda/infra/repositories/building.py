from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from secunda.application.dto import CreateBuildingDTO
from secunda.application.entities import BuildingEntity
from secunda.application.services import GeoService
from secunda.infra.database.models import BuildingModel


class BuildingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _to_entity(self, model: BuildingModel) -> BuildingEntity:
        return BuildingEntity(
            id=model.id,
            address=model.address,
            latitude=model.latitude,
            longitude=model.longitude,
            created_at=model.created_at,
        )

    async def create(self, dto: CreateBuildingDTO) -> BuildingEntity:
        model = BuildingModel(
            address=dto.address,
            latitude=dto.latitude,
            longitude=dto.longitude,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, building_id: int) -> BuildingEntity | None:
        result = await self._session.get(BuildingModel, building_id)
        return self._to_entity(result) if result else None

    async def get_all(self) -> list[BuildingEntity]:
        result = await self._session.execute(select(BuildingModel))
        return [self._to_entity(building_model) for building_model in result.scalars().all()]

    async def get_in_radius(self, lat: float, lon: float, radius_km: float) -> list[BuildingEntity]:
        bounding_box = GeoService.calculate_bounding_box(lat, lon, radius_km)

        stmt = select(BuildingModel).where(
            BuildingModel.latitude.between(bounding_box.min_lat, bounding_box.max_lat),
            BuildingModel.longitude.between(bounding_box.min_lon, bounding_box.max_lon),
        )
        result = await self._session.execute(stmt)
        buildings = result.scalars().all()

        return [
            self._to_entity(building)
            for building in buildings
            if GeoService.is_within_radius(lat, lon, building.latitude, building.longitude, radius_km)
        ]

    async def get_in_rectangle(
        self, min_lat: float, max_lat: float, min_lon: float, max_lon: float
    ) -> list[BuildingEntity]:
        stmt = select(BuildingModel).where(
            BuildingModel.latitude.between(min_lat, max_lat),
            BuildingModel.longitude.between(min_lon, max_lon),
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(building_model) for building_model in result.scalars().all()]
