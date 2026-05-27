import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [records, setRecords] = useState([]);

  const ingestSapData = () => {
    axios
      .post("http://127.0.0.1:8000/api/ingest-sap/")
      .then(() => {
        window.location.reload();
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const updateStatus = (recordId, status) => {
    axios
      .post(
        `http://127.0.0.1:8000/api/records/${recordId}/status/`,
        {
          status: status,
        }
      )
      .then(() => {
        window.location.reload();
      })
      .catch((error) => {
        console.log(error);
      });
  };

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/records/")
      .then((response) => {
        setRecords(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return (
    <div
      style={{
        padding: "40px",
        fontFamily: "Arial",
        backgroundColor: "#f4f6f8",
        minHeight: "100vh",
      }}
    >
      <h1 style={{ marginBottom: "20px" }}>
        ESG Emission Review Dashboard
      </h1>

      <button
        onClick={ingestSapData}
        style={{
          marginBottom: "30px",
          padding: "12px 20px",
          backgroundColor: "#2563eb",
          color: "white",
          border: "none",
          borderRadius: "8px",
          cursor: "pointer",
          fontSize: "16px",
        }}
      >
        Ingest SAP Data
      </button>

      {records.map((record) => (
        <div
          key={record.id}
          style={{
            backgroundColor: "white",
            border: record.is_flagged
              ? "2px solid red"
              : "1px solid #ccc",
            borderRadius: "10px",
            padding: "20px",
            marginBottom: "20px",
            boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
          }}
        >
          <h2>{record.activity_type}</h2>

          <p>
            <strong>Scope:</strong> {record.scope}
          </p>

          <p>
            <strong>Quantity:</strong> {record.quantity}{" "}
            {record.unit}
          </p>

          <p>
            <strong>Status:</strong> {record.status}
          </p>

          <p>
            <strong>Flagged:</strong>{" "}
            {record.is_flagged ? "Yes ⚠️" : "No"}
          </p>

          <div style={{ marginTop: "15px" }}>
            <button
              onClick={() =>
                updateStatus(record.id, "approved")
              }
              style={{
                marginRight: "10px",
                padding: "8px 14px",
                border: "none",
                backgroundColor: "green",
                color: "white",
                borderRadius: "5px",
                cursor: "pointer",
              }}
            >
              Approve
            </button>

            <button
              onClick={() =>
                updateStatus(record.id, "rejected")
              }
              style={{
                padding: "8px 14px",
                border: "none",
                backgroundColor: "red",
                color: "white",
                borderRadius: "5px",
                cursor: "pointer",
              }}
            >
              Reject
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

export default App;