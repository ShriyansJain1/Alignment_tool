import React, { useEffect, useRef } from "react";
import mapboxgl from "mapbox-gl";

mapboxgl.accessToken = "TBU";


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
        zoom: 3
      });

      mapRef.current.on("load", () => {

        mapRef.current.addSource("zips", {
          type: "geojson",
          data: geojson
        });

        mapRef.current.addLayer({
          id: "zip-points",
          type: "circle",
          source: "zips",
          paint: {
            "circle-radius": 5,
            "circle-color": ["get", "color"],
            "circle-opacity": 0.8
          }
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