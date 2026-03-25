export default function SummaryPanel({ summary }) {
  return (
    <div style={{ padding: "20px" }}>
      <h3>Summary</h3>
      {Object.entries(summary).map(([k, v]) => (
        <div key={k}>
          Territory {k}: {v}
        </div>
      ))}
    </div>
  );
}