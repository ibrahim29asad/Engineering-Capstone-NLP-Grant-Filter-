import { useState, useEffect } from "react";
import Dinos from "./dino.png";
import "./App.css";
import CustomHeader from "./CustomHeader";
import * as React from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import useIsAuthenticated from "react-auth-kit/hooks/useIsAuthenticated";
import { useNavigate } from "react-router-dom";
import { ClipLoader } from "react-spinners";

function App() {
  const [profileState, setProfile] = useState("");
  const [emailState, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(false);
  const [buffer, setBuffer] = useState(false);
  const navigate = useNavigate();
  const isAuthenticated = useIsAuthenticated();

  useEffect(() => {
    if (isAuthenticated) {
    } else {
      navigate("/Login");
    }
    setStatus(false);
  }, [status, isAuthenticated, navigate]);

  async function submitResearchers(event) {
    event.preventDefault();
    if (profileState === "" || emailState === "") {
      alert("Please fill in all the text fields");
    } else {
      setBuffer(true);
      setLoading(true);
      const data = {
        profile: profileState,
        email: emailState,
      };
      try {
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
            setBuffer(false);
            setLoading(false);
            alert("Invalid email entered. Please try again.");
          } else {
            setBuffer(false);
            setLoading(false);
            alert("An error occurred. Please try again.");
          }
          return;
        }

        setBuffer(false);
        setLoading(false);
        setProfile("");
        setEmail("");
        setStatus(true);
      } catch (error) {
        console.error("Error submitting funding:", error.message);
        setBuffer(false);
        alert("An error occurred. Please try again later.");
        setLoading(false);
      }
    }
  }

  return (
    <div>
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
                Performing Request...
              </div>
              <ClipLoader color="#ff0000" />
            </div>
          </div>
        )}
        <header className="App-header">
          <img src={Dinos} className="App-logo" alt="logo" />
          <div>
            <p>Please Enter the Following Information</p>
          </div>
          <form
            style={{ display: "flex", flexDirection: "column" }}
            onSubmit={submitResearchers}
          >
            <TextField
              label="Researcher Profile URL"
              placeholder="Researcher URL"
              variant="outlined"
              value={profileState}
              style={{ width: "300px", marginBottom: "10px" }}
              onChange={(event) => setProfile(event.target.value)}
            />
            <TextField
              label="Researcher Email"
              placeholder="Email"
              variant="outlined"
              value={emailState}
              style={{ width: "300px", marginBottom: "10px" }}
              onChange={(event) => setEmail(event.target.value)}
            />
            <button className="EnterButton" type="submit">
              {loading ? "Submitting..." : "Submit"}
            </button>
          </form>
        </header>
      </div>
    </div>
  );
}

export default App;
