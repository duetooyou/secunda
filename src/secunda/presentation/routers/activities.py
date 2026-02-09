from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, status

from secunda.application.dto import CreateActivityDTO
from secunda.application.interactors import (
    CreateActivityInteractor,
    GetActivitiesInteractor,
    GetActivityByIdInteractor,
)
from secunda.presentation.schemas import ActivityCreate, ActivityResponse

router = APIRouter(prefix="/activities", tags=["activities"], route_class=DishkaRoute)


@router.get("", response_model=list[ActivityResponse])
async def get_activities(
    interactor: FromDishka[GetActivitiesInteractor],
) -> list[ActivityResponse]:
    activities = await interactor()
    return [ActivityResponse.model_validate(a) for a in activities]


@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(
    activity_id: int,
    interactor: FromDishka[GetActivityByIdInteractor],
) -> ActivityResponse:
    activity = await interactor(activity_id)
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
    return ActivityResponse.model_validate(activity)


@router.post("", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
async def create_activity(
    data: ActivityCreate,
    interactor: FromDishka[CreateActivityInteractor],
) -> ActivityResponse:
    dto = CreateActivityDTO(name=data.name, parent_id=data.parent_id)
    try:
        activity = await interactor(dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return ActivityResponse.model_validate(activity)
