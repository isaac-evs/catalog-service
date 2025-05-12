from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.models import customer, address, product
from app.views import customer as customer_views
from app.views import address as address_views
from app.views import product as product_views

# Create database tables
customer.Base.metadata.create_all(bind=engine)
address.Base.metadata.create_all(bind=engine)
product.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Catalog Service")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(customer_views.router, prefix="/api/customers", tags=["customers"])
app.include_router(address_views.router, prefix="/api/addresses", tags=["addresses"])
app.include_router(product_views.router, prefix="/api/products", tags=["products"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Catalog Service API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
