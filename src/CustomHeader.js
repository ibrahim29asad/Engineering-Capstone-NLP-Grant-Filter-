import React from "react";
import { FaHome, FaLeaf } from "react-icons/fa";
import { TbPigMoney } from "react-icons/tb";
import { FcReadingEbook } from "react-icons/fc";
import { FcList } from "react-icons/fc";
import { TbClipboardList } from "react-icons/tb";
import { Link } from "react-router-dom";
import { TbHistory } from "react-icons/tb";
import { TbLogout2 } from "react-icons/tb";
import useSignOut from "react-auth-kit/hooks/useSignOut";
import { useNavigate } from "react-router-dom";
import "./navbar.css";

const CustomHeader = () => {
  const signOut = useSignOut();
  const nav = useNavigate();
  function redirect(page) {
    if (page === "Logout") {
      signOut();
      nav("/Login");
    } else {
      nav(`/${page}`);
    }
  }
  return (
    <div className="navbar-main">
      <div className="navbar-left">
        <button
          onClick={() => {
            redirect("");
          }}
          className="button"
        >
          <FaHome />
          Home
        </button>

        <button
          onClick={() => {
            redirect("Funding");
          }}
          className="button"
        >
          <TbPigMoney />
          Insert Fundings
        </button>

        <button
          onClick={() => {
            redirect("Researcher");
          }}
          className="button"
        >
          <FcReadingEbook />
          Insert Researcher
        </button>

        <button
          onClick={() => {
            redirect("FOList");
          }}
          className="button"
        >
          <FcList />
          View FOs
        </button>

        <button
          onClick={() => {
            redirect("ResearcherList");
          }}
          className="button"
        >
          <TbClipboardList />
          View Researchers
        </button>

        <button
          onClick={() => {
            redirect("Archives");
          }}
          className="button"
        >
          <TbHistory />
          Archives
        </button>
      </div>
      <div>
        <button
          onClick={() => {
            redirect("Logout");
          }}
          className="button logout-button"
        >
          <TbLogout2 />
          Logout
        </button>
      </div>
    </div>
  );
};

export default CustomHeader;
