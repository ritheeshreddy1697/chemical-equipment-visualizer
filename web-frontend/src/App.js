import { useState } from "react";
import axios from "axios";
import "./App.css";

// Chart.js imports
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

// Register chart components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const API_BASE = "http://127.0.0.1:8000/api";

function App() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a CSV file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(`${API_BASE}/upload/`, formData);
      setData(response.data);
      setMessage("CSV uploaded successfully ✅");
    } catch (error) {
      console.error(error);
      setMessage("Upload failed ❌");
    }
  };

  const handleDownloadPDF = async () => {
    if (!file) {
      alert("Upload a CSV file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        `${API_BASE}/report/`,
        formData,
        { responseType: "blob" }
      );

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "equipment_report.pdf");
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error(error);
      alert("Failed to download PDF");
    }
  };

  const chartData =
    data && {
      labels: Object.keys(data.type_distribution),
      datasets: [
        {
          label: "Equipment Count",
          data: Object.values(data.type_distribution),
          backgroundColor: "rgba(46, 134, 222, 0.7)",
        },
      ],
    };

  return (
    <div className="app-container">
      <h1>Chemical Equipment Parameter Visualizer</h1>

      {/* Upload Section */}
      <div className="section">
        <h2>Upload CSV</h2>
        <input type="file" accept=".csv" onChange={handleFileChange} />
        <br /><br />

        <button onClick={handleUpload}>Upload CSV</button>
        &nbsp;&nbsp;
        <button onClick={handleDownloadPDF}>Download PDF</button>

        <p>{message}</p>
      </div>

      {/* Analytics Section */}
      {data && (
        <>
          {/* Summary Cards */}
          <div className="section">
            <h2>Summary</h2>
            <div style={{ display: "flex", gap: "20px", flexWrap: "wrap" }}>
              <SummaryCard title="Total Equipment" value={data.total_count} />
              <SummaryCard title="Avg Flowrate" value={data.avg_flowrate.toFixed(2)} />
              <SummaryCard title="Avg Pressure" value={data.avg_pressure.toFixed(2)} />
              <SummaryCard
                title="Avg Temperature"
                value={data.avg_temperature.toFixed(2)}
              />
            </div>
          </div>

          {/* Table */}
          <div className="section">
            <h2>Equipment Data</h2>
            <table
              border="1"
              cellPadding="8"
              style={{ width: "100%", borderCollapse: "collapse" }}
            >
              <thead style={{ backgroundColor: "#f0f3f5" }}>
                <tr>
                  <th>Equipment Name</th>
                  <th>Type</th>
                  <th>Flowrate</th>
                  <th>Pressure</th>
                  <th>Temperature</th>
                </tr>
              </thead>
              <tbody>
                {data.table_data.map((row, index) => (
                  <tr key={index}>
                    <td>{row["Equipment Name"]}</td>
                    <td>{row.Type}</td>
                    <td>{row.Flowrate}</td>
                    <td>{row.Pressure}</td>
                    <td>{row.Temperature}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Chart */}
          <div className="section">
            <h2>Equipment Type Distribution</h2>
            <div style={{ maxWidth: "700px", margin: "auto" }}>
              <Bar data={chartData} />
            </div>
          </div>
        </>
      )}
    </div>
  );
}

/* Summary Card Component */
function SummaryCard({ title, value }) {
  return (
    <div
      style={{
        flex: "1",
        minWidth: "200px",
        background: "#f8f9fa",
        padding: "15px",
        borderRadius: "8px",
        textAlign: "center",
        boxShadow: "0 1px 4px rgba(0,0,0,0.1)",
      }}
    >
      <h3 style={{ marginBottom: "10px", color: "#34495e" }}>{title}</h3>
      <p style={{ fontSize: "20px", fontWeight: "bold" }}>{value}</p>
    </div>
  );
}

export default App;
