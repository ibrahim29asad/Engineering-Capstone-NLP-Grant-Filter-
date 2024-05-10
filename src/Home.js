import React from "react";
import CustomHeader from "./CustomHeader";
import Dinos from "./dino.png";
import "./About.css";
import useIsAuthenticated from "react-auth-kit/hooks/useIsAuthenticated";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { Card, CardContent } from "@mui/material";

const Home = () => {
  const navigate = useNavigate();
  const isAuthenticated = useIsAuthenticated();
  useEffect(() => {
    if (isAuthenticated) {
    } else {
      navigate("/Login");
    }
  }, [isAuthenticated, navigate]);
  return (
    <div className="mainbackground">
      {" "}
      <CustomHeader />
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          marginLeft: "5vw",
          marginRight: "5vw",
        }}
      >
        <div style={{ fontSize: 40, marginBottom: "2vh", textAlign: "center" }}>
          {" "}
          Welcome to IFARM 2.0
        </div>
        <img
          src={Dinos}
          style={{ maxWidth: "20%", height: "30vmin", margin: "0 auto" }}
          alt="logo"
        />{" "}
        <h1 style={{ fontSize: 30, textAlign: "center" }}>
          How to use the application:
          <div style={{ fontSize: 15 }}>
            For more detailed information or other information you may require,
            you can refer to the User Documentation document.
          </div>
        </h1>
        <div style={{ display: "flex", flexDirection: "row" }}>
          <div
            style={{
              fontSize: 25,
              display: "flex",
              flexDirection: "column",
              border: "2px solid black",
              background: "#FAF0D2",
              marginRight: "2vw",
              padding: 20,
            }}
          >
            <div style={{ fontWeight: "bold", textAlign: "center" }}>
              Adding Funding Opportunities
            </div>
            <div style={{ fontSize: 20, marginTop: "2vh" }}>
              1. Navigate to the insert funding opportunities page by selecting
              "Insert Fundings" in the navbar
            </div>
            <div style={{ fontSize: 20, marginTop: "2vh" }}>
              2. Enter the funding opportunity URL you would like to insert into
              the database inside the "Funding Opportunities" box
            </div>
            <div style={{ fontSize: 20, marginTop: "2vh" }}>
              3. Enter the deadline date of the funding opportunity in the
              format of "YYYY-MM_DD" in the "Date" box
            </div>
            <div style={{ fontSize: 20, marginTop: "2vh" }}>
              4. Press the submit button when you are done filling in the
              fields. The submit button will display "Submitting..." while the
              request is being processed. Once it is processed, the text fields
              will be emptied and the submit button will display "Submit" once
              again.
            </div>
            <div style={{ fontSize: 20, marginTop: "2vh" }}>
              5. You may proceed to enter another new funding opportunity.
            </div>
          </div>
          <div
            style={{
              fontSize: 25,
              display: "flex",
              flexDirection: "column",
              border: "2px solid black",
              background: "#FAF0D2",
              padding: 20,
            }}
          >
            <div style={{ fontWeight: "bold", textAlign: "center" }}>
              {" "}
              Adding Researchers and Re-Running Matching
            </div>

            <div style={{ fontSize: 20, marginTop: "2vh" }}>
              1. Navigate to the add researchers page by selecting "Home" in the
              navbar
            </div>
            <div style={{ fontSize: 20, marginTop: "2vh" }}>
              2. Enter the researcher profile page URL and the researchers email
              in the "Researcher Profile" and "Researcher Email" boxes
              respectively.
            </div>
            <div style={{ fontSize: 20, marginTop: "2vh" }}>
              3. Press the submit button when you are done filling in the
              fields. The submit button will display "Submitting..." while the
              request is being processed. Once it is processed, the text fields
              will be emptied and the submit button will display "Submit" once
              again.
            </div>
            <div style={{ fontSize: 20, marginTop: "2vh" }}>
              4. You may proceed to enter another new researcher. <br />
              Note: The matching is automatically performed on the researcher
              when they are inserted and the results are sent via email.
            </div>
            <div style={{ fontSize: 20, marginTop: "2vh" }}>
              5. To re-run the matching of funding opportunities against
              researchers, go to the "View Researcher" tab. You may either
              select whichever researchers you would like to run matching for
              with the checkbox and then clicking the Re-Run Selected
              Researchers button, or you may run the matching for all of them
              with the Re-Run All button.
            </div>
          </div>
        </div>
        <div
          style={{
            fontSize: 25,
            marginTop: "4vh",
            display: "flex",
            flexDirection: "column",
            border: "2px solid black",
            background: "#FAF0D2",
            padding: 20,
            marginBottom: 20,
          }}
        >
          <div
            style={{
              fontWeight: "bold",
              textAlign: "center",
            }}
          >
            {" "}
            Viewing Existing Researchers or Funding Opportunities
          </div>
          <div>
            <div style={{ fontSize: 20, marginTop: "2vh" }}>
              1. To view the list of all researchers in the database and their
              details click the "View Researchers" tab
            </div>
            <div style={{ fontSize: 20, marginTop: "2vh" }}>
              2. To view the list of all funding opportunities in the database
              and their details click the "View FOs" tab
            </div>
            <div style={{ fontSize: 20, marginTop: "2vh" }}>
              3. To delete a researcher, you may click the delete button in the
              "View Researchers" page, and then confirm in the popup window.
            </div>
            <div style={{ fontSize: 20, marginTop: "2vh" }}>
              4. To archive a funding opportunity, you may click the archive
              button in the "View FOs" page, and then confirm in the popup
              window.
            </div>
            <div style={{ fontSize: 20, marginTop: "2vh" }}>
              5. To view archived FOs, click the "Archives" tab. These FOs are
              FOs that have been archived manually by the user, or are not
              accessible anymore.
            </div>
            <br />
            <br />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
