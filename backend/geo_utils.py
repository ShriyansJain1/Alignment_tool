import colorsys

def get_color(i):
    h = (i * 0.618033988749895) % 1
    r, g, b = colorsys.hsv_to_rgb(h, 0.6, 0.95)
    return f"rgb({int(r*255)},{int(g*255)},{int(b*255)})"


def generate_geojson(df, col):

    features = []

    for _, row in df.iterrows():

        terr = int(row[col])

        features.append({
            "type": "Feature",
            "properties": {
                "territory": terr,
                "color": get_color(terr)
            },
            "geometry": {
                "type": "Point",
                "coordinates": [row['lon'], row['lat']]
            }
        })

    return {
        "type": "FeatureCollection",
        "features": features
    }