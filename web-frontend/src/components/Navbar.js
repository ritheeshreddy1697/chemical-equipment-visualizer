import "./Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-title">
        Chemical Equipment Visualizer
      </div>
      <div className="navbar-links">
        <span>Upload</span>
        <span>Summary</span>
        <span>History</span>
        <span>Report</span>
      </div>
    </nav>
  );
}

export default Navbar;