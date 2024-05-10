import React from "react";
import CustomHeader from "./CustomHeader";
import { useState, useEffect } from "react";
import "./About.css";
import "./FOList.css";
import useIsAuthenticated from "react-auth-kit/hooks/useIsAuthenticated";
import { useNavigate } from "react-router-dom";

const FOList = () => {
  const [list, setList] = useState([]);
  const [status, setStatus] = useState(false);
  const navigate = useNavigate();
  const isAuthenticated = useIsAuthenticated();

  useEffect(() => {
    if (isAuthenticated) {
    } else {
      navigate("/Login");
    }
    fetchFundingsList();
    setStatus(false);
  }, [status, isAuthenticated, navigate]);

  async function fetchFundingsList() {
    const response = await fetch("https://10.44.121.166/getAllFunding", {
      method: "GET",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const temp = await response.json();
    setList(temp);
  }

  function deleteFO(id) {
    const data = {
      id: id,
    };
    if (window.confirm("Are you sure you want to archive this item?")) {
      const response = fetch("https://10.44.121.166/deleteAFunding", {
        method: "DELETE",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      setStatus(true);
    }
  }

  //send ID for deletes
  return (
    <div className="mainbackground">
      <CustomHeader />

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th style={{ padding: "10px" }}>URL</th>
              <th style={{ padding: "10px" }}>Keywords</th>
              <th style={{ padding: "10px" }}>Deadline Date</th>
              <th style={{ padding: "10px" }}>Archive</th>
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
                <td className="keywords-column">{item.keywords.join(", ")}</td>
                <td className="closedate-column">{item.closeDate}</td>
                <td className="delete-btn-column">
                  <button
                    className="delete-button"
                    onClick={() => deleteFO(item.id)}
                  >
                    Archive
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default FOList;
