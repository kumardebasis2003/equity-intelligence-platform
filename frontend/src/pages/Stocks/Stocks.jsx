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

function Stocks() {
  return (
    <div className="stocks-page">

      <div className="page-heading">
        <div>
          <span className="eyebrow">MARKET DATA</span>

          <h1>Stocks</h1>

          <p>
            Track stock prices, AI signals and market performance.
          </p>
        </div>

        <div className="market-status">
          <span></span>
          Market Data Ready
        </div>
      </div>

      <div className="stocks-summary">

        <div className="summary-card">
          <span>Total Stocks</span>
          <strong>5</strong>
          <small>Tracked stocks</small>
        </div>

        <div className="summary-card">
          <span>BUY Signals</span>
          <strong>3</strong>
          <small>AI generated signals</small>
        </div>

        <div className="summary-card">
          <span>HOLD Signals</span>
          <strong>2</strong>
          <small>AI generated signals</small>
        </div>

        <div className="summary-card">
          <span>Market Status</span>
          <strong className="positive">OPEN</strong>
          <small>NSE market</small>
        </div>

      </div>

      <div className="panel stocks-panel">

        <div className="panel-header">
          <div>
            <h2>Tracked Stocks</h2>
            <p>AI model predictions and current prices</p>
          </div>

          <button className="view-btn">
            Refresh
          </button>
        </div>

        <div className="stock-table">

          <div className="stock-table-header">
            <span>STOCK</span>
            <span>PRICE</span>
            <span>CHANGE</span>
            <span>AI SIGNAL</span>
          </div>

          {stocks.map((stock) => (
            <div
              className="stock-table-row"
              key={stock.symbol}
            >

              <div className="stock-info">

                <div className="stock-logo">
                  {stock.symbol.substring(0, 2)}
                </div>

                <div>
                  <strong>{stock.symbol}</strong>
                  <span>{stock.name}</span>
                </div>

              </div>

              <strong className="table-price">
                {stock.price}
              </strong>

              <span
                className={
                  stock.change.startsWith("+")
                    ? "positive"
                    : "negative"
                }
              >
                {stock.change}
              </span>

              <span
                className={`signal-badge ${
                  stock.signal.toLowerCase()
                }`}
              >
                {stock.signal}
              </span>

            </div>
          ))}

        </div>

      </div>

    </div>
  );
}

export default Stocks;