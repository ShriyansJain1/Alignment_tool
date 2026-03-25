import React, { useState } from "react";
import Sidebar from "./components/Sidebar";
import MapView from "./components/MapView";

function App() {
  const [current, setCurrent] = useState(null);
  const [proposed, setProposed] = useState(null);

  return (
    <div style={{ display: "flex" }}>
      <Sidebar setCurrent={setCurrent} setProposed={setProposed} />

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
      </div>
    </div>
  );
}

export default App;
