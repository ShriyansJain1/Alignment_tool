import colorsys
import math


def get_color(i):
    h = (i * 0.618033988749895) % 1
    r, g, b = colorsys.hsv_to_rgb(h, 0.6, 0.95)
    return f"rgb({int(r*255)},{int(g*255)},{int(b*255)})"


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
