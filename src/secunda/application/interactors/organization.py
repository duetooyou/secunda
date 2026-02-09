from sqlalchemy.ext.asyncio import AsyncSession

from secunda.application.dto import CreateOrganizationDTO, GeoSearchDTO
from secunda.application.entities import OrganizationEntity
from secunda.application.interfaces import ActivityRepositoryProtocol, OrganizationRepositoryProtocol


class GetOrganizationByIdInteractor:
    def __init__(self, repository: OrganizationRepositoryProtocol) -> None:
        self._repository = repository

    async def __call__(self, organization_id: int) -> OrganizationEntity | None:
        return await self._repository.get_by_id(organization_id)


class GetOrganizationsByBuildingInteractor:
    def __init__(self, repository: OrganizationRepositoryProtocol) -> None:
        self._repository = repository

    async def __call__(self, building_id: int) -> list[OrganizationEntity]:
        return await self._repository.get_by_building_id(building_id)


class GetOrganizationsByActivityInteractor:
    def __init__(
        self,
        organization_repo: OrganizationRepositoryProtocol,
        activity_repo: ActivityRepositoryProtocol,
    ) -> None:
        self._organization_repo = organization_repo
        self._activity_repo = activity_repo

    async def __call__(
        self, activity_id: int, include_children: bool = True
    ) -> list[OrganizationEntity]:
        if include_children:
            activity_ids = await self._activity_repo.get_with_children_recursive(activity_id)
            return await self._organization_repo.get_by_activity_ids(activity_ids)
        return await self._organization_repo.get_by_activity_id(activity_id)


class GetOrganizationsInGeoAreaInteractor:
    def __init__(self, repository: OrganizationRepositoryProtocol) -> None:
        self._repository = repository

    async def __call__(self, dto: GeoSearchDTO) -> list[OrganizationEntity]:
        return await self._repository.get_in_geo_area(dto)


class SearchOrganizationsByNameInteractor:
    def __init__(self, repository: OrganizationRepositoryProtocol) -> None:
        self._repository = repository

    async def __call__(self, name: str) -> list[OrganizationEntity]:
        return await self._repository.search_by_name(name)


class CreateOrganizationInteractor:
    def __init__(self, repository: OrganizationRepositoryProtocol, session: AsyncSession) -> None:
        self._repository = repository
        self._session = session

    async def __call__(self, dto: CreateOrganizationDTO) -> OrganizationEntity:
        result = await self._repository.create(dto)
        await self._session.commit()
        return result
