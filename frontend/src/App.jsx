import { useState } from "react";
import Sidebar from "./components/Sidebar";
import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard/Dashboard";
import "./App.css";

function App() {
  const [activePage, setActivePage] = useState("Dashboard");

  return (
    <div className="app">
      <Sidebar
        activePage={activePage}
        setActivePage={setActivePage}
      />

      <div className="main-area">
        <Navbar />

        <main className="content">
          {activePage === "Dashboard" && <Dashboard />}

          {activePage !== "Dashboard" && (
            <div className="coming-soon">
              <h1>{activePage}</h1>
              <p>
                This page will be added in the next step.
              </p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;