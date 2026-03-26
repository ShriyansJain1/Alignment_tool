import axios from "axios";
import { useState } from "react";

export default function Sidebar({ setCurrent, setProposed, setMapping, setMeta }) {
  const apiBase = process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000";
  const [boundaryPath, setBoundaryPath] = useState("");

  const runRequest = async (baseUrl) => {
    const params = boundaryPath.trim() ? { boundary_path: boundaryPath.trim() } : undefined;
    const res = await axios.get(`${baseUrl}/run`, { params });
    setCurrent(res.data.current);
    setProposed(res.data.proposed);
    setMapping(res.data.mapping || { current: [], proposed: [] });
    setMeta(res.data.meta || null);
  };

  const handleRun = async () => {
    try {
      await runRequest(apiBase);
    } catch (err) {
      const isNetworkError = err?.message === "Network Error" && !err?.response;

      // Common local mismatch: backend listens on localhost while UI calls 127.0.0.1.
      if (isNetworkError && !process.env.REACT_APP_API_BASE_URL && apiBase.includes("127.0.0.1")) {
        try {
          await runRequest("http://localhost:8000");
          return;
        } catch (_) {
          // Fall through to user-facing guidance below.
        }
      }

      const detail = err?.response?.data?.detail || err.message;
      const hint = isNetworkError
        ? "\n\nCould not reach backend API. Start backend and/or set REACT_APP_API_BASE_URL in frontend/.env (example: http://localhost:8000)."
        : "";
      window.alert(`Failed to load ZIP boundary shapes:\n${detail}${hint}`);
    }
  };
  
  return (
    <div style={{ width: "20%", padding: "10px" }}>
      <h3>Controls</h3>
      <div style={{ marginBottom: "10px", fontSize: "12px", color: "#444" }}>
        ZIP boundary file/folder path (optional)
      </div>
      <input
        value={boundaryPath}
        onChange={(event) => setBoundaryPath(event.target.value)}
        placeholder="/path/to/zip_boundaries.geojson or .shp/.zip folder"
        style={{ width: "100%", marginBottom: "8px", padding: "6px", fontSize: "12px" }}
      />
      <button onClick={handleRun}>Run Alignment</button>
    </div>
  );
}
