from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np

from geo_utils import generate_geojson

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATE_BBOX = {
    "AL": (30.1, 35.1, -88.5, -84.8),
    "AZ": (31.3, 37.0, -114.9, -109.0),
    "AR": (33.0, 36.5, -94.7, -89.6),
    "CA": (32.5, 42.0, -124.4, -114.1),
    "CO": (37.0, 41.0, -109.1, -102.0),
    "CT": (41.0, 42.1, -73.8, -71.8),
    "DE": (38.4, 39.9, -75.8, -75.0),
    "FL": (24.5, 31.0, -87.7, -80.0),
    "GA": (30.3, 35.1, -85.7, -80.8),
    "ID": (42.0, 49.0, -117.3, -111.0),
    "IL": (36.9, 42.5, -91.6, -87.0),
    "IN": (37.8, 41.8, -88.1, -84.8),
    "IA": (40.3, 43.6, -96.7, -90.1),
    "KS": (37.0, 40.0, -102.1, -94.6),
    "KY": (36.5, 39.3, -89.6, -81.9),
    "LA": (29.0, 33.1, -94.1, -88.8),
    "ME": (43.0, 47.5, -71.1, -66.9),
    "MD": (37.9, 39.8, -79.6, -75.0),
    "MA": (41.2, 42.9, -73.6, -69.9),
    "MI": (41.7, 48.3, -90.5, -82.3),
    "MN": (43.5, 49.4, -97.3, -89.5),
    "MS": (30.1, 35.0, -91.7, -88.1),
    "MO": (36.0, 40.7, -95.8, -89.1),
    "MT": (44.3, 49.0, -116.1, -104.0),
    "NE": (40.0, 43.0, -104.1, -95.3),
    "NV": (35.0, 42.0, -120.0, -114.0),
    "NH": (42.6, 45.3, -72.7, -70.6),
    "NJ": (38.9, 41.4, -75.6, -73.9),
    "NM": (31.3, 37.0, -109.1, -103.0),
    "NY": (40.5, 45.1, -79.8, -71.8),
    "NC": (33.8, 36.6, -84.4, -75.4),
    "ND": (45.9, 49.0, -104.1, -96.5),
    "OH": (38.4, 42.3, -84.9, -80.5),
    "OK": (33.6, 37.0, -103.0, -94.4),
    "OR": (42.0, 46.3, -124.6, -116.5),
    "PA": (39.7, 42.4, -80.6, -74.7),
    "RI": (41.1, 42.1, -71.9, -71.1),
    "SC": (32.0, 35.2, -83.4, -78.5),
    "SD": (42.5, 45.9, -104.1, -96.4),
    "TN": (35.0, 36.7, -90.4, -81.5),
    "TX": (25.8, 36.5, -106.7, -93.5),
    "UT": (37.0, 42.0, -114.1, -109.0),
    "VT": (42.7, 45.1, -73.5, -71.4),
    "VA": (36.5, 39.5, -83.7, -75.2),
    "WA": (45.5, 49.0, -124.9, -116.8),
    "WV": (37.2, 40.7, -82.7, -77.7),
    "WI": (42.4, 47.3, -92.9, -86.8),
    "WY": (41.0, 45.0, -111.1, -104.0),
}


def closest_state(lat, lon):
    for state, (min_lat, max_lat, min_lon, max_lon) in STATE_BBOX.items():
        if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
            return state

    def center_distance(item):
        _, (min_lat, max_lat, min_lon, max_lon) = item
        c_lat = (min_lat + max_lat) / 2
        c_lon = (min_lon + max_lon) / 2
        return (lat - c_lat) ** 2 + (lon - c_lon) ** 2

    return min(STATE_BBOX.items(), key=center_distance)[0]


def generate_us_grid():
    data = []
    zip_id = 0

    lat_range = np.arange(25, 49, 0.7)
    lon_range = np.arange(-124, -67, 0.7)

    for lat in lat_range:
        for lon in lon_range:
            state = closest_state(lat, lon)
            data.append(
                {
                    "zip": f"Z{zip_id}",
                    "lat": round(float(lat), 4),
                    "lon": round(float(lon), 4),
                    "state": state,
                    "workload": int(np.random.randint(10, 100)),
                }
            )
            zip_id += 1

    return pd.DataFrame(data)


def apply_proposed_merges(df):
    # User requested merge "ME, VE and WA + OR"; interpret VE as VT.
    state_to_group = {state: state for state in STATE_BBOX.keys()}
    state_to_group["ME"] = "VT"
    state_to_group["WA"] = "OR"

    df["proposed_state"] = df["state"].map(state_to_group)
    return df


@app.get("/run")
def run():
    df = generate_us_grid()

    current_states = sorted(df["state"].unique())
    current_id_map = {state: idx for idx, state in enumerate(current_states)}
    df["current_territory"] = df["state"].map(current_id_map)

    df = apply_proposed_merges(df)
    proposed_states = sorted(df["proposed_state"].unique())
    proposed_id_map = {state: idx for idx, state in enumerate(proposed_states)}
    df["proposed_territory"] = df["proposed_state"].map(proposed_id_map)

    return {
        "current": generate_geojson(df, "current_territory"),
        "proposed": generate_geojson(df, "proposed_territory"),
    }
