import { TrendingUp, Brain, ShieldCheck } from "lucide-react";
import StatCard from "../../components/StatCard";
import StockSignals from "../../components/StockSignals";
import PortfolioRisk from "../../components/PortfolioRisk";

function Dashboard() {
  return (
    <div className="dashboard">
      <div className="page-heading">
        <div>
          <span className="eyebrow">MARKET INTELLIGENCE</span>

          <h1>Equity Dashboard</h1>

          <p>
            AI-powered market analysis and portfolio intelligence.
          </p>
        </div>

        <div className="market-status">
          <span></span>
          Market Data Ready
        </div>
      </div>

      <div className="stats-grid">
        <StatCard
          title="NIFTY 50"
          value="24,850.35"
          change="+0.82% today"
          positive={true}
        />

        <StatCard
          title="SENSEX"
          value="81,250.42"
          change="+0.64% today"
          positive={true}
        />

        <StatCard
          title="AI SIGNALS"
          value="3"
          subtitle="Active BUY signals"
        />

        <StatCard
          title="PORTFOLIO RISK"
          value="19.12%"
          subtitle="Annual volatility"
        />
      </div>

      <div className="dashboard-grid">
        <StockSignals />

        <PortfolioRisk />
      </div>

      <div className="research-banner">
        <div className="research-icon">
          <Brain size={25} />
        </div>

        <div className="research-content">
          <span>AI RESEARCH</span>
          <h2>Ask questions about financial documents</h2>
          <p>
            Search annual reports using semantic RAG retrieval
            and get source-backed insights.
          </p>
        </div>

        <button className="research-btn">
          Open AI Research
          <TrendingUp size={17} />
        </button>
      </div>
    </div>
  );
}

export default Dashboard;