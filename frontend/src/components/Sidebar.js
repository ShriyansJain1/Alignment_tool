import axios from "axios";

export default function Sidebar({ setCurrent, setProposed }) {

  const run = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/run");
      setCurrent(res.data.current);
      setProposed(res.data.proposed);
    } catch (err) {
      const detail = err?.response?.data?.detail || err.message;
      window.alert(`Failed to load ZIP boundary shapes:\n${detail}`);
    }
  };

  return (
    <div style={{ width: "20%", padding: "10px" }}>
      <h3>Controls</h3>
      <button onClick={run}>Run Alignment</button>
    </div>
  );
}
