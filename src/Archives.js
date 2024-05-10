import React from "react";
import CustomHeader from "./CustomHeader";
import { useState, useEffect } from "react";
import "./About.css";
import "./FOList.css";
import useIsAuthenticated from "react-auth-kit/hooks/useIsAuthenticated";
import { useNavigate } from "react-router-dom";

const Archives = () => {
  const [list, setList] = useState([]);
  const [status, setStatus] = useState(false);
  const navigate = useNavigate();
  const isAuthenticated = useIsAuthenticated();

  useEffect(() => {
    if (isAuthenticated) {
    } else {
      navigate("/Login");
    }
    fetchArchiveList();
    setStatus(false);
  }, [status, isAuthenticated, navigate]);

  async function fetchArchiveList() {
    const response = await fetch("https://10.44.121.166/getAllArchivedLinks", {
      method: "GET",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const temp = await response.json();
    setList(temp);
  }

  //send ID for deletes
  return (
    <div className="mainbackground">
      <CustomHeader />
      <div
        className="table-container"
        style={{
          display: "flex",
          justifyContent: "center",
        }}
      >
        <table className="data-table">
          <thead>
            <tr>
              <th style={{ padding: "10px" }}>URL</th>
              <th style={{ padding: "10px" }}>Deadline Date</th>
              <th style={{ padding: "10px" }}>Reason</th>
            </tr>
          </thead>
          <tbody>
            {list.map((item, index) => (
              <tr key={index}>
                <td className="url-column">
                  <a href={item.url} target="blank">
                    {item.url}
                  </a>
                </td>
                <td className="closedate-column">{item.closeDate}</td>
                <td className="reason-column">{item.reason}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Archives;
