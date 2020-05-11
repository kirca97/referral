import random
import string

from sqlalchemy.orm import Session

from . import models, schemas


def get_plans(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Plan).offset(skip).limit(limit).all()

def create_plan(db: Session, plan: schemas.PlanBase):
    db_plan = models.Plan(name=plan.name, num_servers=plan.num_servers, price=plan.price)
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def create_voucher(db: Session, voucher: schemas.VoucherBase):
    voucher_postoi = "test"
    while voucher_postoi != None:
        random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        voucher_postoi = db.query(models.Voucher).filter(models.Voucher.code == random_code).first()

    print(random_code)
    db_voucher = models.Voucher(code=random_code,
                                amount=voucher.amount,
                                start_date=voucher.start_date)
    db.add(db_voucher)
    db.commit()
    db.refresh(db_voucher)
    return db_voucher

def get_plan_by_name(db: Session, plan_name: str):
    return db.query(models.Plan).filter(models.Plan.name == plan_name).first()

def get_plan_by_id(db: Session, plan_id: int):
    return db.query(models.Plan).filter(models.Plan.id == plan_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_vouchers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Voucher).filter(models.Voucher.is_used == False).offset(skip).limit(limit).all()


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()
#
#
# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()
#
#
# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()
#
#
#
# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
#
#
# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()
#
#
# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item