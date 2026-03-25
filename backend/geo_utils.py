import colorsys


def get_color(i):
    h = (i * 0.618033988749895) % 1
    r, g, b = colorsys.hsv_to_rgb(h, 0.6, 0.95)
    return f"rgb({int(r*255)},{int(g*255)},{int(b*255)})"


def square_polygon(lat, lon, step=0.7):
    half = step / 2
    return [
        [lon - half, lat - half],
        [lon + half, lat - half],
        [lon + half, lat + half],
        [lon - half, lat + half],
        [lon - half, lat - half],
    ]


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
                    "coordinates": [square_polygon(row["lat"], row["lon"])],
                },
            }
        )

    return {"type": "FeatureCollection", "features": features}
