import React, { useEffect, useRef } from "react";
import mapboxgl from "mapbox-gl";

mapboxgl.accessToken = "TBU";

const US_BOUNDS = [
  [-125, 24],
  [-66, 50],
];

export default function MapView({ geojson }) {
  const mapContainer = useRef(null);
  const mapRef = useRef(null);

  useEffect(() => {
    if (!geojson) return;

    if (!mapRef.current) {
      mapRef.current = new mapboxgl.Map({
        container: mapContainer.current,
        style: "mapbox://styles/mapbox/light-v10",
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
            "fill-opacity": 0.78,
          },
        });

        mapRef.current.addLayer({
          id: "zip-outline",
          type: "line",
          source: "zips",
          paint: {
            "line-color": "#ffffff",
            "line-width": 0.2,
            "line-opacity": 0.22,
          },
        });
      });
    } else {
      const source = mapRef.current.getSource("zips");
      if (source) {
        source.setData(geojson);
      }
    }
  }, [geojson]);

  return <div ref={mapContainer} style={{ height: "600px" }} />;
}
