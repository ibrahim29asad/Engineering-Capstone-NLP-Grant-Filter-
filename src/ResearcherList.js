import React from "react";
import CustomHeader from "./CustomHeader";
import { useState, useEffect } from "react";
import "./About.css";
import "./FOList.css";
import useIsAuthenticated from "react-auth-kit/hooks/useIsAuthenticated";
import { useNavigate } from "react-router-dom";
import { ClipLoader } from "react-spinners";
import { Button } from "@mui/material";
import "./researcher.css";

const ResearcherList = () => {
  const [list, setList] = useState([]);
  const [status, setStatus] = useState(false);
  const [buffer, setBuffer] = useState(false);
  const navigate = useNavigate();
  const isAuthenticated = useIsAuthenticated();
  const [selectedResearchers, setSelectedResearchers] = useState([]);
  const [boxCheck, setBoxCheck] = useState(false);

  useEffect(() => {
    if (isAuthenticated) {
      setBoxCheck(false);
    } else {
      navigate("/Login");
    }
    fetchResearcherList();
    setStatus(false);
    console.log("usefffect" + boxCheck);
  }, [status, isAuthenticated, navigate, boxCheck]);

  async function fetchResearcherList() {
    const response = await fetch("https://10.44.121.166/getAllResearchers", {
      method: "GET",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const temp = await response.json();
    setList(temp);
  }

  function deleteResearcher(id, url) {
    const data = {
      id: id,
      url: url,
    };
    if (window.confirm("Are you sure you want to delete this item?")) {
      const response = fetch("https://10.44.121.166//deleteAResearcher", {
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
  const handleCheckboxChange = (event, item) => {
    const { checked } = event.target;

    let updatedResearchers = [...selectedResearchers];

    if (checked) {
      updatedResearchers.push({ url: item.url, email: item.email });
    } else {
      updatedResearchers = updatedResearchers.filter(
        (researcher) =>
          !(researcher.url === item.url && researcher.email === item.email)
      );
    }

    setSelectedResearchers(updatedResearchers);
    console.log(selectedResearchers);
  };
  const resendSelectedResearchers = async () => {
    setBuffer(true);

    for (const researcher of selectedResearchers) {
      const { url, email } = researcher;
      try {
        await resendFOs(url, email);
      } catch (error) {
        console.error("Error resending FOs:", error.message);
      }
    }

    setBuffer(false);
    setSelectedResearchers([]);
    setBoxCheck(true);
    console.log(boxCheck);
  };

  async function resendFOs(url, email) {
    setBuffer(true);
    const data = {
      profile: url,
      email: email,
    };
    const response = await fetch("https://10.44.121.166/researchers", {
      method: "POST",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      if (response.status === 400) {
        alert("Invalid email entered. Please try again.");
      } else {
        alert("An error occurred. Please try again.");
      }
      setBuffer(false);
      return;
    }
    setStatus(true);
    setBuffer(false);
  }

  async function matchAllResearchers(url, email) {
    if (
      window.confirm(
        "Are you sure you want to re-run the matching for all the researchers? This could take a few moments."
      )
    ) {
      setBuffer(true);
      const response = await fetch(
        "https://10.44.121.166/matchAllResearchers",
        {
          method: "GET",
          mode: "cors",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      if (!response.ok) {
        if (response.status === 400) {
          alert("An error occurred. Please try again.");
        } else {
          alert("An error occurred. Please try again.");
        }
        setBuffer(false);
        return;
      }
      setStatus(true);
      setBuffer(false);
    }
  }

  return (
    <div className="mainbackground">
      <CustomHeader />
      {buffer && (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            position: "fixed",
            top: "0",
            left: "0",
            right: "0",
            bottom: "0",
            background: "rgba(250,250,210,0.5)",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              borderRadius: "10px",
              backgroundColor: "#f3f3f3",
              width: "30vw",
              height: "20vh",
            }}
          >
            <div
              style={{
                position: "sticky",
                marginBottom: "2vh",
                fontSize: "30px",
                color: "black",
              }}
            >
              Matching...
            </div>
            <ClipLoader color="#ff0000" />
          </div>
        </div>
      )}
      <div style={{}}>
        <div
          style={{
            display: "flex",
            flexDirection: "row",
            justifyContent: "space-between",
          }}
        >
          <div
            style={{
              paddingRight: "1vw",
              paddingTop: "1vh",
            }}
          >
            {" "}
            <button
              className="rerun-selected-btn"
              onClick={() => resendSelectedResearchers()}
            >
              RE-RUN SELECTED RESEARCHERS
            </button>
          </div>
          <div
            style={{
              paddingRight: "1vw",
              paddingTop: "1vh",
            }}
          >
            {" "}
            <button
              className="rerun-all-btn"
              onClick={() => matchAllResearchers()}
            >
              RE-RUN ALL
            </button>
          </div>
        </div>

        <div className="research-table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th style={{ padding: "10px" }}>Resend FOs</th>
                <th style={{ padding: "10px" }}>Email</th>
                <th style={{ padding: "10px" }}>Profile URL</th>
                <th style={{ padding: "10px" }}>Keywords</th>
                <th style={{ padding: "10px" }}>Delete</th>
              </tr>
            </thead>
            <tbody>
              {list.map((item, index) => (
                <tr key={index}>
                  <td className="resend-btn-column">
                    <input
                      type="checkbox"
                      checked={selectedResearchers?.find(
                        (val) => val.url === item.url
                      )}
                      onChange={(e) => handleCheckboxChange(e, item)}
                      style={{
                        marginLeft: "1.5vw",
                        width: "1rem",
                        height: "1rem",
                      }}
                    ></input>
                  </td>
                  <td className="email-column">{item.email}</td>
                  <td className="profile-column">
                    <a href={item.url} target="blank">
                      {item.url}
                    </a>
                  </td>
                  <td className="keywords-researcher-column">
                    {item.keywords.join(", ")}
                  </td>
                  <td className="delete-btn-column">
                    <button
                      className="delete-button"
                      onClick={() => deleteResearcher(item.id, item.url)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default ResearcherList;
