from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import json

app = FastAPI()
origins = [
 "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
def shutdown_event():
    #Close Any Open Connections
    db = SessionLocal()
    db.close()

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Search for a specific User
@app.get("/horizon")
async def HorizonServers(
    db: Session = Depends(get_db)
): 
    response_object = {'status': 'success'}
    response_object['vdesks']  = db.query(models.Horizon).all()
    return JSONResponse(content=jsonable_encoder(response_object))

#Search for a specific User
@app.post("/searchdata")
async def HorizonServers(
    request: Request,
    db: Session = Depends(get_db)
): 
    response_object = {'status': 'success'}
    data = await request.json()
    user = data['TitleUser']
    print(user)
    response_object['SearchvDesks']  = db.query(models.Horizon).filter(models.Horizon.UserName == user).all()
    return JSONResponse(content=jsonable_encoder(response_object))


@app.post("/powercycle")
async def selectedMachine(item: dict):
    message = json.loads(json.dumps(item, indent=2))
  
  
    print(message['data']['PowerCycle'])
    print(message['data']['vDesk']['MachineName'])
    
    RabbitMQ_Sender(message) #Passing Message to Class RabbitMQ_Sender
    return JSONResponse(content=jsonable_encoder({'status': 'success'}))
