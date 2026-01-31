import { useState } from "react";
import axios from "axios";

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
      const response = await axios.post(
        "http://127.0.0.1:8000/api/upload/",
        formData
      );

      setData(response.data);
      setMessage("CSV uploaded successfully ✅");
    } catch (error) {
      console.error(error);
      setMessage("Upload failed ❌");
    }
  };

  // Chart data
  const chartData =
    data && {
      labels: Object.keys(data.type_distribution),
      datasets: [
        {
          label: "Equipment Count",
          data: Object.values(data.type_distribution),
          backgroundColor: "rgba(54, 162, 235, 0.7)",
        },
      ],
    };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>Chemical Equipment Parameter Visualizer</h1>

      {/* Upload Section */}
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <br /><br />
      <button onClick={handleUpload}>Upload CSV</button>
      <p>{message}</p>

      {/* Summary Section */}
      {data && (
        <>
          <h2>Summary</h2>
          <ul>
            <li><b>Total Equipment:</b> {data.total_count}</li>
            <li><b>Average Flowrate:</b> {data.avg_flowrate.toFixed(2)}</li>
            <li><b>Average Pressure:</b> {data.avg_pressure.toFixed(2)}</li>
            <li><b>Average Temperature:</b> {data.avg_temperature.toFixed(2)}</li>
          </ul>

          {/* Table Section */}
          <h2>Equipment Data</h2>
          <table border="1" cellPadding="6" style={{ borderCollapse: "collapse" }}>
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

          {/* Chart Section */}
          <h2>Equipment Type Distribution</h2>
          <div style={{ width: "600px" }}>
            <Bar data={chartData} />
          </div>
        </>
      )}
    </div>
  );
}

export default App;
