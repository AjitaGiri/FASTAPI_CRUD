from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import os,json 
from fastapi import HTTPException 

app=FastAPI()

# path for json file
DATA_FILE="customers.json"

class Customer(BaseModel):
    id:int
    name:str
    last_purchased_date:str 
    address:str 

#Helper function
def load_data()->List[dict]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE,'r') as f:
        return json.load(f)

def save_data(data:List[dict]):
    with open(DATA_FILE,'w') as f:
        json.dump(data,f)

@app.get("/")
def index():
    return {"Message":"Hello World"}

@app.get("/customers",response_model=List[Customer])
def get_all_customers():
    return load_data()

@app.get("/customers/{customer_id}",response_model=Customer)
def get_single_customer(customer_id:int):
    customers=load_data()
    for cus in customers:
        if cus['id']==customer_id:
            return cus 
    raise HTTPException(status_code=404,detail=f'Customer with Id {customer_id} not found')

@app.post("/customers",response_model=Customer)
def create_customer(data:Customer):
    customers=load_data()
    if any(cus['id']==data.id for cus in customers):
        raise HTTPException(status_code=400,detail=f'Customer with id {data.id} already exists')
    customers.append(data.dict())
    save_data(customers)
    return  data

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id:int):
    customers=load_data()
    for idx,cust in enumerate(customers):
        if cust['id']==customer_id:
            deleted=customers.pop(idx)
            save_data(customers)
            return {"message":"Customer Successfully Deleted"}
    raise HTTPException(status_code=404,detail='Provided Customer Id not Found')

@app.put("/customers/{customer_id}",response_model=Customer)
def update_customer(customer_id:int, updated_customer:Customer):
    customers=load_data()
    for indx,cust in enumerate(customers):
        if cust['id']==customer_id:
            customers[indx]=updated_customer.dict()
            save_data(customers)
            return updated_customer
    raise HTTPException(status_code=404,detail="Unable to find the customer with id {customer_id}")
        