from sqlalchemy.orm import Session

from models import Customer
from schemas import CustomerCreate


def create(db: Session, customer: CustomerCreate):
    db_customer = Customer(name=customer.name)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def get_by_uid(db: Session, customer_uid: int):
    return db.query(Customer).filter(Customer.uid == customer_uid).first()


def get_by_name(db: Session, name: str):
    return db.query(Customer).filter(Customer.name.like(f"%{name}%")).first()


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer).offset(skip).limit(limit).all()


# def delete_by_id(connection, customer_id):
#     cur = connection.cursor()
#     cur.execute("""DELETE FROM Customer WHERE customerID = ?""", (customer_id,))
#     connection.commit()

# def max_id(connection):
#     cur = connection.cursor()
#     cur.execute("""SELECT MAX (customerID) FROM Customer""")
#     _id = None
#     try:
#         _id = cur.fetchone()[0]
#     except TypeError:
#         pass
#     return _id
