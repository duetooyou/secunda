from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, status

from secunda.application.dto import CreateBuildingDTO
from secunda.application.interactors import (
    CreateBuildingInteractor,
    GetBuildingByIdInteractor,
    GetBuildingsInteractor,
)
from secunda.presentation.schemas import BuildingCreate, BuildingResponse

router = APIRouter(prefix="/buildings", tags=["buildings"], route_class=DishkaRoute)


@router.get("", response_model=list[BuildingResponse])
async def get_buildings(
    interactor: FromDishka[GetBuildingsInteractor],
) -> list[BuildingResponse]:
    buildings = await interactor()
    return [BuildingResponse.model_validate(b) for b in buildings]


@router.get("/{building_id}", response_model=BuildingResponse)
async def get_building(
    building_id: int,
    interactor: FromDishka[GetBuildingByIdInteractor],
) -> BuildingResponse:
    building = await interactor(building_id)
    if not building:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Building not found")
    return BuildingResponse.model_validate(building)


@router.post("", response_model=BuildingResponse, status_code=status.HTTP_201_CREATED)
async def create_building(
    data: BuildingCreate,
    interactor: FromDishka[CreateBuildingInteractor],
) -> BuildingResponse:
    dto = CreateBuildingDTO(
        address=data.address,
        latitude=data.latitude,
        longitude=data.longitude,
    )
    building = await interactor(dto)
    return BuildingResponse.model_validate(building)
