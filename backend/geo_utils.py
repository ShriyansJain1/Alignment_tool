import colorsys
import math


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
