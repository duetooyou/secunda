from sqlalchemy.ext.asyncio import AsyncSession

from secunda.application.dto import CreateBuildingDTO
from secunda.application.entities import BuildingEntity
from secunda.application.interfaces import BuildingRepositoryProtocol


class GetBuildingsInteractor:
    def __init__(self, repository: BuildingRepositoryProtocol) -> None:
        self._repository = repository

    async def __call__(self) -> list[BuildingEntity]:
        return await self._repository.get_all()


class GetBuildingByIdInteractor:
    def __init__(self, repository: BuildingRepositoryProtocol) -> None:
        self._repository = repository

    async def __call__(self, building_id: int) -> BuildingEntity | None:
        return await self._repository.get_by_id(building_id)


class CreateBuildingInteractor:
    def __init__(self, repository: BuildingRepositoryProtocol, session: AsyncSession) -> None:
        self._repository = repository
        self._session = session

    async def __call__(self, dto: CreateBuildingDTO) -> BuildingEntity:
        result = await self._repository.create(dto)
        await self._session.commit()
        return result
