# Alignment Tool

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
