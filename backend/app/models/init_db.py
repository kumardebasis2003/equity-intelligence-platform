from app.models.database import Base, engine
from app.models.stock import Stock, PriceHistory


print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")