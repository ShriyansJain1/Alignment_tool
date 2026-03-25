import axios from "axios";

export default function Sidebar({ setCurrent, setProposed }) {

  const run = async () => {
    const res = await axios.get("http://127.0.0.1:8000/run");

    setCurrent(res.data.current);
    setProposed(res.data.proposed);
  };

  return (
    <div style={{ width: "20%", padding: "10px" }}>
      <h3>Controls</h3>
      <button onClick={run}>Run Alignment</button>
    </div>
  );
}