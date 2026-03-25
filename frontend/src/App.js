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
            <h3>Current (90 Territories)</h3>
            <MapView geojson={current} />
          </div>

          <div style={{ width: "50%" }}>
            <h3>Proposed (100 Territories)</h3>
            <MapView geojson={proposed} />
          </div>

        </div>
      </div>
    </div>
  );
}

export default App;