import colorsys
import math
from copy import deepcopy


TABLEAU_20 = [
    "#4e79a7",
    "#f28e2b",
    "#e15759",
    "#76b7b2",
    "#59a14f",
    "#edc948",
    "#b07aa1",
    "#ff9da7",
    "#9c755f",
    "#bab0ab",
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
]


def hex_to_rgb(color):
    color = color.lstrip("#")
    return tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))


def get_color(i):
    """Return a muted but distinguishable color for territory ids.

    We start from a human-friendly categorical palette and then slightly vary
    lightness for each wrap-around cycle, which keeps neighboring regions from
    becoming neon-saturated while still staying separable.
    """
    base = TABLEAU_20[i % len(TABLEAU_20)]
    cycle = i // len(TABLEAU_20)

    r, g, b = [c / 255 for c in hex_to_rgb(base)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    l = max(0.35, min(0.78, l + (cycle * 0.06)))
    s = max(0.35, min(0.65, s - (cycle * 0.04)))
    r2, g2, b2 = colorsys.hls_to_rgb(h, l, s)

    return f"rgb({int(r2*255)},{int(g2*255)},{int(b2*255)})"


def zip_like_polygon(lat, lon, step=0.7):
    """Return a compact hexagon around a ZIP centroid.

    Hex cells read much closer to area polygons than square grid cells,
    while still being deterministic and lightweight.
    """
    radius = step * 0.43
    vertices = []

    for angle in range(0, 360, 60):
        rad = math.radians(angle)
        x = lon + radius * math.cos(rad)
        y = lat + radius * math.sin(rad)
        vertices.append([x, y])

    vertices.append(vertices[0])
    return vertices


def generate_geojson(df, col):
    features = []

    for _, row in df.iterrows():
        terr = int(row[col])

        features.append(
            {
                "type": "Feature",
                "properties": {
                    "zip": row["zip"],
                    "state": row["state"],
                    "territory": terr,
                    "color": get_color(terr),
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [zip_like_polygon(row["lat"], row["lon"])],
                },
            }
        )

    return {"type": "FeatureCollection", "features": features}


def index_boundaries_by_zip(boundary_geojson, zip_property_candidates=None):
    """Build a zip -> geometry index from a ZIP boundary GeoJSON object.

    The helper supports common ZIP property names used by Census/3rd-party data.
    """
    if not boundary_geojson:
        return {}

    if zip_property_candidates is None:
        zip_property_candidates = [
            "zip",
            "ZIP",
            "zcta",
            "ZCTA",
            "GEOID",
            "GEOID10",
            "GEOID20",
            "ZCTA5CE10",
            "ZCTA5CE20",
            "ZCTA5CE",
            "ZCTA5CE21",
        ]

    features = boundary_geojson.get("features", [])
    geometry_by_zip = {}

    for feature in features:
        props = feature.get("properties", {})
        zip_code = None

        for key in zip_property_candidates:
            value = props.get(key)
            if value is None:
                continue
            value_text = str(value).strip()
            if not value_text:
                continue
            # Typical shapefile DBF values can be numeric-looking (e.g. 98052.0).
            if value_text.endswith(".0"):
                value_text = value_text[:-2]
            zip_code = value_text.zfill(5)
            break

        if not zip_code:
            continue

        geometry = feature.get("geometry")
        if geometry:
            geometry_by_zip[zip_code] = deepcopy(geometry)

    return geometry_by_zip


def generate_geojson_with_boundaries(df, col, geometry_by_zip):
    """Generate ZIP-level choropleth features by coloring existing boundaries.

    This follows the recommended pipeline:
    ZIP boundaries + ZIP->territory mapping -> colored ZIP polygons.
    """
    features = []

    for _, row in df.iterrows():
        zip_code = str(row["zip"]).zfill(5)
        geometry = geometry_by_zip.get(zip_code)

        if not geometry:
            continue

        terr = int(row[col])
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "zip": zip_code,
                    "state": row["state"],
                    "territory": terr,
                    "color": get_color(terr),
                },
                "geometry": geometry,
            }
        )

    return {"type": "FeatureCollection", "features": features}
