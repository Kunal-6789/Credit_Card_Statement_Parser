import { useState } from "react";
import "./App.css";

export default function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleUpload(e) {
    e.preventDefault();
    if (!file) return setError("Please choose a PDF file");
    setError(null);
    setLoading(true);
    const form = new FormData();
    form.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/parse", {
        method: "POST",
        body: form,
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Server error");
      }
      const data = await res.json();
      setResult(data.data || null); // Only the `data` part
    } catch (err) {
      setError(err.message);
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  // Calculate remaining days
  function getDaysRemaining(dueDateStr) {
    if (!dueDateStr) return "-";
    const dueDate = new Date(dueDateStr);
    const today = new Date();
    const diffTime = dueDate - today;
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  }

  // Determine color based on days remaining
  function getDueDateColor(dueDateStr) {
    const days = getDaysRemaining(dueDateStr);
    if (days === "-") return "black";
    if (days <= 3) return "red";       // urgent
    if (days <= 7) return "orange";    // warning
    return "green";                     // safe
  }

  // Download JSON
  const downloadJSON = () => {
    if (!result) return;
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "parsed_data.json";
    a.click();
  };

  // Download CSV
  const downloadCSV = () => {
    if (!result) return;
    const rows = [
      ["Field", "Value"],
      ["Bank / Issuer", result.issuer],
      ["Last 4 Digits", result.last4 || "-"],
      ["Billing Cycle", result.billing_cycle || "-"],
      ["Payment Due Date", result.due_date || "-"],
      ["Total Amount Due", result.total_due || "-"],
      ["Days Remaining", getDaysRemaining(result.due_date)],
    ];
    const csvContent = rows.map(r => r.join(",")).join("\n");
    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "parsed_data.csv";
    a.click();
  };

return (
  <div className="app-container">
    <h1 className="title">Credit Card Statement Parser</h1>

    <form onSubmit={handleUpload} className="upload-form">
      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files[0])}
        className="file-input"
      />
      <button type="submit" disabled={loading} className="btn-primary">
        {loading ? "Parsing..." : "Upload & Parse"}
      </button>
    </form>

    {error && <p className="error-msg">{error}</p>}

    {result && (
      <div className="result-card">
        <h2>Extracted Data</h2>
        <table className="result-table">
          <tbody>
            <tr>
              <td className="field-name">Bank / Issuer</td>
              <td>{result.issuer}</td>
            </tr>
            <tr>
              <td className="field-name">Last 4 Digits</td>
              <td>{result.last4 || "-"}</td>
            </tr>
            <tr>
              <td className="field-name">Billing Cycle</td>
              <td>{result.billing_cycle || "-"}</td>
            </tr>
            <tr>
              <td className="field-name">Payment Due Date</td>
              <td style={{ color: getDueDateColor(result.due_date) }}>
                {result.due_date || "-"} ({getDaysRemaining(result.due_date)} days remaining)
              </td>
            </tr>
            <tr>
              <td className="field-name">Total Amount Due</td>
              <td>{result.total_due || "-"}</td>
            </tr>
          </tbody>
        </table>

        <div className="download-buttons">
          <button onClick={downloadJSON} className="btn-secondary">Download JSON</button>
          <button onClick={downloadCSV} className="btn-secondary">Download CSV</button>
        </div>
      </div>
    )}

    <p className="footer-note">
      Notes: Frontend expects backend at <code>http://localhost:8000/parse</code>
    </p>
  </div>
);
}
