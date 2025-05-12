# app/views/address.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.schemas.address import AddressCreate, AddressUpdate, AddressResponse
from app.controllers.address import AddressController
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[AddressResponse])
def read_addresses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all addresses with pagination"""
    return AddressController.get_addresses(db, skip=skip, limit=limit)

@router.post("/", response_model=AddressResponse, status_code=201)
def create_address(
    address: AddressCreate,
    db: Session = Depends(get_db)
):
    """Create a new address"""
    return AddressController.create_address(db, address)

@router.get("/{address_id}", response_model=AddressResponse)
def read_address(
    address_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific address by ID"""
    return AddressController.get_address(db, address_id)

@router.get("/customer/{customer_id}", response_model=List[AddressResponse])
def read_customer_addresses(
    customer_id: int,
    db: Session = Depends(get_db)
):
    """Get all addresses for a customer"""
    return AddressController.get_customer_addresses(db, customer_id)

@router.put("/{address_id}", response_model=AddressResponse)
def update_address(
    address_id: int,
    address: AddressUpdate,
    db: Session = Depends(get_db)
):
    """Update an address"""
    return AddressController.update_address(db, address_id, address)

@router.delete("/{address_id}")
def delete_address(
    address_id: int,
    db: Session = Depends(get_db)
):
    """Delete an address"""
    return AddressController.delete_address(db, address_id)
