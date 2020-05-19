from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import true, null, false
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

# import configparser
#
# import netifaces
# import requests
# from consul import Consul, Check
# # from fastapi import FastAPI
# from lorem.text import TextLorem
#
# consul_port = 8500
# service_name = "referral"
# service_port = 8010
#
#
# def get_ip():
#     config_parser = configparser.ConfigParser()
#     config_file = "config.ini"
#     config_parser.read(config_file)
#     interface_name = config_parser['NETWORK']['interface']
#     ip = netifaces.ifaddresses(interface_name)[netifaces.AF_INET][0]["addr"]
#     return ip
#
#
# def register_to_consul():
#     consul = Consul(host="consul", port=consul_port)
#
#     agent = consul.agent
#
#     service = agent.service
#
#     ip = get_ip()
#
#     check = Check.http(f"http://{ip}:{service_port}/", interval="10s", timeout="5s", deregister="1s")
#
#     service.register(service_name, service_id=service_name, address=ip, port=service_port, check=check)
#
#
# def get_service(service_id):
#     consul = Consul(host="consul", port=consul_port)
#
#     agent = consul.agent
#
#     service_list = agent.services()
#
#     service_info = service_list[service_id]
#
#     return service_info['Address'], service_info['Port']
#
#
# app = FastAPI()
#
# # register_to_consul()
#
# print("OK service1")
#
#
# @app.get("/")
# def index():
#     return "Service1"
#
#
# @app.get("/sentence-dependent")
# def get_sentence_using_service_2():
#     address, port = get_service("service2")
#
#     words = requests.get(f"http://{address}:{port}/words").json()
#
#     words = words["words"]
#
#     lorem = TextLorem(words=words)
#
#     return {"sentence": lorem.sentence()}
#
#
# @app.get("/sentence-independent")
# def get_sentence_using_own_words():
#     lorem = TextLorem()
#
#     return {"sentence": lorem.sentence()}

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


users_micro = [
{
"referral_link": "test1",
"credits": 10,
"administrator": 1,
"referraled_id": None,
"id": 1
},
{
"referral_link": "test2",
"credits": 20,
"administrator": 0,
"referraled_id": 1,
"id": 2
},
{
"referral_link": "test3",
"credits": 0,
"administrator": 0,
"referraled_id": None,
"id": 42
},
{
"referral_link": "test4",
"credits": 20,
"administrator": 0,
"referraled_id": None,
"id": 43
},
{
"referral_link": "test5",
"credits": 20,
"administrator": 0,
"referraled_id": None,
"id": 44
}
]

def get_user(user_id, db):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        db_user = [x for x in users_micro if x['id'] == user_id][0]
        print(db_user)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        crud.create_user(db=db, user_id=db_user['id'], administrator=db_user['administrator'],
                         referraled_id=db_user['referraled_id'])
    db_user = crud.get_user(db=db, user_id=user_id)
    return db_user


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

@app.post("/{user_id}/{voucher_code}")
def add_credits_to_user(user_id: int, voucher_code: str, db: Session = Depends(get_db)):
    db_voucher = crud.verify_voucher(db=db, voucher_code=voucher_code)
    if db_voucher is None:
        raise HTTPException(status_code=404, detail="Voucher not found")
    if db_voucher.is_used == 1:
        raise HTTPException(status_code=404, detail="Voucher is already used")
    db_user = get_user(user_id, db)
    crud.add_credits_to_user(db=db, user_id=user_id, credits=db_voucher.amount)
    crud.used_voucher(db=db, voucher_code=voucher_code, user_id=user_id)
    return {"name": "successful"}



@app.get("/referral_link/{user_id}")
def get_referral(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(user_id, db)
    return db_user.referral_link


@app.post("/promo_codes", response_model=schemas.PromoCode)
def create_promo_code(promo_code: schemas.PromoCodeBase, db: Session = Depends(get_db)):
    return crud.create_promo_code(db=db, promo_code=promo_code)

@app.post("/promo_codes/{nums}", response_model=List[schemas.PromoCode])
def create_promo_codes(nums: int, promo_code: schemas.PromoCodeBase, db: Session = Depends(get_db)):
    promo_codes = []
    print(nums)
    print(10)
    for i in range(nums):
        promo_codes.append(crud.create_promo_code(db=db, promo_code=promo_code))
    return promo_codes

@app.post("/promo_codes10", response_model=List[schemas.PromoCode])
def create_promo_codes(promo_code: schemas.PromoCodeBase, db: Session = Depends(get_db)):
    promo_codes = []
    # print(num)
    for i in range(10):
        promo_codes.append(crud.create_promo_code(db=db, promo_code=promo_code))
    return promo_codes

@app.get("/promo_codes", response_model=List[schemas.PromoCode])
def get_promo_codes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_promo_codes(db=db, skip=skip, limit=limit)

@app.get("/promo_codes/id/{promo_code_id}", response_model=schemas.PromoCode)
def get_promo_code_by_id(promo_code_id: int, db: Session = Depends(get_db)):
    db_promo_code = crud.get_promo_code_by_id(db=db, promo_code_id=promo_code_id)
    if db_promo_code is None:
        raise HTTPException(status_code=400, detail="Promocode doesn't exists")
    return db_promo_code

@app.get("/promo_codes/name/{promo_code_code}", response_model=schemas.PromoCode)
def get_promo_code_by_code(promo_code_code: str, db: Session = Depends(get_db)):
    db_promo_code = crud.get_promo_code_by_code(db=db, promo_code_code=promo_code_code)
    if db_promo_code is None:
        raise HTTPException(status_code=400, detail="Promocode doesn't exists")
    return db_promo_code

@app.post("/successfulpayment")
def successful_payment(successful: schemas.SuccessfulPayment, db: Session = Depends(get_db)):
    db_user = get_user(successful.user_id, db)
    if(db_user.referraled_id != None):
        db_referraled_user = crud.get_user(db, db_user.referraled_id)
        crud.add_credits_to_user(db, db_referraled_user.id, successful.amount * 0.1)
    crud.add_credits_to_user(db, db_user.id, successful.credits * (-1))
    db_promo_code = crud.get_promo_code_by_code(db, successful.promo_code)
    if(db_promo_code != None):
        crud.used_promo_code(db, db_promo_code.code, db_user.id)
    return {"successful": "payment"}
