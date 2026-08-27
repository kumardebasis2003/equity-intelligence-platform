import { ShieldAlert } from "lucide-react";

function PortfolioRisk() {
  return (
    <div className="panel risk-panel">
      <div className="panel-header">
        <div>
          <h2>Portfolio Risk</h2>
          <p>Historical risk metrics</p>
        </div>

        <ShieldAlert size={21} />
      </div>

      <div className="risk-level">
        HIGH
      </div>

      <p className="risk-description">
        Overall portfolio risk
      </p>

      <div className="risk-divider"></div>

      <div className="risk-metrics">
        <div>
          <span>Return</span>
          <strong className="positive">+174.81%</strong>
        </div>

        <div>
          <span>Sharpe</span>
          <strong>0.87</strong>
        </div>

        <div>
          <span>Max Drawdown</span>
          <strong className="negative">-37.43%</strong>
        </div>
      </div>
    </div>
  );
}

export default PortfolioRisk;