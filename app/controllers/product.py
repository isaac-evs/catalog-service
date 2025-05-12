# app/controllers/product.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from typing import List, Optional

class ProductController:
    @staticmethod
    def get_products(db: Session, skip: int = 0, limit: int = 100, active_only: bool = False):
        query = db.query(Product)
        if active_only:
            query = query.filter(Product.is_active == True)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_product(db: Session, product_id: int):
        product = db.query(Product).filter(Product.id == product_id).first()
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    @staticmethod
    def get_product_by_sku(db: Session, sku: str):
        return db.query(Product).filter(Product.sku == sku).first()

    @staticmethod
    def create_product(db: Session, product: ProductCreate):
        # Check if product with this SKU already exists
        db_product = ProductController.get_product_by_sku(db, sku=product.sku)
        if db_product:
            raise HTTPException(status_code=400, detail="SKU already exists")

        # Create new product
        db_product = Product(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def update_product(db: Session, product_id: int, product: ProductUpdate):
        db_product = ProductController.get_product(db, product_id)

        # Update product data
        update_data = product.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)

        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def delete_product(db: Session, product_id: int):
        db_product = ProductController.get_product(db, product_id)
        db.delete(db_product)
        db.commit()
        return {"message": "Product deleted successfully"}
