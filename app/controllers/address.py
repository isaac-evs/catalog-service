# app/controllers/address.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate
from app.controllers.customer import CustomerController
from typing import List

class AddressController:
    @staticmethod
    def get_addresses(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Address).offset(skip).limit(limit).all()

    @staticmethod
    def get_address(db: Session, address_id: int):
        address = db.query(Address).filter(Address.id == address_id).first()
        if address is None:
            raise HTTPException(status_code=404, detail="Address not found")
        return address

    @staticmethod
    def get_customer_addresses(db: Session, customer_id: int):
        # Verify customer exists
        CustomerController.get_customer(db, customer_id)
        return db.query(Address).filter(Address.customer_id == customer_id).all()

    @staticmethod
    def create_address(db: Session, address: AddressCreate):
        # Verify customer exists
        CustomerController.get_customer(db, address.customer_id)

        # If this is default address, unset any other default
        if address.is_default:
            db.query(Address).filter(
                Address.customer_id == address.customer_id,
                Address.is_default == True
            ).update({"is_default": False})

        # Create new address
        db_address = Address(**address.dict())
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        return db_address

    @staticmethod
    def update_address(db: Session, address_id: int, address: AddressUpdate):
        db_address = AddressController.get_address(db, address_id)

        # If setting as default, unset any other default
        if address.is_default:
            db.query(Address).filter(
                Address.customer_id == db_address.customer_id,
                Address.is_default == True,
                Address.id != address_id
            ).update({"is_default": False})

        # Update address data
        update_data = address.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_address, key, value)

        db.commit()
        db.refresh(db_address)
        return db_address

    @staticmethod
    def delete_address(db: Session, address_id: int):
        db_address = AddressController.get_address(db, address_id)
        db.delete(db_address)
        db.commit()
        return {"message": "Address deleted successfully"}
