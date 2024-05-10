import React from "react";
import "./index.css";
import App from "./App";
import Funding from "./Funding";
import Home from "./Home";
import ResearcherList from "./ResearcherList";
import FOList from "./FOList";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./Login";
import Archives from "./Archives";
import AuthOutlet from "@auth-kit/react-router/AuthOutlet";
export default function Routing() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AuthOutlet fallbackPath="/Login" />}>
          <Route path="/" element={<Home />} />
          <Route path="/Funding" element={<Funding />} />
          <Route path="/Researcher" element={<App />} />
          <Route path="/ResearcherList" element={<ResearcherList />} />
          <Route path="/FOList" element={<FOList />} />
          <Route path="/Archives" element={<Archives />} />
        </Route>
        <Route path="/Login" element={<Login />} />
      </Routes>
    </BrowserRouter>
  );
}
