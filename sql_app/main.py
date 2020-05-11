from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/plans")
def read_plans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    plans = crud.get_plans(db, skip=skip, limit=limit)
    return plans

@app.post("/plans", response_model=schemas.Plan)
def create_plan(plan: schemas.PlanBase, db: Session = Depends(get_db)):
    db_plan = crud.get_plan_by_name(db, plan_name=plan.name)
    if db_plan:
        raise HTTPException(status_code=400, detail="Plan already exists")
    return crud.create_plan(db=db, plan=plan)

@app.get("/plans/name/{plan_name}", response_model=schemas.Plan)
def get_plan_by_name(plan_name: str, db: Session = Depends(get_db)):
    db_plan = crud.get_plan_by_name(db, plan_name=plan_name)
    if db_plan is None:
        raise HTTPException(status_code=400, detail="Plan doesn't exists")
    return db_plan

@app.get("/plans/id/{plan_id}", response_model=schemas.Plan)
def get_plan_by_name(plan_id: int, db: Session = Depends(get_db)):
    db_plan = crud.get_plan_by_id(db, plan_id=plan_id)
    if db_plan is None:
        raise HTTPException(status_code=400, detail="Plan doesn't exists")
    return db_plan

@app.get("/users/", response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/vouchers", response_model=List[schemas.Voucher])
def get_vouchers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vouchers = crud.get_vouchers(db, skip=skip, limit=limit)
    return vouchers

@app.post("/vouchers", response_model=schemas.Voucher)
def create_voucher(voucher: schemas.VoucherBase, db: Session = Depends(get_db)):
    return crud.create_voucher(db=db, voucher=voucher)

@app.post("/vouchers/{num}", response_model=List[schemas.Voucher])
def create_vouchers(num: int, voucher: schemas.VoucherBase, db: Session = Depends(get_db)):
    vouchers = []
    for i in range(num):
        vouchers.append(crud.create_voucher(db=db, voucher=voucher))
    return vouchers

# @app.get("/referral_link/{user_id}")
# def get_referral(user_id: int, db: Session = Depends(get_db)):


# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)
#
#
# @app.get("/users/", response_model=List[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users
#
#
# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
#
#
# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)
#
#
# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items