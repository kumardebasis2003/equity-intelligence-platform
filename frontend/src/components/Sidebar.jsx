import {
  LayoutDashboard,
  BarChart3,
  Brain,
  ShieldAlert,
  BriefcaseBusiness,
  Settings,
} from "lucide-react";

const menuItems = [
  {
    label: "Dashboard",
    icon: LayoutDashboard,
    path: "/",
  },
  {
    label: "Stocks",
    icon: BarChart3,
    path: "/stocks",
  },
  {
    label: "AI Research",
    icon: Brain,
    path: "/research",
  },
  {
    label: "Risk Analysis",
    icon: ShieldAlert,
    path: "/risk",
  },
  {
    label: "Portfolio",
    icon: BriefcaseBusiness,
    path: "/portfolio",
  },
  {
    label: "Settings",
    icon: Settings,
    path: "/settings",
  },
];

function Sidebar({ activePage, setActivePage }) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-logo">AI</div>

        <div>
          <h2>Equity</h2>
          <span>Intelligence</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activePage === item.label;

          return (
            <button
              key={item.label}
              className={`nav-item ${isActive ? "active" : ""}`}
              onClick={() => setActivePage(item.label)}
            >
              <Icon size={19} strokeWidth={1.8} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="ai-status">
        <span className="status-dot"></span>

        <div>
          <strong>AI Engine</strong>
          <small>System operational</small>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;