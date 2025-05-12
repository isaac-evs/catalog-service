from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate
from typing import List, Optional

class CustomerController:
    @staticmethod
    def get_customers(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Customer).offset(skip).limit(limit).all()

    @staticmethod
    def get_customer(db: Session, customer_id: int):
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer

    @staticmethod
    def get_customer_by_email(db: Session, email: str):
        return db.query(Customer).filter(Customer.email == email).first()

    @staticmethod
    def create_customer(db: Session, customer: CustomerCreate):
        # Check if customer with this email already exists
        db_customer = CustomerController.get_customer_by_email(db, email=customer.email)
        if db_customer:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Create new customer
        db_customer = Customer(**customer.dict())
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer

    @staticmethod
    def update_customer(db: Session, customer_id: int, customer: CustomerUpdate):
        db_customer = CustomerController.get_customer(db, customer_id)

        # Update customer data
        update_data = customer.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_customer, key, value)

        db.commit()
        db.refresh(db_customer)
        return db_customer

    @staticmethod
    def delete_customer(db: Session, customer_id: int):
        db_customer = CustomerController.get_customer(db, customer_id)
        db.delete(db_customer)
        db.commit()
        return {"message": "Customer deleted successfully"}
