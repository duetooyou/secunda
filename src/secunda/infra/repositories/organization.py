from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from secunda.application.dto import CreateOrganizationDTO, GeoSearchDTO
from secunda.application.entities import ActivityEntity, BuildingEntity, OrganizationEntity
from secunda.application.services import GeoService
from secunda.infra.database.models import ActivityModel, BuildingModel, OrganizationModel, organization_activity


class OrganizationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _to_entity(self, model: OrganizationModel) -> OrganizationEntity:
        building = None
        if model.building:
            building = BuildingEntity(
                id=model.building.id,
                address=model.building.address,
                latitude=model.building.latitude,
                longitude=model.building.longitude,
                created_at=model.building.created_at,
            )

        activities = []
        if model.activities:
            activities = [
                ActivityEntity(
                    id=activity.id,
                    name=activity.name,
                    level=activity.level,
                    parent_id=activity.parent_id,
                    created_at=activity.created_at,
                )
                for activity in model.activities
            ]

        return OrganizationEntity(
            id=model.id,
            name=model.name,
            phones=model.phones or [],
            building_id=model.building_id,
            building=building,
            activities=activities,
            created_at=model.created_at,
        )

    async def create(self, dto: CreateOrganizationDTO) -> OrganizationEntity:
        model = OrganizationModel(
            name=dto.name,
            phones=dto.phones,
            building_id=dto.building_id,
        )
        self._session.add(model)
        await self._session.flush()

        if dto.activity_ids:
            stmt = select(ActivityModel).where(ActivityModel.id.in_(dto.activity_ids))
            result = await self._session.execute(stmt)
            activities = result.scalars().all()
            model.activities = list(activities)
            await self._session.flush()

        await self._session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, organization_id: int) -> OrganizationEntity | None:
        stmt = (
            select(OrganizationModel)
            .where(OrganizationModel.id == organization_id)
            .options(
                selectinload(OrganizationModel.building),
                selectinload(OrganizationModel.activities),
            )
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_building_id(self, building_id: int) -> list[OrganizationEntity]:
        stmt = (
            select(OrganizationModel)
            .where(OrganizationModel.building_id == building_id)
            .options(
                selectinload(OrganizationModel.building),
                selectinload(OrganizationModel.activities),
            )
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(org_model) for org_model in result.scalars().all()]

    async def get_by_activity_id(self, activity_id: int) -> list[OrganizationEntity]:
        stmt = (
            select(OrganizationModel)
            .join(organization_activity)
            .where(organization_activity.c.activity_id == activity_id)
            .options(
                selectinload(OrganizationModel.building),
                selectinload(OrganizationModel.activities),
            )
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(org_model) for org_model in result.scalars().all()]

    async def get_by_activity_ids(self, activity_ids: list[int]) -> list[OrganizationEntity]:
        stmt = (
            select(OrganizationModel)
            .join(organization_activity)
            .where(organization_activity.c.activity_id.in_(activity_ids))
            .distinct(OrganizationModel.id)
            .options(
                selectinload(OrganizationModel.building),
                selectinload(OrganizationModel.activities),
            )
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(org_model) for org_model in result.scalars().all()]

    async def search_by_name(self, name: str) -> list[OrganizationEntity]:
        stmt = (
            select(OrganizationModel)
            .where(OrganizationModel.name.ilike(f"%{name}%"))
            .options(
                selectinload(OrganizationModel.building),
                selectinload(OrganizationModel.activities),
            )
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(org_model) for org_model in result.scalars().all()]

    async def get_in_geo_area(self, dto: GeoSearchDTO) -> list[OrganizationEntity]:
        if dto.radius_km is not None:
            building_ids = await self._get_building_ids_in_radius(
                dto.latitude, dto.longitude, dto.radius_km
            )
        elif all(coord is not None for coord in [dto.min_lat, dto.max_lat, dto.min_lon, dto.max_lon]):
            building_ids = await self._get_building_ids_in_rectangle(
                dto.min_lat, dto.max_lat, dto.min_lon, dto.max_lon  # type: ignore
            )
        else:
            return []

        if not building_ids:
            return []

        stmt = (
            select(OrganizationModel)
            .where(OrganizationModel.building_id.in_(building_ids))
            .options(
                selectinload(OrganizationModel.building),
                selectinload(OrganizationModel.activities),
            )
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(org_model) for org_model in result.scalars().all()]

    async def _get_building_ids_in_radius(
        self, lat: float, lon: float, radius_km: float
    ) -> list[int]:
        bounding_box = GeoService.calculate_bounding_box(lat, lon, radius_km)

        stmt = select(BuildingModel).where(
            BuildingModel.latitude.between(bounding_box.min_lat, bounding_box.max_lat),
            BuildingModel.longitude.between(bounding_box.min_lon, bounding_box.max_lon),
        )
        result = await self._session.execute(stmt)
        buildings = result.scalars().all()

        return [
            building.id
            for building in buildings
            if GeoService.is_within_radius(lat, lon, building.latitude, building.longitude, radius_km)
        ]

    async def _get_building_ids_in_rectangle(
        self, min_lat: float, max_lat: float, min_lon: float, max_lon: float
    ) -> list[int]:
        stmt = select(BuildingModel.id).where(
            BuildingModel.latitude.between(min_lat, max_lat),
            BuildingModel.longitude.between(min_lon, max_lon),
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
