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

Then run the backend as usual. If neither `ZIP_BOUNDARY_GEOJSON` nor `ZIP_BOUNDARY_SHP` is set, the app falls back to synthetic hex ZIP cells.

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
