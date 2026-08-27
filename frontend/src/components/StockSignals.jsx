import { ArrowUpRight, ArrowDownRight } from "lucide-react";

const stocks = [
  {
    symbol: "RELIANCE",
    name: "Reliance Industries",
    price: "₹1,570.40",
    change: "+1.99%",
    signal: "BUY",
  },
  {
    symbol: "TCS",
    name: "Tata Consultancy Services",
    price: "₹3,420.25",
    change: "-0.85%",
    signal: "HOLD",
  },
  {
    symbol: "INFY",
    name: "Infosys",
    price: "₹1,525.30",
    change: "+0.72%",
    signal: "BUY",
  },
  {
    symbol: "HDFCBANK",
    name: "HDFC Bank",
    price: "₹1,985.60",
    change: "-0.42%",
    signal: "HOLD",
  },
  {
    symbol: "ICICIBANK",
    name: "ICICI Bank",
    price: "₹1,422.75",
    change: "+1.24%",
    signal: "BUY",
  },
];

function StockSignals() {
  return (
    <div className="panel stock-panel">
      <div className="panel-header">
        <div>
          <h2>AI Stock Signals</h2>
          <p>XGBoost model predictions</p>
        </div>

        <button className="view-btn">View all</button>
      </div>

      <div className="stock-list">
        {stocks.map((stock) => {
          const positive = stock.change.startsWith("+");

          return (
            <div className="stock-row" key={stock.symbol}>
              <div className="stock-left">
                <div className="stock-logo">
                  {stock.symbol.substring(0, 2)}
                </div>

                <div>
                  <strong>{stock.symbol}</strong>
                  <span>{stock.name}</span>
                </div>
              </div>

              <div className="stock-price">
                <strong>{stock.price}</strong>

                <span className={positive ? "positive" : "negative"}>
                  {positive ? (
                    <ArrowUpRight size={14} />
                  ) : (
                    <ArrowDownRight size={14} />
                  )}

                  {stock.change}
                </span>
              </div>

              <span
                className={`signal-badge ${stock.signal.toLowerCase()}`}
              >
                {stock.signal}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default StockSignals;