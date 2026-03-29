import React from "react";
// import PixelBlast from "./PixelBlast";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import "../LandingPage.css";

const LandingPage = () => {
  const navigate = useNavigate();
  return (
    <div className="landing-page">
      {/* Animated Three.js background */}
      {/* <PixelBlast
        variant="circle"
        pixelSize={3}
        color="#B19EEF"
        patternScale={2}
        liquid={true}
        liquidStrength={0.15}
        enableRipples={true}
        rippleIntensityScale={1}
        rippleSpeed={0.3}
        transparent={true}
      /> */}

      {/* Glass Navbar */}
      <nav className="glass-navbar">
        <div className="nav-logo">MediBudget</div>
        <ul className="nav-links">
          <li><a href="#">Home</a></li>
          <li><a href="#">Prediction</a></li>
        </ul>
      </nav>

      {/* Hero Section */}
      <div className="hero-content">
        <motion.h1
          className="hero-title"
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1.2 }}
        >
          Medi <span>Budget</span>
        </motion.h1>

        <motion.button
          className="get-started-btn"
          whileHover={{ scale: 1.08 }}
          whileTap={{ scale: 0.96 }}
          onClick={() => navigate('/form')}
        >
          Get Started
        </motion.button>
      </div>
    </div>
  );
};

export default LandingPage;
