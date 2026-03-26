import React, { useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";

const US_BOUNDS = [
  [-125, 24],
  [-66, 50],
];

const MAPTILER_KEY = process.env.REACT_APP_MAPTILER_KEY;

const baseStyle = MAPTILER_KEY
  ? `https://api.maptiler.com/maps/streets-v2/style.json?key=${MAPTILER_KEY}`
  : {
      version: 8,
      sources: {
        osm: {
          type: "raster",
          tiles: [
            "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png",
            "https://b.tile.openstreetmap.org/{z}/{x}/{y}.png",
            "https://c.tile.openstreetmap.org/{z}/{x}/{y}.png",
          ],
          tileSize: 256,
          attribution:
            '© OpenStreetMap contributors <a href="https://www.openstreetmap.org/copyright">ODbL</a>',
        },
      },
      layers: [
        {
          id: "osm",
          type: "raster",
          source: "osm",
        },
      ],
    };

export default function MapView({ geojson }) {
  const mapContainer = useRef(null);
  const mapRef = useRef(null);
  const popupRef = useRef(null);

  useEffect(() => {
    if (!geojson) return;

    if (!mapRef.current) {
      mapRef.current = new maplibregl.Map({
        container: mapContainer.current,
        style: baseStyle,
        center: [-98, 38],
        zoom: 3,
        renderWorldCopies: false,
        minZoom: 2,
      });

      mapRef.current.on("load", () => {
        mapRef.current.fitBounds(US_BOUNDS, { padding: 8, duration: 0 });

        mapRef.current.addSource("zips", {
          type: "geojson",
          data: geojson,
        });

        mapRef.current.addLayer({
          id: "zip-fill",
          type: "fill",
          source: "zips",
          paint: {
            "fill-color": ["get", "color"],
            "fill-opacity": 0.56,
          },
        });

        mapRef.current.addLayer({
          id: "zip-outline",
          type: "line",
          source: "zips",
          paint: {
            "line-color": "rgba(255,255,255,0.85)",
            "line-width": 0.45,
            "line-opacity": 0.5,
          },
        });

        mapRef.current.on("click", "zip-fill", (event) => {
          const feature = event.features?.[0];
          const props = feature?.properties || {};
          const content = [
            `<b>ZIP:</b> ${props.zip || "-"}`,
            `<b>Territory:</b> ${props.territory ?? "-"}`,
            `<b>Shape ID:</b> ${props.shape_id || props.zip || "-"}`,
          ].join("<br/>");

          if (!popupRef.current) {
            popupRef.current = new maplibregl.Popup({ closeButton: true, closeOnClick: true });
          }
          popupRef.current.setLngLat(event.lngLat).setHTML(content).addTo(mapRef.current);
        });

        mapRef.current.on("mouseenter", "zip-fill", () => {
          mapRef.current.getCanvas().style.cursor = "pointer";
        });

        mapRef.current.on("mouseleave", "zip-fill", () => {
          mapRef.current.getCanvas().style.cursor = "";
        });
      });
    } else {
      const source = mapRef.current.getSource("zips");
      if (source) {
        source.setData(geojson);
      }
    }
  }, [geojson]);

  return <div ref={mapContainer} style={{ height: "600px", borderRadius: "10px" }} />;
}
