import React from "react";
import { Link } from "react-router-dom";

const Header = () => (
  <header>
    <nav>
      <Link to="/">Home</Link> | <Link to="/login">Login</Link> | <Link to="/register">Register</Link> | <Link to="/metrics">Metrics</Link>
    </nav>
  </header>
);

export default Header;
