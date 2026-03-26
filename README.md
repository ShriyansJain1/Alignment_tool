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

Set an environment variable that points to your ZIP boundary GeoJSON:

```bash
export ZIP_BOUNDARY_GEOJSON=/absolute/path/to/zip_boundaries.geojson
```

Then run the backend as usual. If `ZIP_BOUNDARY_GEOJSON` is missing, the app falls back to synthetic hex ZIP cells.

### Supported ZIP property names

The ZIP boundary loader recognizes these property names by default:

- `zip`
- `ZIP`
- `zcta`
- `ZCTA`
- `ZCTA5CE10`

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
