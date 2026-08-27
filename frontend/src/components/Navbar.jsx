import { Bell, Search } from "lucide-react";

function Navbar() {
  return (
    <header className="navbar">
      <div className="search-box">
        <Search size={19} />

        <input
          type="text"
          placeholder="Search stocks, companies..."
        />
      </div>

      <div className="navbar-right">
        <button className="notification-btn">
          <Bell size={20} />
        </button>

        <div className="profile">
          <div className="profile-avatar">DK</div>

          <div className="profile-info">
            <strong>Investor</strong>
            <span>Research Workspace</span>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Navbar;