from sqlalchemy.ext.asyncio import AsyncSession

from secunda.application.dto import CreateActivityDTO
from secunda.application.entities import ActivityEntity
from secunda.application.interfaces import ActivityRepositoryProtocol


class GetActivitiesInteractor:
    def __init__(self, repository: ActivityRepositoryProtocol) -> None:
        self._repository = repository

    async def __call__(self) -> list[ActivityEntity]:
        return await self._repository.get_all()


class GetActivityByIdInteractor:
    def __init__(self, repository: ActivityRepositoryProtocol) -> None:
        self._repository = repository

    async def __call__(self, activity_id: int) -> ActivityEntity | None:
        return await self._repository.get_by_id(activity_id)


class CreateActivityInteractor:
    def __init__(self, repository: ActivityRepositoryProtocol, session: AsyncSession) -> None:
        self._repository = repository
        self._session = session

    async def __call__(self, dto: CreateActivityDTO) -> ActivityEntity:
        result = await self._repository.create(dto)
        await self._session.commit()
        return result


class GetActivityWithChildrenInteractor:
    def __init__(self, repository: ActivityRepositoryProtocol) -> None:
        self._repository = repository

    async def __call__(self, activity_id: int) -> list[int]:
        return await self._repository.get_with_children_recursive(activity_id)
