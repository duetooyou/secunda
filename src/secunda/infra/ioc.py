from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing_extensions import AsyncIterable

from secunda.application.interfaces import (
    ActivityRepositoryProtocol,
    BuildingRepositoryProtocol,
    OrganizationRepositoryProtocol,
)
from secunda.application.interactors import (
    CreateActivityInteractor,
    CreateBuildingInteractor,
    CreateOrganizationInteractor,
    GetActivitiesInteractor,
    GetActivityByIdInteractor,
    GetActivityWithChildrenInteractor,
    GetBuildingByIdInteractor,
    GetBuildingsInteractor,
    GetOrganizationByIdInteractor,
    GetOrganizationsByActivityInteractor,
    GetOrganizationsByBuildingInteractor,
    GetOrganizationsInGeoAreaInteractor,
    SearchOrganizationsByNameInteractor,
)
from secunda.infra.config import AppSettings, PostgresSettings
from secunda.infra.database import new_session_maker
from secunda.infra.repositories import (
    ActivityRepository,
    BuildingRepository,
    OrganizationRepository,
)


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def get_postgres_settings(self) -> PostgresSettings:
        return PostgresSettings()

    @provide(scope=Scope.APP)
    def get_app_settings(self) -> AppSettings:
        return AppSettings()


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_session_maker(
        self, psql_config: PostgresSettings
    ) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(psql_config)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session


class RepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_building_repository(self, session: AsyncSession) -> BuildingRepositoryProtocol:
        return BuildingRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_activity_repository(self, session: AsyncSession) -> ActivityRepositoryProtocol:
        return ActivityRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_organization_repository(self, session: AsyncSession) -> OrganizationRepositoryProtocol:
        return OrganizationRepository(session)


class InteractorProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_buildings(self, repository: BuildingRepositoryProtocol) -> GetBuildingsInteractor:
        return GetBuildingsInteractor(repository)

    @provide(scope=Scope.REQUEST)
    def get_building_by_id(
        self, repository: BuildingRepositoryProtocol
    ) -> GetBuildingByIdInteractor:
        return GetBuildingByIdInteractor(repository)

    @provide(scope=Scope.REQUEST)
    def create_building(
        self, repository: BuildingRepositoryProtocol, session: AsyncSession
    ) -> CreateBuildingInteractor:
        return CreateBuildingInteractor(repository, session)

    @provide(scope=Scope.REQUEST)
    def get_activities(self, repository: ActivityRepositoryProtocol) -> GetActivitiesInteractor:
        return GetActivitiesInteractor(repository)

    @provide(scope=Scope.REQUEST)
    def get_activity_by_id(
        self, repository: ActivityRepositoryProtocol
    ) -> GetActivityByIdInteractor:
        return GetActivityByIdInteractor(repository)

    @provide(scope=Scope.REQUEST)
    def create_activity(
        self, repository: ActivityRepositoryProtocol, session: AsyncSession
    ) -> CreateActivityInteractor:
        return CreateActivityInteractor(repository, session)

    @provide(scope=Scope.REQUEST)
    def get_activity_with_children(
        self, repository: ActivityRepositoryProtocol
    ) -> GetActivityWithChildrenInteractor:
        return GetActivityWithChildrenInteractor(repository)

    @provide(scope=Scope.REQUEST)
    def get_organization_by_id(
        self, repository: OrganizationRepositoryProtocol
    ) -> GetOrganizationByIdInteractor:
        return GetOrganizationByIdInteractor(repository)

    @provide(scope=Scope.REQUEST)
    def get_organizations_by_building(
        self, repository: OrganizationRepositoryProtocol
    ) -> GetOrganizationsByBuildingInteractor:
        return GetOrganizationsByBuildingInteractor(repository)

    @provide(scope=Scope.REQUEST)
    def get_organizations_by_activity(
        self,
        organization_repo: OrganizationRepositoryProtocol,
        activity_repo: ActivityRepositoryProtocol,
    ) -> GetOrganizationsByActivityInteractor:
        return GetOrganizationsByActivityInteractor(organization_repo, activity_repo)

    @provide(scope=Scope.REQUEST)
    def get_organizations_in_geo_area(
        self, repository: OrganizationRepositoryProtocol
    ) -> GetOrganizationsInGeoAreaInteractor:
        return GetOrganizationsInGeoAreaInteractor(repository)

    @provide(scope=Scope.REQUEST)
    def search_organizations_by_name(
        self, repository: OrganizationRepositoryProtocol
    ) -> SearchOrganizationsByNameInteractor:
        return SearchOrganizationsByNameInteractor(repository)

    @provide(scope=Scope.REQUEST)
    def create_organization(
        self, repository: OrganizationRepositoryProtocol, session: AsyncSession
    ) -> CreateOrganizationInteractor:
        return CreateOrganizationInteractor(repository, session)
