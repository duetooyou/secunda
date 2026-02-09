from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, Query, status

from secunda.application.dto import CreateOrganizationDTO, GeoSearchDTO
from secunda.application.interactors import (
    CreateOrganizationInteractor,
    GetOrganizationByIdInteractor,
    GetOrganizationsByActivityInteractor,
    GetOrganizationsByBuildingInteractor,
    GetOrganizationsInGeoAreaInteractor,
    SearchOrganizationsByNameInteractor,
)
from secunda.presentation.schemas import (
    GeoRadiusSearch,
    GeoRectangleSearch,
    OrganizationCreate,
    OrganizationResponse,
)

router = APIRouter(prefix="/organizations", tags=["organizations"], route_class=DishkaRoute)


@router.get("/{organization_id}", response_model=OrganizationResponse)
async def get_organization(
    organization_id: int,
    interactor: FromDishka[GetOrganizationByIdInteractor],
) -> OrganizationResponse:
    organization = await interactor(organization_id)
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    return OrganizationResponse.model_validate(organization)


@router.get("/building/{building_id}", response_model=list[OrganizationResponse])
async def get_organizations_by_building(
    building_id: int,
    interactor: FromDishka[GetOrganizationsByBuildingInteractor],
) -> list[OrganizationResponse]:
    organizations = await interactor(building_id)
    return [OrganizationResponse.model_validate(o) for o in organizations]


@router.get("/activity/{activity_id}", response_model=list[OrganizationResponse])
async def get_organizations_by_activity(
    activity_id: int,
    include_children: bool = Query(True, description="Include child activities"),
    interactor: FromDishka[GetOrganizationsByActivityInteractor] = None,
) -> list[OrganizationResponse]:
    organizations = await interactor(activity_id, include_children)
    return [OrganizationResponse.model_validate(o) for o in organizations]


@router.get("/search/name", response_model=list[OrganizationResponse])
async def search_organizations_by_name(
    name: str = Query(..., min_length=1),
    interactor: FromDishka[SearchOrganizationsByNameInteractor] = None,
) -> list[OrganizationResponse]:
    organizations = await interactor(name)
    return [OrganizationResponse.model_validate(o) for o in organizations]


@router.post("/search/radius", response_model=list[OrganizationResponse])
async def get_organizations_in_radius(
    data: GeoRadiusSearch,
    interactor: FromDishka[GetOrganizationsInGeoAreaInteractor],
) -> list[OrganizationResponse]:
    dto = GeoSearchDTO(
        latitude=data.latitude,
        longitude=data.longitude,
        radius_km=data.radius_km,
    )
    organizations = await interactor(dto)
    return [OrganizationResponse.model_validate(o) for o in organizations]


@router.post("/search/rectangle", response_model=list[OrganizationResponse])
async def get_organizations_in_rectangle(
    data: GeoRectangleSearch,
    interactor: FromDishka[GetOrganizationsInGeoAreaInteractor],
) -> list[OrganizationResponse]:
    dto = GeoSearchDTO(
        latitude=0,
        longitude=0,
        min_lat=data.min_lat,
        max_lat=data.max_lat,
        min_lon=data.min_lon,
        max_lon=data.max_lon,
    )
    organizations = await interactor(dto)
    return [OrganizationResponse.model_validate(o) for o in organizations]


@router.post("", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    data: OrganizationCreate,
    interactor: FromDishka[CreateOrganizationInteractor],
) -> OrganizationResponse:
    dto = CreateOrganizationDTO(
        name=data.name,
        phones=data.phones,
        building_id=data.building_id,
        activity_ids=data.activity_ids,
    )
    organization = await interactor(dto)
    return OrganizationResponse.model_validate(organization)
