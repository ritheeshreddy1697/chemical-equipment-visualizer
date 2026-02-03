import "./Navbar.css";

function Navbar({ onUploadClick, onHistoryClick }) {
  return (
    <nav className="navbar">
      <div className="navbar-title">
        Chemical Equipment Visualizer
      </div>

      <div className="navbar-links">
        <span onClick={onUploadClick}>Upload</span>
        <span>Summary</span>
        <span onClick={onHistoryClick}>History</span>
        <span>Report</span>
      </div>
    </nav>
  );
}

export default Navbar;