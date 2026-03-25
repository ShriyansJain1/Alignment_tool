import { useEffect, useState } from "react";
import axios from "axios";

export default function ScenarioPanel() {

  const [scenarios, setScenarios] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/scenarios")
      .then(res => setScenarios(res.data));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h3>Saved Scenarios</h3>
      {scenarios.map(s => <div key={s}>{s}</div>)}
    </div>
  );
}