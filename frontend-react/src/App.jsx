import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import WalletProcessor from "./components/WalletProcessor";

const App = () => (
  <Router>
    <div className="bg-gray-100 flex items-center justify-center min-h-screen">
      <Routes>
        <Route path="/" element={<WalletProcessor />} />
      </Routes>
    </div>
  </Router>
);

export default App;
