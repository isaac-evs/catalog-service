# app/views/customer.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from app.controllers.customer import CustomerController
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[CustomerResponse])
def read_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all customers with pagination"""
    return CustomerController.get_customers(db, skip=skip, limit=limit)

@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    """Create a new customer"""
    return CustomerController.create_customer(db, customer)

@router.get("/{customer_id}", response_model=CustomerResponse)
def read_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific customer by ID"""
    return CustomerController.get_customer(db, customer_id)

@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    db: Session = Depends(get_db)
):
    """Update a customer"""
    return CustomerController.update_customer(db, customer_id, customer)

@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    """Delete a customer"""
    return CustomerController.delete_customer(db, customer_id)
