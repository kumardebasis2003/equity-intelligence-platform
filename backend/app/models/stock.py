from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Numeric,
    BigInteger,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.models.database import Base


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)

    ticker = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    company_name = Column(
        String(150),
        nullable=False,
    )

    exchange = Column(
        String(20),
        default="NSE",
    )

    sector = Column(
        String(100),
        nullable=True,
    )

    price_history = relationship(
        "PriceHistory",
        back_populates="stock",
        cascade="all, delete-orphan",
    )


class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)

    stock_id = Column(
        Integer,
        ForeignKey("stocks.id"),
        nullable=False,
        index=True,
    )

    date = Column(
        Date,
        nullable=False,
        index=True,
    )

    open = Column(Numeric(15, 4))
    high = Column(Numeric(15, 4))
    low = Column(Numeric(15, 4))
    close = Column(Numeric(15, 4))
    adjusted_close = Column(Numeric(15, 4))

    volume = Column(BigInteger)

    stock = relationship(
        "Stock",
        back_populates="price_history",
    )

    __table_args__ = (
        UniqueConstraint(
            "stock_id",
            "date",
            name="unique_stock_date",
        ),
    )