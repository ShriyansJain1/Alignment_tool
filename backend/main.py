from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np

from alignment_engine import optimize
from geo_utils import generate_geojson

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def generate_us_grid():

    data = []
    zip_id = 0

    lat_range = np.arange(25, 49, 1.5)
    lon_range = np.arange(-124, -67, 1.5)

    for lat in lat_range:
        for lon in lon_range:
            data.append({
                "zip": f"Z{zip_id}",
                "lat": lat,
                "lon": lon,
                "workload": np.random.randint(10, 100)
            })
            zip_id += 1

    df = pd.DataFrame(data)

    df['territory'] = np.random.randint(0, 90, len(df))

    return df


@app.get("/run")
def run():

    df = generate_us_grid()

    df['current_territory'] = df['territory']

    assign = optimize(df, 100)
    df['proposed_territory'] = df['zip'].map(assign)

    return {
        "current": generate_geojson(df, "current_territory"),
        "proposed": generate_geojson(df, "proposed_territory")
    }