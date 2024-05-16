from shapely.geometry import Point, Polygon, MultiPolygon
def get_position_of_geom(geom, r=max, latitude=True):
    """
    Find the position (either min or max) of a geometry by latitude or longitude.

    Args:
        geom: A shapely geometry object (Polygon, MultiPolygon, or Point).
        r: A function to apply (min or max).
        latitude: If True, find the point by latitude; otherwise, by longitude.

    Returns:
        A tuple representing the coordinates of the desired position.
    """
    def coord_extractor(coord):
        return coord[1] if latitude else coord[0]

    if isinstance(geom, Point):
        return (geom.x, geom.y)
    elif isinstance(geom, Polygon):
        coords = list(geom.exterior.coords)
    elif isinstance(geom, MultiPolygon):
        coords = [coord for polygon in geom.geoms for coord in polygon.exterior.coords]
    else:
        raise ValueError("Unsupported geometry type.")

    # Extract the desired coordinate based on latitude or longitude
    desired_coord = r(coords, key=coord_extractor)
    return desired_coord

def get_extremity(geom_a, geom_b, latitude=True):
    """
    Determine which of two geometries has the most extreme point (north/south or east/west).

    Args:
        geom_a: A shapely geometry object.
        geom_b: Another shapely geometry object.
        latitude: If True, compares by latitude (north/south); otherwise, by longitude (east/west).

    Returns:
        A dictionary containing the geometries and their extreme points.
    """
    comparison_key = 1 if latitude else 0

    # Choose comparison function based on direction
    r = max if latitude else min

    max_a = get_position_of_geom(geom_a, r=r, latitude=latitude)
    max_b = get_position_of_geom(geom_b, r=r, latitude=latitude)

    is_a_more_extreme = max_a[comparison_key] > max_b[comparison_key] if latitude else max_a[comparison_key] < max_b[comparison_key]
    return {
        "max": {
            "geom": 'a' if is_a_more_extreme else 'b',
            "geometry": geom_a if is_a_more_extreme else geom_b,
            "coordinates": max_a if is_a_more_extreme else max_b,
            'direction': latitude
        },
        "min": {
            "geom": 'b' if is_a_more_extreme else 'a',
            "geometry": geom_b if is_a_more_extreme else geom_a,
            "coordinates": max_b if is_a_more_extreme else max_a,
            'direction': latitude
        }
    }

def get_auto_most(geom_a, geom_b, latitude='north'):
    """
    Determine the most extreme geometry based on cardinal direction.

    Args:
        geom_a: A shapely geometry object.
        geom_b: Another shapely geometry object.
        latitude: One of 'north', 'south', 'east', 'west'.

    Returns:
        A dictionary containing the geometries and their extreme points.
    """
    latitude_lower = str(latitude).lower()
    if latitude_lower in ['south', 'west']:
        r = min
    else:
        r = max

    latitude = latitude_lower in ['north', 'south']
    return get_extremity(geom_a, geom_b, latitude=latitude)

def get_range(geom_a, geom_b, latitude='north', rangeInclusiveA=False, rangeInclusiveB=False):
    """
    Determine the range between two geometries based on the specified direction.

    Args:
        geom_a: A shapely geometry object.
        geom_b: Another shapely geometry object.
        latitude: One of 'north', 'south', 'east', 'west'.
        rangeInclusiveA: Boolean specifying whether the first geometry should include its extremity.
        rangeInclusiveB: Boolean specifying whether the second geometry should include its extremity.

    Returns:
        A dictionary containing the directional range limits and their corresponding coordinates.
    """
    reference_js = {"a": {"geom": geom_a, "inclusive": rangeInclusiveA}, "b": {"geom": geom_b, "inclusive": rangeInclusiveB}}
    auto_js = get_auto_most(geom_a, geom_b, latitude=latitude)

    # Determine the reference functions (min or max) based on inclusivity
    r_a = max if reference_js[auto_js['max']['geom']]["inclusive"] else min
    r_b = min if reference_js[auto_js['min']['geom']]["inclusive"] else max

    return {
        "latitude": [auto_js['min']['direction'], auto_js['max']['direction']],
        "range": [
            get_position_of_geom(reference_js[auto_js['min']['geom']]["geom"], r=r_b, latitude=auto_js['min']['direction']),
            get_position_of_geom(reference_js[auto_js['max']['geom']]["geom"], r=r_a, latitude=auto_js['max']['direction'])
        ]
    }

# Function to check if a geometry's latitude lies within specified bounds, supporting both Polygon and MultiPolygon
def is_within_bounds(geometry, lower_bound, upper_bound):
    def extract_latitudes(polygon):
        """Extract latitudes from a polygon's exterior coordinates."""
        return [coord[1] for coord in polygon.exterior.coords]

    latitudes = []
    if isinstance(geometry, Polygon):
        latitudes = extract_latitudes(geometry)
    elif isinstance(geometry, MultiPolygon):
        for polygon in geometry.geoms:
            latitudes.extend(extract_latitudes(polygon))
    else:
        raise TypeError("Unsupported geometry type")

    # Check if any latitude falls within the specified bounds
    return any(lower_bound <= lat <= upper_bound for lat in latitudes)
