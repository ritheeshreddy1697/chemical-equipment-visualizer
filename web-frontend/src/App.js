import { useState } from "react";
import axios from "axios";
import "./App.css";
import Navbar from "./components/Navbar";

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

const API_BASE =
  "https://chemical-equipment-visualizer-i9my.onrender.com/api";

function App() {
  /* ---------------- STATE ---------------- */
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [message, setMessage] = useState("");

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);

  /* ---------------- HANDLERS ---------------- */
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!name || !email) {
      setMessage("Please enter your name and email");
      return;
    }

    if (!file) {
      setMessage("Please select a CSV file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        `${API_BASE}/upload/`,
        formData
      );

      setData(response.data);
      setMessage("CSV uploaded successfully ✅");
      setShowHistory(false); // return to upload view

      const newEntry = {
        name,
        email,
        timestamp: new Date().toLocaleString(),
        total: response.data.total_count,
      };

      setHistory((prev) => [newEntry, ...prev]);
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

      const url = window.URL.createObjectURL(
        new Blob([response.data])
      );
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

  /* ---------------- CHART DATA ---------------- */
  const chartData =
    data && {
      labels: Object.keys(data.type_distribution),
      datasets: [
        {
          label: "Equipment Count",
          data: Object.values(data.type_distribution),
          backgroundColor: "rgba(255, 106, 0, 0.7)",
        },
      ],
    };

  /* ---------------- UI ---------------- */
  return (
    <>
      <Navbar
        onUploadClick={() => setShowHistory(false)}
        onHistoryClick={() => setShowHistory(true)}
      />

      <div className="page-container">
        {/* Upload Card */}
        <div className="upload-card">
          <h2>Upload CSV File</h2>

          <input
            type="text"
            placeholder="Your Name"
            className="file-input"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />

          <input
            type="email"
            placeholder="Your Email"
            className="file-input"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="file"
            accept=".csv"
            className="file-input"
            onChange={handleFileChange}
          />

          <div className="button-row">
            <button className="btn-primary" onClick={handleUpload}>
              Upload
            </button>

            <button
              className="btn-secondary"
              onClick={handleDownloadPDF}
            >
              Download Report
            </button>
          </div>

          <p className="status-text">{message}</p>
        </div>

        {/* Analytics Sections */}
        {data && !showHistory && (
          <>
            {/* Summary */}
            <div className="section-card">
              <h2>Summary</h2>
              <div className="summary-grid">
                <SummaryCard
                  title="Total Equipment"
                  value={data.total_count}
                />
                <SummaryCard
                  title="Avg Flowrate"
                  value={data.avg_flowrate.toFixed(2)}
                />
                <SummaryCard
                  title="Avg Pressure"
                  value={data.avg_pressure.toFixed(2)}
                />
                <SummaryCard
                  title="Avg Temperature"
                  value={data.avg_temperature.toFixed(2)}
                />
              </div>
            </div>

            {/* Table */}
            <div className="section-card">
              <h2>Equipment Data</h2>
              <table className="data-table">
                <thead>
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
            <div className="section-card">
              <h2>Equipment Type Distribution</h2>
              <div style={{ maxWidth: "700px", margin: "auto" }}>
                <Bar data={chartData} />
              </div>
            </div>
          </>
        )}

        {/* History Section (ONLY when clicked) */}
        {showHistory && history.length > 0 && (
          <div className="section-card">
            <h2>Upload History</h2>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Uploaded At</th>
                  <th>Total Equipment</th>
                </tr>
              </thead>
              <tbody>
                {history.map((item, index) => (
                  <tr key={index}>
                    <td>{item.name}</td>
                    <td>{item.email}</td>
                    <td>{item.timestamp}</td>
                    <td>{item.total}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </>
  );
}

/* ---------------- SUMMARY CARD ---------------- */
function SummaryCard({ title, value }) {
  return (
    <div className="summary-card">
      <h3>{title}</h3>
      <p>{value}</p>
    </div>
  );
}

export default App;