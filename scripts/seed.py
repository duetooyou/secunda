import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from secunda.infra.config import PostgresSettings
from secunda.infra.database.models import ActivityModel, BuildingModel, OrganizationModel


async def seed_data(session: AsyncSession) -> None:
    await session.execute(text("TRUNCATE TABLE organization_activity, organizations, activities, buildings RESTART IDENTITY CASCADE"))

    buildings = [
        BuildingModel(address="г. Москва, ул. Ленина 1, офис 3", latitude=55.7558, longitude=37.6173),
        BuildingModel(address="г. Москва, ул. Блюхера 32/1", latitude=55.7600, longitude=37.6200),
        BuildingModel(address="г. Москва, пр. Мира 15", latitude=55.7700, longitude=37.6300),
        BuildingModel(address="г. Санкт-Петербург, Невский пр. 100", latitude=59.9343, longitude=30.3351),
        BuildingModel(address="г. Санкт-Петербург, ул. Садовая 50", latitude=59.9300, longitude=30.3200),
    ]
    session.add_all(buildings)
    await session.flush()

    food = ActivityModel(name="Еда", level=1)
    session.add(food)
    await session.flush()

    meat = ActivityModel(name="Мясная продукция", parent_id=food.id, level=2)
    dairy = ActivityModel(name="Молочная продукция", parent_id=food.id, level=2)
    session.add_all([meat, dairy])
    await session.flush()

    beef = ActivityModel(name="Говядина", parent_id=meat.id, level=3)
    pork = ActivityModel(name="Свинина", parent_id=meat.id, level=3)
    milk = ActivityModel(name="Молоко", parent_id=dairy.id, level=3)
    cheese = ActivityModel(name="Сыры", parent_id=dairy.id, level=3)
    session.add_all([beef, pork, milk, cheese])
    await session.flush()

    auto = ActivityModel(name="Автомобили", level=1)
    session.add(auto)
    await session.flush()

    trucks = ActivityModel(name="Грузовые", parent_id=auto.id, level=2)
    cars = ActivityModel(name="Легковые", parent_id=auto.id, level=2)
    parts = ActivityModel(name="Запчасти", parent_id=auto.id, level=2)
    session.add_all([trucks, cars, parts])
    await session.flush()

    accessories = ActivityModel(name="Аксессуары", parent_id=parts.id, level=3)
    session.add(accessories)
    await session.flush()

    org1 = OrganizationModel(
        name='ООО "Рога и Копыта"',
        phones=["2-222-222", "3-333-333", "8-923-666-13-13"],
        building_id=buildings[0].id,
    )
    org1.activities = [meat, dairy]

    org2 = OrganizationModel(
        name='ООО "МясоТорг"',
        phones=["8-800-555-35-35"],
        building_id=buildings[1].id,
    )
    org2.activities = [beef, pork]

    org3 = OrganizationModel(
        name='ООО "Молочный Рай"',
        phones=["8-495-123-45-67", "8-495-123-45-68"],
        building_id=buildings[0].id,
    )
    org3.activities = [milk, cheese]

    org4 = OrganizationModel(
        name='ООО "АвтоМир"',
        phones=["8-812-999-88-77"],
        building_id=buildings[2].id,
    )
    org4.activities = [cars, trucks]

    org5 = OrganizationModel(
        name='ООО "Запчасти Плюс"',
        phones=["8-812-111-22-33"],
        building_id=buildings[3].id,
    )
    org5.activities = [parts, accessories]

    org6 = OrganizationModel(
        name='ИП Иванов "Продукты"',
        phones=["8-999-888-77-66"],
        building_id=buildings[4].id,
    )
    org6.activities = [food]

    org7 = OrganizationModel(
        name='ООО "ГрузАвто"',
        phones=["8-800-100-20-30"],
        building_id=buildings[2].id,
    )
    org7.activities = [trucks]

    session.add_all([org1, org2, org3, org4, org5, org6, org7])
    await session.commit()

    print("Seed data inserted successfully!")
    print(f"Buildings: {len(buildings)}")
    print("Activities: 12 (3 levels)")
    print("Organizations: 7")


async def main() -> None:
    settings = PostgresSettings()
    engine = create_async_engine(settings.async_url())
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_maker() as session:
        await seed_data(session)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
