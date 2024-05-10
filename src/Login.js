import { useState, useEffect } from "react";
import Dinos from "./dino.png";
import "./App.css";
import * as React from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import useSignIn from "react-auth-kit/hooks/useSignIn";
import { useNavigate } from "react-router-dom";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(false);
  const navigate = useNavigate();
  const signIn = useSignIn();
  useEffect(() => {
    setStatus(false);
  }, [status]);

  async function sendLogin(event) {
    event.preventDefault();
    if (username === "" || password === "") {
      alert("Please fill in all the text fields");
    } else {
      setLoading(true);
      const data = {
        username: username,
        password: password,
      };
      try {
        const response = await fetch("https://10.44.121.166/login", {
          method: "POST",
          mode: "cors",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        });
        if (!response.ok) {
          if (response.status === 401) {
            setLoading(false);
            alert("Invalid email or password entered. Please try again.");
          } else {
            setLoading(false);
            alert("Invalid email or password entered. Please try again.");
          }
          return;
        } else {
          const jsonResponse = await response.json();
          signIn({
            auth: { token: jsonResponse.access_token, type: "Bearer" },
            userState: { name: "IFARM" },
          });
          setLoading(false);
          navigate("/");
        }
      } catch (error) {
        alert("An error occurred. Please try again later.");
        setLoading(false);
      }
    }
  }

  return (
    <div>
      <div className="App">
        <header className="login-header">
          <img src={Dinos} className="App-logo" alt="logo" />
          <div>
            <p>Please Enter the Following Information</p>
          </div>
          <form
            style={{ display: "flex", flexDirection: "column" }}
            onSubmit={sendLogin}
          >
            <TextField
              label="Username"
              placeholder="Username"
              variant="outlined"
              value={username}
              onChange={(event) => {
                setUsername(event.target.value);
              }}
              style={{ width: "300px", marginBottom: "10px" }}
            />
            <TextField
              label="Password"
              type="password"
              variant="outlined"
              placeholder="Password"
              value={password}
              onChange={(event) => {
                setPassword(event.target.value);
              }}
              style={{ width: "300px", marginBottom: "10px" }}
            />
            <button className="EnterButton" type="submit">
              {loading ? "Logging in..." : "Login"}
            </button>
          </form>
        </header>
      </div>
    </div>
  );
}

export default Login;
