function StatCard({
  title,
  value,
  change,
  subtitle,
  positive = true,
}) {
  return (
    <div className="stat-card">
      <div className="stat-card-header">
        <span>{title}</span>
      </div>

      <h2>{value}</h2>

      {change && (
        <div className={positive ? "change positive" : "change negative"}>
          {change}
        </div>
      )}

      {subtitle && <p>{subtitle}</p>}
    </div>
  );
}

export default StatCard;