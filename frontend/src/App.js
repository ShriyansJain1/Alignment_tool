import React, { useState } from "react";
import Sidebar from "./components/Sidebar";
import MapView from "./components/MapView";

function App() {
  const [current, setCurrent] = useState(null);
  const [proposed, setProposed] = useState(null);
  const [mapping, setMapping] = useState({ current: [], proposed: [] });

  return (
    <div style={{ display: "flex" }}>
      <Sidebar setCurrent={setCurrent} setProposed={setProposed} setMapping={setMapping} />

      <div style={{ width: "80%" }}>
        <div style={{ display: "flex" }}>
          <div style={{ width: "50%" }}>
            <h3>Current Alignment (State-wise)</h3>
            <MapView geojson={current} />
          </div>

          <div style={{ width: "50%" }}>
            <h3>Proposed Alignment (ME→VT, WA→OR)</h3>
            <MapView geojson={proposed} />
          </div>
        </div>

        <div style={{ padding: "10px 16px" }}>
          <h3>Territory → ZIP → Shape ID (Current)</h3>
          <div style={{ maxHeight: "220px", overflow: "auto", border: "1px solid #ddd" }}>
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "13px" }}>
              <thead>
                <tr>
                  <th style={{ textAlign: "left", padding: "6px", borderBottom: "1px solid #ddd" }}>Territory</th>
                  <th style={{ textAlign: "left", padding: "6px", borderBottom: "1px solid #ddd" }}>ZIP</th>
                  <th style={{ textAlign: "left", padding: "6px", borderBottom: "1px solid #ddd" }}>Shape ID</th>
                </tr>
              </thead>
              <tbody>
                {mapping.current.slice(0, 400).map((row) => (
                  <tr key={`${row.territory}-${row.zip}`}>
                    <td style={{ padding: "6px", borderBottom: "1px solid #f0f0f0" }}>{row.territory}</td>
                    <td style={{ padding: "6px", borderBottom: "1px solid #f0f0f0" }}>{row.zip}</td>
                    <td style={{ padding: "6px", borderBottom: "1px solid #f0f0f0" }}>{row.shape_id}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
