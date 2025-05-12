# app/views/product.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.controllers.product import ProductController
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def read_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    active_only: bool = Query(False),
    db: Session = Depends(get_db)
):
    """Get all products with pagination and filtering"""
    return ProductController.get_products(db, skip=skip, limit=limit, active_only=active_only)

@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """Create a new product"""
    return ProductController.create_product(db, product)

@router.get("/{product_id}", response_model=ProductResponse)
def read_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific product by ID"""
    return ProductController.get_product(db, product_id)

@router.get("/sku/{sku}", response_model=ProductResponse)
def read_product_by_sku(
    sku: str,
    db: Session = Depends(get_db)
):
    """Get a specific product by SKU"""
    product = ProductController.get_product_by_sku(db, sku)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update a product"""
    return ProductController.update_product(db, product_id, product)

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Delete a product"""
    return ProductController.delete_product(db, product_id)
