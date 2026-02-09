from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from secunda.application.constants import MAX_ACTIVITY_NESTING_LEVEL
from secunda.application.dto import CreateActivityDTO
from secunda.application.entities import ActivityEntity
from secunda.infra.database.models import ActivityModel


class ActivityRepository:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _to_entity(self, model: ActivityModel, include_children: bool = False) -> ActivityEntity:
        children = []
        if include_children and model.children:
            children = [self._to_entity(child, include_children=True) for child in model.children]
        return ActivityEntity(
            id=model.id,
            name=model.name,
            level=model.level,
            parent_id=model.parent_id,
            created_at=model.created_at,
            children=children,
        )

    async def create(self, dto: CreateActivityDTO) -> ActivityEntity:
        level = 1
        if dto.parent_id:
            parent = await self._session.get(ActivityModel, dto.parent_id)
            if parent:
                level = parent.level + 1
                if level > MAX_ACTIVITY_NESTING_LEVEL:
                    raise ValueError(f"Максимальный уровень вложенности: {MAX_ACTIVITY_NESTING_LEVEL}")

        model = ActivityModel(
            name=dto.name,
            parent_id=dto.parent_id,
            level=level,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, activity_id: int) -> ActivityEntity | None:
        stmt = (
            select(ActivityModel)
            .where(ActivityModel.id == activity_id)
            .options(
                selectinload(ActivityModel.children)
                .selectinload(ActivityModel.children)
                .selectinload(ActivityModel.children)
            )
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model, include_children=True) if model else None

    async def get_all(self) -> list[ActivityEntity]:
        stmt = (
            select(ActivityModel)
            .where(ActivityModel.parent_id.is_(None))
            .options(
                selectinload(ActivityModel.children)
                .selectinload(ActivityModel.children)
                .selectinload(ActivityModel.children)
            )
        )
        result = await self._session.execute(stmt)
        return [
            self._to_entity(activity_model, include_children=True)
            for activity_model in result.scalars().all()
        ]

    async def get_with_children_recursive(self, activity_id: int) -> list[int]:
        ids = [activity_id]
        await self._collect_children_ids(activity_id, ids)
        return ids

    async def _collect_children_ids(self, parent_id: int, ids: list[int]) -> None:
        stmt = select(ActivityModel.id).where(ActivityModel.parent_id == parent_id)
        result = await self._session.execute(stmt)
        child_ids = result.scalars().all()
        for cid in child_ids:
            ids.append(cid)
            await self._collect_children_ids(cid, ids)
