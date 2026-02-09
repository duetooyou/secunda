import math
from dataclasses import dataclass


@dataclass
class BoundingBox:
    min_lat: float
    max_lat: float
    min_lon: float
    max_lon: float


class GeoService:
    EARTH_RADIUS_KM = 6371.0
    DEGREES_PER_KM = 111.0

    @classmethod
    def calculate_bounding_box(cls, lat: float, lon: float, radius_km: float) -> BoundingBox:
        lat_delta = radius_km / cls.DEGREES_PER_KM
        lon_delta = radius_km / (cls.DEGREES_PER_KM * math.cos(math.radians(lat)))

        return BoundingBox(
            min_lat=lat - lat_delta,
            max_lat=lat + lat_delta,
            min_lon=lon - lon_delta,
            max_lon=lon + lon_delta,
        )

    @classmethod
    def haversine_distance(cls, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = (
            math.sin(delta_phi / 2) ** 2
            + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        )
        return 2 * cls.EARTH_RADIUS_KM * math.asin(math.sqrt(a))

    @classmethod
    def is_within_radius(cls, center_lat: float, center_lon: float, point_lat: float, point_lon: float, radius_km: float) -> bool:
        distance = cls.haversine_distance(center_lat, center_lon, point_lat, point_lon)
        return distance <= radius_km
