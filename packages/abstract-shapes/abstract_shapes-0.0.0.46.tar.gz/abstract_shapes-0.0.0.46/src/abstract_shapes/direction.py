from shapely.geometry import Point, Polygon, MultiPolygon

def coord_extractor(coord, latitude=True):
    return coord[1] if latitude else coord[0]

def get_position_of_geom(geom, r=max, latitude=True):
    if isinstance(geom, Point):
        return (geom.x, geom.y)
    elif isinstance(geom, Polygon):
        coords = list(geom.exterior.coords)
    elif isinstance(geom, MultiPolygon):
        coords = [coord for polygon in geom.geoms for coord in polygon.exterior.coords]
    else:
        raise ValueError("Unsupported geometry type.")
    
    desired_coord = r(coords, key=lambda c: coord_extractor(c, latitude))
    return desired_coord

def get_extremity(geom_a, geom_b, latitude=True):
    comparison_key = 1 if latitude else 0
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
    latitude_lower = str(latitude).lower()
    r = min if latitude_lower in ['south', 'west'] else max
    latitude = latitude_lower in ['north', 'south']
    return get_extremity(geom_a, geom_b, latitude=latitude)

def get_geom_range(geom_a, geom_b, latitude='north', rangeInclusiveA=False, rangeInclusiveB=False, strictA=False, strictB=False):
    reference_js = {"a": {"geom": geom_a, "inclusive": rangeInclusiveA, "strict": strictA}, "b": {"geom": geom_b, "inclusive": rangeInclusiveB, "strict": strictB}}
    auto_js = get_auto_most(geom_a, geom_b, latitude=latitude)
    
    r_a = max if bool(reference_js[auto_js['max']['geom']]["inclusive"]) else min
    r_b = min if bool(reference_js[auto_js['min']['geom']]["inclusive"]) else max

    return {
        "latitude": [auto_js['min']['direction'], auto_js['max']['direction']],
        "strict": [bool(reference_js[auto_js['min']['geom']]['strict']), bool(reference_js[auto_js['max']['geom']]['strict'])],
        "range": [
            get_position_of_geom(reference_js[auto_js['min']['geom']]["geom"], r=r_b, latitude=auto_js['min']['direction']),
            get_position_of_geom(reference_js[auto_js['max']['geom']]["geom"], r=r_a, latitude=auto_js['max']['direction'])
        ]
    }

def is_geom_within_bounds(geometry, geom_range):
    def extract_latitudes(polygon, latitude):
        return [coord_extractor(coord, latitude=latitude) for coord in polygon.exterior.coords]
    
    lower_bound = coord_extractor(geom_range["range"][0], geom_range["latitude"][0])
    upper_bound = coord_extractor(geom_range["range"][1], geom_range["latitude"][1])

    latitudes = []
    for i, latitude in enumerate(geom_range["latitude"]):
        latitudes.append([])
        if isinstance(geometry, Polygon):
            latitudes[-1] = extract_latitudes(geometry, latitude)
        elif isinstance(geometry, MultiPolygon):
            for polygon in geometry.geoms:
                latitudes[-1].extend(extract_latitudes(polygon, latitude))
        else:
            raise TypeError("Unsupported geometry type")
        
        
    if geom_range["strict"][0] and geom_range["strict"][1]:
        if latitudes[0] == latitudes[1]:
            if any((lower_bound > lat or upper_bound < lat) for lat in latitudes[0]):
                return False
            return any(lower_bound <= lat <= upper_bound for lat in latitudes[0])
        else:
            if any(lower_bound > lat for lat in latitudes[0]) or any(upper_bound < lat for lat in latitudes[1]):
                return False
            return any(lower_bound <= lat <= upper_bound for lat in latitudes[0])
    elif geom_range["strict"][0] and not geom_range["strict"][1]:
        if any(lower_bound > lat for lat in latitudes[0]):
            return False
        return any(lower_bound <= lat <= upper_bound for lat in latitudes[0])
    elif geom_range["strict"][1] and not geom_range["strict"][0]:
        if any(upper_bound < lat for lat in latitudes[1]):
            return False
        return any(lower_bound <= lat <= upper_bound for lat in latitudes[0])
    else:
        if latitudes[0] == latitudes[1]:
            return any(lower_bound <= lat <= upper_bound for lat in latitudes[0])
        else:
            return any(lower_bound <= lat for lat in latitudes[0]) and any(lat <= upper_bound for lat in latitudes[1])
    return True
