# Alignment Tool

## ZIP-first territory coloring (recommended pipeline)

You can now run the backend in a **ZIP-first choropleth mode** (no territory dissolve step).

### Why this mode

Instead of building synthetic territory polygons, the backend can color each ZIP boundary directly:

1. Start with ZIP boundary GeoJSON.
2. Join ZIP -> territory mapping.
3. Render ZIP polygons with territory color.

This keeps real geography, preserves ZIP-level granularity, and makes scattered territory assignments obvious.

### Configure

You can provide ZIP boundaries in either format:

1) **GeoJSON** (already converted):

```bash
export ZIP_BOUNDARY_GEOJSON=/absolute/path/to/zip_boundaries.geojson
```

2) **Shapefile** (`.shp` + `.dbf` + `.shx` + `.prj` + `.cpg` together):

```bash
export ZIP_BOUNDARY_SHP=/absolute/path/to/tl_2020_us_zcta520.shp
```

PowerShell example (Windows):

```powershell
$env:ZIP_BOUNDARY_SHP="C:\Users\ShriyansJain\Downloads\tl_2020_us_zcta520.shp"
```

The backend accepts this Windows-style path format directly. If you run backend in WSL/Linux, ensure the file is reachable there (for example `/mnt/c/Users/...`).

You can also point `ZIP_BOUNDARY_SHP` to a **folder** that contains shapefiles; the backend will auto-pick a `.shp` file (prefers names containing `zcta`).

3) **Zipped shapefile** (`.zip` that contains `.shp/.dbf/.shx`):

```bash
export ZIP_BOUNDARY_SHP_ZIP=/absolute/path/to/tl_2020_us_zcta520.zip
```

The backend now auto-extracts this archive and will use either:
- a `.geojson` inside the zip (if present), or
- the first `.shp` set (prefers filenames containing `zcta`).

4) **Directory input** (explicit folder variable):

```bash
export ZIP_BOUNDARY_DIR=/absolute/path/to/downloads/extracted_folder
```

Then run the backend as usual. If neither `ZIP_BOUNDARY_GEOJSON` nor `ZIP_BOUNDARY_SHP` is set, the app falls back to synthetic hex ZIP cells.
If any boundary env var is set but loading fails, `/run` now returns an explicit error instead of silently falling back, so issues are visible immediately.

When either variable is set, `/run` builds rows from your ZIP boundary features so the map renders **exact ZIP polygons** (instead of synthetic hexes).

### Supported ZIP property names

The ZIP boundary loader recognizes these property names by default:

- `zip`
- `ZIP`
- `zcta`
- `ZCTA`
- `ZCTA5CE10`
- `ZCTA5CE20`
- `GEOID20`

Use 5-digit ZIP codes in your mapping data so joins are consistent (`00501`, `10001`, etc.).

### Example with your downloaded Census files

If your folder has files like:

- `tl_2020_us_zcta520.shp`
- `tl_2020_us_zcta520.dbf`
- `tl_2020_us_zcta520.shx`

set:

```bash
export ZIP_BOUNDARY_SHP=/path/to/tl_2020_us_zcta520.shp
```

and start backend/frontend; the map will use those exact ZCTA geometries.

### Troubleshooting (if you still see hexagons)

If `/run` cannot build a ZIP->polygon index, the backend falls back to synthetic hexes.
Check the `/run` response `meta` object:

- `meta.source` should be `zip_boundary_polygons`
- `meta.joined_polygon_count` should be greater than `0`

If not, verify:

- your env var points to an existing file
- if you use a folder, it must contain at least one `.shp` (with matching `.dbf/.shx`)
- DBF has a ZIP field (supported examples: `ZCTA5CE10`, `ZCTA5CE20`, `GEOID10`, `GEOID20`)
- ZIP codes are 5-digit strings in your assignment data

### Conceptual join

The core idea in code is:

```python
zip_geo["territory"] = zip_geo["zip"].map(mapping_dict)
```

Then color by the territory field.

## Frontend map provider

The frontend now uses **MapLibre GL**.

- If you provide a `REACT_APP_MAPTILER_KEY`, the app loads a **vector tile** basemap from MapTiler.
- If you do not provide a key, the app falls back to OpenStreetMap raster tiles.

### Where to put the token

Create this file:

```bash
frontend/.env
```

Then add:

```bash
REACT_APP_MAPTILER_KEY=your_maptiler_key_here
```

Restart the frontend after changing `.env`.

## Backend connectivity (fixes `Network Error` in UI)

If the UI shows `Failed to load ZIP boundary shapes: Network Error`, it means the frontend cannot reach the backend API.

Start backend:

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Or, from `backend/`, run directly:

```bash
python main.py
```

Optionally set API URL explicitly for frontend:

```bash
# frontend/.env
REACT_APP_API_BASE_URL=http://localhost:8000
```

## Backend dependency note (`ModuleNotFoundError: No module named 'shapefile'`)

Shapefile loading requires **pyshp** (import name: `shapefile`).

Install backend dependencies before starting:

```bash
pip install -r requirements.txt
```
